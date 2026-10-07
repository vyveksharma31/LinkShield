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
    <div className="flex items-center justify-center w-full h-full p-8">
      <p className="text-sm text-muted-foreground leading-relaxed">{content}</p>
    </div>
  );
}

const items: FeatureItem[] = [
  {
    title: "Zero-SSRF Defensive Static Analysis",
    alt: "LinkShield evaluates structural syntax and protocol semantics safely without making outbound web requests.",
    content: "https://cdn.21st.dev/assets/mirror/8c/8c4e18b6cde77ac53f3fa40ce7146594c03dd5fd0ebbd2adc9de141804a4d845.webm",
  },
  {
    title: "30-Dimensional Lexical & Entropy Matrix",
    alt: "Shannon entropy calculations, symbol ratios, and path tokens statically characterize URL structure in sub-15ms.",
    content: "https://cdn.21st.dev/assets/mirror/25/25228e9cefa50f9db3c28b77375e51fb15fc5975d98a6fbe23dbeeb9e068395d.webm",
  },
  {
    title: "Deterministic Brand Impersonation Forensics",
    alt: "High-value financial and tech brand tokens detected inside subdomains or paths when domains are untrusted.",
    content:
      "https://cdn.21st.dev/assets/localized/bd5e2be5d76b2e4f1612e70510357cf6865869dfed81859c4fd7b597ca38b9a6.png",
  },
  {
    title: "Calibrated Random Forest Inference",
    alt: "Machine learning classifier trained on balanced benchmarks with statistical confidence scoring and fail-soft fallback.",
    content: "https://cdn.21st.dev/assets/mirror/16/167a5626e0c8f3aa59c25b5dc3324a2d0178bbec206084a4375f5363e29ade5f.webm",
  },
  {
    title: "Actionable SOC Defense Guidance",
    alt: "Transparent explainability with concrete evidence strings and defense guidance tailored for SOC analysts.",
    content: "https://cdn.21st.dev/assets/mirror/6e/6eae938226ca5a8c25295b2f1a8cfee3d7e96db1445e63bdc7eff68309f95036.webm",
  },
];

export default function FeaturesWithPanel() {
  const [active, setActive] = React.useState(0);

  return (
    <section className="relative w-full py-16">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 lg:gap-16 lg:items-start">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 mb-4">
              DEFENSE-IN-DEPTH
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground md:text-4xl lg:text-5xl mb-4">
              Core Detection Capabilities.
            </h2>
            <p className="text-muted-foreground text-sm md:text-base mb-8 max-w-lg">
              Explore how LinkShield combines static mathematics, forensic domain heuristics, and machine learning into an explainable threat assessment platform.
            </p>

            <ul className="flex flex-col gap-1">
              {items.map((item, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, y: 8 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{
                    duration: 0.35,
                    delay: index * 0.07,
                    ease: "easeOut",
                  }}
                  onClick={() => setActive(index)}
                  className={cn(
                    "flex flex-col px-4 py-3.5 rounded-xl cursor-pointer transition-all duration-200 lg:flex-row lg:items-center lg:gap-4",
                    active === index
                      ? "ring-1 ring-foreground bg-muted/30"
                      : "ring-1 ring-transparent hover:bg-muted/10",
                  )}
                >
                  <div className="flex flex-row items-center gap-4 w-full lg:contents">
                    <span
                      className={cn(
                        "size-7 rounded-full flex items-center justify-center text-xs font-medium shrink-0 transition-colors duration-200",
                        active === index
                          ? "bg-foreground text-background"
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
                        <Card className="w-full mt-3 overflow-hidden p-0 gap-0 aspect-4/3 relative">
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

          <div className="hidden lg:block sticky top-24">
            <Card className="relative w-full aspect-4/3 overflow-hidden p-0 gap-0 border-border shadow-xl">
              <AnimatePresence mode="wait">
                <motion.div
                  key={active}
                  initial={{ opacity: 0, y: 12, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -8, scale: 0.98 }}
                  transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
                  className="absolute inset-0"
                >
                  <FeatureMedia
                    content={items[active].content}
                    alt={items[active].alt}
                  />
                </motion.div>
              </AnimatePresence>
            </Card>
            <div className="mt-4 p-4 rounded-xl bg-card border border-border">
              <p className="text-xs font-mono text-emerald-400 mb-1">CAPABILITY 0{active + 1}</p>
              <h4 className="text-sm font-semibold text-foreground mb-1">{items[active].title}</h4>
              <p className="text-xs text-muted-foreground">{items[active].alt}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
