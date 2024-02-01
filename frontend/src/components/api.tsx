import axios, { AxiosResponse } from 'axios';

// Define types for your API responses if needed
// For example, if your reset API returns a specific object:
type ResetResponse = {
  message: string;
  // other fields
};

// Set the base URL for axios requests
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create an instance of axios with the base URL
const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Function to reset the conversation
export const resetConversation = async (): Promise<AxiosResponse<ResetResponse>> => {
  try {
    const response = await apiClient.get<ResetResponse>('/reset');
    return response;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Handle Axios errors here
      console.error("Axios error:", error.message);
      // You can access error.response, error.request, etc.
    } else {
      // Handle non-Axios errors here
      console.error("Unexpected error:", error);
    }
    throw error;
  }
};
