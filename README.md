# ChronoSelf — Human Potential Optimized

**Algorithmic gap arbitration between real-time cognitive behavior and your Ideal Executive Persona.**

ChronoSelf is a time-management web app built for a 1.5-hour college hackathon. It goes beyond a plain to-do list by giving every user a personalized **"Ideal Self" benchmark** and then continuously showing them the live gap between who they are today and who they're calibrated to become — with an AI-styled engine that swaps out low-value habits for high-leverage ones in real time.

---

## ✨ Core Concept

Most productivity apps track tasks. ChronoSelf tracks **you vs. your potential**.

1. Pick a persona (Student / Working Professional / Executive Staff) and calibrate your ideal sleep, focus windows, and chronotype.
2. The **Daily Command Hub** compares your actual behavior against that benchmark in real time.
3. The **Neural Swap Engine** flags low-value tasks (doomscrolling, unfocused sprints, reactive email) and instantly suggests a higher-leverage replacement.
4. **Wellbeing & Brain Gym** tracks sleep architecture and sharpens focus with quick cognitive drills.
5. **Analytics & Reports** turns everything into a historical, chart-driven performance record — with streaks and ChronoXP to keep it addictive in a good way.

---

## 🖥️ Pages / Features

| Page | File | What it does |
|---|---|---|
| **Onboarding & Persona** | `onboarding.html` | "Persona & Benchmark Calibration" — pick your archetype (Academic Polymath / Strategic High-Performer / Vanguard Visionary), set target sleep hours, peak-focus window, chronotype (Early Bird / Night Owl), and flag your known friction points (doomscrolling, context switching, etc.) |
| **Daily Command Hub** | `index.html` | The main dashboard: a live **Gap Telemetry** radar (% match to your Ideal Self), the **Smart Task Replacement / Neural Swap Engine** (accept/decline AI-suggested task swaps for ChronoXP), a Gap Breakdown panel (Deep Cognitive Work vs. friction/drift vs. Biometric Energy Resonance), a daily timeline, a to-do matrix, and a streak/momentum tracker |
| **Wellbeing & Brain Gym** | `wellbeing.html` | Sleep score, sleep-stage architecture (Deep / REM / Light), a sleep hypnogram, circadian phase engine, and quick brain-training drills (Dual N-Back memory sprint, Pomodoro alpha-wave breathwork, cognitive-refocus "distraction purge") |
| **Analytics & Reports** | `analytics.html` | Task-completion velocity and historical performance charts derived from your Ideal Self archetype, auto-generated from the Command Hub layout |
| **Time Logger** (embedded widget logic) | `app.js` | A lighter-weight category time-logger (Sleep / Study / Screens / Exercise / Social / Other) with ideal-hours comparison bars, a 24-hour dial visualization, quick-load day presets (Study / Work / Rest day), and rule-based daily insights |

---

## 🎨 Design System — "Kinetic Obsidian"

A custom dark, glassmorphic, high-contrast design language built specifically for this app (see `front end/kinetic_obsidian/DESIGN.md` for the full spec):

- **Vibe:** command-center-of-a-quantum-compute-engine — glassmorphism over an ultra-deep slate canvas, lit by neon micro-glows.
- **Palette:** Electric Cyan (`#00F0FF`) primary, Electric Indigo (`#6366F1`) secondary, Neon Emerald (`#10B981`) for streaks/success, Amber/Coral for alerts — all on a Slate-950 (`#0B1326`) base.
- **Type:** Plus Jakarta Sans (headers), Inter (body/UI), JetBrains Mono (live numeric/telemetry data).
- **Motifs:** glowing progress rings, pill-shaped streak/status chips, translucent blurred cards, hairline neon borders.
- **Grid:** 12-column fluid grid (desktop), collapsing to 8 → 4 columns on tablet/mobile, 8pt spacing scale.

Reference component mockups and rendered screenshots for each major screen live under `front end/` (brand logo, Daily Command Hub, Persona/Ideal-Self setup, Wellbeing & Brain Gym).

---

## 🛠️ Tech Stack

Built to ship fast with **zero build step and zero backend**:

- **HTML5 + Tailwind CSS** (via CDN, `cdn.tailwindcss.com`) with a fully custom `tailwind.config` for the Kinetic Obsidian color/type/spacing tokens
- **Vanilla JavaScript** for all interactivity, state, and DOM rendering (no framework)
- **`localStorage`** for client-side persistence — no database, no auth, no server
- **Google Fonts** (Plus Jakarta Sans, Inter, JetBrains Mono) + **Material Symbols** for iconography
- **Inline SVG** for the radar gauges, day-dial, and progress rings
- **Python** utility scripts (stdlib only, except `ppt.py`) used during the build to patch navigation links across pages and to auto-generate `analytics.html` from `index.html`'s shared header/footer shell

No package manager, no build pipeline — open a page in a browser and it runs.

---

## 📁 Project Structure

```
time-manage/
├── index.html                          # Daily Command Hub (main dashboard)
├── onboarding.html                     # Persona & Benchmark Calibration
├── wellbeing.html                      # Wellbeing & Brain Gym
├── analytics.html                      # Analytics & Reports
├── app.js                              # Category time-logger widget logic + localStorage state
├── style.css                           # Supplementary custom styles
├── generate_analytics.py               # Builds analytics.html from index.html's shared shell
├── patch.py                            # Wires up nav links (onboarding/hub/wellbeing) across pages
├── patch_index_js.py                   # JS patch/injection utility for index.html
├── patch_analytics_links.py            # Wires up the Analytics nav link across pages
├── ppt.py                              # Generates the project's pitch-deck slides (python-pptx)
├── docs/
│   ├── PRD.md                          # Product requirements & MVP scope
│   ├── Design.md                       # UI/UX design spec
│   ├── Architecture.md                 # Technical architecture & data model
│   ├── Rules.md                        # Hackathon team/build rules
│   └── To-do.md                        # 90-minute build checklist
└── front end/
    ├── kinetic_obsidian/DESIGN.md      # Full design-system spec (colors, type, elevation, components)
    ├── chronoself_brand_logo/          # Logo reference (code + screenshot)
    ├── chronoself_daily_command_hub/   # Command Hub mockup (code + screenshot)
    ├── chronoself_persona_ideal_self_setup/  # Onboarding mockup (code + screenshot)
    └── chronoself_wellbeing_brain_gym/ # Wellbeing mockup (code + screenshot)
```

---

## 🚀 Getting Started

No installation required for the web app itself:

1. Clone or unzip the project.
2. Open `onboarding.html` in any modern browser to start from persona setup, **or** open `index.html` to land directly on the Daily Command Hub.
3. Navigate between pages using the top nav bar (Onboarding & Persona · Daily Command Hub · Wellbeing & Brain Gym · Analytics & Reports).
4. All activity is saved locally in your browser via `localStorage` — no sign-up, no server.

> Requires an internet connection on first load (Tailwind CDN + Google Fonts + Material Symbols are loaded remotely).

### Regenerating pages (optional, for developers)

The Python scripts are one-time build utilities used to keep navigation and layout consistent across pages — you generally won't need to re-run them unless you're editing the shared header/footer shell:

```bash
python patch.py                    # sync nav links across index/onboarding/wellbeing
python patch_analytics_links.py    # sync the Analytics nav link
python generate_analytics.py       # rebuild analytics.html from index.html's shell
pip install python-pptx            # only needed for ppt.py
python ppt.py                      # regenerate the pitch-deck slides
```

---

## 🧭 Product Docs

Full planning documentation is in [`/docs`](./docs):
- **PRD.md** — problem statement, personas, MVP scope, success metrics, demo script
- **Design.md** — UI/UX system, layout, component behavior, role-based theming
- **Architecture.md** — tech stack rationale, data model, core scoring logic
- **Rules.md** — hackathon time-boxing and team rules
- **To-do.md** — the 90-minute, phase-by-phase build checklist this project was executed against

---

## 🏆 Why It's Different

- **Personalization that actually changes the UI**, not just the data — every persona gets different targets, labels, and benchmarks.
- **The gap is the product.** Instead of a static task list, the whole app is oriented around a single live metric: how close you are to your calibrated Ideal Self.
- **Built entirely client-side in a 90-minute hackathon window** — no backend, no build tools, no dependencies beyond CDN links — while still shipping a four-page, fully navigable, animated product.

---

## 📌 Status

Hackathon MVP — client-side only, single-browser persistence via `localStorage`. Not intended for production use as-is (no auth, no multi-device sync, no real biometric/circadian data source — sleep/telemetry figures are simulated for the demo).

---

*ChronoSelf © 2025 ChronoSelf AI Systems. Human Potential Optimized.*
