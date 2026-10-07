export type VerdictType = 'LEGITIMATE' | 'SUSPICIOUS' | 'PHISHING';

export type SeverityType = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface HeuristicFlag {
  code: string;
  severity: SeverityType;
  category: string;
  title: string;
  description: string;
  evidence: string;
  score_impact: number;
}

export interface PositiveFlag {
  category: string;
  title: string;
  description: string;
}

export interface MlPrediction {
  phishing_probability: number;
  raw_label: string;
  model_version: string;
  confidence: number;
}

export interface FeatureMetrics {
  url_length: number;
  hostname_length: number;
  path_length: number;
  query_length: number;
  num_path_segments: number;
  num_query_params: number;
  tld_length: number;
  subdomain_depth: number;
  count_dots: number;
  count_hyphens: number;
  count_underscores: number;
  count_slashes: number;
  count_question: number;
  count_equals: number;
  count_at: number;
  count_percent: number;
  count_digits: number;
  digit_ratio: number;
  entropy_url: number;
  entropy_hostname: number;
  entropy_path: number;
  count_suspicious_keywords: number;
  has_brand_in_subdomain: boolean;
  has_brand_in_path: boolean;
  is_shortened_url: boolean;
  has_hex_encoded_char: boolean;
  is_ip_address: boolean;
  is_https: boolean;
  has_non_standard_port: boolean;
  is_punycode: boolean;
  tld: string;
  domain: string;
}

export interface AnalysisResponse {
  url: string;
  normalized_url: string;
  verdict: VerdictType;
  risk_score: number;
  confidence: number;
  ml_prediction?: MlPrediction;
  heuristic_flags: HeuristicFlag[];
  positive_flags: PositiveFlag[];
  features: FeatureMetrics;
  recommendations: string[];
  analyzed_at: string;
  execution_time_ms: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  model_loaded: boolean;
  timestamp: string;
}

export interface ScanHistoryItem {
  id: string;
  url: string;
  verdict: VerdictType;
  risk_score: number;
  timestamp: string;
}
