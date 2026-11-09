# 🔎 Member 1 Audit — Frontend Development & UI/UX

**Area:** Landing page, Dashboard, navigation, and the UI/UX of Legal Research, Case Brief, Document Drafting & Source Library.
**Date:** 23 Oct 2026
**Method:** Read the actual source files and ran the project's own gate scripts (`check-landing-v5.mjs`, `check-product-copy.mjs`, `check-corpus.mjs`). Findings below are evidence-based, not assumed.

---

## 1. What is already implemented and working

| Area | File(s) | Status |
|---|---|---|
| Top navigation + mobile hamburger | `components/top-nav.tsx` | ✅ Working — responsive menu toggle, active-link state, brand, CTA |
| Root layout + footer | `app/layout.tsx` | ✅ Working — footer with brand, links, disclaimer |
| Landing page (full narrative) | `components/parallax-home.tsx` | ⚠️ Rich & functional, but **fails the project's own v5 gate** (see §2) |
| Dashboard | `components/dashboard-client.tsx`, `app/dashboard/page.tsx` | ✅ Working — hero, case list, empty state, skeleton, metric rail, bottom strip |
| Login (demo) | `components/login-demo.tsx`, `app/login/page.tsx` | ✅ Working — localStorage demo profile, validation, redirect to dashboard |
| Sources / Source Library | `app/sources/page.tsx`, `components/source-library.tsx` | ✅ Page + layout present; corpus check passes |
| Legal Research UI | `app/research/page.tsx`, `components/legal-research-demo.tsx` | ✅ Page wired to component |
| Case intake / result | `components/case-intake.tsx`, `components/case-result.tsx`, `app/case/new`, `app/case/[id]` | ✅ Pages wired |
| Icon system | `components/icons.tsx` | ✅ 12 inline SVG icons, consistent stroke style |
| Theme / CSS | `app/globals.css` (~1000 lines, 106 KB) | ✅ Substantial design system in place |
| Product-copy safety check | `scripts/check-product-copy.mjs` | ✅ PASS (22 files) |
| Corpus/source-domain check | `scripts/check-corpus.mjs` | ✅ PASS |

**Bottom line:** The frontend is far from a blank slate. A complete landing page, dashboard, login, and all route pages already exist with a cohesive design language.

---

## 2. What is incomplete or NOT working

### 🔴 BLOCKER — Landing page fails the project's own quality gate
`scripts/check-landing-v5.mjs` (run by `npm run test:core` → `npm run check`) expects the **v5 single-stage cinematic** architecture described in `docs/LANDING_V5_REBUILD.md`:

- one `experience-track` (`height:650vh`) + one sticky `experience-stage`
- continuous progress var `--p` and overlapping phase vars `--story`, `--organize`, `--law`, `--docs`, `--finale`
- pointer-depth vars `--mx` / `--my`
- `prefers-reduced-motion` fallback

The **current** `parallax-home.tsx` is an older multi-`<section>` structure (`landing-page`, `video-story`, `--story-progress`). Result when run:

```
FAIL landing v5 — single cinematic track
FAIL landing v5 — single sticky stage
FAIL landing v5 — continuous progress variable
FAIL landing v5 — overlapping story/organize/law/document phase
FAIL landing v5 — finale phase
FAIL landing v5 — pointer depth
```

So the whole `npm run check` pipeline is currently red. Either the component must be rebuilt to v5, or the team must consciously decide the v5 spec is retired and update/remove the gate. **This decision needs the team.**

### 🟠 Theme vs. brief
The brief asks for a **professional dark navy-blue theme with sidebar + navbar**. The current design is a warm **chocolate/walnut/ivory** cinematic direction (per `LANDING_V5_REBUILD.md`) with a **top nav, no sidebar**. This is a real divergence — needs a team decision: adopt navy-blue + sidebar, or keep the existing art direction?

### 🟡 Responsiveness — needs verification, not assumed
CSS is large and the nav has a mobile toggle, but I have **not** visually verified tablet/mobile breakpoints for the dashboard grid, landing narrative, and research/sources layouts. This must be checked in a running browser before marking "responsive" complete.

### 🟡 Document Drafting interface
Brief lists "Document Drafting" as a Member-1 surface. I found case intake/result and sources, but **no dedicated drafting UI component**. Confirm whether drafting lives inside case-result or needs a new interface.

---

## 3. Relevant files & components (Member 1 ownership map)

```
app/layout.tsx                      root shell, footer, metadata
app/page.tsx            ->  components/parallax-home.tsx      (LANDING)
app/dashboard/page.tsx  ->  components/dashboard-client.tsx   (DASHBOARD)
app/login/page.tsx      ->  components/login-demo.tsx
app/research/page.tsx   ->  components/legal-research-demo.tsx
app/sources/page.tsx    ->  components/source-library.tsx
app/case/new/page.tsx   ->  components/case-intake.tsx
app/case/[id]/page.tsx  ->  components/case-result.tsx
components/top-nav.tsx              navbar + mobile menu
components/icons.tsx                shared SVG icon set
components/reveal.tsx               scroll-reveal animation helper
components/hero-demo.tsx            (check usage)
app/globals.css                     full design system (~1000 lines)
docs/LANDING_V5_REBUILD.md          the spec the gate enforces
scripts/check-landing-v5.mjs        the gate that currently FAILS
```

---

## 4. Dependencies & blockers

- **Stack:** Next.js **16.3.8**, React **19.2.0** (very new — see `AGENTS.md`: "This is NOT the Next.js you know." Check `node_modules/next/dist/docs/` before writing new Next.js code; APIs may differ from older versions).
- **Blocker 1 (team decision):** v5 landing gate vs. current component — rebuild, or retire the gate?
- **Blocker 2 (team decision):** navy-blue + sidebar (brief) vs. chocolate/ivory top-nav (current). Shared file `app/globals.css` — coordinate before major theme edits.
- **Shared-file risk:** `globals.css` and `top-nav.tsx` are touched by every page. Announce before large edits per team rules.
- **No automated UI/responsive tests** — verification is manual in-browser.

---

## 5. Recommended next implementation step

1. **Get two team decisions first** (blockers above): (a) v5 landing rebuild vs. retire gate, (b) navy-blue+sidebar vs. keep current art direction. Nothing big should start before these are settled, since both touch shared files.
2. Once decided, **make `npm run check` green** — this is the single most important fix; the pipeline is currently red because of the landing gate.
3. Then do a **real responsive pass** (dashboard grid, landing, research, sources) verified at mobile/tablet/desktop widths in a browser.
4. Clarify and build the **Document Drafting** interface if it's a distinct surface.

---

## 6. Estimated time

| Work | Estimate |
|---|---|
| Team decisions + align on theme/landing direction | 0.5 day (discussion) |
| Reconcile landing gate (rebuild v5 **or** update/retire gate) | 1.5–3 days (rebuild) / 0.5 day (retire gate) |
| Navy-blue theme + sidebar (if chosen) | 2–3 days |
| Responsive pass + fixes across all pages | 1.5–2 days |
| Document Drafting UI (if new) | 1–2 days |
| **Total (typical path)** | **~5–8 working days** |

---

### Safety / integrity notes (kept intact)
- No credentials read or exposed during this audit.
- Demo data (login profile, local case store) is clearly demo-labeled — preserved.
- Source-provenance guardrails (`sources` page, product-copy check) are passing; do not present unverified legal info as authoritative.
```
