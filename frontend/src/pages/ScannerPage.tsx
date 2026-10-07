import React, { useState, useEffect } from 'react';
import { Header } from '../components/Header';
import { UrlForm } from '../components/UrlForm';
import { VerdictCard } from '../components/VerdictCard';
import { ThreatIndicators } from '../components/ThreatIndicators';
import { PositiveFlags } from '../components/PositiveFlags';
import { FeaturesGrid } from '../components/FeaturesGrid';
import { RecommendationsList } from '../components/RecommendationsList';
import { HistoryDrawer } from '../components/HistoryDrawer';
import { analyzeUrl, checkApiHealth } from '../services/api';
import { AnalysisResponse, HealthResponse, ScanHistoryItem } from '../types';

const HISTORY_STORAGE_KEY = 'linkshield_scan_history_v1';

export const ScannerPage: React.FC = () => {
  const [url, setUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState<boolean>(true);
  const [history, setHistory] = useState<ScanHistoryItem[]>([]);

  // 1. Initial Health Check & History Load
  useEffect(() => {
    async function loadHealth() {
      try {
        const data = await checkApiHealth();
        setHealth(data);
      } catch {
        setHealth(null);
      } finally {
        setHealthLoading(false);
      }
    }

    loadHealth();
    const intervalId = setInterval(loadHealth, 30000);

    try {
      const stored = localStorage.getItem(HISTORY_STORAGE_KEY);
      if (stored) {
        setHistory(JSON.parse(stored));
      }
    } catch {
      // Ignore storage read error
    }

    return () => clearInterval(intervalId);
  }, []);

  // 2. Handle URL Submission
  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    const targetUrl = url.trim();
    if (!targetUrl) return;

    setLoading(true);
    setError(null);

    try {
      const response = await analyzeUrl(targetUrl);
      setResult(response);

      // Append to history
      const historyItem: ScanHistoryItem = {
        id: `${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
        url: targetUrl,
        verdict: response.verdict,
        risk_score: response.risk_score,
        timestamp: new Date().toISOString(),
      };

      setHistory((prev) => {
        const filtered = prev.filter((item) => item.url !== targetUrl);
        const updated = [historyItem, ...filtered].slice(0, 10);
        try {
          localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(updated));
        } catch {
          // Ignore storage write error
        }
        return updated;
      });
    } catch (err: any) {
      setError(err.message || 'An unexpected analysis error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectHistory = (selectedUrl: string) => {
    setUrl(selectedUrl);
  };

  const handleClearHistory = () => {
    setHistory([]);
    try {
      localStorage.removeItem(HISTORY_STORAGE_KEY);
    } catch {
      // Ignore storage error
    }
  };

  return (
    <div className="scanner-page-container">
      <Header health={health} healthLoading={healthLoading} />

      <UrlForm
        url={url}
        setUrl={setUrl}
        onSubmit={handleAnalyze}
        loading={loading}
        error={error}
      />

      <HistoryDrawer
        history={history}
        onSelect={handleSelectHistory}
        onClear={handleClearHistory}
      />

      {loading && (
        <div className="cyber-card scanning-state" style={{ marginTop: '2rem' }}>
          <div className="radar-sweep-box" />
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              Executing Defensive Static Dissection...
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.25rem', fontFamily: 'var(--font-mono)' }}>
              Extracting 30 lexical metrics, evaluating threat heuristics, and calculating ML score
            </div>
          </div>
        </div>
      )}

      {result && !loading && (
        <div style={{ marginTop: '2rem' }}>
          <div className="assessment-grid">
            <VerdictCard data={result} />

            <div className="findings-panel">
              <div className="cyber-card" style={{ padding: '1.5rem' }}>
                <div className="panel-header-bar" style={{ marginBottom: '1rem' }}>
                  <div className="panel-title">
                    <span>Forensic Threat Indicators</span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                      ({result.heuristic_flags.length} Flagged)
                    </span>
                  </div>
                </div>

                <ThreatIndicators flags={result.heuristic_flags} />
              </div>

              {result.positive_flags.length > 0 && (
                <div className="cyber-card" style={{ padding: '1.5rem' }}>
                  <div className="panel-header-bar" style={{ marginBottom: '1rem' }}>
                    <div className="panel-title">
                      <span>Positive Security Factors</span>
                      <span style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', fontFamily: 'var(--font-mono)' }}>
                        ({result.positive_flags.length} Verified)
                      </span>
                    </div>
                  </div>

                  <PositiveFlags flags={result.positive_flags} />
                </div>
              )}

              <RecommendationsList recommendations={result.recommendations} />
            </div>
          </div>

          <FeaturesGrid features={result.features} />
        </div>
      )}
    </div>
  );
};

export default ScannerPage;
