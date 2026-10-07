import React from 'react';
import { Search, ArrowRight, AlertTriangle, Play } from 'lucide-react';

interface UrlFormProps {
  url: string;
  setUrl: (url: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  loading: boolean;
  error: string | null;
}

const PRESET_URLS = [
  { label: 'PayPal Spoof', url: 'https://paypal.secure-verification-portal.com/login' },
  { label: 'Legit Google', url: 'https://www.google.com/search?q=cybersecurity' },
  { label: 'Raw IP Host', url: 'http://192.168.1.100/login/verify' },
  { label: 'IDN Homoglyph', url: 'https://xn--pypal-4ve.com/signin' },
  { label: 'URL Shortener', url: 'https://bit.ly/secure-redirect-3x' },
];

export const UrlForm: React.FC<UrlFormProps> = ({
  url,
  setUrl,
  onSubmit,
  loading,
  error,
}) => {
  return (
    <div className="cyber-card hero-input-card">
      <div className="input-instructions">
        <h2>Static URL Forensics & Risk Engine</h2>
        <p>Submit any link for defensive static inspection, brand impersonation detection, and ML risk scoring.</p>
      </div>

      <form onSubmit={onSubmit} className="url-input-bar">
        <Search size={18} className="input-prefix-icon" />
        <input
          type="text"
          className="cyber-input"
          placeholder="e.g. https://secure-login.paypal.com.account-update.xyz/verify"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={loading}
          autoFocus
        />
        <button type="submit" className="cyber-button-submit" disabled={loading || !url.trim()}>
          {loading ? (
            <>ANALYZING...</>
          ) : (
            <>
              DISSECT URL <ArrowRight size={16} />
            </>
          )}
        </button>
      </form>

      <div className="presets-bar">
        <span className="presets-label">Sample Test Vectors:</span>
        {PRESET_URLS.map((preset) => (
          <button
            key={preset.label}
            type="button"
            className="preset-chip"
            onClick={() => setUrl(preset.url)}
            disabled={loading}
          >
            <Play size={10} style={{ display: 'inline', marginRight: '4px' }} />
            {preset.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="error-banner">
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
