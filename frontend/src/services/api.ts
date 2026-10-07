import { AnalysisResponse, HealthResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number = 500) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

/**
 * Check backend API operational readiness and ML model availability.
 */
export async function checkApiHealth(): Promise<HealthResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/health`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    if (!res.ok) {
      throw new ApiError(`Health check responded with status ${res.status}`, res.status);
    }
    return await res.json();
  } catch (error: any) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(`Backend service unreachable: ${error.message || 'Connection refused'}`, 0);
  }
}

/**
 * Submit URL to LinkShield static analysis and risk classification engine.
 */
export async function analyzeUrl(url: string): Promise<AnalysisResponse> {
  const cleanUrl = url.trim();
  if (!cleanUrl) {
    throw new ApiError('Please enter a target URL to analyze.', 400);
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000);

    const res = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ url: cleanUrl }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!res.ok) {
      let errMsg = `Server returned status ${res.status}`;
      try {
        const errorJson = await res.json();
        if (errorJson.detail) {
          if (Array.isArray(errorJson.detail)) {
            errMsg = errorJson.detail.map((d: any) => d.msg).join('; ');
          } else {
            errMsg = errorJson.detail;
          }
        }
      } catch {
        // Fall back to default error string
      }
      throw new ApiError(errMsg, res.status);
    }

    return await res.json();
  } catch (error: any) {
    if (error.name === 'AbortError') {
      throw new ApiError('Analysis timed out. The backend did not respond within 15 seconds.', 408);
    }
    if (error instanceof ApiError) throw error;
    throw new ApiError(`Network request failed: ${error.message || 'Cannot connect to backend API'}`, 0);
  }
}
