# Design System & Visual Identity: Developer Reel

## 1. Creative Direction

**Developer Reel** pairs a programmatic terminal animation with a structured, technical Markdown portfolio.

The design creates a deliberate progression:
1. **The Opening Scene**: A restrained, text-based terminal animation presenting identity, core technical focus, and verified flagship milestones.
2. **The Portfolio**: A clean Markdown layout articulating technical tradeoffs, architecture decisions, and engineering milestones.

### Visual Design System
- **Palette**:
  - Near-black charcoal canvas (`#0E1217` / `#101418`): Harmonious across GitHub Dark (`#0D1117`) and framed on GitHub Light.
  - Off-white typography (`#F0F4F8` / `#E6EDF3`): High-legibility primary text (contrast > 12:1).
  - Muted slate-gray (`#8B949E` / `#7D8B99`): Secondary descriptions, branches, and metadata (contrast > 4.8:1).
  - Subtle sage-green accent (`#88A98E`): Commands, status indicators, and subtle control dot (contrast > 5.5:1).
- **Typography**:
  - Terminal: JetBrains Mono (Open Font License) with monospace fallback.
  - Markdown: GitHub native high-legibility type stack (`-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif`).
- **Restraint Principles**:
  - No decorative ASCII mascots, rainbow colors, neon glow, or wall of badges.
  - No fake BIOS diagnostics, fictional dates, or fabricated terminal commands.
  - No third-party card widgets or broken external dependencies.

---

## 2. Terminal Animation Storyboard

The animation in `assets/developer-reel.gif` executes a 5-stage narrative loop (~10.8s):

| Stage | Command / Prompt | Content Displayed | Intent |
| :--- | :--- | :--- | :--- |
| **1. Identity** | `$ whoami` | `CH_JASWANTH_KUMAR · GITAM University` | Introduces the engineer with crisp, bold typography. |
| **2. Engineering Focus** | `$ cat focus.spec` | `Software Engineering / Full Stack / AI Systems` | Establishes technical discipline taxonomy. |
| **3. Selected Builds** | `$ tree ./selected-work` | `merchantos/` & `memra/` | Highlights flagship independent builds and automated test guards. |
| **4. Team Engineering** | *(tree continuation)* | `barabari/` | Showcases JPMorgan Chase Code for Good 2026 participation. |
| **5. Closing Callout** | `$ explore --projects` | `→ Technical architecture & source code below.` | Guides the reader into the Markdown portfolio below. |

### Technical Specifications
- **Dimensions**: `740 × 390` px (optimized for desktop sharpness and 320–375px mobile scale).
- **File Size**: ~21.3 KB (highly compact, fast cold-load).
- **Frame Optimization**: Adaptive 32-color quantized palette with variable frame durations (100ms typing, 1.1s–2.2s reading pauses).
- **Accessibility**: Comprehensive descriptive alt text embedded in Markdown.

---

## 3. Regenerating the Terminal Animation

The animation is generated with `scripts/generate_reel.py` using Python and Pillow (`PIL`).

### Requirements
```bash
pip install pillow
```

### Run Generator
```bash
python3 scripts/generate_reel.py
```

The script outputs `assets/developer-reel.gif` directly into the repository.
