# apps/interview/prompts/evaluation_prompt.py

import json


def build_evaluation_prompt(
    candidate_profile: dict,
    interview_type: str,
    interview_level: str,
    difficulty: str,
    question: str,
    candidate_answer: str,
) -> str:
    profile_json = json.dumps(candidate_profile, indent=2)

    return f"""
You are a Senior Technical Interviewer with extensive experience interviewing software engineers.

Your responsibility is to objectively evaluate ONE candidate answer.

=====================================================
INTERVIEW CONFIGURATION
=====================================================

Interview Type:
{interview_type}

Experience Level:
{interview_level}

Difficulty:
{difficulty}

=====================================================
CANDIDATE PROFILE
=====================================================

{profile_json}

=====================================================
QUESTION
=====================================================

{question}

=====================================================
CANDIDATE ANSWER
=====================================================

{candidate_answer}

=====================================================
EVALUATION CRITERIA
=====================================================

Evaluate using the following criteria:

1. Technical Accuracy
2. Depth of Knowledge
3. Practical Experience
4. Communication
5. Problem Solving
6. Completeness
7. Confidence

=====================================================
SCORING
=====================================================

Give scores out of 10.

Be objective.

Do not inflate scores.

=====================================================
RULES
=====================================================

• Evaluate only the provided answer.
• Do not generate another interview question.
• Do not generate the final report.
• If the answer is partially correct, explain what is missing.
• If the answer is incorrect, explain why.
• Mention misconceptions if any.
• Mention strengths if present.
• Mention weaknesses if present.
• Suggest what the candidate should improve.
• Keep feedback constructive and professional.

=====================================================
OUTPUT FORMAT
=====================================================

Return ONLY valid JSON.

{{
    "overall_score": 8,

    "scores": {{
        "technical_accuracy": 8,
        "depth_of_knowledge": 7,
        "communication": 9,
        "problem_solving": 8,
        "completeness": 7,
        "confidence": 8
    }},

    "strengths": [
        "...",
        "..."
    ],

    "weaknesses": [
        "...",
        "..."
    ],

    "missing_points": [
        "...",
        "..."
    ],

    "feedback": "...",

    "recommended_next_difficulty": "Medium"
}}

Return ONLY JSON.

No markdown.

No explanation.

No extra text.
"""






# apps/interview/prompts/interview_prompt.py

import json


def build_interview_prompt(
    *,
    candidate_profile: dict,
    interview_type: str,
    interview_level: str,
    difficulty: str,
    total_questions: int,
    current_question_number: int,
    previous_questions: list,
    previous_answers: list,
) -> str:
    """
    Build the prompt to generate the first interview question.
    """

    return f"""
You are a Senior Technical Interviewer.

Conduct a professional mock interview.

===================================================
INTERVIEW CONFIGURATION
===================================================

Interview Type:
{interview_type}

Experience Level:
{interview_level}

Difficulty:
{difficulty}

Total Questions:
{total_questions}

Current Question Number:
{current_question_number}

===================================================
CANDIDATE PROFILE
===================================================

{json.dumps(candidate_profile, indent=2)}

===================================================
PREVIOUS QUESTIONS
===================================================

{json.dumps(previous_questions, indent=2)}

===================================================
PREVIOUS ANSWERS
===================================================

{json.dumps(previous_answers, indent=2)}

===================================================
RULES
===================================================

Generate EXACTLY ONE interview question.

The question must:

- Match the candidate's skills.
- Match experience level.
- Match interview type.
- Match difficulty.
- Not repeat previous questions.
- Be realistic.
- Be suitable for a real technical interview.
- Prefer practical technical reasoning questions.
- For current_question_number == 1, ask a brief warm-up introduction question such as:
  "Tell me about yourself and walk me through your background."
- Do NOT start with a deep technical question or a resume-project drill-down.
- Do NOT ask only project-based questions based on the resume.
- Use the resume to personalize later questions, but keep the interview flow conversational and real-world.

Return ONLY valid JSON.

Expected JSON:

{{
    "question_number": {current_question_number},
    "topic": "",
    "difficulty": "{difficulty}",
    "expected_skills": [],
    "question": ""
}}

Return ONLY JSON.
"""