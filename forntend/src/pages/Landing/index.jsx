import React from "react";
import ResumeUploadSection from "../../components/sections/ResumeUploadSection";
import MainLayout from "../../layouts/MainLayout"; // Import it!

const LandingPage = () => {
  return (
    <MainLayout>
      {" "}
      {/* Wrap the page */}
      <div className="flex flex-col items-center pt-20">
        <div className="text-center px-4 max-w-3xl mx-auto mb-8">
          <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4">
            AI-Powered ATS Resume Checker
          </h1>
          <p className="text-lg text-gray-600">
            Upload your resume, select your target role, and let our AI analyze
            your strengths, weaknesses, and match you with the best jobs.
          </p>
        </div>
        <ResumeUploadSection />
      </div>
    </MainLayout>
  );
};

export default LandingPage;
