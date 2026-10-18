import os
import shutil
import sys
from pathlib import Path

# =============================================================================
# 1. Color Palette Configuration (Deep Ink, Sea-Glass Teal, Muted Amber, Slate)
# =============================================================================
# - Background: deep ink #0B1220
# - Primary text: soft white #E8EDF2
# - Main accent: sea-glass teal #55D6BE
# - Secondary accent: muted amber #E6AA6E
# - Secondary text: slate #8B9AA8
# - Subtle separators: dark blue-gray #273449

_user = os.environ.get("GH_USER", "jaswanth")
os.environ["GIFOS_GENERAL_USER_NAME"] = _user
os.environ["GIFOS_GENERAL_COLOR_SCHEME"] = "jaswanth"

config_dir = Path.home() / ".config" / "gifos"
config_dir.mkdir(parents=True, exist_ok=True)
colors_toml = config_dir / "ansi_escape_colors.toml"
with open(colors_toml, "w") as f:
    f.write("""[jaswanth]
    [jaswanth.default_colors]
    fg = "#E8EDF2"
    bg = "#0B1220"

    [jaswanth.normal_colors]
    black = "#273449"
    red = "#E06C75"
    green = "#55D6BE"
    yellow = "#E6AA6E"
    blue = "#6BA4B8"
    magenta = "#B39DDB"
    cyan = "#55D6BE"
    white = "#E8EDF2"

    [jaswanth.bright_colors]
    black = "#8B9AA8"
    red = "#EF7D84"
    green = "#55D6BE"
    yellow = "#F0C294"
    blue = "#82B1FF"
    magenta = "#C5B3E6"
    cyan = "#6EE7D0"
    white = "#FFFFFF"
""")

import gifos
import gifos.gifos

USER = _user

# Locate font file robustly
FONT_FILE_BITMAP = (
    "./fonts/gohufont-uni-14.pil"
    if os.path.exists("./fonts/gohufont-uni-14.pil")
    else f"{gifos.gifos.font_path}/gohufont-uni-14.pil"
)

# Distinct prompt using sea-glass teal and slate
CUSTOM_PROMPT = f"\x1b[32m{USER}\x1b[0m@\x1b[90mdev\x1b[0m ~> "
PORTRAIT_FILE = "assets/source/jaswanth-portrait.txt"


def load_colored_portrait(filepath: str) -> tuple[list[str], int, int]:
    """
    Reads the exact 80x51 ASCII portrait from disk without altering lines or spacing,
    applying restrained ANSI colors matching the terminal theme.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Portrait file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = [line.rstrip("\r\n") for line in f]

    colored_lines = []
    for line in raw_lines:
        out = ""
        curr_color = None
        for ch in line:
            if ch in "#%":
                c = "96"  # Sea-glass teal for dense hair/features
            elif ch in "*+":
                c = "97"  # Soft white for contours, highlights, smile
            elif ch == "=":
                c = "90"  # Slate for midtone structure
            elif ch in "-:.":
                c = "30"  # Dark gray / ink slate for subtle background shading
            else:
                c = "0"   # Normal / space
            if c != curr_color:
                out += f"\x1b[{c}m"
                curr_color = c
            out += ch
        out += "\x1b[0m"
        colored_lines.append(out)

    return colored_lines, len(raw_lines), max(len(l) for l in raw_lines)


def main():
    # -------------------------------------------------------------------------
    # 1. Canvas Dimensions: 750px wide x 1020px tall
    # In gohufont-uni-14 (8x18 character cell with 15px padding):
    # - num_cols = (750 - 30) // 8 = 90 cols (Portrait is 80 cols -> centered with 5 cols margin)
    # - num_rows = (1020 - 30) // 18 = 55 rows (Portrait is 51 rows -> fits completely with header & prompt)
    # -------------------------------------------------------------------------
    t = gifos.Terminal(750, 1020, 15, 15, FONT_FILE_BITMAP, 15)
    t.set_prompt(CUSTOM_PROMPT)

    portrait_lines, portrait_h, portrait_w = load_colored_portrait(PORTRAIT_FILE)
    print(f"Loaded portrait: {portrait_h} rows x {portrait_w} cols. Terminal: {t.num_rows} rows x {t.num_cols} cols.")

    # =========================================================================
    # SCENE 1: Welcome ("wasssup guys")
    # =========================================================================
    t.gen_prompt(1, count=3)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("wasssup guys", 1, prompt_col, contin=True, speed=1)
    t.clone_frame(15)  # Hold welcome phrase

    t.gen_text(CUSTOM_PROMPT, 3, 1, count=1, contin=True)
    prompt_col2 = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("cat assets/source/jaswanth-portrait.txt", 3, prompt_col2, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)

    # Transition to portrait scene
    t.clear_frame()
    t.set_font(FONT_FILE_BITMAP, 15)
    t.set_prompt(CUSTOM_PROMPT)

    # =========================================================================
    # SCENE 2: Full ASCII Portrait
    # =========================================================================
    # Header command line at row 1
    t.gen_text(CUSTOM_PROMPT, 1, 1, count=1, contin=True)
    t.gen_text("\x1b[92mcat assets/source/jaswanth-portrait.txt\x1b[0m", 1, t.curr_col, contin=True)

    # Center 80-col portrait in 90-col terminal: start at col 6
    col_start = int((t.num_cols - portrait_w) // 2 + 1)  # 6

    # Reveal portrait lines in streaming terminal stdout chunks
    chunk_size = 6
    for idx in range(0, portrait_h, chunk_size):
        chunk = portrait_lines[idx : idx + chunk_size]
        for offset, pline in enumerate(chunk):
            t.gen_text(pline, 2 + idx + offset, col_start, count=0, contin=True)
        t.clone_frame(1)

    # Hold complete, unclipped portrait so viewers can clearly recognize it
    t.clone_frame(35)

    # =========================================================================
    # SCENE 3: Transition (Terminal "clear" command)
    # =========================================================================
    t.gen_text(CUSTOM_PROMPT, 53, 1, count=1, contin=True)
    prompt_col_clear = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("clear", 53, prompt_col_clear, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)

    # Clear screen cleanly
    t.clear_frame()
    t.set_font(FONT_FILE_BITMAP, 15)
    t.set_prompt(CUSTOM_PROMPT)

    # =========================================================================
    # SCENE 4: Profile Story (Spacious, Structured Developer Story)
    # =========================================================================
    # Header command
    t.gen_text(CUSTOM_PROMPT, 1, 1, count=1, contin=True)
    t.gen_text("\x1b[92m./profile.sh\x1b[0m", 1, t.curr_col, contin=True)
    t.clone_frame(2)

    # 1. Identity & Engineering Focus (Rows 3-5)
    t.gen_text("\x1b[97;1mJaswanth Kumar Chettupalli\x1b[0m \x1b[90m-\x1b[0m \x1b[96mComputer Science @ GITAM University\x1b[0m", 3, 2, contin=True)
    t.gen_text("\x1b[90mFocus:\x1b[0m \x1b[97mSoftware Engineering \x1b[90m|\x1b[0m \x1b[97mFull-Stack Systems \x1b[90m|\x1b[0m \x1b[97mReliable Architecture \x1b[90m|\x1b[0m \x1b[97mApplied AI\x1b[0m", 4, 2, contin=True)
    t.gen_text("\x1b[30m------------------------------------------------------------------------------------\x1b[0m", 5, 2, contin=True)
    t.clone_frame(3)

    # 2. Experience (Rows 7-14)
    t.gen_text("\x1b[93;1mEXPERIENCE\x1b[0m", 7, 2, contin=True)
    t.gen_text("\x1b[96m* Xentro\x1b[0m          \x1b[90m|\x1b[0m \x1b[97mFrontend Head\x1b[0m        \x1b[90m|\x1b[0m \x1b[90mTyped UI Architecture & RBAC Systems\x1b[0m", 9, 2, contin=True)
    t.gen_text("\x1b[96m* Toji Labs\x1b[0m       \x1b[90m|\x1b[0m \x1b[97mCo-founder & Engineer\x1b[0m \x1b[90m|\x1b[0m \x1b[90mWeb Platforms & Product Engineering\x1b[0m", 11, 2, contin=True)
    t.gen_text("\x1b[96m* Webbheads\x1b[0m       \x1b[90m|\x1b[0m \x1b[97mFull-Stack Developer\x1b[0m  \x1b[90m|\x1b[0m \x1b[90mInternal Tools, CRM & Analytics\x1b[0m", 13, 2, contin=True)
    t.gen_text("\x1b[30m------------------------------------------------------------------------------------\x1b[0m", 15, 2, contin=True)
    t.clone_frame(3)

    # 3. Featured Systems & Projects (Rows 17-31)
    t.gen_text("\x1b[93;1mFEATURED SYSTEMS & PROJECTS\x1b[0m", 17, 2, contin=True)
    t.gen_text("\x1b[96m* MerchantOS\x1b[0m                \x1b[90m|\x1b[0m \x1b[97mAutonomous Revenue & Discount Engine\x1b[0m \x1b[90m(107 automated tests)\x1b[0m", 19, 2, contin=True)
    t.gen_text("  \x1b[90mStack: Next.js 16, React 19, Express 5, Python ML services\x1b[0m", 20, 2, contin=True)

    t.gen_text("\x1b[96m* Memra\x1b[0m                     \x1b[90m|\x1b[0m \x1b[97mPrivacy-First Conversation Memory Book\x1b[0m \x1b[90m(Groq Llama 3.3)\x1b[0m", 22, 2, contin=True)
    t.gen_text("  \x1b[90mArchitecture: In-browser WhatsApp parser, zero-storage narrative synthesis, client PDF\x1b[0m", 23, 2, contin=True)

    t.gen_text("\x1b[96m* AI Visibility Score Tracker\x1b[0m \x1b[90m|\x1b[0m \x1b[97mMulti-Model LLM Brand Auditing Platform\x1b[0m", 25, 2, contin=True)
    t.gen_text("  \x1b[90mPipeline: Programmatic prompt evaluation pipeline via FastAPI, PostgreSQL, Redis\x1b[0m", 26, 2, contin=True)

    t.gen_text("\x1b[96m* Barabari Collective Hub\x1b[0m    \x1b[90m|\x1b[0m \x1b[97mProject-Isolated Vector RAG Workbench\x1b[0m \x1b[90m(JPMC CFG '26)\x1b[0m", 28, 2, contin=True)
    t.gen_text("  \x1b[90mCore: Gemini 768D embeddings paired with MongoDB Atlas Vector Search\x1b[0m", 29, 2, contin=True)
    t.gen_text("\x1b[30m------------------------------------------------------------------------------------\x1b[0m", 31, 2, contin=True)
    t.clone_frame(4)

    # 4. Honors & Recognition (Rows 33-41)
    t.gen_text("\x1b[93;1mHONORS & RECOGNITION\x1b[0m", 33, 2, contin=True)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mWinner, IdeaSprint 3.0\x1b[0m \x1b[90m- AI & Full-Stack Track\x1b[0m", 35, 2, contin=True)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mJPMorgan Chase Code for Good 2026\x1b[0m \x1b[90m- Selected GITAM University Representative\x1b[0m", 37, 2, contin=True)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mAWS Student Builder Group\x1b[0m \x1b[90m- Technical Member @ IIT Jodhpur\x1b[0m", 39, 2, contin=True)
    t.gen_text("\x1b[30m------------------------------------------------------------------------------------\x1b[0m", 41, 2, contin=True)
    t.clone_frame(4)

    # =========================================================================
    # SCENE 5: Closing Statement
    # =========================================================================
    t.gen_text(CUSTOM_PROMPT, 44, 2, count=1, contin=True)
    prompt_col_status = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("echo $STATUS", 44, prompt_col_status, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)

    t.gen_text("\x1b[92m\"still curious. still building. still figuring it out.\"\x1b[0m", 46, 2, count=1, contin=True)
    t.clone_frame(5)

    # Final prompt with active cursor pause
    t.gen_text(CUSTOM_PROMPT, 48, 2, count=1, contin=True)
    t.toggle_show_cursor(True)
    t.clone_frame(70)

    # Generate GIF
    print("Generating output.gif ...")
    t.gen_gif()
    print("Generated output.gif successfully!")

    # Clean up temporary build frames
    shutil.rmtree("frames", ignore_errors=True)


if __name__ == "__main__":
    main()
