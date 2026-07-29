import type { Evidence, Prediction } from '../types';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string | any[];
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
    let errorMessage = data.error || `Failed to fetch from ${path}`;
    if (data.detail) {
      if (Array.isArray(data.detail)) {
        errorMessage = data.detail.map((err: any) => `${err.loc?.join('.') || 'Field'}: ${err.msg}`).join(', ');
      } else {
        errorMessage = String(data.detail);
      }
    }
    throw new Error(errorMessage);
  }
  return data.data ?? (data as T);
};

export const getOutbreakPrediction = async (evidence: Evidence, model: string, location: string = "Unknown"): Promise<Prediction> => {
  return await apiRequest<Prediction>("assess", { hazard: "disease", location, data: evidence, model });
};
