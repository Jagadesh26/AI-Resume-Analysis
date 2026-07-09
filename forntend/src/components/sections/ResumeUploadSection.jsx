import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeResume } from "../../services/resume.service";
import Button from "../ui/Button";
import Select from "../ui/Select";
import Input from "../ui/Input";
import Card from "../ui/Card";
import AnalysisLoader from "../loaders/AnalysisLoader";

const ResumeUploadSection = () => {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [targetRole, setTargetRole] = useState("");
  const [provider, setProvider] = useState("gemini");

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const providerOptions = [
    { value: "gemini", label: "Google Gemini" },
    { value: "groq", label: "Groq (Fast)" },
    { value: "openrouter", label: "OpenRouter" },
    { value: "openai", label: "OpenAI (ChatGPT)" },
    { value: "claude", label: "Anthropic Claude" },
  ];

  // Validation: Check File Extension and Size
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    const maxFileSize = 5 * 1024 * 1024; // 5MB limit

    // Validate type
    if (
      !allowedTypes.includes(selectedFile.type) &&
      !selectedFile.name.endsWith(".pdf") &&
      !selectedFile.name.endsWith(".docx")
    ) {
      setError("Invalid file type. Only PDF and DOCX files are allowed.");
      setFile(null);
      return;
    }

    // Validate size
    if (selectedFile.size > maxFileSize) {
      setError("File is too large. Maximum allowed size is 5MB.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate Required Fields
    if (!file) {
      setError("Please select and upload a valid resume file.");
      return;
    }
    if (!targetRole.trim()) {
      setError("Please enter a target role.");
      return;
    }
    if (targetRole.trim().length < 3) {
      setError("Target role must be at least 3 characters long.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await analyzeResume(file, provider, targetRole.trim());

      if (response.success) {
        navigate("/results", { state: { analysisData: response.data } });
      } else {
        setError(response.message || "Something went wrong during analysis.");
      }
    } catch (err) {
      console.error(err);
      setError(
        "Failed to connect to the server. Please verify your backend is running.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {isLoading && <AnalysisLoader />}

      <div className="max-w-2xl mx-auto my-12 w-full px-4">
        <Card title="Analyze Your Resume">
          <form onSubmit={handleSubmit} className="flex flex-col gap-6">
            <div className="border-2 border-dashed border-blue-200 rounded-xl p-8 text-center bg-blue-50">
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
                className="hidden"
                id="resume-upload"
                disabled={isLoading}
              />
              <label
                htmlFor="resume-upload"
                className="cursor-pointer flex flex-col items-center justify-center gap-2"
              >
                <svg
                  className="w-10 h-10 text-blue-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                  ></path>
                </svg>
                <span className="text-gray-700 font-medium">
                  {file ? file.name : "Click to upload your Resume (PDF/DOCX)"}
                </span>
              </label>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Target Role"
                name="targetRole"
                placeholder="e.g., Frontend Developer"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                disabled={isLoading}
              />

              <Select
                label="AI Provider"
                name="provider"
                options={providerOptions}
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                disabled={isLoading}
              />
            </div>

            {error && (
              <p className="text-red-500 text-sm font-medium">{error}</p>
            )}

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 mt-2"
            >
              {isLoading ? "Analyzing Resume..." : "Analyze Resume"}
            </Button>
          </form>
        </Card>
      </div>
    </>
  );
};

export default ResumeUploadSection;
