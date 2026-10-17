#!/usr/bin/env python3
"""
scripts/generate_reel.py
Programmatic Terminal Animation Generator for CH Jaswanth Kumar.
Uses Pillow to create a compact, accessible, high-legibility developer reel GIF.
Visual system: Near-black charcoal, off-white, muted gray, and sage-green accent.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (optimized for desktop sharpness and 320-375px mobile scale)
WIDTH = 740
HEIGHT = 390

# Color Palette (WCAG AA compliant against #0E1217)
BG_COLOR = (14, 18, 23)        # #0E1217 - near-black charcoal canvas
HEADER_COLOR = (22, 27, 34)    # #161B22 - window header
BORDER_COLOR = (39, 46, 56)    # #272E38 - subtle window hairline
HEADER_TEXT = (125, 139, 153)  # #7D8B99 - window title & metadata
DOT_INACTIVE = (48, 54, 61)    # #30363D - minimal window controls
DOT_ACTIVE = (100, 125, 105)   # #647D69 - subtle sage window control
SAGE_ACCENT = (136, 169, 142)  # #88A98E - primary sage green
TEXT_PRIMARY = (240, 244, 248) # #F0F4F8 - off-white
TEXT_MUTED = (139, 148, 158)   # #8B949E - muted gray
BRANCH_COLOR = (72, 79, 88)    # #484F58 - tree branches

# Font Paths
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT_REGULAR_PATH = os.path.join(WORKSPACE_ROOT, "assets", "fonts", "JetBrainsMono-Regular.ttf")
FONT_BOLD_PATH = os.path.join(WORKSPACE_ROOT, "assets", "fonts", "JetBrainsMono-Bold.ttf")

# Fallback to system fonts if needed
if not os.path.exists(FONT_REGULAR_PATH):
    FONT_REGULAR_PATH = "/usr/share/fonts/jetbrains-mono-fonts/JetBrainsMono-Regular.otf"
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = "/usr/share/fonts/jetbrains-mono-fonts/JetBrainsMono-Bold.otf"

font_header = ImageFont.truetype(FONT_REGULAR_PATH, 15)
font_code = ImageFont.truetype(FONT_REGULAR_PATH, 17)
font_code_bold = ImageFont.truetype(FONT_BOLD_PATH, 17)
font_title_bold = ImageFont.truetype(FONT_BOLD_PATH, 18)


def draw_window_frame():
    """Renders the outer terminal bezel, header, and control dots."""
    im = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(im)

    # 1px subtle hairline border
    draw.rectangle([(0, 0), (WIDTH - 1, HEIGHT - 1)], outline=BORDER_COLOR, width=1)

    # Header bar
    draw.rectangle([(1, 1), (WIDTH - 2, 38)], fill=HEADER_COLOR)
    draw.line([(1, 38), (WIDTH - 2, 38)], fill=BORDER_COLOR, width=1)

    # Subtle control dots (restrained, no traffic-light neon)
    draw.ellipse([(18, 14), (28, 24)], fill=DOT_INACTIVE)
    draw.ellipse([(34, 14), (44, 24)], fill=DOT_INACTIVE)
    draw.ellipse([(50, 14), (60, 24)], fill=DOT_ACTIVE)

    # Header session title
    draw.text((76, 11), "jaswanth@workstation: ~ (developer-reel)", font=font_header, fill=HEADER_TEXT)

    return im


def render_content_state(state):
    """
    Renders terminal content according to state dictionary:
    - prompt1_text, prompt1_cursor
    - show_out1
    - prompt2_text, prompt2_cursor
    - show_out2
    - prompt3_text, prompt3_cursor
    - show_out3_builds
    - show_out3_team
    - prompt4_text, prompt4_cursor
    - show_out4
    - cursor_blink_final
    """
    im = draw_window_frame()
    draw = ImageDraw.Draw(im)

    x_margin = 28
    x_desc = 205

    # Line 1: Stage 1 Prompt
    y1 = 56
    p1 = state.get("prompt1_text", "$ whoami")
    draw.text((x_margin, y1), p1, font=font_code, fill=SAGE_ACCENT)
    if state.get("prompt1_cursor"):
        bbox = draw.textbbox((x_margin, y1), p1, font=font_code)
        draw.text((bbox[2] + 2, y1), "▌", font=font_code, fill=SAGE_ACCENT)

    # Line 2: Stage 1 Output
    y2 = 84
    if state.get("show_out1"):
        draw.text((x_margin, y2), "CH_JASWANTH_KUMAR", font=font_title_bold, fill=TEXT_PRIMARY)
        draw.text((230, y2), "·  GITAM University", font=font_code, fill=TEXT_MUTED)

    # Line 3: Stage 2 Prompt
    y3 = 122
    p2 = state.get("prompt2_text")
    if p2 is not None:
        draw.text((x_margin, y3), p2, font=font_code, fill=SAGE_ACCENT)
        if state.get("prompt2_cursor"):
            bbox = draw.textbbox((x_margin, y3), p2, font=font_code)
            draw.text((bbox[2] + 2, y3), "▌", font=font_code, fill=SAGE_ACCENT)

    # Line 4: Stage 2 Output
    y4 = 150
    if state.get("show_out2"):
        draw.text((x_margin, y4), "Software Engineering  /  Full Stack  /  AI Systems", font=font_code_bold, fill=TEXT_PRIMARY)

    # Line 5: Stage 3 & 4 Prompt
    y5 = 188
    p3 = state.get("prompt3_text")
    if p3 is not None:
        draw.text((x_margin, y5), p3, font=font_code, fill=SAGE_ACCENT)
        if state.get("prompt3_cursor"):
            bbox = draw.textbbox((x_margin, y5), p3, font=font_code)
            draw.text((bbox[2] + 2, y5), "▌", font=font_code, fill=SAGE_ACCENT)

    # Line 6 & 7: Stage 3 Output (Selected builds: MerchantOS & Memra)
    y6 = 216
    y7 = 242
    if state.get("show_out3_builds"):
        # MerchantOS
        draw.text((x_margin, y6), "├── ", font=font_code, fill=BRANCH_COLOR)
        draw.text((x_margin + 36, y6), "merchantos/ ", font=font_code_bold, fill=TEXT_PRIMARY)
        draw.text((x_desc, y6), "Revenue engine · 107 automated tests", font=font_code, fill=TEXT_MUTED)

        # Memra
        draw.text((x_margin, y7), "├── ", font=font_code, fill=BRANCH_COLOR)
        draw.text((x_margin + 36, y7), "memra/      ", font=font_code_bold, fill=TEXT_PRIMARY)
        draw.text((x_desc, y7), "Privacy memory books · in-browser PDF", font=font_code, fill=TEXT_MUTED)

    # Line 8: Stage 4 Output (Team engineering: Barabari Collective)
    y8 = 268
    if state.get("show_out3_team"):
        draw.text((x_margin, y8), "└── ", font=font_code, fill=BRANCH_COLOR)
        draw.text((x_margin + 36, y8), "barabari/   ", font=font_code_bold, fill=TEXT_PRIMARY)
        draw.text((x_desc, y8), "Artisan RAG platform · JPMC Code for Good", font=font_code, fill=TEXT_MUTED)

    # Line 9: Stage 5 Prompt
    y9 = 306
    p4 = state.get("prompt4_text")
    if p4 is not None:
        draw.text((x_margin, y9), p4, font=font_code, fill=SAGE_ACCENT)
        if state.get("prompt4_cursor"):
            bbox = draw.textbbox((x_margin, y9), p4, font=font_code)
            draw.text((bbox[2] + 2, y9), "▌", font=font_code, fill=SAGE_ACCENT)

    # Line 10: Stage 5 Closing Callout
    y10 = 334
    if state.get("show_out4"):
        draw.text((x_margin, y10), "→ Technical architecture & source code below.", font=font_code, fill=SAGE_ACCENT)
        if state.get("cursor_blink_final"):
            bbox = draw.textbbox((x_margin, y10), "→ Technical architecture & source code below.", font=font_code)
            draw.text((bbox[2] + 4, y10), "▌", font=font_code, fill=SAGE_ACCENT)

    return im


def generate_animation_frames():
    """Generates the sequential story frames with respective display durations."""
    frames = []
    durations = []

    # ----------------------------------------------------
    # STAGE 1: Introduction (CH_JASWANTH_KUMAR)
    # First frame is fully styled and intentional!
    # ----------------------------------------------------
    # Frame 0: Initial prompt with blinking cursor
    frames.append(render_content_state({
        "prompt1_text": "$ whoami",
        "prompt1_cursor": True,
    }))
    durations.append(650)

    # Frame 1: Execute whoami -> show CH_JASWANTH_KUMAR
    frames.append(render_content_state({
        "prompt1_text": "$ whoami",
        "prompt1_cursor": False,
        "show_out1": True,
    }))
    durations.append(1100)

    # ----------------------------------------------------
    # STAGE 2: Engineering Focus
    # ----------------------------------------------------
    # Typing $ cat focus.spec
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ c", "prompt2_cursor": True,
    }))
    durations.append(100)

    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat f", "prompt2_cursor": True,
    }))
    durations.append(100)

    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "prompt2_cursor": True,
    }))
    durations.append(280)

    # Show Focus output
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "prompt2_cursor": False,
        "show_out2": True,
    }))
    durations.append(1300)

    # ----------------------------------------------------
    # STAGE 3: Selected Builds (MerchantOS & Memra)
    # ----------------------------------------------------
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tr", "prompt3_cursor": True,
    }))
    durations.append(100)

    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "prompt3_cursor": True,
    }))
    durations.append(300)

    # Show MerchantOS and Memra
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "prompt3_cursor": False,
        "show_out3_builds": True,
    }))
    durations.append(1300)

    # ----------------------------------------------------
    # STAGE 4: Team Engineering (Barabari Collective / JPMC)
    # ----------------------------------------------------
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "prompt3_cursor": False,
        "show_out3_builds": True,
        "show_out3_team": True,
    }))
    durations.append(1500)

    # ----------------------------------------------------
    # STAGE 5: Closing frame ($ explore --projects)
    # ----------------------------------------------------
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "show_out3_builds": True, "show_out3_team": True,
        "prompt4_text": "$ ex", "prompt4_cursor": True,
    }))
    durations.append(100)

    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "show_out3_builds": True, "show_out3_team": True,
        "prompt4_text": "$ explore --projects", "prompt4_cursor": True,
    }))
    durations.append(350)

    # Output appears with cursor
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "show_out3_builds": True, "show_out3_team": True,
        "prompt4_text": "$ explore --projects", "prompt4_cursor": False,
        "show_out4": True,
        "cursor_blink_final": True,
    }))
    durations.append(900)

    # Cursor blinks off
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "show_out3_builds": True, "show_out3_team": True,
        "prompt4_text": "$ explore --projects", "prompt4_cursor": False,
        "show_out4": True,
        "cursor_blink_final": False,
    }))
    durations.append(600)

    # Final hold with cursor on
    frames.append(render_content_state({
        "prompt1_text": "$ whoami", "show_out1": True,
        "prompt2_text": "$ cat focus.spec", "show_out2": True,
        "prompt3_text": "$ tree ./selected-work", "show_out3_builds": True, "show_out3_team": True,
        "prompt4_text": "$ explore --projects", "prompt4_cursor": False,
        "show_out4": True,
        "cursor_blink_final": True,
    }))
    durations.append(2200)

    return frames, durations


def save_optimized_gif(frames, durations, output_path):
    """Converts RGB frames into an optimized palette GIF."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate an adaptive 32-color palette across all frames for crisp rendering
    # Combining frames into a single image to compute global palette
    combined_w = WIDTH
    combined_h = HEIGHT * min(len(frames), 5)
    palette_sample = Image.new("RGB", (combined_w, combined_h))
    for idx, f in enumerate(frames[:5]):
        palette_sample.paste(f, (0, idx * HEIGHT))

    sample_p = palette_sample.quantize(colors=32, method=Image.Quantize.MEDIANCUT)

    palette_frames = []
    for f in frames:
        p_frame = f.quantize(palette=sample_p, dither=Image.Dither.NONE)
        palette_frames.append(p_frame)

    # Save animated GIF
    palette_frames[0].save(
        output_path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )

    size_kb = os.path.getsize(output_path) / 1024.0
    total_dur_sec = sum(durations) / 1000.0
    print(f"Generated {output_path}:")
    print(f"  Frames: {len(frames)}")
    print(f"  Duration: {total_dur_sec:.2f}s")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}")
    print(f"  Size: {size_kb:.2f} KB")


def main():
    output_gif = os.path.join(WORKSPACE_ROOT, "assets", "developer-reel.gif")
    print("Generating Developer Reel frames...")
    frames, durations = generate_animation_frames()
    print("Optimizing and saving GIF...")
    save_optimized_gif(frames, durations, output_gif)


if __name__ == "__main__":
    main()
