import React from 'react';
import { HeuristicFlag } from '../types';

interface ThreatIndicatorsProps {
  flags: HeuristicFlag[];
}

export const ThreatIndicators: React.FC<ThreatIndicatorsProps> = ({ flags }) => {
  if (flags.length === 0) {
    return (
      <div style={{ padding: '1rem', background: 'var(--bg-secondary)', borderRadius: '8px', border: '1px solid var(--border-subtle)', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
        No threat heuristics triggered. The target domain and structure exhibit clean patterns.
      </div>
    );
  }

  return (
    <div className="threat-flags-list">
      {flags.map((flag, index) => {
        const severityClass = flag.severity.toLowerCase();
        return (
          <div key={`${flag.code}-${index}`} className="threat-flag-card">
            <div className="flag-top-row">
              <span className="flag-category-badge">{flag.category}</span>
              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                <span className={`flag-severity-pill ${severityClass}`}>
                  {flag.severity}
                </span>
                <span style={{ fontSize: '0.7rem', color: 'var(--accent-crimson)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                  +{flag.score_impact} PTS
                </span>
              </div>
            </div>

            <div className="flag-title">{flag.title}</div>
            <div className="flag-description">{flag.description}</div>

            {flag.evidence && (
              <div className="flag-evidence">
                Evidence: {flag.evidence}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
