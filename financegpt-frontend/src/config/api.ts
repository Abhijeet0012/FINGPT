export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000', // Backend is running on port 8000
  ENDPOINTS: {
    QUERY: '/query',
    LOGIN: '/auth/login',
    SIGNUP: '/auth/signup',
    LOGOUT: '/auth/logout',
  }
} as const;

// Helper function to get full API URL
export const getApiUrl = (endpoint: keyof typeof API_CONFIG.ENDPOINTS): string => {
  return `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS[endpoint]}`;
}; 