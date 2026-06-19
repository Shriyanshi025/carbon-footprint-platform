import axios from 'axios';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const calculateCarbonFootprint = async (formData) => {
  const response = await apiClient.post('/calculate', formData);
  return response.data;
};

export const fetchReductionTips = async (footprintData) => {
  const response = await apiClient.post('/tips', {
    footprint_data: footprintData,
  });

  return response.data;
};