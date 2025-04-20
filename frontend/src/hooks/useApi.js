import { useState, useCallback } from 'react';
import axios from 'axios';

// Determine API base URL based on environment
const getApiUrl = () => {
  // In production Docker environment
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // For local development with webpack proxy
  return '';
};

const API_BASE_URL = getApiUrl();

// Create axios instance with defaults
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

/**
 * Custom hook for making API calls
 */
export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Start a new research job
   */
  const startResearchJob = useCallback(async (topic, filename = "research_paper.pdf") => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.post('/api/start', { topic, filename });
      return response.data;
    } catch (err) {
      console.error('API error:', err);
      setError(err.response?.data?.message || 'Failed to start research job');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Get job status updates
   */
  const getJobStatus = useCallback(async (jobId) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.get(`/api/status/${jobId}`);
      return response.data;
    } catch (err) {
      console.error('API error:', err);
      setError(err.response?.data?.message || 'Failed to get job status');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Get download URL for generated file
   */
  const getDownloadUrl = useCallback((filename) => {
    return `${API_BASE_URL}/api/download/${filename}`;
  }, []);

  /**
   * Test API with arXiv search
   */
  const testArxivSearch = useCallback(async (query, limit = 3) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.get(`/api/test/arxiv?query=${encodeURIComponent(query)}&limit=${limit}`);
      return response.data;
    } catch (err) {
      console.error('API error:', err);
      setError(err.response?.data?.message || 'Failed to search arXiv');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Check API health
   */
  const checkHealth = useCallback(async () => {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (err) {
      console.error('Health check error:', err);
      return { status: 'error', message: 'API is not responding' };
    }
  }, []);

  return {
    loading,
    error,
    startResearchJob,
    getJobStatus,
    getDownloadUrl,
    testArxivSearch,
    checkHealth
  };
};

export default useApi; 