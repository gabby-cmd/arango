/**
 * API client for backend communication
 */
import axios from 'axios';
import type { Drug, InteractionResult, Stats, ConditionWarningsResult } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Search for drugs by name
 */
export const searchDrugs = async (query: string): Promise<Drug[]> => {
  try {
    const response = await apiClient.get<Drug[]>('/drugs', {
      params: { search: query, limit: 20 },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to search drugs');
    }
    throw error;
  }
};

/**
 * Get a single drug by its _key
 */
export const getDrugByKey = async (drugKey: string): Promise<Drug> => {
  try {
    const response = await apiClient.get<Drug>(`/drugs/${drugKey}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || `Failed to get drug: ${drugKey}`);
    }
    throw error;
  }
};

/**
 * Check for interactions between multiple drugs
 */
export const checkInteractions = async (drugKeys: string[]): Promise<InteractionResult> => {
  try {
    const response = await apiClient.post<InteractionResult>('/check-interactions', {
      drug_keys: drugKeys,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const errorMessage = error.response?.data?.detail || 'Failed to check interactions';
      throw new Error(errorMessage);
    }
    throw error;
  }
};

/**
 * Get database statistics
 */
export const getStats = async (): Promise<Stats> => {
  try {
    const response = await apiClient.get<Stats>('/stats');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to get statistics');
    }
    throw error;
  }
};

/**
 * Health check
 */
export const healthCheck = async (): Promise<{ status: string; database: string }> => {
  try {
    const response = await apiClient.get<{ status: string; database: string }>('/health');
    return response.data;
  } catch (error) {
    throw new Error('API health check failed');
  }
};

/**
 * Check for condition-based drug warnings
 */
export const checkConditionWarnings = async (
  drugKeys: string[],
  conditions: string[]
): Promise<ConditionWarningsResult> => {
  try {
    const response = await apiClient.post<ConditionWarningsResult>('/check-condition-warnings', {
      drug_keys: drugKeys,
      conditions: conditions
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to check condition warnings');
    }
    throw error;
  }
};

