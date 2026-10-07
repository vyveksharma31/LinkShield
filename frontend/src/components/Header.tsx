import React from 'react';
import { Shield, Cpu, Github } from 'lucide-react';
import { HealthResponse } from '../types';

interface HeaderProps {
  health: HealthResponse | null;
  healthLoading: boolean;
}

export const Header: React.FC<HeaderProps> = ({ health, healthLoading }) => {
  const isHealthy = health?.status === 'healthy';
  const modelLoaded = health?.model_loaded ?? false;

  return (
    <header className="cyber-header">
      <div className="brand-section">
        <div className="brand-icon-box">
          <Shield size={24} />
        </div>
        <div className="brand-titles">
          <h1>
            LINKSHIELD
            <span style={{ fontSize: '0.65rem', color: 'var(--accent-cyan)', background: 'rgba(6,182,212,0.1)', border: '1px solid var(--accent-cyan)', padding: '2px 6px', borderRadius: '4px' }}>
              v1.0
            </span>
          </h1>
          <div className="brand-subtitle">Defensive Static Phishing Analysis & ML Intelligence</div>
        </div>
      </div>

      <div className="system-status-pills">
        <div className="status-pill" title="Backend API Connectivity">
          <span className={`status-dot ${isHealthy ? '' : 'offline'}`} />
          <span>{healthLoading ? 'CONNECTING...' : isHealthy ? 'API ONLINE' : 'API DISCONNECTED'}</span>
        </div>

        <div className="status-pill" title="Random Forest Classifier Inference State">
          <Cpu size={14} color={modelLoaded ? 'var(--accent-emerald)' : 'var(--accent-amber)'} />
          <span>{modelLoaded ? 'RF-MODEL ACTIVE' : 'HEURISTIC MODE'}</span>
        </div>

        <a
          href="https://github.com/vyveksharma31/LinkShield"
          target="_blank"
          rel="noopener noreferrer"
          className="status-pill"
          style={{ textDecoration: 'none', color: 'inherit' }}
          title="GitHub Repository"
        >
          <Github size={14} />
          <span>GITHUB</span>
        </a>
      </div>
    </header>
  );
};
