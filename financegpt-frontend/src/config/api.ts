export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000', // Backend is running on port 8000
  WS_BASE_URL: 'ws://localhost:8000', // WebSocket base URL for backend
  ENDPOINTS: {
    QUERY: '/query',
    LOGIN: '/auth/login',
    SIGNUP: '/auth/signup',
    LOGOUT: '/auth/logout',
    WS_STREAM: '/ws/stream', // WebSocket stream endpoint
  }
} as const;

// Helper function to get full API URL
export const getApiUrl = (endpoint: keyof typeof API_CONFIG.ENDPOINTS): string => {
  return `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS[endpoint]}`;
};

// Helper function to get full WebSocket URL
export const getWsUrl = (endpoint: keyof typeof API_CONFIG.ENDPOINTS): string => {
  // Use wss if the page is loaded over https
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = API_CONFIG.BASE_URL.replace(/^http(s?):\/\//, '');
  return `${protocol}//${host}${API_CONFIG.ENDPOINTS[endpoint]}`;
}; 