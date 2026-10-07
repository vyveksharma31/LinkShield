import React from 'react';
import { Shield, Moon, Sun, Terminal, Info, Home, ArrowRight } from 'lucide-react';

export type NavTab = 'home' | 'scanner' | 'about';

interface NavbarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  theme,
  toggleTheme,
}) => {
  return (
    <header className="main-navbar">
      <div className="navbar-inner">
        {/* Brand Logo & Name */}
        <div
          className="brand-logo"
          onClick={() => setActiveTab('home')}
          style={{ cursor: 'pointer' }}
          role="button"
          tabIndex={0}
          aria-label="LinkShield Home"
        >
          <div className="logo-icon-box">
            <Shield size={20} className="logo-shield-icon" />
          </div>
          <div className="brand-text">
            <span className="brand-name">
              LINK<span className="brand-name-accent">SHIELD</span>
            </span>
            <span className="brand-tagline">FORENSIC ENGINE</span>
          </div>
        </div>

        {/* Navigation Links */}
        <nav aria-label="Main Navigation">
          <ul className="nav-links">
            <li>
              <button
                type="button"
                className={`nav-link-btn ${activeTab === 'home' ? 'active' : ''}`}
                onClick={() => setActiveTab('home')}
              >
                <Home size={15} />
                <span>Home</span>
              </button>
            </li>
            <li>
              <button
                type="button"
                className={`nav-link-btn ${activeTab === 'scanner' ? 'active' : ''}`}
                onClick={() => setActiveTab('scanner')}
              >
                <Terminal size={15} />
                <span>Scanner Tool</span>
              </button>
            </li>
            <li>
              <button
                type="button"
                className={`nav-link-btn ${activeTab === 'about' ? 'active' : ''}`}
                onClick={() => setActiveTab('about')}
              >
                <Info size={15} />
                <span>About Us</span>
              </button>
            </li>
          </ul>
        </nav>

        {/* Right Actions: Theme Toggle + Launch Scanner CTA */}
        <div className="nav-right-actions">
          <button
            type="button"
            className="theme-toggle-btn"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
          </button>

          <button
            type="button"
            className="nav-cta-btn"
            onClick={() => setActiveTab('scanner')}
          >
            <span>Launch Scanner</span>
            <ArrowRight size={14} />
          </button>
        </div>
      </div>
    </header>
  );
};
