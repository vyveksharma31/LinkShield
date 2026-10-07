import React from 'react';
import { Shield, Github, ExternalLink, ShieldCheck, Heart } from 'lucide-react';
import { NavTab } from './Navbar';

interface FooterProps {
  setActiveTab: (tab: NavTab) => void;
}

export const Footer: React.FC<FooterProps> = ({ setActiveTab }) => {
  return (
    <footer className="main-footer">
      <div className="footer-inner">
        {/* Column 1: Brand & Philosophy */}
        <div className="footer-col brand-col">
          <div
            className="brand-logo"
            onClick={() => setActiveTab('home')}
            style={{ cursor: 'pointer', marginBottom: '1rem' }}
          >
            <div className="logo-icon-box">
              <Shield size={20} className="logo-shield-icon" />
            </div>
            <div className="brand-text">
              <span className="brand-name">
                LINK<span className="brand-name-accent">SHIELD</span>
              </span>
              <span className="brand-tagline">STATIC FORENSIC SUITE</span>
            </div>
          </div>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6, maxWidth: '380px' }}>
            High-assurance static threat analysis and lexical entropy dissection engine. Designed for SOC analysts, security engineers, and privacy-first organizations.
          </p>
          <div style={{ marginTop: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-emerald)', fontSize: '0.75rem', fontFamily: 'var(--font-mono)' }}>
            <ShieldCheck size={16} />
            <span>Zero-SSRF Defensive Guarantee</span>
          </div>
        </div>

        {/* Column 2: Platform Navigation */}
        <div className="footer-col">
          <h4>Navigation</h4>
          <ul className="footer-links">
            <li>
              <button type="button" onClick={() => setActiveTab('home')}>
                Home Landing
              </button>
            </li>
            <li>
              <button type="button" onClick={() => setActiveTab('scanner')}>
                Scanner Tool
              </button>
            </li>
            <li>
              <button type="button" onClick={() => setActiveTab('about')}>
                About & Methodology
              </button>
            </li>
            <li>
              <button type="button" onClick={() => { setActiveTab('home'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>
                Back to Top
              </button>
            </li>
          </ul>
        </div>

        {/* Column 3: Forensic Resources */}
        <div className="footer-col">
          <h4>Documentation</h4>
          <ul className="footer-links">
            <li>
              <a
                href="http://127.0.0.1:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
              >
                <span>Interactive OpenAPI</span>
                <ExternalLink size={12} />
              </a>
            </li>
            <li>
              <a
                href="http://127.0.0.1:8000/health"
                target="_blank"
                rel="noopener noreferrer"
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
              >
                <span>Health & Telemetry</span>
                <ExternalLink size={12} />
              </a>
            </li>
            <li>
              <a
                href="https://github.com/vyveksharma31/LinkShield"
                target="_blank"
                rel="noopener noreferrer"
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
              >
                <span>GitHub Repository</span>
                <Github size={12} />
              </a>
            </li>
          </ul>
        </div>

        {/* Column 4: Architectural Standard */}
        <div className="footer-col">
          <h4>Safety Standard</h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
            LinkShield operates under RFC 3986 lexical parsing and deterministic heuristics. Zero outbound requests ensure zero SSRF attack vectors and zero tracking pixel activation.
          </p>
          <div style={{ marginTop: '1rem', padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '8px', border: '1px solid var(--border-subtle)', fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)' }}>
            Status: <span style={{ color: 'var(--accent-emerald)' }}>Production Ready</span> (v1.0)
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div>
          © {new Date().getFullYear()} LinkShield Security Suite. Developed by{' '}
          <strong style={{ color: 'var(--text-primary)' }}>Vyvek Sharma</strong>. MIT License.
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span>Crafted for high-trust cybersecurity with</span>
          <Heart size={14} style={{ color: 'var(--accent-emerald)', fill: 'var(--accent-emerald)' }} />
        </div>
      </div>
    </footer>
  );
};
