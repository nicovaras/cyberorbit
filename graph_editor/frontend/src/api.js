// src/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api'; // Ensure this matches your running backend

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Graph API Calls ---
export const getGraphs = () => apiClient.get('/graphs');

// --- Node API Calls ---
export const getGraphNodes = (graphId) => apiClient.get(`/graphs/${graphId}/nodes`);
export const getNodeDetails = (nodeId) => apiClient.get(`/nodes/${nodeId}`);
export const createNode = (graphId, nodeData) => apiClient.post(`/graphs/${graphId}/nodes`, nodeData);
export const updateNode = (nodeId, nodeData) => apiClient.put(`/nodes/${nodeId}`, nodeData);
export const deleteNode = (nodeId) => apiClient.delete(`/nodes/${nodeId}`);

// --- Exercise API Calls ---
export const addExercise = (nodeId, exerciseData) => apiClient.post(`/nodes/${nodeId}/exercises`, exerciseData);
export const updateExercise = (exerciseId, exerciseData) => apiClient.put(`/exercises/${exerciseId}`, exerciseData);
export const deleteExercise = (exerciseId) => apiClient.delete(`/exercises/${exerciseId}`);


// --- Error handling interceptor ---
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API call error:', error.response?.data?.description || error.response?.data || error.message);
    // Return a rejected promise with a user-friendly error message if possible
    const errorMessage = error.response?.data?.description || error.response?.data?.message || 'An API error occurred.';
    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;