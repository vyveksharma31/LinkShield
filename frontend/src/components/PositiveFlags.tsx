import React from 'react';
import { CheckCircle2 } from 'lucide-react';
import { PositiveFlag } from '../types';

interface PositiveFlagsProps {
  flags: PositiveFlag[];
}

export const PositiveFlags: React.FC<PositiveFlagsProps> = ({ flags }) => {
  if (flags.length === 0) return null;

  return (
    <div className="positive-flags-container">
      {flags.map((flag, idx) => (
        <div key={idx} className="positive-flag-card">
          <div className="positive-title">
            <CheckCircle2 size={14} />
            <span>{flag.title}</span>
          </div>
          <div className="positive-desc">{flag.description}</div>
        </div>
      ))}
    </div>
  );
};
