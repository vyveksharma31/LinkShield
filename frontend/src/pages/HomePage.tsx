import React, { useEffect, useState } from 'react';
import GlyphPortal from '@/components/ui/glyph-portal';
import FeaturesWithPanel from '@/components/ui/features-with-panel';
import {
  ShieldCheck,
  Zap,
  Terminal,
  Layers,
  CheckCircle2,
  ArrowRight,
  Code2,
  Users
} from 'lucide-react';

interface HomePageProps {
  onLaunchScanner: () => void;
}

const family = '"Glyph Portal Jakarta", "Inter", Arial, sans-serif';
let fontLoad: Promise<void> | undefined;

export const HomePage: React.FC<HomePageProps> = ({ onLaunchScanner }) => {
  const [face, setFace] = useState<string | null>(null);

  useEffect(() => {
    let settled = false;
    let timeoutId: number | undefined;
    const finish = (value: string) => {
      if (!settled) {
        settled = true;
        setFace(value);
      }
    };

    // Load custom face with graceful 800ms fallback so there is zero UI hang
    try {
      if (typeof window !== 'undefined' && 'fonts' in document) {
        fontLoad ??= new FontFace(
          'Glyph Portal Jakarta',
          'url("https://cdn.21st.dev/assets/mirror/15/153fc85b70298beeb1d61a5f723331649e7f23bb77302a66e61cb3e2fbdb5e79.woff2")',
          { weight: '400 700' }
        )
          .load()
          .then((font) => {
            document.fonts.add(font);
          });

        timeoutId = window.setTimeout(() => finish('Arial, sans-serif'), 800);
        void fontLoad.then(
          () => finish(family),
          () => finish('Arial, sans-serif')
        );
      } else {
        finish('Arial, sans-serif');
      }
    } catch {
      finish('Arial, sans-serif');
    }

    return () => {
      settled = true;
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, []);

  return (
    <div className="homepage-wrapper">
      {/* =========================================================================
          HERO SECTION: 21st.dev GLYPH PORTAL INTERACTION
          White background + Emerald Green Ink & Depth
          ========================================================================= */}
      <section className="glyph-hero-container" style={{ position: 'relative', width: '100%', minHeight: '85vh', overflow: 'hidden', background: 'var(--bg-primary)' }}>
        <div
          data-demo-scroll
          data-slipstream-demo
          tabIndex={0}
          role="region"
          aria-label="LinkShield. Interactive Scroll Portal."
          style={{
            width: '100%',
            height: 'min(780px, 92svh)',
            overflowY: 'auto',
            background: 'var(--bg-primary)',
            containerType: 'inline-size',
            fontFamily: face ?? 'Arial, sans-serif',
            borderRadius: '16px',
            border: '1px solid var(--border-subtle)',
            boxShadow: 'var(--shadow-md)',
          }}
        >
          <style>{`
            [data-slipstream-demo] [data-gp-caption]{inset:calc(var(--gp-word-bottom,50%) + 82px) 24px auto;justify-content:center;}
            [data-slipstream-demo] [data-gp-hint]{display:none;}
            [data-slipstream-demo] [data-gp-enter]{min-height:46px;padding:0 22px;gap:18px;background:#064e3b;border:1px solid #047857;border-radius:10px;color:#fff;font-size:13px;font-weight:600;box-shadow:0 2px 8px rgba(4,120,87,0.25);transition:all .18s;cursor:pointer;text-decoration:none;}
            [data-slipstream-demo] [data-gp-enter]:hover{background:#047857;box-shadow:0 4px 14px rgba(5,150,105,0.35);transform:translateY(-1px);}
            [data-slipstream-demo] [data-gp-enter]:focus-visible{outline:2px solid #10b981;outline-offset:4px;}
            [data-slipstream-demo] [data-gp-touch-picker]{top:auto;bottom:18px;left:50%;}
            [data-slipstream-demo] [data-gp-select]{border-color:transparent;border-radius:8px;font-size:12px;color:#626964;}
            [data-sublime-header]{position:absolute;inset:clamp(20px,4cqw,40px) clamp(20px,5cqw,56px) auto;display:flex;align-items:center;justify-content:space-between;gap:20px;}
            [data-sublime-logo]{font-size:20px;font-weight:700;letter-spacing:-.04em;color:var(--text-primary);display:flex;align-items:center;gap:6px;}
            [data-sublime-category]{font-size:12px;line-height:1.5;color:var(--text-secondary);font-family:var(--font-mono);font-weight:500;}
            [data-sublime-eyebrow]{position:absolute;inset:auto 24px calc(100% - var(--gp-word-top,35%) + 28px);margin:0;text-align:center;font-size:14px;font-weight:500;letter-spacing:.02em;color:var(--accent-emerald);}
            [data-sublime-support]{position:absolute;inset:calc(var(--gp-word-bottom,50%) + 24px) 24px auto;margin:0;text-align:center;font-size:16px;font-weight:400;line-height:1.5;color:var(--text-secondary);}
            [data-sublime-scroll]{position:absolute;inset:auto 24px 6%;text-align:center;color:var(--text-muted);font-size:11px;letter-spacing:.02em;}
            @media(any-pointer:coarse){[data-sublime-scroll]{bottom:12%;}}
            @container(max-width:450px){[data-sublime-category]{display:none;}[data-sublime-eyebrow]{font-size:12px;}[data-sublime-support]{font-size:13px;}[data-slipstream-demo] [data-gp-caption]{top:calc(var(--gp-word-bottom,50%) + 72px);}}
            @container(max-height:479px){[data-sublime-header]{top:16px;}[data-sublime-support]{top:calc(var(--gp-word-bottom,50%) + 14px);}[data-slipstream-demo] [data-gp-caption]{top:calc(var(--gp-word-bottom,50%) + 56px);}[data-sublime-scroll]{display:none;}}
            [data-slipstream-demo] [data-gp-content]{padding:4.5rem clamp(1.25rem,5cqw,4.5rem) 5.5rem;font-family:inherit;}
            [data-slipstream-copy]{display:flex;width:min(100%,80rem);margin:auto;flex-direction:column;align-items:flex-start;gap:clamp(1.5rem,4svh,2.75rem);}
            [data-slipstream-copy] h2{max-width:48rem;margin:0;color:inherit;font-size:clamp(1.75rem,1.1rem + 2.1cqw,2.4rem);font-weight:600;line-height:1.2;letter-spacing:-0.02em;text-wrap:balance;}
            [data-slipstream-features]{display:grid;width:100%;grid-template-columns:1fr;gap:1.75rem;}
            [data-slipstream-feature]{border-top:1px solid rgba(251,251,250,.25);padding-top:1.1rem;}
            [data-slipstream-feature] h3{margin:0;color:inherit;font-size:1.15rem;font-weight:600;line-height:1.2;letter-spacing:0;}
            [data-slipstream-feature] p{margin:.55rem 0 0;color:rgba(251,251,250,.88);font-size:.925rem;line-height:1.55;}
            [data-slipstream-no]{display:inline-block;margin-right:.7rem;color:var(--accent-emerald);font:700 .8rem var(--font-mono);letter-spacing:.08em;transform:translateY(-.1em);}
            @container(min-width:768px){[data-slipstream-features]{grid-template-columns:repeat(3,minmax(0,1fr));gap:2.5rem;}}
          `}</style>

          {face ? (
            <GlyphPortal
              word="LINKSHIELD"
              fontFamily={face}
              fontWeight={800}
              style={{
                fontFamily: face,
                // Harmonious emerald and clean paper palette
                '--gp-paper': 'var(--bg-primary)',
                '--gp-ink': 'var(--text-primary)',
                '--gp-field': '#0b3b2a',
                '--gp-foreground': '#fbfbfa',
              } as any}
              scrollLength={2.2}
              interactive={true}
              annotations={false}
              enterLabel="Step Inside Forensic Engine"
              front={
                <>
                  <div data-sublime-header>
                    <span data-sublime-logo>
                      LINK<span style={{ color: 'var(--accent-emerald)' }}>SHIELD</span>
                    </span>
                    <span data-sublime-category>STATIC FORENSIC SUITE</span>
                  </div>
                  <p data-sublime-eyebrow>Zero Outbound Requests · Zero SSRF · Sub-15ms</p>
                  <p data-sublime-support>High-trust mathematical URL threat dissection for modern security teams.</p>
                  <span data-sublime-scroll>Scroll letter to step inside ↓</span>
                </>
              }
            >
              <div data-slipstream-copy>
                <h2>A letter opens into forensic defense.</h2>
                <div data-slipstream-features>
                  <div data-slipstream-feature>
                    <h3>
                      <span data-slipstream-no>01</span>30 Static Metrics
                    </h3>
                    <p>Calculates Shannon entropy, symbol density, punycode, and path depth purely from URL structure.</p>
                  </div>
                  <div data-slipstream-feature>
                    <h3>
                      <span data-slipstream-no>02</span>Zero-SSRF Safety
                    </h3>
                    <p>Never executes DNS calls or HTTP fetches. Safely dissect malware links without triggering web beacons.</p>
                  </div>
                  <div data-slipstream-feature>
                    <h3>
                      <span data-slipstream-no>03</span>Explainable Forensics
                    </h3>
                    <p>Delivers concrete evidence strings and Calibrated Random Forest scores, not black-box guesses.</p>
                  </div>
                </div>

                <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    onClick={onLaunchScanner}
                    className="action-btn-primary"
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.6rem',
                      background: '#10b981',
                      color: '#022c22',
                      fontWeight: 700,
                      padding: '0.75rem 1.75rem',
                      borderRadius: '8px',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '0.95rem',
                      boxShadow: '0 4px 12px rgba(16,185,129,0.3)',
                    }}
                  >
                    <span>Launch Scanner Tool</span>
                    <ArrowRight size={18} />
                  </button>
                </div>
              </div>
            </GlyphPortal>
          ) : (
            <div
              role="status"
              style={{
                height: '100%',
                display: 'grid',
                placeItems: 'center',
                color: 'var(--text-muted)',
                fontSize: 14,
                fontFamily: 'var(--font-mono)',
              }}
            >
              Initializing LinkShield Cyber Engine...
            </div>
          )}
        </div>
      </section>

      {/* =========================================================================
          SECTION 1: WHAT LINKSHIELD DOES & FOR WHOM IT CAN BE USED
          ========================================================================= */}
      <section className="landing-section">
        <div className="section-tag">
          <Layers size={14} />
          <span>Purpose & Target Personas</span>
        </div>
        <h2 className="section-title">What is LinkShield and Who is it Built For?</h2>
        <p className="section-desc">
          LinkShield is a dedicated, zero-trust static URL inspection engine. It transforms raw, untrusted URLs into an actionable 30-point forensic matrix and calibrated risk score in under 15 milliseconds—without ever connecting to the destination server.
        </p>

        <div className="audience-grid">
          {/* Persona 1: SOC Analysts */}
          <div className="audience-card">
            <div className="audience-icon-box">
              <ShieldCheck size={26} />
            </div>
            <h3>SOC Analysts & Incident Responders</h3>
            <p>
              Triage phishing campaigns and suspicious alerts instantly. Inspect suspicious domains, punycode spoofs, and brand hijacking tokens with 100% safety, avoiding canary token activation or attacker reconnaissance logs.
            </p>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.75rem', fontSize: '0.825rem', color: 'var(--text-secondary)' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Zero risk of triggering attacker callbacks
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Concrete rule IDs for SIEM/SOAR tickets
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Instant verification of typosquats & homoglyphs
              </li>
            </ul>
          </div>

          {/* Persona 2: Developers & AppSec */}
          <div className="audience-card">
            <div className="audience-icon-box">
              <Code2 size={26} />
            </div>
            <h3>Security Engineers & Developers</h3>
            <p>
              Embed high-throughput link sanitization into chat apps, user submission forms, and email filtering gateways. LinkShield’s deterministic REST API evaluates thousands of requests per second without the overhead of headless browsers.
            </p>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.75rem', fontSize: '0.825rem', color: 'var(--text-secondary)' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Sub-15ms inline processing latency
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Zero-SSRF architecture guarantees system safety
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> OpenAPI v3 specification with typed schemas
              </li>
            </ul>
          </div>

          {/* Persona 3: Privacy-First Organizations */}
          <div className="audience-card">
            <div className="audience-icon-box">
              <Users size={26} />
            </div>
            <h3>Organizations & Everyday Users</h3>
            <p>
              Verify suspicious SMS messages, QR-code destinations, or unverified email attachments before clicking. LinkShield strips obfuscations and alerts you when a banking or social media domain is being impersonated.
            </p>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.75rem', fontSize: '0.825rem', color: 'var(--text-secondary)' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Plain-English risk verdicts: Safe, Suspicious, Malicious
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Zero tracking or third-party ad profiling
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--accent-emerald)" /> Actionable defensive advice for every scan
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 2: WHY LINKSHIELD IS DIFFERENT & MORE USEFUL THAN AI TOOLS
          ========================================================================= */}
      <section className="landing-section">
        <div className="section-tag">
          <Zap size={14} />
          <span>Architectural Advantage</span>
        </div>
        <h2 className="section-title">Why LinkShield Outperforms Generic AI / LLM Tools</h2>
        <p className="section-desc">
          Large Language Models (ChatGPT, Claude, Gemini) are probabilistic token generators. When asked about a URL, they cannot reliably compute Shannon entropy, detect exact Punycode byte-mappings, or guarantee zero network calls. Here is how LinkShield differs:
        </p>

        <div className="comparison-container">
          <table className="comparison-table">
            <thead>
              <tr>
                <th>Evaluation Dimension</th>
                <th className="highlight-col">LinkShield Engine</th>
                <th>Generic AI / LLM Bots</th>
                <th>Dynamic Web Scrapers</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="feature-name">Threat Hallucination Risk</td>
                <td className="highlight-col">
                  <strong>Zero (0%)</strong> — Deterministic equations and verified heuristic rulebooks.
                </td>
                <td>
                  <span style={{ color: 'var(--accent-crimson)' }}>High</span> — LLMs fabricate whois dates, registrar names, and reputation.
                </td>
                <td>
                  Low — Shows live content, but can be fooled by cloaking.
                </td>
              </tr>
              <tr>
                <td className="feature-name">Execution Latency</td>
                <td className="highlight-col">
                  <strong>&lt; 15 ms</strong> — Instant mathematical evaluation in-memory.
                </td>
                <td>
                  3,000 ms – 10,000 ms — Heavy transformer token decoding.
                </td>
                <td>
                  4,000 ms – 15,000 ms — Browser spin-up, timeouts, retries.
                </td>
              </tr>
              <tr>
                <td className="feature-name">Network Safety & SSRF</td>
                <td className="highlight-col">
                  <strong>Zero-SSRF</strong> — Never dials out to target IP or domain.
                </td>
                <td>
                  Uncertain — Web-browsing agents visit attacker servers directly.
                </td>
                <td>
                  <span style={{ color: 'var(--accent-crimson)' }}>High Risk</span> — Direct HTTP GET runs malware, triggers beacons.
                </td>
              </tr>
              <tr>
                <td className="feature-name">Punycode & Homoglyph Math</td>
                <td className="highlight-col">
                  <strong>Full RFC 3492 ASCII Decode</strong> — Catches Greek/Cyrillic spoofing.
                </td>
                <td>
                  Unreliable — LLM tokenizers often normalize or overlook homoglyphs.
                </td>
                <td>
                  Passive — Displays whatever DNS returns without character forensics.
                </td>
              </tr>
              <tr>
                <td className="feature-name">Explainable Audit Trail</td>
                <td className="highlight-col">
                  <strong>Exact Rule IDs & 30 Metrics</strong> — Ready for SOC SIEM/SOAR tickets.
                </td>
                <td>
                  Polite conversational text lacking structured SOC indicators.
                </td>
                <td>
                  Raw HTML dump with minimal automated security explanation.
                </td>
              </tr>
              <tr>
                <td className="feature-name">Data Privacy</td>
                <td className="highlight-col">
                  <strong>100% Confidential</strong> — Runs locally; no sensitive URLs sent to 3rd-party clouds.
                </td>
                <td>
                  URL sent to public LLM cloud and potentially stored for model training.
                </td>
                <td>
                  Target server logs your scanner’s IP and user-agent.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* =========================================================================
          SECTION 3: 21st.dev FEATURES WITH PANEL COMPONENT
          ========================================================================= */}
      <FeaturesWithPanel />

      {/* =========================================================================
          SECTION 4: HIGH-IMPACT LAUNCH SCANNER CTA BANNER
          ========================================================================= */}
      <section style={{ padding: '3rem 0 5rem' }}>
        <div className="cta-banner-card">
          <div className="section-tag" style={{ background: 'rgba(16, 185, 129, 0.15)' }}>
            <Terminal size={14} />
            <span>TRY IT LIVE</span>
          </div>
          <h2>Ready to Dissect a Suspicious URL?</h2>
          <p>
            Experience instant, zero-compromise static threat detection. Test known malicious URLs, IP-based bypasses, or corporate domains right now.
          </p>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem', flexWrap: 'wrap', justifyContent: 'center' }}>
            <button
              type="button"
              className="action-btn-primary"
              onClick={onLaunchScanner}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.6rem',
                fontSize: '1rem',
                padding: '0.85rem 2rem',
                background: 'linear-gradient(135deg, var(--accent-emerald), #047857)',
                color: '#ffffff',
                border: 'none',
                borderRadius: '10px',
                fontWeight: 600,
                cursor: 'pointer',
                boxShadow: 'var(--glow-emerald)',
              }}
            >
              <span>Launch Scanner Now</span>
              <ArrowRight size={18} />
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
