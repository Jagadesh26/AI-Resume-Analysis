import React, { useState } from "react";
import { fetchRecommendedJobs } from "../../services/jobs.service";
import Button from "./Button";
import Input from "./Input";
import JobCard from "./JobCard";

const JobSearchModal = ({ isOpen, onClose }) => {
  const [roles, setRoles] = useState("");
  const [location, setLocation] = useState("");
  const [skills, setSkills] = useState("");
  const [experience, setExperience] = useState("1");

  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [validationErrors, setValidationErrors] = useState({});

  if (!isOpen) return null;

  // Validation Logic
  const validateForm = () => {
    const errors = {};

    // Check if everything is blank
    if (!roles.trim() && !location.trim() && !skills.trim()) {
      errors.general =
        "Please fill out at least one search field (Roles, Location, or Skills) to search.";
    }

    // Validate Experience input
    const parsedExp = parseInt(experience);
    if (
      experience.trim() &&
      (isNaN(parsedExp) || parsedExp < 0 || parsedExp > 45)
    ) {
      errors.experience =
        "Experience must be a positive number between 0 and 45.";
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setValidationErrors({});

    // Run validation checks
    if (!validateForm()) return;

    setLoading(true);
    setSearched(true);

    try {
      const payload = {
        roles: roles
          .split(",")
          .map((r) => r.trim())
          .filter(Boolean),
        preferred_location: location.trim(),
        skills: skills
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        experience_level: parseInt(experience) || 1,
      };

      const jobResponse = await fetchRecommendedJobs(payload);
      setJobs(jobResponse.data.recommended_jobs || []);
    } catch (error) {
      console.error("Failed to fetch jobs in modal", error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setRoles("");
    setLocation("");
    setSkills("");
    setExperience("1");
    setJobs([]);
    setSearched(false);
    setValidationErrors({});
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      <div className="relative bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[90vh] flex flex-col z-10 m-4 overflow-hidden">
        <div className="flex justify-between items-center px-6 py-4 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-900">Quick Job Search</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-semibold cursor-pointer"
          >
            &times;
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
          <form
            onSubmit={handleSearch}
            className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl border border-gray-100"
          >
            <Input
              label="Roles (comma separated)"
              placeholder="e.g., React Developer, Frontend"
              value={roles}
              onChange={(e) => setRoles(e.target.value)}
              disabled={loading}
            />
            <Input
              label="Preferred Location"
              placeholder="e.g., Chennai"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              disabled={loading}
            />
            <Input
              label="Skills (comma separated)"
              placeholder="e.g., React, JavaScript"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              disabled={loading}
            />
            <Input
              label="Experience Level (Years)"
              placeholder="e.g., 1"
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              disabled={loading}
            />

            {/* Validation Error Displays */}
            <div className="md:col-span-2">
              {validationErrors.general && (
                <p className="text-red-500 text-sm font-medium mt-1">
                  {validationErrors.general}
                </p>
              )}
              {validationErrors.experience && (
                <p className="text-red-500 text-sm font-medium mt-1">
                  {validationErrors.experience}
                </p>
              )}
            </div>

            {/* 🔥 FIXED BUTTON LOGIC 🔥 */}
            <div className="md:col-span-2 flex justify-end mt-2">
              {loading ? (
                /* State 1: Currently loading (Shows Processing) */
                <Button type="button" disabled={true} className="py-2 px-6">
                  Searching...
                </Button>
              ) : searched ? (
                /* State 2: Done loading, results are showing (Shows Clear button) */
                <Button
                  type="button"
                  onClick={handleReset}
                  variant="outline"
                  className="py-2 px-6"
                >
                  Clear Results & Search Again
                </Button>
              ) : (
                /* State 3: Default state (Shows Search button) */
                <Button type="submit" className="py-2 px-6">
                  Search Jobs
                </Button>
              )}
            </div>
          </form>

          <div className="space-y-4">
            {loading ? (
              <div className="flex flex-col items-center py-12">
                <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
                <p className="mt-4 text-sm text-gray-500">
                  Scanning job portals...
                </p>
              </div>
            ) : searched ? (
              <>
                <h3 className="text-lg font-bold text-gray-900 mb-2">
                  Search Results ({jobs.length})
                </h3>
                {jobs.length > 0 ? (
                  <div className="space-y-4 max-h-[40vh] overflow-y-auto pr-2 scrollbar-hide">
                    {jobs.map((job, index) => (
                      <JobCard key={index} job={job} />
                    ))}
                  </div>
                ) : (
                  <p className="text-center text-gray-500 py-8">
                    No jobs found. Try adjusting your skills or roles.
                  </p>
                )}
              </>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <svg
                  className="w-12 h-12 mx-auto mb-3 opacity-50"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  ></path>
                </svg>
                <p className="text-sm">
                  Enter search parameters above to hunt for available jobs.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobSearchModal;
