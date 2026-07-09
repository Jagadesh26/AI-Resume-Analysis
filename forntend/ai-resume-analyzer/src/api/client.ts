import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 60000, // 60s timeout for heavy AI processing
  headers: {
    'Accept': 'application/json',
  },
  // Ensure we don't drop connections on large file uploads
  maxBodyLength: Infinity,
  maxContentLength: Infinity,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Centralized error mapping
    return Promise.reject(error?.response?.data || error.message);
  }
);