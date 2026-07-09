import React from "react";

const AnalysisLoader = () => {
  return (
    <div className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-white/80 backdrop-blur-md">
      {/* Cool animated spinner */}
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600 mb-6"></div>

      <h2 className="text-2xl font-bold text-gray-900 animate-pulse">
        AI is analyzing your resume...
      </h2>
      <p className="text-gray-600 mt-2 font-medium">
        This might take 10-20 seconds. Please do not close the page.
      </p>
    </div>
  );
};

export default AnalysisLoader;
