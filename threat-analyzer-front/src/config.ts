// Configuration de l'API
export const API_BASE_URL = import.meta.env.DEV 
  ? 'http://localhost:8000'
  : '/api';

export const API_ENDPOINTS = {
  HEALTH: `${API_BASE_URL}/health`,
  ANALYZE: `${API_BASE_URL}/analyze`,
  GENERATE_PDF: `${API_BASE_URL}/generate-pdf`,
  REGISTER: `${API_BASE_URL}/api/auth/register`,
  LOGIN: `${API_BASE_URL}/api/auth/login`,
  GET_USER: `${API_BASE_URL}/api/auth/user`,
};
