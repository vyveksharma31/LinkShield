import React from 'react';
import { VerdictType } from '../types';

interface RiskGaugeProps {
  score: number;
  verdict: VerdictType;
}

export const RiskGauge: React.FC<RiskGaugeProps> = ({ score, verdict }) => {
  const radius = 75;
  const circumference = 2 * Math.PI * radius;
  const boundedScore = Math.min(100, Math.max(0, score));
  const offset = circumference - (boundedScore / 100) * circumference;

  let strokeColor = 'var(--accent-emerald)';
  let glowColor = 'var(--glow-emerald)';
  if (verdict === 'PHISHING') {
    strokeColor = 'var(--accent-crimson)';
    glowColor = 'var(--glow-crimson)';
  } else if (verdict === 'SUSPICIOUS') {
    strokeColor = 'var(--accent-amber)';
    glowColor = '0 0 20px rgba(245, 158, 11, 0.4)';
  }

  return (
    <div className="gauge-wrapper" style={{ filter: `drop-shadow(${glowColor})` }}>
      <svg className="gauge-svg" viewBox="0 0 180 180">
        <circle
          className="gauge-bg-circle"
          cx="90"
          cy="90"
          r={radius}
        />
        <circle
          className="gauge-progress-circle"
          cx="90"
          cy="90"
          r={radius}
          stroke={strokeColor}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="gauge-center-content">
        <span className="gauge-score-number" style={{ color: strokeColor }}>
          {boundedScore}
        </span>
        <span className="gauge-score-label">THREAT SCORE</span>
      </div>
    </div>
  );
};
