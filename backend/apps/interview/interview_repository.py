# apps/interview/repositories/interview_state_repository.py

from datetime import timedelta
from uuid import UUID

from django.utils import timezone

from apps.interview.models import InterviewSession, InterviewState


class InterviewStateRepository:
    """
    Repository responsible for persisting active interview state.
    """

    def _normalize_conversation_id(self, conversation_id: str) -> UUID:
        return UUID(str(conversation_id))

    def save(self, conversation_id: str, state: dict, timeout: int = 7200):
        conversation_uuid = self._normalize_conversation_id(conversation_id)
        expires_at = timezone.now() + timedelta(seconds=timeout)

        InterviewState.objects.update_or_create(
            conversation_id=conversation_uuid,
            defaults={
                "interview_session_id": state["session_id"],
                "state_json": state,
                "expires_at": expires_at,
            },
        )

    def get(self, conversation_id: str) -> dict | None:
        conversation_uuid = self._normalize_conversation_id(conversation_id)

        try:
            interview_state = InterviewState.objects.get(
                conversation_id=conversation_uuid,
            )
        except InterviewState.DoesNotExist:
            return None

        if interview_state.is_expired:
            interview_state.delete()
            return None

        return interview_state.state_json

    def delete(self, conversation_id: str):
        conversation_uuid = self._normalize_conversation_id(conversation_id)
        InterviewState.objects.filter(
            conversation_id=conversation_uuid,
        ).delete()

    def delete_for_session(self, session: InterviewSession):
        InterviewState.objects.filter(
            interview_session=session,
        ).delete()
