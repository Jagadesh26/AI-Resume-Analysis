from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory

from apps.jobs.providers.remoteok_provider import RemoteOKProvider
from apps.jobs.schemas.job_schema import JobSchema
from apps.jobs.services.normalization_service import NormalizationService
from apps.jobs.views import JobSearchAPIView


class RemoteOKProviderTests(SimpleTestCase):
    @patch.object(RemoteOKProvider, "get")
    def test_search_jobs_matches_resume_skills_when_title_is_not_exact(
        self,
        mock_get,
    ):
        mock_get.return_value = [
            {"legal": "metadata"},
            {
                "position": "Senior AI Engineer Architect",
                "company": "Lemon.io",
                "location": "Remote",
                "tags": ["python", "sql"],
                "description": "Build backend systems.",
                "apply_url": "https://remoteok.com/job",
            },
            {
                "position": "Customer Support Specialist",
                "company": "Example",
                "location": "Remote",
                "tags": ["support"],
                "description": "Support customers.",
                "apply_url": "https://remoteok.com/support",
            },
        ]

        jobs = RemoteOKProvider().search_jobs(
            role="Python Developer",
            location="Chennai, India",
            skills=["Python", "Django"],
        )

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].job_title, "Senior AI Engineer Architect")
        self.assertEqual(jobs[0].company, "Lemon.io")
        self.assertEqual(jobs[0].apply_url, "https://remoteok.com/job")


class NormalizationServiceTests(SimpleTestCase):
    def test_normalize_remoteok_prefers_apply_url(self):
        job = NormalizationService.normalize_remoteok(
            {
                "position": "Python Developer",
                "company": "Example",
                "apply_url": "https://remoteok.com/apply",
                "url": "https://remoteok.com/view",
            }
        )

        self.assertEqual(job.apply_url, "https://remoteok.com/apply")


class JobSearchAPIViewTests(SimpleTestCase):
    @patch("apps.jobs.views.JobSearchService.search_jobs")
    def test_post_returns_recommended_jobs(
        self,
        mock_search_jobs,
    ):
        mock_search_jobs.return_value = [
            JobSchema(
                job_title="Python Developer",
                company="Example",
                location="Remote",
                experience="Mid-Level",
                employment_type="Full Time",
                work_mode="Remote",
                salary="",
                description="Build APIs.",
                skills=["python"],
                apply_url="https://remoteok.com/job",
                source="RemoteOK",
                match_score=90,
                match_reason="Good skill match.",
            )
        ]

        request = APIRequestFactory().post(
            "/api/v1/jobs/search/",
            {
                "roles": ["Python Developer"],
                "preferred_location": "Chennai, India",
                "skills": ["Python"],
                "experience_level": "Mid-Level",
                "work_modes": ["Remote"],
            },
            format="json",
        )

        response = JobSearchAPIView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["recommended_jobs"][0]["company"],
            "Example",
        )
        self.assertEqual(
            response.data["data"]["recommended_jobs"][0]["apply_url"],
            "https://remoteok.com/job",
        )
