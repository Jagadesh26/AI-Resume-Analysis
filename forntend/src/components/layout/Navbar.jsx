import React, { useState } from "react"; // Import useState
import { Link, useLocation } from "react-router-dom";
import Button from "../ui/Button";
import JobSearchModal from "../ui/JobSearchModal"; // Import the Modal!

const Navbar = () => {
  const location = useLocation();
  const [isModalOpen, setIsModalOpen] = useState(false); // State to open/close modal

  const showUploadButton = location.pathname !== "/";

  return (
    <>
      <nav className="bg-white border-b border-gray-100 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo Section */}
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg
                  className="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  ></path>
                </svg>
              </div>
              <span className="text-xl font-bold text-gray-900 tracking-tight">
                Resume<span className="text-blue-600">AI</span>
              </span>
            </Link>

            {/* Center Links */}
            <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
              <Link to="/" className="hover:text-blue-600 transition-colors">
                Home
              </Link>
              {/* This button opens the Modal */}
              <button
                onClick={() => setIsModalOpen(true)}
                className="hover:text-blue-600 transition-colors cursor-pointer font-medium"
              >
                Search Jobs
              </button>
              <a
                href="#pricing"
                className="hover:text-blue-600 transition-colors"
              >
                Pricing
              </a>
            </div>

            {/* Right Action Button */}
            <div className="flex items-center gap-4">
              {/* Quick Search trigger for mobile/small screens too */}
              <button
                onClick={() => setIsModalOpen(true)}
                className="text-gray-500 hover:text-blue-600 md:hidden cursor-pointer"
              >
                🔍
              </button>

              {showUploadButton && (
                <Link to="/">
                  <Button variant="primary" className="text-sm">
                    New Analysis
                  </Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Render the search modal globally */}
      <JobSearchModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
};

export default Navbar;
