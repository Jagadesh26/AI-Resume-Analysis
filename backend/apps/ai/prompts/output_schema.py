import json


class OutputSchema:
    """
    Expected JSON response from every AI provider.
    """

    @staticmethod
    def schema() -> dict:
        return {
            "overall_score": {
                "score": 0,
                "grade": "",
                "reason": ""
            },
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "detected_skills": [],
            "missing_skills": [],
            "grammar": {
                "score": 0,
                "issues": []
            },
            "formatting": {
                "score": 0,
                "issues": []
            },
            "section_scores": {
                "summary": {
                    "score": 0,
                    "reason": ""
                },
                "experience": {
                    "score": 0,
                    "reason": ""
                },
                "projects": {
                    "score": 0,
                    "reason": ""
                },
                "skills": {
                    "score": 0,
                    "reason": ""
                },
                "education": {
                    "score": 0,
                    "reason": ""
                }
            },
            "keyword_analysis": {
                "detected_keywords": [],
                "missing_keywords": [],
                "keyword_density": 0
            },
            "achievement_suggestions": [],
            "resume_rewrites": [],
            "recommendations": [],
            "role_match": [],
            "recruiter_feedback": {
                "interview_probability": "",
                "feedback": ""
            },
            "recommended_jobs": [],
            "job_search": {
                "roles": [],
                "preferred_location": "",
                "experience_level": "",
                "employment_types": [],
                "work_modes": [],
                "skills": []
            }
        }

    @classmethod
    def as_json(cls) -> str:
        return json.dumps(
            cls.schema(),
            indent=4
        )