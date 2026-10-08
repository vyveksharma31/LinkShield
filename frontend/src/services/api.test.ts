import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { analyzeUrl, checkApiHealth } from './api';

describe('Frontend API Service', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('analyzeUrl', () => {
    it('throws ApiError when url is empty or whitespace only', async () => {
      await expect(analyzeUrl('   ')).rejects.toThrow('Please enter a target URL to analyze.');
    });

    it('successfully posts to /api/v1/analyze and returns structured report', async () => {
      const mockReport = {
        url: 'https://example.com',
        normalized_url: 'https://example.com',
        verdict: 'LEGITIMATE',
        risk_score: 10,
        confidence: 0.95,
        features: { is_https: true },
        heuristic_flags: [],
        positive_flags: [],
        recommendations: ['Safe to browse'],
        analyzed_at: '2026-10-08T09:00:00Z',
        execution_time_ms: 12.5,
      };

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockReport,
      } as any);

      const result = await analyzeUrl('https://example.com');
      expect(result).toEqual(mockReport);
      expect(globalThis.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/analyze'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ url: 'https://example.com' }),
        })
      );
    });

    it('parses error detail from 422 unprocessable responses', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 422,
        json: async () => ({ detail: 'Dangerous or non-web scheme is not permitted.' }),
      } as any);

      await expect(analyzeUrl('javascript:alert(1)')).rejects.toThrow('Dangerous or non-web scheme is not permitted.');
    });

    it('handles network failure with connection refused message', async () => {
      globalThis.fetch = vi.fn().mockRejectedValue(new Error('Failed to fetch'));

      await expect(analyzeUrl('https://example.com')).rejects.toThrow('Network request failed: Failed to fetch');
    });
  });

  describe('checkApiHealth', () => {
    it('returns health payload when server is reachable', async () => {
      const mockHealth = {
        status: 'healthy',
        version: '1.0.0',
        model_loaded: true,
        timestamp: '2026-10-08T09:00:00Z',
      };

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockHealth,
      } as any);

      const result = await checkApiHealth();
      expect(result).toEqual(mockHealth);
    });

    it('throws ApiError if health check endpoint returns 500 error', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
      } as any);

      await expect(checkApiHealth()).rejects.toThrow('Health check responded with status 500');
    });
  });
});
