import axios from 'axios';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const wait = (milliseconds) =>
  new Promise((resolve) => setTimeout(resolve, milliseconds));

const shouldRetryRequest = (error) => {
  const isNetworkError = !error.response;
  const isTimeout = error.code === 'ECONNABORTED';
  const isServerError = error.response?.status >= 500;

  return isNetworkError || isTimeout || isServerError;
};

const postWithRetry = async (
  endpoint,
  payload,
  {
    timeout = 15000,
    retries = 1,
  } = {}
) => {
  let lastError;

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      return await apiClient.post(endpoint, payload, {
        timeout,
      });
    } catch (error) {
      lastError = error;

      const noRetriesLeft = attempt === retries;

      if (noRetriesLeft || !shouldRetryRequest(error)) {
        throw error;
      }

      await wait(1200);
    }
  }

  throw lastError;
};

export const calculateCarbonFootprint = async (formData) => {
  const response = await postWithRetry(
    '/calculate',
    formData,
    {
      timeout: 20000,
      retries: 1,
    }
  );

  return response.data;
};

export const fetchReductionTips = async (footprintData) => {
  const response = await postWithRetry(
    '/tips',
    {
      footprint_data: footprintData,
    },
    {
      timeout: 15000,
      retries: 1,
    }
  );

  return response.data;
};

export const wakeBackend = async () => {
    try {
      await apiClient.get('/', {
        timeout: 60000,
      });
  
      return true;
    } catch {
      return false;
    }
  };