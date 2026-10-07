import React, { useState } from 'react';
import { Database, Binary, BarChart2, ShieldCheck, Globe } from 'lucide-react';
import { FeatureMetrics } from '../types';

interface FeaturesGridProps {
  features: FeatureMetrics;
}

type TabType = 'all' | 'structural' | 'entropy' | 'symbols' | 'semantics' | 'network';

export const FeaturesGrid: React.FC<FeaturesGridProps> = ({ features }) => {
  const [activeTab, setActiveTab] = useState<TabType>('all');

  const categories = [
    {
      id: 'structural',
      title: 'Structural & Lengths',
      icon: <Database size={14} />,
      items: [
        { label: 'URL Length', value: features.url_length },
        { label: 'Hostname Length', value: features.hostname_length },
        { label: 'Path Length', value: features.path_length },
        { label: 'Query Length', value: features.query_length },
        { label: 'Path Segments', value: features.num_path_segments },
        { label: 'Query Parameters', value: features.num_query_params },
        { label: 'TLD Length', value: features.tld_length },
        { label: 'Subdomain Depth', value: features.subdomain_depth },
      ],
    },
    {
      id: 'entropy',
      title: 'Shannon Entropy (bits/symbol)',
      icon: <BarChart2 size={14} />,
      items: [
        { label: 'URL Entropy', value: features.entropy_url.toFixed(3) },
        { label: 'Hostname Entropy', value: features.entropy_hostname.toFixed(3) },
        { label: 'Path Entropy', value: features.entropy_path.toFixed(3) },
      ],
    },
    {
      id: 'symbols',
      title: 'Symbol Counts & Ratios',
      icon: <Binary size={14} />,
      items: [
        { label: 'Dot Count (.)', value: features.count_dots },
        { label: 'Hyphen Count (-)', value: features.count_hyphens },
        { label: 'Underscores (_)', value: features.count_underscores },
        { label: 'Slash Count (/)', value: features.count_slashes },
        { label: 'Question Marks (?)', value: features.count_question },
        { label: 'Equals (=)', value: features.count_equals },
        { label: 'At Symbol (@)', value: features.count_at },
        { label: 'Percent Escapes (%)', value: features.count_percent },
        { label: 'Digit Count', value: features.count_digits },
        { label: 'Digit Ratio', value: (features.digit_ratio * 100).toFixed(1) + '%' },
      ],
    },
    {
      id: 'semantics',
      title: 'Brand Impersonation & Lures',
      icon: <ShieldCheck size={14} />,
      items: [
        { label: 'Suspicious Keywords', value: features.count_suspicious_keywords },
        { label: 'Brand in Subdomain', value: features.has_brand_in_subdomain ? 'YES' : 'NO', isBool: true, boolVal: features.has_brand_in_subdomain },
        { label: 'Brand in Path/Query', value: features.has_brand_in_path ? 'YES' : 'NO', isBool: true, boolVal: features.has_brand_in_path },
        { label: 'Shortener Domain', value: features.is_shortened_url ? 'YES' : 'NO', isBool: true, boolVal: features.is_shortened_url },
        { label: 'Hex Encoded Pattern', value: features.has_hex_encoded_char ? 'YES' : 'NO', isBool: true, boolVal: features.has_hex_encoded_char },
      ],
    },
    {
      id: 'network',
      title: 'Network & Protocol Hygiene',
      icon: <Globe size={14} />,
      items: [
        { label: 'IP Address Host', value: features.is_ip_address ? 'YES' : 'NO', isBool: true, boolVal: features.is_ip_address },
        { label: 'HTTPS Scheme', value: features.is_https ? 'YES' : 'NO', isBool: true, boolVal: !features.is_https },
        { label: 'Non-Standard Port', value: features.has_non_standard_port ? 'YES' : 'NO', isBool: true, boolVal: features.has_non_standard_port },
        { label: 'Punycode / IDN', value: features.is_punycode ? 'YES' : 'NO', isBool: true, boolVal: features.is_punycode },
        { label: 'Registered Domain', value: features.domain || 'N/A' },
        { label: 'TLD Suffix', value: features.tld ? `.${features.tld}` : 'N/A' },
      ],
    },
  ];

  const filteredCategories = activeTab === 'all'
    ? categories
    : categories.filter((c) => c.id === activeTab);

  return (
    <div className="cyber-card features-inspector-card">
      <div className="panel-header-bar">
        <div className="panel-title">
          <Database size={18} color="var(--accent-cyan)" />
          <span>Extracted Static Features (30 Metrics)</span>
        </div>

        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
          <button
            type="button"
            className="preset-chip"
            style={{ borderColor: activeTab === 'all' ? 'var(--accent-cyan)' : 'var(--border-subtle)' }}
            onClick={() => setActiveTab('all')}
          >
            All (30)
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              type="button"
              className="preset-chip"
              style={{ borderColor: activeTab === cat.id ? 'var(--accent-cyan)' : 'var(--border-subtle)' }}
              onClick={() => setActiveTab(cat.id as TabType)}
            >
              {cat.title.split(' ')[0]}
            </button>
          ))}
        </div>
      </div>

      {filteredCategories.map((cat) => (
        <div key={cat.id} style={{ marginTop: '1.25rem' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.5rem' }}>
            {cat.icon}
            <span>{cat.title}</span>
          </div>

          <div className="features-table-grid">
            {cat.items.map((item, idx) => {
              let valClass = '';
              if ('isBool' in item && item.isBool) {
                valClass = item.boolVal ? 'bool-true' : 'bool-false';
              }
              return (
                <div key={idx} className="feature-box">
                  <span className="feature-label">{item.label}</span>
                  <span className={`feature-value ${valClass}`}>{item.value}</span>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
};
