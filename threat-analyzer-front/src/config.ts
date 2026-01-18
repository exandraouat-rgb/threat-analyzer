// Configuration de l'API
export const API_BASE_URL = import.meta.env.DEV 
  ? 'http://localhost:8000'
  : '/api';

export const API_ENDPOINTS = {
  ANALYZE: `${API_BASE_URL}/analyze`,
  GENERATE_PDF: `${API_BASE_URL}/generate-pdf`,
};
