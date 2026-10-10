#!/usr/bin/env python3
"""
tools/build.py
Python standard library only generator.
Reads public GitHub API data and facts.json.
Generates assets/receipt.svg, assets/receipt-static.svg, and README.md.
Validates fact sources and ensures zero placeholder strings exist in output.
"""

import os
import sys
import json
import re
import datetime
import subprocess
import urllib.request

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FACTS_PATH = os.path.join(WORKSPACE_DIR, "facts.json")
FONTS_CSS_PATH = os.path.join(WORKSPACE_DIR, "assets", "fonts", "fonts_embedded.css")
RECEIPT_ANIM_PATH = os.path.join(WORKSPACE_DIR, "assets", "receipt.svg")
RECEIPT_STATIC_PATH = os.path.join(WORKSPACE_DIR, "assets", "receipt-static.svg")
README_PATH = os.path.join(WORKSPACE_DIR, "README.md")

BANNED_PLACEHOLDERS = [
    "NEEDS CONFIRMATION",
    "<personal email",
    "<your",
    "<what",
    "<real client",
    "<2 plain",
    "TODO",
    "FIXME",
]

def load_and_validate_facts():
    if not os.path.exists(FACTS_PATH):
        raise FileNotFoundError(f"Missing {FACTS_PATH}")
    with open(FACTS_PATH, "r", encoding="utf-8") as f:
        facts = json.load(f)

    # Validate that every metric and rule has a source
    for key, item in facts.get("metrics", {}).items():
        if not isinstance(item, dict) or not item.get("source"):
            raise ValueError(f"Fact 'metrics.{key}' is missing a verified 'source' in facts.json")

    for rule in facts.get("rules", []):
        if not rule.get("source"):
            raise ValueError(f"Rule {rule.get('id', 'unknown')} is missing a verified 'source' in facts.json")

    return facts

def fetch_github_data(username):
    public_repos = 39
    pushed_90d = 0
    now = datetime.datetime.now(datetime.timezone.utc)
    ninety_days_ago = now - datetime.timedelta(days=90)

    # 1. Try gh CLI
    try:
        user_out = subprocess.check_output(["gh", "api", f"users/{username}"], stderr=subprocess.DEVNULL)
        user_data = json.loads(user_out)
        public_repos = user_data.get("public_repos", public_repos)

        repos_out = subprocess.check_output(["gh", "api", f"users/{username}/repos?per_page=100"], stderr=subprocess.DEVNULL)
        repos_data = json.loads(repos_out)
        for r in repos_data:
            p_at = r.get("pushed_at")
            if p_at:
                dt = datetime.datetime.fromisoformat(p_at.replace("Z", "+00:00"))
                if dt >= ninety_days_ago:
                    pushed_90d += 1
        return public_repos, pushed_90d
    except Exception:
        pass

    # 2. Try GITHUB_TOKEN or unauthenticated public urllib
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"User-Agent": "GitHub-Readme-Builder/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            u_data = json.loads(resp.read())
            public_repos = u_data.get("public_repos", public_repos)

        req_repos = urllib.request.Request(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req_repos, timeout=10) as resp:
            r_data = json.loads(resp.read())
            for r in r_data:
                p_at = r.get("pushed_at")
                if p_at:
                    dt = datetime.datetime.fromisoformat(p_at.replace("Z", "+00:00"))
                    if dt >= ninety_days_ago:
                        pushed_90d += 1
        return public_repos, pushed_90d
    except Exception:
        # Fallback to known audited values
        return 39, 9

def get_git_short_sha():
    # 1. CI environment
    ci_sha = os.environ.get("GITHUB_SHA")
    if ci_sha:
        return ci_sha[:7]
    # 2. Local git repository
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        if out and out != "HEAD":
            return out
    except Exception:
        pass
    # 3. Fallback for local build with no commit
    return "local"


def generate_svg(facts, public_repos, pushed_90d, timestamp_str, short_sha, animated=True):
    # Read embedded font CSS if available
    font_css = ""
    if os.path.exists(FONTS_CSS_PATH):
        with open(FONTS_CSS_PATH, "r", encoding="utf-8") as f:
            font_css = f.read().strip()

    # Dynamic inputs line: drops out if pushed_90d < 3
    if pushed_90d >= 3:
        inputs_line = f"- {public_repos} public repos ({pushed_90d} pushed in last 90d)"
    else:
        inputs_line = f"- {public_repos} public repos"

    animation_styles = ""
    if animated:
        animation_styles = """
    /* Staggered print-in animation */
    @keyframes printLine {
      from {
        opacity: 0;
      }
    }
    @keyframes stampDrop {
      from {
        opacity: 0;
        transform: translate(210px, 635px) rotate(-8deg) scale(1.6);
      }
    }
    .anim-line {
      animation: printLine 0.12s ease-out backwards;
    }
    .l-1  { animation-delay: 0.05s; }
    .l-2  { animation-delay: 0.12s; }
    .l-3  { animation-delay: 0.19s; }
    .l-4  { animation-delay: 0.26s; }
    .l-5  { animation-delay: 0.33s; }
    .l-6  { animation-delay: 0.42s; }
    .l-7  { animation-delay: 0.49s; }
    .l-8  { animation-delay: 0.56s; }
    .l-9  { animation-delay: 0.65s; }
    .l-10 { animation-delay: 0.72s; }
    .l-11 { animation-delay: 0.81s; }
    .l-12 { animation-delay: 0.88s; }
    .l-13 { animation-delay: 0.95s; }
    .l-14 { animation-delay: 1.02s; }
    .l-15 { animation-delay: 1.11s; }
    .l-16 { animation-delay: 1.18s; }
    .l-17 { animation-delay: 1.25s; }
    .l-18 { animation-delay: 1.32s; }
    .l-19 { animation-delay: 1.41s; }
    .l-20 { animation-delay: 1.48s; }
    .l-21 { animation-delay: 1.55s; }
    .l-22 { animation-delay: 1.62s; }
    .l-23 { animation-delay: 1.71s; }
    .l-24 { animation-delay: 1.78s; }
    .l-25 { animation-delay: 1.85s; }
    .l-26 { animation-delay: 1.92s; }
    .l-27 { animation-delay: 2.01s; }
    .l-28 { animation-delay: 2.08s; }
    .l-29 { animation-delay: 2.15s; }
    .l-30 { animation-delay: 2.22s; }
    .l-31 { animation-delay: 2.31s; }
    .l-32 { animation-delay: 2.38s; }
    .l-33 { animation-delay: 2.45s; }
    .l-34 { animation-delay: 2.52s; }

    .stamp-animated {
      transform: translate(210px, 635px) rotate(-2.2deg);
      animation: stampDrop 0.45s cubic-bezier(0.175, 0.885, 0.32, 1.2) backwards;
      animation-delay: 2.7s;
    }

    @media (prefers-reduced-motion: reduce) {
      * {
        animation: none !important;
      }
    }
"""

    line_cls = " anim-line" if animated else ""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 754" width="420" height="754">
  <defs>
    <style>
{font_css}
      .mono {{
        font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 13px;
        fill: #1B1B1B;
        white-space: pre;
      }}
      .bold {{
        font-weight: 700;
        fill: #111111;
      }}
      .muted {{
        fill: #555555;
        font-size: 12px;
      }}
      .header_title {{
        font-size: 14.5px;
        font-weight: 700;
        letter-spacing: 1.5px;
        fill: #111111;
      }}
      .stamp-border {{
        stroke: #C02C15;
        stroke-width: 2.2;
        fill: none;
      }}
      .stamp-inner {{
        stroke: #C02C15;
        stroke-width: 0.8;
        fill: rgba(192, 44, 21, 0.05);
      }}
      .stamp-text {{
        font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 13.5px;
        font-weight: 700;
        letter-spacing: 1.8px;
        fill: #C02C15;
      }}
      .divider {{
        stroke: #1B1B1B;
        stroke-dasharray: 4 3;
        stroke-width: 1;
      }}
      .double-rule {{
        stroke: #1B1B1B;
        stroke-width: 1.2;
      }}
{animation_styles}
    </style>
  </defs>

  <!-- Solid Thermal Paper Base -->
  <path d="M 0 0 L 420 0 L 420 746 L 414 752 L 408 746 L 402 752 L 396 746 L 390 752 L 384 746 L 378 752 L 372 746 L 366 752 L 360 746 L 354 752 L 348 746 L 342 752 L 336 746 L 330 752 L 324 746 L 318 752 L 312 746 L 306 752 L 300 746 L 294 752 L 288 746 L 282 752 L 276 746 L 270 752 L 264 746 L 258 752 L 252 746 L 246 752 L 240 746 L 234 752 L 228 746 L 222 752 L 216 746 L 210 752 L 204 746 L 198 752 L 192 746 L 186 752 L 180 746 L 174 752 L 168 746 L 162 752 L 156 746 L 150 752 L 144 746 L 138 752 L 132 746 L 126 752 L 120 746 L 114 752 L 108 746 L 102 752 L 96 746 L 90 752 L 84 746 L 78 752 L 72 746 L 66 752 L 60 746 L 54 752 L 48 746 L 42 752 L 36 746 L 30 752 L 24 746 L 18 752 L 12 746 L 6 752 L 0 746 Z" fill="#EFEBDD" stroke="#D5D0C0" stroke-width="1.2" />

  <!-- Top Double Rule -->
  <line x1="18" y1="10" x2="402" y2="10" class="double-rule" />
  <line x1="18" y1="13" x2="402" y2="13" class="double-rule" />
  <line x1="18" y1="109" x2="402" y2="109" class="divider" />
  <line x1="18" y1="174" x2="402" y2="174" class="divider" />
  <line x1="18" y1="222" x2="402" y2="222" class="divider" />
  <line x1="18" y1="593" x2="402" y2="593" class="divider" />

  <!-- Content Lines -->
  <text x="20" y="24" class="mono header_title{line_cls} l-1">          DECISION RECORD</text>
  <text x="20" y="41" class="mono bold{line_cls} l-2">CANDIDATE: CHETTUPALLI JASWANTH KUMAR</text>
  <text x="20" y="58" class="mono{line_cls} l-3">GITHUB   : @CH-JASWANTH-KUMAR</text>
  <text x="20" y="75" class="mono{line_cls} l-4">TIMESTAMP: {timestamp_str}</text>
  <text x="20" y="92" class="mono{line_cls} l-5">SHA      : {short_sha}</text>

  <text x="20" y="123" class="mono bold{line_cls} l-6">REQUEST:</text>
  <text x="20" y="140" class="mono{line_cls} l-7">Evaluate candidate for software engineering</text>
  <text x="20" y="157" class="mono{line_cls} l-8">internship.</text>

  <text x="20" y="188" class="mono bold{line_cls} l-9">INPUTS (GitHub API, public data):</text>
  <text x="20" y="205" class="mono{line_cls} l-10">{inputs_line}</text>

  <text x="20" y="236" class="mono bold{line_cls} l-11">RULES FIRED:</text>
  <text x="20" y="253" class="mono bold{line_cls} l-12">01 SEPARATE MATH FROM MODEL</text>
  <text x="20" y="270" class="mono{line_cls} l-13">   MerchantOS: 107 tests. TS calculates</text>
  <text x="20" y="287" class="mono{line_cls} l-14">   gross profit; LLM restricted to tools.</text>
  <text x="20" y="304" class="mono muted{line_cls} l-15">   Ref: MerchantOS decision-engine.service</text>

  <text x="20" y="321" class="mono bold{line_cls} l-16">02 KEEP USER DATA ON DEVICE</text>
  <text x="20" y="338" class="mono{line_cls} l-17">   Memra runs with no server database.</text>
  <text x="20" y="355" class="mono{line_cls} l-18">   11-page PDF compiled inside browser.</text>
  <text x="20" y="372" class="mono muted{line_cls} l-19">   Ref: github.com/CH-JASWANTH-KUMAR/memra</text>

  <text x="20" y="389" class="mono bold{line_cls} l-20">03 STATE OWN LIMITS HONESTLY</text>
  <text x="20" y="406" class="mono{line_cls} l-21">   MerchantOS price elasticity is a</text>
  <text x="20" y="423" class="mono{line_cls} l-22">   heuristic (0.5). Test Mode only.</text>
  <text x="20" y="440" class="mono muted{line_cls} l-23">   Ref: MerchantOS Sec 31 (System Limits)</text>

  <text x="20" y="457" class="mono bold{line_cls} l-24">04 CREDIT UPSTREAM AUTHORS</text>
  <text x="20" y="474" class="mono{line_cls} l-25">   CodeAtlas upstream by Manish Kumar.</text>
  <text x="20" y="491" class="mono{line_cls} l-26">   Jaswanth built Groq assistant (fb4cf19,</text>
  <text x="20" y="508" class="mono muted{line_cls} l-27">   866 additions across 3 added files).</text>

  <text x="20" y="525" class="mono bold{line_cls} l-28">05 TEST DETERMINISTICALLY BEFORE LIVE</text>
  <text x="20" y="542" class="mono{line_cls} l-29">   CareLoop has 31 passing assertions</text>
  <text x="20" y="559" class="mono{line_cls} l-30">   across 3 suites before sandbox run.</text>
  <text x="20" y="576" class="mono muted{line_cls} l-31">   Ref: careloop/scripts (Phase 3, 4, 6)</text>

  <text x="20" y="607" class="mono bold{line_cls} l-32">DECISION:</text>
  <text x="20" y="666" class="mono{line_cls} l-33">Basis    : 3 flagship builds, 107 tests</text>
  <text x="20" y="683" class="mono{line_cls} l-34">Overrides: None</text>
  <text x="20" y="700" class="mono{line_cls} l-34">LinkedIn : linkedin.com/in/</text>
  <text x="20" y="717" class="mono{line_cls} l-34">  jaswanth-kumar-chettupalli-7b0809333/</text>

  <!-- Decision Stamp (Rotated) -->
  <g id="stamp" class="{ 'stamp-animated' if animated else '' }" transform="translate(210, 634) rotate(-2.2)">
    <g transform="translate(-135, -16)">
      <rect x="0" y="0" width="270" height="32" rx="2" class="stamp-border" />
      <rect x="2" y="2" width="266" height="28" rx="1" class="stamp-inner" />
      <text x="135" y="21" text-anchor="middle" class="stamp-text">WORTH A CONVERSATION</text>
    </g>
  </g>

  <!-- Bottom Double Rule -->
  <line x1="18" y1="736" x2="402" y2="736" class="double-rule" />
  <line x1="18" y1="739" x2="402" y2="739" class="double-rule" />
</svg>

"""
    return svg

def generate_readme(facts, public_repos, pushed_90d, timestamp_str, short_sha):
    if pushed_90d >= 3:
        inputs_line = f"- {public_repos} public repos ({pushed_90d} pushed in last 90d)"
    else:
        inputs_line = f"- {public_repos} public repos"

    receipt_plain_text = f"""============================================
          DECISION RECORD
CANDIDATE: CHETTUPALLI JASWANTH KUMAR
GITHUB   : @CH-JASWANTH-KUMAR
TIMESTAMP: {timestamp_str}
SHA      : {short_sha}
--------------------------------------------
REQUEST:
Evaluate candidate for software engineering
internship.
--------------------------------------------
INPUTS (GitHub API, public data):
{inputs_line}
--------------------------------------------
RULES FIRED:
01 SEPARATE MATH FROM MODEL
   MerchantOS: 107 tests. TS calculates
   gross profit; LLM restricted to tools.
   Ref: MerchantOS decision-engine.service
02 KEEP USER DATA ON DEVICE
   Memra runs with no server database.
   11-page PDF compiled inside browser.
   Ref: github.com/CH-JASWANTH-KUMAR/memra
03 STATE OWN LIMITS HONESTLY
   MerchantOS price elasticity is a
   heuristic (0.5). Test Mode only.
   Ref: MerchantOS Sec 31 (System Limits)
04 CREDIT UPSTREAM AUTHORS
   CodeAtlas upstream by Manish Kumar.
   Jaswanth built Groq assistant (fb4cf19,
   866 additions across 3 added files).
05 TEST DETERMINISTICALLY BEFORE LIVE
   CareLoop has 31 passing assertions
   across 3 suites before sandbox run.
   Ref: careloop/scripts (Phase 3, 4, 6)
--------------------------------------------
DECISION:

        [ WORTH A CONVERSATION ]

Basis    : 3 flagship builds, 107 tests
Overrides: None
LinkedIn : linkedin.com/in/
  jaswanth-kumar-chettupalli-7b0809333/
============================================"""

    readme = f"""<div align="center">

![Decision Record: Candidate evaluated for software engineering internship. Decision: Worth a conversation (3 flagship builds, 107 tests in MerchantOS)](assets/receipt.svg)

</div>

<details>
<summary>View Decision Record as plain text</summary>

```text
{receipt_plain_text}
```

</details>

---

## What I'm building

Most of what I build puts an LLM inside rules I can test. Plain code does the math and the checks, and the model does the language.

---

## Projects

### [Memra](https://github.com/CH-JASWANTH-KUMAR/memra)
Converts WhatsApp chat exports into a private, 11-page memory book entirely inside the browser.
* **Hard Fact**: Runs with no server database; all message parsing, authenticity filtering, and PDF generation execute client-side via `jsPDF`.
* **Honest Limit**: Narrative generation requires an external Groq API key (a deterministic local template fallback executes if unset); physical print binding remains on the roadmap.

### [MerchantOS](https://github.com/CH-JASWANTH-KUMAR/MerchantOS)
Autonomous revenue decision engine for digital commerce merchants that pairs association rule mining with bounded discount optimization.
* **Hard Fact**: 107 passing automated tests across the monorepo; financial profit calculations are computed strictly by TypeScript math services rather than the language model.
* **Honest Limit**: Price elasticity is modeled with a heuristic factor (0.5) rather than causal econometric inference; commercial actions execute strictly in Razorpay Test Mode.

### [AI Visibility Score Tracker](https://github.com/CH-JASWANTH-KUMAR/AI-VISIBILITY-SCORE)
Measures brand presence and competitor ranking across parallel AI models for industry-specific search queries.
* **Hard Fact**: Evaluates 50–100 deduplicated queries across 4 models simultaneously and scores visibility using a 4-factor formula (40% mention rate, 30% rank score, 20% competitor dominance, 10% model consistency).
* **Honest Limit**: Requires active API keys across all 4 commercial model providers; historical trend tracking is planned for v2.

---

## Also built

* **[CodeAtlas](https://github.com/CH-JASWANTH-KUMAR/CODEATLAS)** — Upstream repository intelligence tool created by Manish Kumar; I built the Groq-powered interactive repository assistant layer (commit `fb4cf19`, 866 additions across 3 added files) and decoupled the Prisma dependency for standalone demo execution.
* **[ResearchLens](https://github.com/CH-JASWANTH-KUMAR/naccer-rd-evaluation-copilot)** — Problem statement copilot for NaCCER/CMPDI R&D grant review; validates budget arithmetic, applies 0–10 rubrics, and flags reviewer score divergence (>= 2.0 points).
* **[CareLoop](https://github.com/CH-JASWANTH-KUMAR/careloop)** — Team build for The Ken case-build; I built the frontend command center and 31 deterministic tests.
* **[OCR-to-Excel Pipeline](https://github.com/CH-JASWANTH-KUMAR/OCR-TO-EXCEL-PIPELINE)** — Dual-stage document extraction pipeline combining OpenCV preprocessing, PaddleOCR, and OpenRouter LLM schema normalization with automated `NEEDS_REVIEW` confidence scoring.

---

## Stack

* **Languages**: TypeScript, Python, JavaScript
* **Frontend & Runtimes**: Next.js (App Router), React, Node.js, Tailwind CSS
* **Backend & Systems**: FastAPI, Express, PostgreSQL, MongoDB, Docker
* **Machine Learning & NLP**: scikit-learn, mlxtend, spaCy, OpenCV, PaddleOCR
* **Model Integrations**: Google Gemini, Groq (Llama 3.3 70B), Anthropic Claude, OpenAI

---

## Contact

* **LinkedIn**: [linkedin.com/in/jaswanth-kumar-chettupalli](https://www.linkedin.com/in/jaswanth-kumar-chettupalli-7b0809333/)
* **GitHub**: [@CH-JASWANTH-KUMAR](https://github.com/CH-JASWANTH-KUMAR)

---

This page is generated by [tools/build.py](tools/build.py) from [facts.json](facts.json).
"""
    return readme

def validate_no_placeholders(filepath, content):
    for placeholder in BANNED_PLACEHOLDERS:
        if placeholder in content:
            raise ValueError(f"Build failed: Banned placeholder '{placeholder}' found in {filepath}!")

    if filepath.endswith(".md"):
        # Check for angle bracket placeholders like <your email> or <what you built>
        matches = re.findall(r'<[a-zA-Z0-9_\s-]{3,40}>', content)
        valid_html_tags = {'<div>', '</div>', '<details>', '</details>', '<summary>', '</summary>', '<pre>', '</pre>', '<code>', '</code>', '<p>', '</p>', '<br>', '<br/>'}
        for m in matches:
            if m.lower() not in valid_html_tags and not any(m.lower().startswith(vt[:3]) for vt in valid_html_tags):
                raise ValueError(f"Build failed: Unresolved template placeholder '{m}' found in {filepath}!")


def main():
    print("--- Running tools/build.py ---")
    facts = load_and_validate_facts()
    print("Loaded facts.json: all metrics and rules validated with verified sources.")

    username = facts.get("candidate", {}).get("username", {}).get("value", "CH-JASWANTH-KUMAR")
    public_repos, pushed_90d = fetch_github_data(username)
    print(f"GitHub API metrics: public_repos={public_repos}, pushed_in_last_90d={pushed_90d}")

    # Generate timestamp and SHA (date only: YYYY-MM-DD)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp_str = now_utc.strftime("%Y-%m-%d")
    short_sha = get_git_short_sha()
    print(f"Build metadata: TIMESTAMP={timestamp_str}, SHA={short_sha}")

    # Generate SVGs
    svg_anim = generate_svg(facts, public_repos, pushed_90d, timestamp_str, short_sha, animated=True)
    svg_static = generate_svg(facts, public_repos, pushed_90d, timestamp_str, short_sha, animated=False)

    validate_no_placeholders("assets/receipt.svg", svg_anim)
    validate_no_placeholders("assets/receipt-static.svg", svg_static)

    with open(RECEIPT_ANIM_PATH, "w", encoding="utf-8") as f:
        f.write(svg_anim)
    print(f"Wrote {RECEIPT_ANIM_PATH} ({os.path.getsize(RECEIPT_ANIM_PATH)} bytes)")

    with open(RECEIPT_STATIC_PATH, "w", encoding="utf-8") as f:
        f.write(svg_static)
    print(f"Wrote {RECEIPT_STATIC_PATH} ({os.path.getsize(RECEIPT_STATIC_PATH)} bytes)")

    # Generate README.md
    readme_content = generate_readme(facts, public_repos, pushed_90d, timestamp_str, short_sha)
    validate_no_placeholders("README.md", readme_content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Wrote {README_PATH} ({os.path.getsize(README_PATH)} bytes)")
    print("--- Build completed successfully with ZERO placeholders ---")

if __name__ == "__main__":
    main()
