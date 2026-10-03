"use client";

import Link from "next/link";
import { useEffect, useRef } from "react";
import { Icon } from "./icons";

const clamp = (value: number) => Math.min(1, Math.max(0, value));
const smooth = (value: number) => {
  const x = clamp(value);
  return x * x * (3 - 2 * x);
};
const phase = (p: number, start: number, end: number) => smooth((p - start) / (end - start));
const bell = (p: number, start: number, peakIn: number, peakOut: number, end: number) => {
  const enter = phase(p, start, peakIn);
  const exit = 1 - phase(p, peakOut, end);
  return Math.min(enter, exit);
};

const setNumber = (node: HTMLElement, name: string, value: number) => {
  node.style.setProperty(name, value.toFixed(4));
};

export function ParallaxHome() {
  const experienceRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const experience = experienceRef.current;
    if (!experience) return;

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let frame = 0;
    let pointerFrame = 0;

    const render = () => {
      frame = 0;
      const rect = experience.getBoundingClientRect();
      const travel = Math.max(1, rect.height - window.innerHeight);
      const p = clamp(-rect.top / travel);

      setNumber(experience, "--p", p);
      setNumber(experience, "--intro", 1 - phase(p, 0.09, 0.20));
      setNumber(experience, "--story", bell(p, 0.10, 0.18, 0.28, 0.37));
      setNumber(experience, "--organize", bell(p, 0.28, 0.36, 0.47, 0.56));
      setNumber(experience, "--law", bell(p, 0.46, 0.54, 0.65, 0.74));
      setNumber(experience, "--docs", bell(p, 0.64, 0.72, 0.82, 0.89));
      setNumber(experience, "--finale", phase(p, 0.82, 0.95));
      setNumber(experience, "--brown-to-green", phase(p, 0.36, 0.58));
      setNumber(experience, "--green-to-brown", phase(p, 0.68, 0.80));
      setNumber(experience, "--camera", smooth(p));
    };

    const requestRender = () => {
      if (!frame) frame = window.requestAnimationFrame(render);
    };

    const onPointerMove = (event: PointerEvent) => {
      if (reduceMotion || event.pointerType === "touch") return;
      if (pointerFrame) window.cancelAnimationFrame(pointerFrame);
      pointerFrame = window.requestAnimationFrame(() => {
        const x = (event.clientX / Math.max(window.innerWidth, 1) - 0.5) * 2;
        const y = (event.clientY / Math.max(window.innerHeight, 1) - 0.5) * 2;
        setNumber(experience, "--mx", x);
        setNumber(experience, "--my", y);
      });
    };

    const resetPointer = () => {
      setNumber(experience, "--mx", 0);
      setNumber(experience, "--my", 0);
    };

    render();
    window.addEventListener("scroll", requestRender, { passive: true });
    window.addEventListener("resize", requestRender);
    experience.addEventListener("pointermove", onPointerMove, { passive: true });
    experience.addEventListener("pointerleave", resetPointer);

    return () => {
      window.removeEventListener("scroll", requestRender);
      window.removeEventListener("resize", requestRender);
      experience.removeEventListener("pointermove", onPointerMove);
      experience.removeEventListener("pointerleave", resetPointer);
      if (frame) window.cancelAnimationFrame(frame);
      if (pointerFrame) window.cancelAnimationFrame(pointerFrame);
    };
  }, []);

  return (
    <div className="experience-home">
      <section ref={experienceRef} id="story" className="experience-track" aria-label="Pakistan Justice Navigator product story">
        <div className="experience-stage">
          <div className="experience-light light-warm" aria-hidden="true" />
          <div className="experience-light light-green" aria-hidden="true" />
          <div className="experience-grain" aria-hidden="true" />

          <div className="experience-architecture" aria-hidden="true">
            <div className="architecture-floor" />
            <div className="architecture-column col-one" />
            <div className="architecture-column col-two" />
            <div className="architecture-column col-three" />
            <div className="architecture-column col-four" />
            <div className="architecture-portal portal-one" />
            <div className="architecture-portal portal-two" />
            <div className="architecture-portal portal-three" />
            <div className="architecture-horizon" />
          </div>

          <div className="experience-progress" aria-hidden="true">
            <span className="progress-label">01</span>
            <span className="progress-line"><i /></span>
            <span className="progress-label">06</span>
          </div>

          <div className="experience-scene scene-intro">
            <div className="experience-copy intro-copy">
              <span className="experience-eyebrow">PAKISTAN JUSTICE NAVIGATOR —</span>
              <h1>Justice should not feel <em>out of reach.</em></h1>
              <p>Tell us what happened. We help organize the story, surface official sources, and prepare you for the next legal conversation.</p>
              <div className="experience-actions">
                <Link href="/case/new" className="experience-cta primary">Start your case <Icon name="arrow" size={18} /></Link>
                <Link href="/research" className="experience-cta ghost">Explore official sources</Link>
              </div>
              <div className="experience-microcopy">Information support — not legal representation.</div>
            </div>

            <div className="experience-console" aria-label="Product preview">
              <div className="console-topline"><span>CASE PREPARATION</span><b>LIVE</b></div>
              <div className="console-user">Mere chacha ne hamari inherited property par qabza kar liya hai.</div>
              <div className="console-step"><i>01</i><div><strong>Clarify the facts</strong><span>Do you have ownership or inheritance documents?</span></div></div>
              <div className="console-step emphasized"><i>02</i><div><strong>Find source context</strong><span>Official legislation is retrieved with provenance.</span></div></div>
              <div className="console-step"><i>03</i><div><strong>Prepare the brief</strong><span>Facts, gaps, documents and source context.</span></div></div>
            </div>

            <div className="intro-caption">Built around Pakistani laws, courts and citizens.</div>
          </div>

          <div className="experience-scene scene-story">
            <div className="story-center">
              <span className="experience-eyebrow">START WITH YOUR OWN WORDS —</span>
              <h2>You know something is wrong.<br /><em>You may not know the legal words.</em></h2>
              <p>That is enough to begin.</p>
            </div>

            <div className="story-message">“Mere chacha ne hamari inherited property par qabza kar liya hai.”</div>

            <div className="floating-paper paper-notice"><b>LEGAL NOTICE</b><span>Response period</span><small>ORIGINAL SOURCE</small></div>
            <div className="floating-paper paper-deed"><b>SALE DEED</b><span>Ownership record</span><small>DOCUMENT</small></div>
            <div className="floating-paper paper-order"><b>COURT ORDER</b><span>Case record</span><small>JUDGMENT</small></div>
            <div className="floating-paper paper-fir"><b>FIR</b><span>Police record</span><small>CASE FILE</small></div>
          </div>

          <div className="experience-scene scene-organize">
            <div className="organize-copy">
              <span className="experience-eyebrow">FROM STORY TO STRUCTURE —</span>
              <h2><span>Understand.</span><span><em>Organize.</em></span><span>Verify.</span></h2>
              <p>Your words remain your words. AI organization and verified evidence stay visibly separate.</p>
            </div>
            <div className="case-orbit" aria-hidden="true">
              <div className="orbit-disc"><Icon name="scale" size={32} /><strong>YOUR CASE</strong></div>
              <div className="orbit-line orbit-line-one" />
              <div className="orbit-line orbit-line-two" />
              <div className="case-chip chip-one">PROPERTY</div>
              <div className="case-chip chip-two">INHERITANCE</div>
              <div className="case-chip chip-three">POSSESSION</div>
              <div className="case-chip chip-four">MISSING FACTS</div>
            </div>
          </div>

          <div className="experience-scene scene-law">
            <div className="law-copy-new">
              <span className="experience-eyebrow">OFFICIAL-SOURCE FIRST —</span>
              <h2>Pakistani law.<br /><em>Not generic AI.</em></h2>
              <p>Source identity stays attached to every result. Exact provisions appear only when retrieved from source text.</p>
              <Link href="/research" className="experience-cta ivory">Open legal research <Icon name="arrow" size={17} /></Link>
            </div>

            <div className="law-book" aria-label="Official legal source preview">
              <div className="law-book-spine">PAKISTAN CODE</div>
              <div className="law-book-page">
                <span className="law-seal"><Icon name="scale" size={22} /></span>
                <small>OFFICIAL SOURCE</small>
                <h3>Transfer of Property Act, 1882</h3>
                <div className="law-rule" />
                <p>Federal legislation</p>
                <div className="law-source-row"><span>Authority</span><strong>Ministry of Law & Justice</strong></div>
                <div className="law-source-row"><span>Status</span><strong>Source-linked</strong></div>
                <div className="law-source-row"><span>Exact section</span><strong>Only after retrieval</strong></div>
              </div>
            </div>

            <div className="law-source-tabs" aria-hidden="true">
              <span>Pakistan Code</span><span>Sindh Laws</span><span>Court Judgments</span>
            </div>
          </div>

          <div className="experience-scene scene-docs">
            <div className="docs-copy-new">
              <span className="experience-eyebrow">DOCUMENT INTELLIGENCE —</span>
              <h2>Your documents.<br /><em>Understood.</em></h2>
              <p>Important facts separate from the page without losing the original source.</p>
            </div>

            <div className="document-explosion" aria-hidden="true">
              <div className="document-main">
                <small>ORIGINAL DOCUMENT</small>
                <strong>LEGAL NOTICE</strong>
                <span>Property dispute — source preserved</span>
                <div className="document-lines"><i /><i /><i /><i /><i /></div>
              </div>
              <div className="fact-card fact-date"><small>DATE</small><strong>12 MAR 2018</strong><span>From page 1</span></div>
              <div className="fact-card fact-parties"><small>PARTIES</small><strong>SELLER / BUYER</strong><span>From document</span></div>
              <div className="fact-card fact-deadline"><small>DEADLINE</small><strong>NEEDS REVIEW</strong><span>Not assumed</span></div>
              <div className="fact-card fact-source"><small>PROVENANCE</small><strong>PAGE 1</strong><span>Traceable</span></div>
            </div>
          </div>

          <div className="experience-scene scene-finale">
            <div className="finale-copy-new">
              <span className="experience-eyebrow">WALK IN PREPARED —</span>
              <h2>Story + documents + law<br /><em>become one clear brief.</em></h2>
              <p>Not a verdict. Not legal representation. A clearer starting point for professional review.</p>
            </div>

            <div className="brief-object" aria-label="Lawyer-ready brief preview">
              <div className="brief-shadow-card shadow-three">OFFICIAL SOURCES</div>
              <div className="brief-shadow-card shadow-two">DOCUMENTS + TIMELINE</div>
              <div className="brief-shadow-card shadow-one">FACTS + OPEN QUESTIONS</div>
              <div className="brief-main-card">
                <span><Icon name="document" size={26} /></span>
                <small>PREPARED FOR LEGAL REVIEW</small>
                <strong>LAWYER-READY BRIEF</strong>
                <i>Facts — timeline — documents — source context</i>
              </div>
            </div>

            <Link href="/case/new" className="experience-cta primary finale-button">Start your case <Icon name="arrow" size={18} /></Link>
          </div>

          <div className="experience-scroll-hint" aria-hidden="true"><span>SCROLL</span><i /></div>
        </div>
      </section>

      <section className="experience-proof">
        <div className="page-shell proof-inner">
          <div><span>01</span><strong>Your facts</strong><small>What you actually told the system.</small></div>
          <div><span>02</span><strong>AI organization</strong><small>Issues and questions prepared for review.</small></div>
          <div><span>03</span><strong>Official sources</strong><small>Source identity remains visible.</small></div>
          <div><span>04</span><strong>Verified evidence</strong><small>Only after retrieval confirms it.</small></div>
        </div>
      </section>
    </div>
  );
}
