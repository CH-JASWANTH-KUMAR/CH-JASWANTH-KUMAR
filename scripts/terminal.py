import os
import shutil
import sys

# Configure environment BEFORE gifos import
_user = os.environ.get("GH_USER", "jaswanth")
os.environ["GIFOS_GENERAL_USER_NAME"] = _user
os.environ["GIFOS_GENERAL_COLOR_SCHEME"] = "yoru"

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


def main():
    t = gifos.Terminal(750, 500, 15, 15, FONT_FILE_BITMAP, 15)
    t.set_prompt(CUSTOM_PROMPT)

    # Initial frame pause with cursor
    t.gen_prompt(1, count=10)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)

    # 1. Identity & Engineering Focus
    t.gen_typing_text("whoami", 1, prompt_col, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[96mJaswanth Kumar Chettupalli\x1b[0m \x1b[90m-\x1b[0m \x1b[93mCS @ GITAM University\x1b[0m", 2)
    t.gen_text("\x1b[90mFocus:\x1b[0m Full-stack systems \x1b[90m|\x1b[0m Reliable architecture \x1b[90m|\x1b[0m Applied AI", 3)
    t.clone_frame(8)

    # 2. Experience
    t.gen_prompt(5, count=4)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("cat experience.txt", 5, prompt_col, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[94m*\x1b[0m \x1b[96mXentro\x1b[0m     \x1b[90m|\x1b[0m Frontend Head        \x1b[90m|\x1b[0m Typed UI architecture & RBAC", 6)
    t.gen_text("\x1b[94m*\x1b[0m \x1b[96mToji Labs\x1b[0m  \x1b[90m|\x1b[0m Co-founder & Eng     \x1b[90m|\x1b[0m Web platforms & client workflows", 7)
    t.gen_text("\x1b[94m*\x1b[0m \x1b[96mWebbheads\x1b[0m  \x1b[90m|\x1b[0m Full-Stack Developer \x1b[90m|\x1b[0m CRM modules & spatial analytics", 8)
    t.clone_frame(8)

    # 3. Selected Projects
    t.gen_prompt(10, count=4)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("ls -1 projects/", 10, prompt_col, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[92mMerchantOS\x1b[0m            Autonomous revenue decision engine \x1b[90m(107 tests)\x1b[0m", 11)
    t.gen_text("\x1b[92mMemra\x1b[0m                 Privacy-first memory book \x1b[90m|\x1b[0m in-browser PDF engine", 12)
    t.gen_text("\x1b[92mAI-Visibility-Score\x1b[0m   Multi-model brand visibility & ranking analysis", 13)
    t.gen_text("\x1b[92mBarabari-Fellows-Hub\x1b[0m  Project-isolated vector RAG platform \x1b[90m(CFG '26)\x1b[0m", 14)
    t.clone_frame(8)

    # 4. Recognition & Communities
    t.gen_prompt(16, count=4)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("cat milestones.log", 16, prompt_col, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mJPMorgan Chase Code for Good 2026\x1b[0m \x1b[90m-\x1b[0m Selected GITAM representative", 17)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mAWS Student Builder Group\x1b[0m         \x1b[90m-\x1b[0m Selected @ IIT Jodhpur \x1b[90m(top 27)\x1b[0m", 18)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mIdeaSprint 3.0 Hackathon\x1b[0m          \x1b[90m-\x1b[0m Winner \x1b[90m(AI & Full-Stack Track)\x1b[0m", 19)
    t.gen_text("\x1b[93m*\x1b[0m \x1b[97mDeveloper Communities\x1b[0m             \x1b[90m-\x1b[0m Core technical member @ GDG & AWS", 20)
    t.clone_frame(8)

    # 5. Closing
    t.gen_prompt(22, count=4)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("echo $STATUS", 22, prompt_col, contin=True, speed=1)
    t.clone_frame(3)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[92m\"Continuing to build, iterate, and learn.\"\x1b[0m", 23)

    # 6. Final prompt with blinking cursor pause
    t.gen_prompt(25, count=1)
    t.toggle_show_cursor(True)
    t.clone_frame(70)

    # Generate GIF
    t.gen_gif()

    # Clean up temporary build frames
    shutil.rmtree("frames", ignore_errors=True)


if __name__ == "__main__":
    main()
