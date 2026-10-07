"use client";

import * as React from "react";
import { motion, AnimatePresence } from "motion/react";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface FeatureItem {
  title: string;
  alt?: string;
  content: string | React.ReactNode;
}

function FeatureMedia({
  content,
  alt,
}: {
  content: string | React.ReactNode;
  alt?: string;
}) {
  if (typeof content !== "string") {
    return <div className="w-full h-full">{content}</div>;
  }

  const isVideo = /\.(mp4|webm|ogg)$/i.test(content);
  const isImage =
    /\.(jpg|jpeg|png|webp|gif|avif|svg)$/i.test(content) ||
    /unsplash|images\./i.test(content);

  if (isVideo) {
    return (
      <video
        src={content}
        autoPlay
        muted
        loop
        playsInline
        className="w-full h-full object-cover"
      />
    );
  }

  if (isImage) {
    return (
      <img src={content} alt={alt} className="w-full h-full object-cover" />
    );
  }

  return (
    <div className="flex items-center justify-center w-full h-full p-8 text-center">
      <p className="text-sm text-muted-foreground leading-relaxed">{content}</p>
    </div>
  );
}

const items: FeatureItem[] = [
  {
    title: "Zero Hallucinations: 100% Mathematical Proof",
    alt: "LLMs guess word probabilities and fabricate WHOIS data. LinkShield computes exact Shannon entropy and deterministic RFC 3986 rules.",
    content: "https://cdn.21st.dev/assets/mirror/8c/8c4e18b6cde77ac53f3fa40ce7146594c03dd5fd0ebbd2adc9de141804a4d845.webm",
  },
  {
    title: "Sub-15ms Inline Latency vs 3-Second LLMs",
    alt: "Evaluates thousands of URLs per second directly in memory. Fast enough for inline email gateways, reverse proxies, and CI/CD pipelines.",
    content: "https://cdn.21st.dev/assets/mirror/25/25228e9cefa50f9db3c28b77375e51fb15fc5975d98a6fbe23dbeeb9e068395d.webm",
  },
  {
    title: "Zero-SSRF Safety: Never Touches The Target",
    alt: "Chatbots and web scrapers crawl attacker URLs, leaking your IP or downloading exploits. LinkShield never makes an outbound socket call.",
    content:
      "https://cdn.21st.dev/assets/localized/bd5e2be5d76b2e4f1612e70510357cf6865869dfed81859c4fd7b597ca38b9a6.png",
  },
  {
    title: "Punycode & Homoglyph Spoof Decoding",
    alt: "Adversaries use Cyrillic and Greek characters (like 'а' in pаypal) that fool LLM tokenizers. LinkShield mathematically resolves Punycode to ASCII.",
    content: "https://cdn.21st.dev/assets/mirror/16/167a5626e0c8f3aa59c25b5dc3324a2d0178bbec206084a4375f5363e29ade5f.webm",
  },
  {
    title: "Verifiable Evidence & Calibrated ML Scores",
    alt: "Outputs concrete heuristic rule IDs, lexical parameters, and calibrated Random Forest probabilities ready for SOC SIEM tickets.",
    content: "https://cdn.21st.dev/assets/mirror/6e/6eae938226ca5a8c25295b2f1a8cfee3d7e96db1445e63bdc7eff68309f95036.webm",
  },
];

export default function FeaturesWithPanel() {
  const [active, setActive] = React.useState(0);

  return (
    <section className="relative w-full py-12 lg:py-16">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 lg:gap-14 lg:items-start">
          {/* Left Column: Titles & Accordion */}
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 mb-3">
              DETERMINISTIC FORENSICS VS GENERIC AI
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground md:text-4xl mb-3">
              Why LinkShield Beats AI Tools.
            </h2>
            <p className="text-muted-foreground text-sm md:text-base mb-6 max-w-lg leading-relaxed">
              Generic LLMs hallucinate when evaluating URLs. LinkShield uses mathematical formulas and zero-outbound static analysis to deliver verifiable results in milliseconds.
            </p>

            <ul className="flex flex-col gap-1.5">
              {items.map((item, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, y: 8 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{
                    duration: 0.35,
                    delay: index * 0.05,
                    ease: "easeOut",
                  }}
                  onClick={() => setActive(index)}
                  className={cn(
                    "flex flex-col px-4 py-3 rounded-xl cursor-pointer transition-all duration-200 lg:flex-row lg:items-center lg:gap-4",
                    active === index
                      ? "ring-1 ring-foreground bg-muted/40 shadow-xs"
                      : "ring-1 ring-transparent hover:bg-muted/20",
                  )}
                >
                  <div className="flex flex-row items-center gap-4 w-full lg:contents">
                    <span
                      className={cn(
                        "size-7 rounded-full flex items-center justify-center text-xs font-medium shrink-0 transition-colors duration-200",
                        active === index
                          ? "bg-foreground text-background font-bold"
                          : "bg-muted text-muted-foreground",
                      )}
                    >
                      {index + 1}
                    </span>
                    <span
                      className={cn(
                        "text-sm font-medium transition-colors duration-200",
                        active === index
                          ? "text-foreground font-semibold"
                          : "text-muted-foreground",
                      )}
                    >
                      {item.title}
                    </span>
                  </div>

                  <AnimatePresence initial={false}>
                    {active === index && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
                        className="w-full overflow-hidden lg:hidden"
                      >
                        <Card
                          className="w-full mt-3 overflow-hidden p-0 gap-0 relative rounded-xl border"
                          style={{ aspectRatio: "4/3" }}
                        >
                          <div className="absolute inset-0">
                            <FeatureMedia
                              content={item.content}
                              alt={item.alt}
                            />
                          </div>
                        </Card>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.li>
              ))}
            </ul>
          </div>

          {/* Right Column: Sticky Media Panel */}
          <div className="hidden lg:block sticky top-20">
            <Card
              className="relative w-full overflow-hidden p-0 gap-0 rounded-2xl border shadow-md bg-muted/20"
              style={{ aspectRatio: "4/3", maxHeight: "380px" }}
            >
              <AnimatePresence mode="wait">
                <motion.div
                  key={active}
                  initial={{ opacity: 0, y: 10, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -6, scale: 0.98 }}
                  transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
                  className="absolute inset-0"
                >
                  <FeatureMedia
                    content={items[active].content}
                    alt={items[active].alt}
                  />
                </motion.div>
              </AnimatePresence>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}
