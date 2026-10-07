import React from 'react';
import {
  Shield,
  Cpu,
  Lock,
  Terminal,
  Zap,
  CheckCircle2,
  Code2,
  ShieldAlert,
  ArrowRight,
  FileCode2,
  Sparkles
} from 'lucide-react';

interface AboutPageProps {
  onLaunchScanner: () => void;
}

export const AboutPage: React.FC<AboutPageProps> = ({ onLaunchScanner }) => {
  return (
    <div className="about-container">
      {/* Header */}
      <div className="about-header">
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.75rem', fontFamily: 'var(--font-mono)', fontWeight: 600, background: 'var(--accent-emerald-subtle)', color: 'var(--accent-emerald)', border: '1px solid var(--border-glow)', marginBottom: '1rem' }}>
          <Shield size={13} />
          <span>ABOUT LINKSHIELD</span>
        </div>
        <h1>High-Assurance Static URL Threat Intelligence</h1>
        <p>
          Built on zero-trust principles, LinkShield provides mathematical, transparent, and instant lexical forensics to protect organizations without the vulnerabilities of web scrapers or the hallucinations of AI chatbots.
        </p>
      </div>

      {/* 2-Column Core Architecture Cards */}
      <div className="about-grid-2">
        <div className="clean-card">
          <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: 'var(--accent-emerald-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-emerald)', marginBottom: '1rem' }}>
            <Lock size={20} />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
            The Zero-SSRF Philosophy
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>
            Traditional URL crawlers launch headless browsers or curl commands to fetch remote targets. This exposes the scanner to Server-Side Request Forgery (SSRF), triggers attacker tracking pixels, and risks payload execution.
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6, marginTop: '0.5rem' }}>
            LinkShield operates under a strict <strong>Zero Outbound Network</strong> invariant. Every computation is performed in-memory on the URL string itself.
          </p>
        </div>

        <div className="clean-card">
          <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: 'var(--accent-emerald-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-emerald)', marginBottom: '1rem' }}>
            <Cpu size={20} />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
            4-Layer Dissection Pipeline
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>
            LinkShield executes an integrated defense-in-depth pipeline:
          </p>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem', marginTop: '0.75rem', fontSize: '0.825rem', color: 'var(--text-secondary)' }}>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ color: 'var(--accent-emerald)', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>01</span>
              <span><strong>RFC 3986 Lexical Parsing:</strong> Punycode & percent-encoding resolution.</span>
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ color: 'var(--accent-emerald)', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>02</span>
              <span><strong>30 Mathematical Features:</strong> Shannon entropy & lexical ratios.</span>
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ color: 'var(--accent-emerald)', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>03</span>
              <span><strong>Forensic Heuristics:</strong> 7 high-trust detection rules with evidence strings.</span>
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ color: 'var(--accent-emerald)', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>04</span>
              <span><strong>Calibrated Random Forest:</strong> Statistical ML classification with fallback.</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Why Deterministic Beats Generative AI */}
      <div style={{ marginBottom: '3.5rem' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
          Why Deterministic Forensics Beats Generative AI for URLs
        </h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Large Language Models are probabilistic token decoders. They cannot reliably compute Shannon entropy, detect exact Punycode byte-mappings, or guarantee zero network calls.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem' }}>
          <div className="clean-card">
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <CheckCircle2 size={16} /> Zero Hallucinations
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.825rem', lineHeight: 1.55 }}>
              LLMs guess the next word based on token associations, often fabricating fake WHOIS data or missing subtle typosquats. LinkShield uses mathematical formulas that guarantee 100% reproducible results.
            </p>
          </div>

          <div className="clean-card">
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Zap size={16} /> Sub-15ms Latency
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.825rem', lineHeight: 1.55 }}>
              Waiting 3 to 10 seconds for an LLM to generate conversational prose makes inline email filtering or reverse-proxy inspection impossible. LinkShield evaluates every metric in-memory in under 15 milliseconds.
            </p>
          </div>

          <div className="clean-card">
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Lock size={16} /> Complete Confidentiality
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.825rem', lineHeight: 1.55 }}>
              Pasting sensitive internal corporate URLs, password reset links, or customer endpoints into public LLM clouds leaks data. LinkShield runs completely isolated on your own infrastructure.
            </p>
          </div>

          <div className="clean-card">
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Sparkles size={16} /> Homoglyph Math
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.825rem', lineHeight: 1.55 }}>
              Adversaries frequently use Cyrillic or Greek homoglyphs to deceive human eyes and LLM tokenizers. LinkShield mathematically decodes Punycode into ASCII codepoints and flags visually confusable characters.
            </p>
          </div>
        </div>
      </div>

      {/* Target Audiences */}
      <div style={{ marginBottom: '3.5rem' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1.25rem' }}>
          Who Can Use LinkShield?
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem' }}>
          <div className="clean-card">
            <div style={{ color: 'var(--accent-emerald)', marginBottom: '0.5rem' }}><Terminal size={20} /></div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>SOC Analysts</h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.825rem', lineHeight: 1.55 }}>
              Triage reported phishing campaigns instantly without triggering attacker beacons, with full evidence strings for SIEM tickets.
            </p>
          </div>

          <div className="clean-card">
            <div style={{ color: 'var(--accent-emerald)', marginBottom: '0.5rem' }}><Code2 size={20} /></div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>Developers & AppSec</h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.825rem', lineHeight: 1.55 }}>
              Integrate LinkShield into high-velocity CI/CD workflows, reverse proxies, and mail filters with sub-15ms throughput.
            </p>
          </div>

          <div className="clean-card">
            <div style={{ color: 'var(--accent-emerald)', marginBottom: '0.5rem' }}><ShieldAlert size={20} /></div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>Incident Responders</h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.825rem', lineHeight: 1.55 }}>
              Audit suspicious links extracted from malware or memory dumps without tipping off adversaries or leaking client data.
            </p>
          </div>
        </div>
      </div>

      {/* Technical Stack Attribution */}
      <div className="clean-card" style={{ marginBottom: '3rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.75rem' }}>
          <FileCode2 size={20} color="var(--accent-emerald)" />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)' }}>
            Engineering Standards & Technical Stack
          </h3>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: 1.6 }}>
          Backend in Python 3.12 (FastAPI, scikit-learn, Pydantic v2) with 132/132 passing Pytest security and regression tests. Frontend in React 18 with TypeScript, Vite, Tailwind CSS, Motion, and Shadcn UI components.
        </p>
        <div style={{ marginTop: '1rem', display: 'flex', gap: '1.5rem', flexWrap: 'wrap', fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
          <div>Engine: <span style={{ color: 'var(--accent-emerald)' }}>FastAPI + ML</span></div>
          <div>Architecture: <span style={{ color: 'var(--accent-emerald)' }}>Zero-SSRF Static</span></div>
          <div>Author: <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>Vyvek Sharma</span></div>
        </div>
      </div>

      {/* Launch CTA */}
      <div style={{ textAlign: 'center' }}>
        <button
          type="button"
          onClick={onLaunchScanner}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.75rem 1.85rem',
            fontSize: '0.9rem',
            fontWeight: 600,
            background: 'var(--accent-emerald-dark)',
            color: '#fff',
            border: 'none',
            borderRadius: '9px',
            cursor: 'pointer',
            boxShadow: 'var(--shadow-sm)',
          }}
        >
          <span>Open LinkShield Scanner</span>
          <ArrowRight size={15} />
        </button>
      </div>
    </div>
  );
};

export default AboutPage;
