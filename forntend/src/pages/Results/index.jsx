import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import Button from "../../components/ui/Button";
import { fetchRecommendedJobs } from "../../services/jobs.service"; // Import service
import JobCard from "../../components/ui/JobCard"; // Import JobCard
import MainLayout from "../../layouts/MainLayout"; // Import it!

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Extract the data from the router state
  const data = location.state?.analysisData;

  // If someone navigates to /results without uploading, send them back
  if (!data || !data.analysis) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
        <h2 className="text-2xl font-bold mb-4">No Resume Data Found</h2>
        <Button onClick={() => navigate("/")}>Go Upload a Resume</Button>
      </div>
    );
  }

  const { analysis } = data;

  // Helper function to color-code the score
  const getScoreColor = (score) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-500";
    return "text-red-500";
  };

  const [jobs, setJobs] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(false);

  useEffect(() => {
    const getJobs = async () => {
      if (data?.analysis?.job_search) {
        setLoadingJobs(true);
        try {
          const searchInfo = data.analysis.job_search;

          // Prepare the payload for your Backend API
          const payload = {
            roles: searchInfo.roles,
            preferred_location: searchInfo.preferred_location,
            skills: searchInfo.skills,
            // Simple logic to turn string experience into a number for your API
            experience_level: parseInt(searchInfo.experience_level) || 1,
          };

          const jobResponse = await fetchRecommendedJobs(payload);
          setJobs(jobResponse.data.recommended_jobs || []);
        } catch (err) {
          console.error("Failed to load jobs");
        } finally {
          setLoadingJobs(false);
        }
      }
    };

    getJobs();
  }, [data]);
  return (
    <MainLayout>
      <div className="py-10 px-4">
        <div className="max-w-6xl mx-auto space-y-6">
          {/* Header Navigation */}
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl font-extrabold text-gray-900">
              Analysis Results
            </h1>
            <Link to="/" className="text-blue-600 font-medium hover:underline">
              &larr; Analyze Another Resume
            </Link>
          </div>

          {/* Top Row: Score & Recruiter Feedback */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Overall Score Card */}
            <Card className="col-span-1 flex flex-col items-center justify-center text-center p-8">
              <h3 className="text-lg font-semibold text-gray-600 mb-2">
                Overall Score
              </h3>
              <div
                className={`text-7xl font-extrabold ${getScoreColor(analysis.overall_score.score)}`}
              >
                {analysis.overall_score.score}
              </div>
              <div className="text-xl font-bold text-gray-800 mt-2">
                Grade: {analysis.overall_score.grade}
              </div>
            </Card>

            {/* Recruiter Feedback Card */}
            <Card
              title="Recruiter Feedback"
              className="col-span-1 md:col-span-2"
            >
              <div className="mb-4">
                <span className="font-semibold text-gray-800">
                  Interview Probability:{" "}
                </span>
                <span className="text-gray-700">
                  {analysis.recruiter_feedback.interview_probability}
                </span>
              </div>
              <p className="text-gray-600 leading-relaxed text-sm">
                {analysis.recruiter_feedback.feedback}
              </p>
            </Card>
          </div>

          {/* Middle Row: Strengths & Weaknesses */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card
              title="Key Strengths"
              className="border-t-4 border-t-green-500"
            >
              <ul className="space-y-3">
                {analysis.strengths.map((strength, index) => (
                  <li
                    key={index}
                    className="flex items-start gap-2 text-sm text-gray-700"
                  >
                    <svg
                      className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M5 13l4 4L19 7"
                      ></path>
                    </svg>
                    <span
                      dangerouslySetInnerHTML={{
                        __html: strength.replace(
                          /\*\*(.*?)\*\*/g,
                          "<strong>$1</strong>",
                        ),
                      }}
                    />
                  </li>
                ))}
              </ul>
            </Card>

            <Card
              title="Areas for Improvement"
              className="border-t-4 border-t-red-500"
            >
              <ul className="space-y-3">
                {analysis.weaknesses.map((weakness, index) => (
                  <li
                    key={index}
                    className="flex items-start gap-2 text-sm text-gray-700"
                  >
                    <svg
                      className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M6 18L18 6M6 6l12 12"
                      ></path>
                    </svg>
                    <span
                      dangerouslySetInnerHTML={{
                        __html: weakness.replace(
                          /\*\*(.*?)\*\*/g,
                          "<strong>$1</strong>",
                        ),
                      }}
                    />
                  </li>
                ))}
              </ul>
            </Card>
          </div>

          {/* Bottom Row: Skills Mapping */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card title="Detected Skills">
              <div className="flex flex-wrap gap-2">
                {analysis.detected_skills.map((skill, i) => (
                  <Badge key={i} text={skill} variant="green" />
                ))}
              </div>
            </Card>

            <Card title="Missing Skills (Keywords to add)">
              <div className="flex flex-wrap gap-2">
                {analysis.missing_skills.map((skill, i) => (
                  <Badge key={i} text={skill} variant="red" />
                ))}
              </div>
            </Card>
          </div>

          {/* Step 5 Placeholder: We will add Jobs here next */}
          <div id="jobs-section" className="mt-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Recommended Jobs for You
            </h2>

            {loadingJobs ? (
              <div className="flex flex-col items-center py-10">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                <p className="mt-4 text-gray-600">
                  Finding matches based on your profile...
                </p>
              </div>
            ) : jobs.length > 0 ? (
              <div className="grid grid-cols-1 gap-4">
                {jobs.map((job, index) => (
                  <JobCard key={index} job={job} />
                ))}
              </div>
            ) : (
              <Card className="text-center py-10">
                <p className="text-gray-500">
                  No matching jobs found at this moment. Try adjusting your
                  target role.
                </p>
              </Card>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ResultsPage;
