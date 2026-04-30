import type { Evidence, Prediction } from '../types';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}

const apiRequest = async <T>(path: string, payload: Record<string, any>): Promise<T> => {
  const response = await fetch(`/api/${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = (await response.json().catch(() => ({}))) as ApiResponse<T>;
  if (!response.ok) {
    throw new Error(data.error || data.detail || `Failed to fetch from ${path}`);
  }
  return data.data ?? (data as T);
};

export const getOutbreakPrediction = async (evidence: Evidence, model: string): Promise<Prediction> => {
  return await apiRequest<Prediction>("predict", { evidence, model });
};
