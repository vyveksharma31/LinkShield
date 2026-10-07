import React from 'react';
import { Info } from 'lucide-react';

interface RecommendationsListProps {
  recommendations: string[];
}

export const RecommendationsList: React.FC<RecommendationsListProps> = ({ recommendations }) => {
  if (recommendations.length === 0) return null;

  return (
    <div className="recommendations-card">
      <div className="panel-title" style={{ fontSize: '0.9rem' }}>
        <Info size={16} color="var(--accent-cyan)" />
        <span>Actionable Security Guidance & SOC Defense</span>
      </div>

      <ul className="recommendations-list">
        {recommendations.map((rec, index) => (
          <li key={index}>{rec}</li>
        ))}
      </ul>
    </div>
  );
};
