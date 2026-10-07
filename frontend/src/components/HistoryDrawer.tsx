import React from 'react';
import { History, Trash2 } from 'lucide-react';
import { ScanHistoryItem } from '../types';

interface HistoryDrawerProps {
  history: ScanHistoryItem[];
  onSelect: (url: string) => void;
  onClear: () => void;
}

export const HistoryDrawer: React.FC<HistoryDrawerProps> = ({
  history,
  onSelect,
  onClear,
}) => {
  if (history.length === 0) return null;

  return (
    <div className="cyber-card history-section">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          <History size={15} color="var(--accent-cyan)" />
          <span>Recent Analysis History ({history.length})</span>
        </div>

        <button
          type="button"
          onClick={onClear}
          style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem' }}
          title="Clear history"
        >
          <Trash2 size={13} />
          <span>Clear</span>
        </button>
      </div>

      <div className="history-items-row">
        {history.map((item) => {
          let scoreColor = 'var(--accent-emerald)';
          if (item.verdict === 'PHISHING') scoreColor = 'var(--accent-crimson)';
          else if (item.verdict === 'SUSPICIOUS') scoreColor = 'var(--accent-amber)';

          return (
            <div
              key={item.id}
              className="history-chip"
              onClick={() => onSelect(item.url)}
              title={item.url}
            >
              <span
                className="history-chip-score"
                style={{ color: scoreColor, background: 'rgba(0,0,0,0.3)', border: `1px solid ${scoreColor}` }}
              >
                {item.risk_score}
              </span>
              <span className="history-chip-url">{item.url}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
