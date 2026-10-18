import os
import shutil
import sys
from pathlib import Path

# 1. Configure custom theme before gifos is imported
_user = os.environ.get("GH_USER", "jaswanth")
os.environ["GIFOS_GENERAL_USER_NAME"] = _user
os.environ["GIFOS_GENERAL_COLOR_SCHEME"] = "jaswanth"

# Setup custom coordinated color scheme in ~/.config/gifos
config_dir = Path.home() / ".config" / "gifos"
config_dir.mkdir(parents=True, exist_ok=True)
colors_toml = config_dir / "ansi_escape_colors.toml"
with open(colors_toml, "w") as f:
    f.write("""[jaswanth]
    [jaswanth.default_colors]
    fg = "#F2F4F5"
    bg = "#0f1722"

    [jaswanth.normal_colors]
    black = "#17243B"
    red = "#e06c75"
    green = "#63D8CB"
    yellow = "#F0B879"
    blue = "#709ad2"
    magenta = "#b39ddb"
    cyan = "#63D8CB"
    white = "#d1d5db"

    [jaswanth.bright_colors]
    black = "#8997A8"
    red = "#ef7d84"
    green = "#78e8dc"
    yellow = "#f7c78d"
    blue = "#82b1ff"
    magenta = "#c5b3e6"
    cyan = "#78e8dc"
    white = "#F2F4F5"
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

CUSTOM_PROMPT = f"\x1b[32m{USER}\x1b[0m@\x1b[94mdev\x1b[0m ~> "

# Jaswanth's face monochrome ASCII portrait generated from actual source photo
# 26 columns wide x 21 rows tall
ASCII_PORTRAIT_RAW = [
    r"                          ",
    r"     ..              .    ",
    r"    ..               .    ",
    r"   -.         ..      ..  ",
    r"   :    :==-+@@@#-     .  ",
    r"   -   :*%@@@@@@@#+.   .  ",
    r"   -. :*#@@@@@@@@@**  .   ",
    r"   .--*:::-*@@@+--:-+ .   ",
    r"   ..%+ .   +@=   ..%-    ",
    r"   :-@+==*#+#@++#+=+%+.   ",
    r"  .++@@@@@@%@@@%@@@@@%=-  ",
    r"  .#*@%@@%*+*@*+*%@@@@*=  ",
    r"   =#@:--+*.   .#=:-##*   ",
    r"   .+#::=..+###+..-:**=   ",
    r"     :+.++=%@@@%=*+-+     ",
    r"      -..+=:+*+-++:-.     ",
    r"      .+.-+*++***=-=      ",
    r"       = .:=+++=-.:=      ",
    r"       :          ::      ",
    r"    .  .:        .:       ",
    r"       .:.       .        ",
]

# Color ASCII portrait lines with primary teal accent \x1b[96m
ASCII_PORTRAIT = "\n".join([f"\x1b[96m{line}\x1b[0m" for line in ASCII_PORTRAIT_RAW])


def main():
    # Terminal dimension: 750x500 (26 rows x 90 cols)
    t = gifos.Terminal(750, 500, 15, 15, FONT_FILE_BITMAP, 15)
    t.set_prompt(CUSTOM_PROMPT)

    # =========================================================================
    # SCENE 1: Mandatory Opening Greeting ("wasssup guys")
    # =========================================================================
    t.gen_prompt(1, count=4)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text('echo "wasssup guys"', 1, prompt_col, contin=True, speed=1)
    t.clone_frame(2)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[96mwasssup guys\x1b[0m \x1b[90m- welcome to my dev terminal\x1b[0m", 2, 1, contin=True)
    t.clone_frame(10)

    # Trigger profile launch
    t.gen_text(CUSTOM_PROMPT, 4, 1, count=2, contin=True)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("./profile.sh", 4, prompt_col, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)

    # Transition to main profile view
    t.clear_frame()
    t.set_font(FONT_FILE_BITMAP, 15)
    t.set_prompt(CUSTOM_PROMPT)

    # =========================================================================
    # SCENE 2: Main Profile View (ASCII Portrait + Full Portfolio Story)
    # =========================================================================
    # Header command
    t.gen_text(CUSTOM_PROMPT, 1, 1, count=1, contin=True)
    t.gen_text("\x1b[92m./profile.sh\x1b[0m", 1, t.curr_col, contin=True)

    # Left Column: Jaswanth's Face ASCII Portrait (Row 2, Col 2)
    t.gen_text(ASCII_PORTRAIT, 2, 2, contin=True)
    t.clone_frame(3)

    # Right Column: Section 1 - Identity & Engineering Focus (Col 30)
    col_r = 30
    t.gen_text("\x1b[96mJaswanth Kumar Chettupalli\x1b[0m \x1b[90m-\x1b[0m \x1b[93mCS @ GITAM University\x1b[0m", 2, col_r, contin=True)
    t.gen_text("\x1b[90mFocus:\x1b[0m Full-stack systems \x1b[90m|\x1b[0m Architecture \x1b[90m|\x1b[0m Applied AI", 3, col_r, contin=True)
    t.gen_text("\x1b[90m--------------------------------------------------------\x1b[0m", 4, col_r, contin=True)
    t.clone_frame(4)

    # Right Column: Section 2 - Experience
    t.gen_text("\x1b[93mExperience\x1b[0m", 5, col_r, contin=True)
    t.gen_text("\x1b[96m* Xentro\x1b[0m    \x1b[90m|\x1b[0m Frontend Head   \x1b[90m|\x1b[0m Typed UI & RBAC", 6, col_r, contin=True)
    t.gen_text("\x1b[96m* Toji Labs\x1b[0m \x1b[90m|\x1b[0m Co-founder      \x1b[90m|\x1b[0m Web Platforms", 7, col_r, contin=True)
    t.gen_text("\x1b[96m* Webbheads\x1b[0m \x1b[90m|\x1b[0m Full-Stack Dev  \x1b[90m|\x1b[0m CRM & Analytics", 8, col_r, contin=True)
    t.gen_text("\x1b[90m--------------------------------------------------------\x1b[0m", 9, col_r, contin=True)
    t.clone_frame(4)

    # Right Column: Section 3 - Projects
    t.gen_text("\x1b[93mProjects\x1b[0m", 10, col_r, contin=True)
    t.gen_text("\x1b[96m* MerchantOS\x1b[0m   \x1b[90m|\x1b[0m Autonomous Revenue Engine \x1b[90m(107 tests)\x1b[0m", 11, col_r, contin=True)
    t.gen_text("\x1b[96m* Memra\x1b[0m        \x1b[90m|\x1b[0m Privacy-First Memory Book \x1b[90m(Groq)\x1b[0m", 12, col_r, contin=True)
    t.gen_text("\x1b[96m* AI-Vis-Score\x1b[0m \x1b[90m|\x1b[0m Multi-Model Brand Intelligence", 13, col_r, contin=True)
    t.gen_text("\x1b[96m* Barabari Hub\x1b[0m \x1b[90m|\x1b[0m Vector RAG Platform \x1b[90m(CFG '26)\x1b[0m", 14, col_r, contin=True)
    t.gen_text("\x1b[90m--------------------------------------------------------\x1b[0m", 15, col_r, contin=True)
    t.clone_frame(4)

    # Right Column: Section 4 - Achievements
    t.gen_text("\x1b[93mAchievements\x1b[0m", 16, col_r, contin=True)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mWinner IdeaSprint 3.0\x1b[0m \x1b[90m(AI & Full-Stack Track)\x1b[0m", 17, col_r, contin=True)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mJPMorgan Chase Code for Good 2026\x1b[0m \x1b[90m(Selected Rep)\x1b[0m", 18, col_r, contin=True)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mAWS Student Builder Group\x1b[0m \x1b[90m@ IIT Jodhpur\x1b[0m", 19, col_r, contin=True)
    t.gen_text("\x1b[90m--------------------------------------------------------\x1b[0m", 20, col_r, contin=True)
    t.clone_frame(5)

    # Bottom: Section 5 - Closing Statement
    t.gen_text(CUSTOM_PROMPT, 23, 1, count=2, contin=True)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("echo $STATUS", 23, prompt_col, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[92m\"Continuing to build, iterate, and learn.\"\x1b[0m", 24, 1, contin=True)
    t.clone_frame(4)

    # Final prompt with blinking cursor pause
    t.gen_text(CUSTOM_PROMPT, 25, 1, count=1, contin=True)
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
