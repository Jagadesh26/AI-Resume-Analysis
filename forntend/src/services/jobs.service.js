import apiClient from "../api/axios";

export const fetchRecommendedJobs = async (searchParams) => {
  try {
    // searchParams contains roles, preferred_location, skills, experience_level
    const response = await apiClient.post("/jobs/search/", searchParams);
    return response.data;
  } catch (error) {
    console.error("Error fetching jobs:", error);
    throw error;
  }
};
