import React from 'react';
import { NavTab } from './Navbar';

interface FooterProps {
  setActiveTab: (tab: NavTab) => void;
}

export const Footer: React.FC<FooterProps> = ({ setActiveTab }) => {
  return (
    <footer className="slim-footer">
      <div className="slim-footer-inner">
        <div>
          <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>linkshield.</span>
          <span style={{ marginLeft: '0.5rem', color: 'var(--text-muted)' }}>
            Static Threat Forensics & Lexical Dissection Engine · Zero-SSRF Guarantee
          </span>
        </div>

        <ul className="slim-footer-links">
          <li>
            <button type="button" onClick={() => setActiveTab('home')}>
              Home
            </button>
          </li>
          <li>
            <button type="button" onClick={() => setActiveTab('scanner')}>
              Scanner Tool
            </button>
          </li>
          <li>
            <button type="button" onClick={() => setActiveTab('about')}>
              About Us
            </button>
          </li>
          <li>
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
            >
              OpenAPI Docs
            </a>
          </li>
          <li>
            <a
              href="https://github.com/vyveksharma31/LinkShield"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
          </li>
        </ul>
      </div>
    </footer>
  );
};
