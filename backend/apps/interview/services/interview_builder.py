from uuid import uuid4

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.interview.expections import InterviewException
from apps.interview.gemini_provider import GeminiService
from apps.interview.interview_repository import InterviewStateRepository
from apps.interview.models import InterviewReport, InterviewSession
from apps.interview.prompts.evaluation_prompt import build_interview_prompt
from apps.interview.prompts.interview_prompt import build_interview_round_prompt
from apps.interview.prompts.report_prompt import build_report_prompt
from apps.interview.services.extractor_factory import ResumeExtractorFactory
from apps.interview.services.json_validator import JsonValidator
from apps.interview.services.profile_builder import ProfileBuilder


class InterviewService:
    def __init__(self):
        self.profile_builder = ProfileBuilder()
        self.gemini_service = GeminiService()
        self.json_validator = JsonValidator()
        self.state_repository = InterviewStateRepository()

    @transaction.atomic
    def start_interview(
        self,
        *,
        user,
        uploaded_file,
        interview_type,
        interview_level,
        difficulty,
        total_questions,
    ):
        resume_text = self._extract_resume(uploaded_file)
        candidate_profile = self._build_candidate_profile(resume_text)

        session = self._create_session(
            user=user,
            resume_text=resume_text,
            candidate_profile=candidate_profile,
            interview_type=interview_type,
            interview_level=interview_level,
            difficulty=difficulty,
            total_questions=total_questions,
        )

        first_question = self._generate_first_question(
            candidate_profile=candidate_profile,
            interview_type=interview_type,
            interview_level=interview_level,
            difficulty=difficulty,
            total_questions=total_questions,
        )

        conversation_id = str(uuid4())
        state = self._build_state(
            session=session,
            conversation_id=conversation_id,
            first_question=first_question,
        )
        self._save_state(conversation_id, state)

        return {
            "conversation_id": conversation_id,
            "session_id": str(session.id),
            "question": first_question,
        }

    def submit_answer(self, *, conversation_id, answer):
        state = self._load_state(conversation_id)
        session = self._get_session_from_state(state)

        result = self._generate_interview_round(
            session=session,
            current_question=state["current_question_data"],
            answer=answer,
            history=state["history"],
        )

        self._append_history(
            history=state["history"],
            question_number=state["current_question"],
            question=state["current_question_data"],
            answer=answer,
            evaluation=result["evaluation"],
        )

        if state["current_question"] >= state["total_questions"]:
            report = self._complete_interview(
                session=session,
                conversation_id=conversation_id,
                history=state["history"],
            )
            return {
                "completed": True,
                "report": report,
            }

        state["current_question"] += 1
        state["current_question_data"] = result["next_question"]
        self._save_state(conversation_id, state)

        return {
            "completed": False,
            "evaluation": result["evaluation"],
            "interviewer_response": result.get("interviewer_response", ""),
            "question": result["next_question"],
        }

    @transaction.atomic
    def end_interview(self, *, conversation_id):
        state = self._load_state(conversation_id)
        session = self._get_session_from_state(state)

        report = self._complete_interview(
            session=session,
            conversation_id=conversation_id,
            history=state["history"],
        )

        return {
            "completed": True,
            "report": report,
        }

    def _extract_resume(self, uploaded_file):
        extractor = ResumeExtractorFactory.get(uploaded_file)
        resume_text = extractor.extract(uploaded_file)
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        return resume_text

    def _build_candidate_profile(self, resume_text: str):
        return self.profile_builder.build(resume_text)

    def _create_session(
        self,
        *,
        user,
        resume_text,
        candidate_profile,
        interview_type,
        interview_level,
        difficulty,
        total_questions,
    ):
        return InterviewSession.objects.create(
            user=user,
            raw_content=resume_text,
            candidate_profile=candidate_profile,
            interview_type=interview_type,
            interview_level=interview_level,
            difficulty=difficulty,
            total_questions=total_questions,
            status="in_progress",
            started_at=timezone.now(),
        )

    def _generate_first_question(
        self,
        *,
        candidate_profile,
        interview_type,
        interview_level,
        difficulty,
        total_questions,
    ):
        prompt = build_interview_prompt(
            candidate_profile=candidate_profile,
            interview_type=interview_type,
            interview_level=interview_level,
            difficulty=difficulty,
            total_questions=total_questions,
            current_question_number=1,
            previous_questions=[],
            previous_answers=[],
        )
        response = self.gemini_service.generate_question(prompt)
        return self.json_validator.parse(response)

    def _generate_interview_round(
        self,
        *,
        session,
        current_question,
        answer,
        history,
    ):
        prompt = build_interview_round_prompt(
            candidate_profile=session.candidate_profile,
            interview_type=session.interview_type,
            interview_level=session.interview_level,
            difficulty=session.difficulty,
            current_question=current_question,
            candidate_answer=answer,
            interview_history=history,
        )
        response = self.gemini_service.evaluate_answer(prompt)
        return self.json_validator.parse(response)

    def _generate_final_report(self, *, session, history):
        prompt = build_report_prompt(
            candidate_profile=session.candidate_profile,
            interview_type=session.interview_type,
            interview_level=session.interview_level,
            difficulty=session.difficulty,
            interview_history=history,
        )
        response = self.gemini_service.generate_report(prompt)
        return self.json_validator.parse(response)

    def _complete_interview(self, *, session, conversation_id, history):
        if hasattr(session, "interview_report"):
            self._delete_state(conversation_id)
            return session.interview_report.report_json

        report = self._generate_final_report(
            session=session,
            history=history,
        )

        InterviewReport.objects.create(
            interview_session=session,
            overall_score=report["overall_score"],
            report_json=report,
        )

        session.status = "completed"
        session.completed_at = timezone.now()
        session.save(update_fields=["status", "completed_at"])

        self._delete_state(conversation_id)
        return report

    def _build_state(self, *, session, conversation_id, first_question):
        return {
            "session_id": str(session.id),
            "conversation_id": conversation_id,
            "current_question": 1,
            "total_questions": session.total_questions,
            "history": [],
            "current_question_data": first_question,
            "started_at": timezone.now().isoformat(),
        }

    def _save_state(self, conversation_id, state):
        self.state_repository.save(conversation_id, state)

    def _load_state(self, conversation_id):
        state = self.state_repository.get(conversation_id)
        if not state:
            raise InterviewException("Interview session not found.")
        return state

    def _delete_state(self, conversation_id):
        self.state_repository.delete(conversation_id)

    def _get_session_from_state(self, state):
        try:
            return InterviewSession.objects.get(id=state["session_id"])
        except InterviewSession.DoesNotExist as exc:
            raise InterviewException("Interview session not found.") from exc

    def _append_history(
        self,
        *,
        history,
        question_number,
        question,
        answer,
        evaluation,
    ):
        history.append(
            {
                "question_number": question_number,
                "question": question,
                "answer": answer,
                "evaluation": evaluation,
            }
        )
        return history

    def get_report(self, *, session_id, user=None):
        queryset = InterviewReport.objects.select_related("interview_session")
        if user is not None:
            queryset = queryset.filter(interview_session__user=user)

        return get_object_or_404(
            queryset,
            interview_session_id=session_id,
        )

    def get_history(self, *, user):
        return (
            InterviewSession.objects.filter(user=user)
            .select_related("interview_report")
            .order_by("-started_at")
        )

    def get_interview(self, *, user, session_id):
        return get_object_or_404(
            InterviewSession.objects.select_related("interview_report"),
            id=session_id,
            user=user,
        )


    def _load_state(self, conversation_id):

        print("Loading:", conversation_id)

        state = self.state_repository.get(conversation_id)

        print("State:", state)

        if not state:
            raise InterviewException("Interview session not found.")

        return state
