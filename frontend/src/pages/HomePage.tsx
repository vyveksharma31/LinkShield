import React, { useEffect, useState } from 'react';
import GlyphPortal from '@/components/ui/glyph-portal';
import FeaturesWithPanel from '@/components/ui/features-with-panel';
import { ArrowRight } from 'lucide-react';

interface HomePageProps {
  onLaunchScanner: () => void;
}

const family = '"Glyph Portal Jakarta", Arial, sans-serif';
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

        timeoutId = window.setTimeout(() => finish('Arial, sans-serif'), 1200);
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
    <div className="homepage-container" style={{ width: '100%', background: 'var(--bg-primary)' }}>
      {/* =========================================================================
          COMPONENT 1: 21st.dev GLYPH PORTAL
          Scroll-driven camera through live type 'LINKSHIELD'
          ========================================================================= */}
      <section className="glyph-section-frame">
        <div
          data-demo-scroll
          data-slipstream-demo
          tabIndex={0}
          role="region"
          aria-label="LinkShield. Scroll to step inside."
          style={{
            width: '100%',
            height: 'min(760px, 94svh)',
            overflowY: 'auto',
            background: 'var(--bg-primary)',
            containerType: 'inline-size',
            fontFamily: face ?? 'Arial, sans-serif',
          }}
        >
          <style>{`
            [data-slipstream-demo] [data-gp-caption]{inset:calc(var(--gp-word-bottom,50%) + 82px) 24px auto;justify-content:center;}
            [data-slipstream-demo] [data-gp-hint]{display:none;}
            [data-slipstream-demo] [data-gp-enter]{min-height:46px;padding:0 22px;gap:20px;background:#064e3b;border:1px solid #047857;border-radius:10px;color:#fff;font-size:13px;font-weight:500;box-shadow:0 1px 2px rgba(4,120,87,0.2);transition:background .18s,box-shadow .18s;}
            [data-slipstream-demo] [data-gp-enter]:hover{background:#047857;box-shadow:0 3px 8px rgba(4,120,87,0.3);}
            [data-slipstream-demo] [data-gp-enter]:focus-visible{outline:2px solid #10b981;outline-offset:4px;}
            [data-slipstream-demo] [data-gp-touch-picker]{top:auto;bottom:18px;left:50%;}
            [data-slipstream-demo] [data-gp-select]{border-color:transparent;border-radius:8px;font-size:12px;color:#626964;}
            [data-sublime-header]{position:absolute;inset:clamp(24px,4.5cqw,48px) clamp(24px,5cqw,64px) auto;display:flex;align-items:center;justify-content:space-between;gap:20px;}
            [data-sublime-logo]{font-size:19px;font-weight:600;letter-spacing:-.065em;color:var(--text-primary);}
            [data-sublime-category]{font-size:12px;line-height:1.5;color:var(--text-secondary);}
            [data-sublime-eyebrow]{position:absolute;inset:auto 24px calc(100% - var(--gp-word-top,35%) + 32px);margin:0;text-align:center;font-size:13px;font-weight:400;line-height:1.5;letter-spacing:.005em;color:var(--text-secondary);}
            [data-sublime-support]{position:absolute;inset:calc(var(--gp-word-bottom,50%) + 32px) 24px auto;margin:0;text-align:center;font-size:16px;font-weight:400;line-height:1.5;color:var(--text-secondary);}
            [data-sublime-scroll]{position:absolute;inset:auto 24px 7%;text-align:center;color:var(--text-muted);font-size:11px;letter-spacing:.01em;}
            @media(any-pointer:coarse){[data-sublime-scroll]{bottom:13%;}}
            @container(max-width:450px){[data-sublime-category]{max-width:12ch;text-align:right;}[data-sublime-eyebrow]{font-size:12px;}[data-sublime-support]{font-size:14px;}[data-slipstream-demo] [data-gp-caption]{top:calc(var(--gp-word-bottom,50%) + 76px);}}
            @container(max-height:479px){[data-sublime-header]{top:18px;}[data-sublime-support]{top:calc(var(--gp-word-bottom,50%) + 16px);}[data-slipstream-demo] [data-gp-caption]{top:calc(var(--gp-word-bottom,50%) + 60px);}[data-sublime-scroll]{display:none;}}
            [data-slipstream-demo] [data-gp-content]{padding:5.5rem clamp(1.25rem,5cqw,5rem) 6.5rem;font-family:inherit;}
            [data-slipstream-demo] section,[data-slipstream-demo] [data-gp-caption]{font-family:inherit;}
            [data-slipstream-copy]{display:flex;width:min(100%,80rem);margin:auto;flex-direction:column;align-items:flex-start;gap:clamp(2rem,5svh,3.5rem);}
            [data-slipstream-copy] h2{max-width:48rem;margin:0;color:inherit;font-size:clamp(1.75rem,1.1rem + 2.1cqw,2.25rem);font-weight:400;line-height:1.25;letter-spacing:0;text-wrap:balance;}
            [data-slipstream-features]{display:grid;width:100%;grid-template-columns:1fr;gap:1.75rem;}
            [data-slipstream-feature]{border-top:1px solid rgba(251,251,250,.22);padding-top:1.1rem;}
            [data-slipstream-feature] h3{margin:0;color:inherit;font-size:1.125rem;font-weight:500;line-height:1.2;letter-spacing:0;}
            [data-slipstream-feature] p{margin:.55rem 0 0;color:rgba(251,251,250,.85);font-size:.9375rem;line-height:1.55;}
            [data-slipstream-no]{display:inline-block;margin-right:.7rem;color:rgba(251,251,250,.85);font:500 .75rem ui-monospace,monospace;letter-spacing:.08em;transform:translateY(-.1em);}
            @container(min-width:768px){[data-slipstream-features]{grid-template-columns:repeat(3,minmax(0,1fr));gap:3.5rem;}}
          `}</style>
          {face ? (
            <GlyphPortal
              word="LINKSHIELD"
              fontFamily={face}
              fontWeight={700}
              style={{
                fontFamily: face,
                '--gp-paper': 'var(--bg-primary)',
                '--gp-ink': 'var(--text-primary)',
                '--gp-field': '#0b3b2a',
                '--gp-foreground': '#fbfbfa',
              } as any}
              scrollLength={2.4}
              interactive={true}
              annotations={false}
              enterLabel="Step inside"
              front={
                <>
                  <div data-sublime-header>
                    <span data-sublime-logo>linkshield.</span>
                    <span data-sublime-category>Static Threat Forensics</span>
                  </div>
                  <p data-sublime-eyebrow>Zero Outbound Requests · Zero SSRF · Sub-15ms</p>
                  <p data-sublime-support>High-trust mathematical URL threat dissection for modern security teams.</p>
                  <span data-sublime-scroll>Scroll for a closer look ↓</span>
                </>
              }
            >
              <div data-slipstream-copy>
                <h2>Forensic precision without the black box.</h2>
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
                      <span data-slipstream-no>03</span>Deterministic & Fast
                    </h3>
                    <p>Sub-15ms execution that delivers explainable audit trails superior to generic AI hallucinations.</p>
                  </div>
                </div>

                <div style={{ marginTop: '1.5rem' }}>
                  <button
                    type="button"
                    onClick={onLaunchScanner}
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.6rem',
                      background: '#10b981',
                      color: '#022c22',
                      fontWeight: 600,
                      padding: '0.75rem 1.75rem',
                      borderRadius: '8px',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '0.9rem',
                    }}
                  >
                    <span>Launch Scanner Tool</span>
                    <ArrowRight size={16} />
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
                fontSize: 13,
                fontFamily: 'var(--font-mono)',
              }}
            >
              Loading type…
            </div>
          )}
        </div>
      </section>

      {/* =========================================================================
          COMPONENT 2: 21st.dev FEATURES WITH PANEL
          Cleanly fitted into the viewport with no old UI clutter
          ========================================================================= */}
      <section className="features-section-frame">
        <FeaturesWithPanel />
      </section>
    </div>
  );
};

export default HomePage;
