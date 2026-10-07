import React from 'react';
import {
  Shield,
  Cpu,
  Lock,
  Terminal,
  Zap,
  CheckCircle2,
  Code2,
  Users,
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
    <div className="about-page-wrapper" style={{ padding: '2rem 0 5rem' }}>
      {/* Hero Header */}
      <div style={{ textAlign: 'center', maxWidth: '820px', margin: '0 auto 4rem' }}>
        <div className="section-tag" style={{ margin: '0 auto 1.25rem' }}>
          <Shield size={14} />
          <span>ABOUT LINKSHIELD</span>
        </div>
        <h1 className="section-title" style={{ fontSize: 'clamp(2.2rem, 4vw, 3.2rem)' }}>
          High-Assurance Static URL Threat Intelligence
        </h1>
        <p className="section-desc" style={{ margin: '0 auto', fontSize: '1.1rem' }}>
          Built on zero-trust principles, LinkShield provides mathematical, transparent, and instant lexical forensics to protect organizations without the vulnerabilities of web scrapers or the hallucinations of AI chatbots.
        </p>
      </div>

      {/* Grid: Core Philosophy & Architecture */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem', marginBottom: '4.5rem' }}>
        <div className="cyber-card" style={{ padding: '2rem' }}>
          <div className="audience-icon-box" style={{ marginBottom: '1.25rem' }}>
            <Lock size={24} />
          </div>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
            The Zero-SSRF Philosophy
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Most traditional URL scanners launch headless browsers or curl commands to crawl destinations. This exposes the scanner to Server-Side Request Forgery (SSRF), triggers canary tokens, alerts attackers that their phishing campaign is being analyzed, and risks browser exploit delivery.
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6, marginTop: '0.75rem' }}>
            LinkShield operates under a strict <strong>Zero Outbound Network</strong> invariant. Every computation is performed in-memory on the URL string itself.
          </p>
        </div>

        <div className="cyber-card" style={{ padding: '2rem' }}>
          <div className="audience-icon-box" style={{ marginBottom: '1.25rem' }}>
            <Cpu size={24} />
          </div>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
            4-Layer Dissection Pipeline
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            LinkShield executes an integrated defense-in-depth pipeline:
          </p>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.75rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
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

      {/* Section: Who Can Use It */}
      <section className="landing-section" style={{ padding: '2rem 0 4rem' }}>
        <div className="section-tag">
          <Users size={14} />
          <span>Intended Users & Workflows</span>
        </div>
        <h2 className="section-title">Built for Modern Security Operators & Developers</h2>
        <p className="section-desc">
          Designed from the ground up to integrate seamlessly into diverse security workflows.
        </p>

        <div className="audience-grid">
          <div className="audience-card">
            <div className="audience-icon-box">
              <Terminal size={24} />
            </div>
            <h3>SOC Analysts & CSIRTs</h3>
            <p>
              When an employee reports a suspicious email, SOC analysts need instant answers. LinkShield breaks down the URL’s subdomain depth, flags target brand spoofs (e.g., PayPal or Microsoft tokens in untrusted domains), and calculates Shannon entropy in milliseconds.
            </p>
          </div>

          <div className="audience-card">
            <div className="audience-icon-box">
              <Code2 size={24} />
            </div>
            <h3>DevSecOps & Platform Engineers</h3>
            <p>
              Integrate LinkShield into high-velocity CI/CD workflows, reverse proxies, and mail transfer agents (MTAs). With an execution latency under 15ms, LinkShield acts as a first-line static firewall preventing phishing links from entering enterprise chat systems.
            </p>
          </div>

          <div className="audience-card">
            <div className="audience-icon-box">
              <ShieldAlert size={24} />
            </div>
            <h3>Incident Responders & Researchers</h3>
            <p>
              During active incident investigations, responders can safely audit batches of URLs extracted from memory dumps, malicious macros, or command lines without tipping off threat actors or leaking client data.
            </p>
          </div>
        </div>
      </section>

      {/* Section: Why Different & More Useful Than AI */}
      <section className="landing-section" style={{ padding: '2rem 0 4rem' }}>
        <div className="section-tag">
          <Zap size={14} />
          <span>Deterministic vs Generative</span>
        </div>
        <h2 className="section-title">Why Deterministic Forensics Beats Generative AI for URLs</h2>
        <p className="section-desc">
          Generic AI tools (LLMs) are revolutionary for text synthesis, but they are intrinsically ill-suited for critical cybersecurity URL evaluation.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
          <div className="cyber-card" style={{ padding: '1.75rem' }}>
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <CheckCircle2 size={18} /> Determinism vs Hallucination
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>
              LLMs guess the next token based on word associations. When asked if a URL is malicious, they often hallucinate fake WHOIS data or miss subtle typosquats. LinkShield uses mathematical formulas and verifiable rulebooks that guarantee 100% reproducible results.
            </p>
          </div>

          <div className="cyber-card" style={{ padding: '1.75rem' }}>
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Zap size={18} /> Sub-15ms vs 3000ms+ Latency
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>
              Waiting 3 to 10 seconds for an LLM to generate conversational prose makes inline email filtering or high-volume proxy inspection impossible. LinkShield evaluates every metric in-memory in under 15 milliseconds.
            </p>
          </div>

          <div className="cyber-card" style={{ padding: '1.75rem' }}>
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Lock size={18} /> Air-Gapped Confidentiality
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>
              Pasting sensitive internal corporate URLs, password reset tokens, or customer URLs into public LLM clouds leaks proprietary data and risks compliance violations. LinkShield runs completely isolated on your own infrastructure.
            </p>
          </div>

          <div className="cyber-card" style={{ padding: '1.75rem' }}>
            <h4 style={{ color: 'var(--accent-emerald)', fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Sparkles size={18} /> Mathematical Character Decoding
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>
              Adversaries frequently use Cyrillic or Greek homoglyphs (e.g., Cyrillic 'а' in <code>pаypal.com</code>) to deceive human eyes and LLM tokenizers. LinkShield mathematically decodes Punycode into ASCII codepoints and flags visually confusable characters.
            </p>
          </div>
        </div>
      </section>

      {/* Section: Technical Stack & Attribution */}
      <section className="cyber-card" style={{ padding: '2.5rem', marginTop: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
          <FileCode2 size={24} color="var(--accent-emerald)" />
          <h3 style={{ fontSize: '1.35rem', fontWeight: 600, color: 'var(--text-primary)' }}>
            Engineering Standards & Technical Stack
          </h3>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6, maxWidth: '850px' }}>
          LinkShield was engineered with production-grade rigor. The backend is written in Python 3.12 utilizing FastAPI and scikit-learn, validated by an automated test suite containing 132/132 passing Pytest unit, property-based, and security regression tests. The frontend is built on modern React with TypeScript, Vite, Tailwind CSS, and Shadcn UI components.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1.75rem' }}>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>BACKEND ENGINE</div>
            <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '0.25rem' }}>FastAPI + Pydantic v2</div>
          </div>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>MACHINE LEARNING</div>
            <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '0.25rem' }}>Calibrated Random Forest</div>
          </div>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>FRONTEND INTERFACE</div>
            <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '0.25rem' }}>React 18 + TypeScript + Vite</div>
          </div>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>AUTHOR & ARCHITECT</div>
            <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent-emerald)', marginTop: '0.25rem' }}>Vyvek Sharma</div>
          </div>
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <div style={{ marginTop: '4rem', textAlign: 'center' }}>
        <button
          type="button"
          onClick={onLaunchScanner}
          className="action-btn-primary"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.6rem',
            padding: '0.85rem 2.25rem',
            fontSize: '1rem',
            background: 'linear-gradient(135deg, var(--accent-emerald), #047857)',
            color: '#fff',
            border: 'none',
            borderRadius: '10px',
            fontWeight: 600,
            cursor: 'pointer',
            boxShadow: 'var(--glow-emerald)',
          }}
        >
          <span>Open LinkShield Scanner</span>
          <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
};

export default AboutPage;
