import React from 'react';
import { Moon, Sun, ArrowRight } from 'lucide-react';

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
    <header className="slim-navbar">
      <div className="slim-navbar-inner">
        {/* Brand: Minimalist typography matching 21st.dev aesthetic */}
        <div
          className="brand-minimal"
          onClick={() => setActiveTab('home')}
          role="button"
          tabIndex={0}
        >
          <span>linkshield</span>
          <span className="brand-dot">.</span>
        </div>

        {/* Navigation Tabs */}
        <nav aria-label="Main Navigation">
          <ul className="slim-nav-links">
            <li>
              <button
                type="button"
                className={`slim-nav-btn ${activeTab === 'home' ? 'active' : ''}`}
                onClick={() => setActiveTab('home')}
              >
                Home
              </button>
            </li>
            <li>
              <button
                type="button"
                className={`slim-nav-btn ${activeTab === 'scanner' ? 'active' : ''}`}
                onClick={() => setActiveTab('scanner')}
              >
                Scanner Tool
              </button>
            </li>
            <li>
              <button
                type="button"
                className={`slim-nav-btn ${activeTab === 'about' ? 'active' : ''}`}
                onClick={() => setActiveTab('about')}
              >
                About Us
              </button>
            </li>
          </ul>
        </nav>

        {/* Right Side Actions: Compact Theme Toggle + Launch Scanner */}
        <div className="slim-nav-right">
          <button
            type="button"
            className="theme-toggle-minimal"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? <Moon size={15} /> : <Sun size={15} />}
          </button>

          <button
            type="button"
            className="nav-cta-minimal"
            onClick={() => setActiveTab('scanner')}
          >
            <span>Launch Scanner</span>
            <ArrowRight size={13} />
          </button>
        </div>
      </div>
    </header>
  );
};
