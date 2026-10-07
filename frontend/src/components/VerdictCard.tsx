import React from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle } from 'lucide-react';
import { AnalysisResponse } from '../types';
import { RiskGauge } from './RiskGauge';

interface VerdictCardProps {
  data: AnalysisResponse;
}

export const VerdictCard: React.FC<VerdictCardProps> = ({ data }) => {
  const { verdict, risk_score, confidence, execution_time_ms, ml_prediction, normalized_url } = data;

  const getVerdictClass = () => {
    switch (verdict) {
      case 'PHISHING':
        return 'phishing';
      case 'SUSPICIOUS':
        return 'suspicious';
      default:
        return 'legitimate';
    }
  };

  const getVerdictIcon = () => {
    switch (verdict) {
      case 'PHISHING':
        return <ShieldAlert size={20} />;
      case 'SUSPICIOUS':
        return <AlertTriangle size={20} />;
      default:
        return <ShieldCheck size={20} />;
    }
  };

  return (
    <div className="cyber-card verdict-gauge-card">
      <div className={`verdict-badge ${getVerdictClass()}`}>
        {getVerdictIcon()}
        <span>{verdict}</span>
      </div>

      <RiskGauge score={risk_score} verdict={verdict} />

      <div style={{ fontSize: '0.785rem', color: 'var(--text-secondary)', maxWidth: '280px', wordBreak: 'break-all', fontFamily: 'var(--font-mono)' }}>
        {normalized_url}
      </div>

      <div className="telemetry-row">
        <div className="telemetry-item">
          <span className="telemetry-key">CONFIDENCE</span>
          <span className="telemetry-val">{(confidence * 100).toFixed(0)}%</span>
        </div>
        <div className="telemetry-item">
          <span className="telemetry-key">LATENCY</span>
          <span className="telemetry-val">{execution_time_ms} ms</span>
        </div>
        <div className="telemetry-item">
          <span className="telemetry-key">ML PROBABILITY</span>
          <span className="telemetry-val">
            {ml_prediction ? `${(ml_prediction.phishing_probability * 100).toFixed(1)}%` : 'N/A'}
          </span>
        </div>
        <div className="telemetry-item">
          <span className="telemetry-key">CLASSIFIER</span>
          <span className="telemetry-val">
            {ml_prediction ? ml_prediction.model_version : 'Heuristic'}
          </span>
        </div>
      </div>
    </div>
  );
};
