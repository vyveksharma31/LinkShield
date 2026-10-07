import React, { useState, useEffect, Suspense, lazy } from 'react';
import { Navbar, NavTab } from './components/Navbar';
import { Footer } from './components/Footer';
import { Shield } from 'lucide-react';
import './styles/cyber.css';

// Lazy load page components to optimize bundle performance and guarantee zero UI lag
const HomePage = lazy(() => import('./pages/HomePage'));
const ScannerPage = lazy(() => import('./pages/ScannerPage'));
const AboutPage = lazy(() => import('./pages/AboutPage'));

// Tactical loading indicator for seamless suspense transitions
const TacticalLoader: React.FC = () => (
  <div
    style={{
      minHeight: '60vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '1.25rem',
    }}
  >
    <div
      style={{
        position: 'relative',
        width: '56px',
        height: '56px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: '50%',
          border: '2px solid rgba(16, 185, 129, 0.2)',
          borderTopColor: 'var(--accent-emerald)',
          animation: 'spin 0.8s linear infinite',
        }}
      />
      <Shield size={24} color="var(--accent-emerald)" />
    </div>
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.85rem',
          fontWeight: 600,
          color: 'var(--text-primary)',
          letterSpacing: '0.05em',
        }}
      >
        LOADING MODULE...
      </div>
      <div
        style={{
          fontSize: '0.75rem',
          color: 'var(--text-muted)',
          marginTop: '0.25rem',
        }}
      >
        Streaming static forensic assets
      </div>
    </div>
  </div>
);

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>('home');
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  // Initialize theme from localStorage or default to requested 'light' mode
  useEffect(() => {
    const savedTheme = localStorage.getItem('linkshield_theme') as 'light' | 'dark' | null;
    const initialTheme = savedTheme || 'light';
    setTheme(initialTheme);

    if (initialTheme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(nextTheme);
    localStorage.setItem('linkshield_theme', nextTheme);

    if (nextTheme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark');
    }
  };

  const handleTabChange = (tab: NavTab) => {
    setActiveTab(tab);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="site-wrapper" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Slim Global Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={handleTabChange}
        theme={theme}
        toggleTheme={toggleTheme}
      />

      {/* Main Page Body with Zero-Lag Lazy Loading */}
      <main style={{ flex: '1 0 auto', width: '100%' }}>
        <Suspense fallback={<TacticalLoader />}>
          {activeTab === 'home' && (
            <HomePage onLaunchScanner={() => handleTabChange('scanner')} />
          )}
          {activeTab === 'scanner' && <ScannerPage />}
          {activeTab === 'about' && (
            <AboutPage onLaunchScanner={() => handleTabChange('scanner')} />
          )}
        </Suspense>
      </main>

      {/* Minimal Footer */}
      <Footer setActiveTab={handleTabChange} />
    </div>
  );
};

export default App;
