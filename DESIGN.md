# Design System & Visual Identity: Cinematic Developer Timeline

## 1. Creative Direction

**Cinematic Developer Timeline** transforms the GitHub profile into an animated narrative documentary of an engineer's journey.

The design structure consists of three intentional elements:
1. **The Tagline Quote**: An original engineering philosophy establishing identity without decorative banner images:
   > *Software gets interesting when it stops being a demo and starts being dependable.*
2. **Compact Navigation**: Clean, unobtrusive links to GitHub and LinkedIn.
3. **The Cinematic Timeline Animation**: A compact terminal window that walks the viewer through chapters of engineering foundations, flagship builds, collaborative achievements, professional experience, and community milestones.

All primary storytelling content lives inside the animated terminal reel. Redundant, lengthy Markdown résumé sections have been removed from the profile page.

---

## 2. Visual Design System

- **Palette**:
  - Near-black charcoal canvas (`#0E1217` / `#0F1216`): Blends harmoniously with GitHub Dark (`#0D1117`) and frames cleanly as a dark terminal card on GitHub Light.
  - Warm off-white (`#F0F4F8` / `#E6EDF3`): Primary high-legibility typographic elements (contrast > 12:1).
  - Controlled sage-green accent (`#7EA895` / `#88A98E`): Chapter badges, timeline progress scrubber, and active prompts (contrast > 5.5:1).
  - Muted slate-gray (`#8B949E`): Secondary technical summaries and architecture descriptions (contrast > 4.8:1).
  - Dim slate (`#646E78`): Contextual tertiary metadata and timeline track background (`#1C222A`).
- **Typography**:
  - JetBrains Mono (SIL Open Font License 1.1) rendered locally without external network dependencies.
  - Unified typographic hierarchy optimized for high legibility across mobile viewports (320px–375px):
    - Scene Headlines: 28 px Bold (`font_title`)
    - Subheadings & Key Metrics: 20 px Bold (`font_subtitle`)
    - Supporting Lines (max 2 per scene): 20 px Regular (`font_body`)
    - Terminal Prompt Line: 20 px Bold (`font_prompt`)
    - Window Shell Title & Scrubber Indicator: 13 px Regular / Bold (`font_header` / `font_badge`)
  - Generous line-height, dedicated project scenes, and guaranteed right margin (> 50 px) ensuring zero text clipping across mobile screens.
- **Form Factor**:
  - Dimensions: `680 × 320` px (compact wide-screen 2.125:1 cinematic ratio).
  - Embedded at native 680 px width (`width="680"` in README) to avoid desktop over-scaling while allowing GitHub's responsive styling to naturally constrain the image on narrow viewports.

---

## 3. Narrative Storyboard (8 Chapters)

The animation in `assets/developer-reel.gif` executes a 19.0-second narrative loop across 8 dedicated chapters:

| Chapter | Scrubber | Theme | Key Storytelling Content |
| :--- | :--- | :--- | :--- |
| **01** | `[1/8]` | **The Foundations** | Computer Science @ GITAM · Full-Stack & Systems Architecture · Bounded automation & deterministic math services · Moving software from demo to dependable. |
| **02** | `[2/8]` | **MerchantOS** | Flagship revenue engine · 107 automated tests · Profit-bounded discount engine for digital commerce · Deterministic pricing guards protect margin math. |
| **03** | `[3/8]` | **Memra** | Privacy-first memory books · In-browser PDF engine · In-browser compilation with zero cloud storage · Client-side PDF generation via native Web APIs. |
| **04** | `[4/8]` | **AI Visibility Tracker** | Applied AI & benchmarking · Cross-model brand presence analytics · Benchmarking presence across 4 LLMs · spaCy entity recognition & citation auditing. |
| **05** | `[5/8]` | **Barabari Collective** | Collaborative engineering @ JPMorgan Chase Code for Good 2026 · Operational platform built for artisan teams · Isolated RAG with Gemini & MongoDB Vector Search. |
| **06** | `[6/8]` | **Professional Experience** | Clean role roster without unverified dates: **Xentro** (Frontend Head) & **Toji Labs** (Co-founder & Engineer) · **Webbheads** (Full-Stack Developer · CRM & REST APIs). |
| **07** | `[7/8]` | **Recognition & Communities** | **IdeaSprint 3.0** (1st place winner) & **AWS Student Builders** · Technical core team @ **GDG GITAM** & **AWS Cloud Club**. |
| **08** | `[8/8]` | **The Next Chapter** | *THE NEXT CHAPTER* · Dependable Systems & Autonomous Workflows · Seeking software engineering internships · Prompt: `> journey --continue ▌`. |

---

## 4. Technical Specifications & Reproduction

- **File**: `assets/developer-reel.gif`
- **Resolution**: `680 × 320` px
- **Duration**: `19.00` seconds
- **File Size**: `92.49` KB (fast cold load, zero lag)
- **Palette**: Adaptive 32-color quantized palette with zero dithering noise.
- **Generator**: `scripts/generate_reel.py` (Python 3 + Pillow)

### How to Regenerate
```bash
python3 scripts/generate_reel.py
```
Outputs `assets/developer-reel.gif` in place.
