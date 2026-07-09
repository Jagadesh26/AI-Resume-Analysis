import apiClient from "../api/axios";

export const analyzeResume = async (file, provider, targetRole) => {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("provider", provider);
  formData.append("target_role", targetRole);

  // Content-Type is automatically set to multipart/form-data by Axios when using FormData
  const response = await apiClient.post("/resumes/analyze/", formData);
  return response.data;
};
