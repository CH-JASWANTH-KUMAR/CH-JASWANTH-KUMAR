# Design System & Engineering Architecture: The Decision Record

## 1. Concept: The Decision Receipt

Most developer profile READMEs suffer from marketing puffery: subjective claims, generic shield badges, and unverified skill graphs.

The **Decision Record** inverts this pattern. It presents the candidate's engineering qualifications as an authentic, deterministic **audit log** printed on thermal paper answering a single concrete question:

> *"Evaluate candidate for software engineering internship."*

### Visual & Physical Design Principles
- **Substrate**: Thermal receipt paper (`#EFEBDD`) with a perforated sawtooth bottom tear edge.
- **Ink**: Deep carbon near-black (`#1B1B1B`) at 13px monospaced sizing with high-contrast bold headers (`#111111`).
- **Accent Stamp**: A single vermilion red stamp (`#D9432B`) stamped at `-2.2°` rotation stating `[ WORTH A CONVERSATION ]`.
- **Typography**: Subsetted JetBrains Mono (OFL license in `assets/fonts/OFL.txt`) embedded directly into the SVG as base64 WOFF2 with system monospace fallback.
- **Discipline**: Every line is constrained to **44 characters or fewer**, guaranteeing zero text overflow across all viewports and monospace fonts.

### Animation & Motion Architecture
- **CSS-Only**: Zero JavaScript execution inside the SVG.
- **Top-to-Bottom Print Sequence**: Lines reveal sequentially with staggered animation delays over ~2.5 seconds.
- **Stamp Impact**: At ~2.7s, the `WORTH A CONVERSATION` stamp drops in from scale 1.6 to 1 with a slight rotation settle, completing by 3.1s.
- **Resilient Fallback**: Keyframes are defined exclusively with `from { ... }`. The default state of every element is the complete, finished receipt. If animations fail, block, or take place in static renderers, the receipt displays completely.
- **Accessibility**: `@media (prefers-reduced-motion: reduce)` immediately disables all keyframe animations.
- **Static Asset**: A static duplicate is maintained at `assets/receipt-static.svg` for headless rasterization and fallback contexts.

---

## 2. Fact Integrity & Zero-Placeholder Governance

Every claim and metric on both the SVG receipt and the README is governed by `facts.json`:
- **Traceability**: Every metric must contain `value`, `source`, and `verified_on`.
- **Stack Dependency Verification**: Every technology listed in the Stack is cross-referenced with repository source files in `facts.json` (e.g. `AI-VISIBILITY-SCORE/docker-compose.yml`, `MerchantOS/package.json`).
- **Build Enforcement**: `tools/build.py` validates that every fact has a verifiable source. If any fact lacks a source or if any placeholder text (such as `NEEDS CONFIRMATION` or `<...>` tokens) is detected, the build aborts with an exit code of 1.

---

## 3. How to Add a Rule

To add or modify an evaluation rule:

1. **Verify Evidence**: Locate the verifiable commit, test assertion, or architectural boundary in the target repository.
2. **Open `facts.json`**: Navigate to the `"rules"` array and add a new entry:
   ```json
   {
     "id": "06",
     "title": "DESCRIPTIVE RULE NAME",
     "fact_line1": "Concise fact under 44 characters.",
     "fact_line2": "Second line under 44 characters.",
     "ref": "Ref: repo/path/to/evidence",
     "source": "Exact file or commit reference proving the claim"
   }
   ```
3. **Check Character Limits**: Ensure neither `fact_line1` nor `fact_line2` exceeds 44 characters.
4. **Rebuild**: Run `python3 tools/build.py`.

---

## 4. How to Rebuild Locally

### Prerequisites
- Python 3.10+
- `gh` CLI (authenticated) or network access for GitHub API metrics

### Commands
```bash
# 1. (One-time or font update) Subset JetBrains Mono and generate embedded CSS:
python3 tools/prepare_font.py

# 2. Rebuild the animated SVG, static SVG, and README.md:
python3 tools/build.py

# 3. Optional: Render static SVG to PNG for preview:
magick assets/receipt-static.svg assets/receipt.png
magick -resize 360x assets/receipt-static.svg assets/receipt-360.png
```

---

## 5. Continuous Automation

The repository includes `.github/workflows/build.yml` which:
- Runs automatically on every push to `main`.
- Runs on a daily schedule (`06:00 UTC`) to refresh GitHub public repository counts and 90-day activity.
- Dynamically drops the "pushed in last 90d" counter if activity falls below 3 repos.
- Uses minimal GitHub Actions permissions (`contents: write`).
- Commits and pushes only when regenerated output files differ from the repository state.
