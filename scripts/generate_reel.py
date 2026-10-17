#!/usr/bin/env python3
"""
scripts/generate_reel.py
Cinematic Developer Timeline Generator for CH Jaswanth Kumar.
Uses Pillow to create a compact, high-legibility developer journey GIF.
Refined for maximum reading comfort across desktop and mobile screens (320px–360px).
Features an 8-scene narrative storyboard with dedicated project scenes,
clear 28px headlines, and at most two concise 20px supporting lines.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (compact 680x320 cinematic ratio, optimized for 28px/20px typography)
WIDTH = 680
HEIGHT = 320

# Restrained Palette (WCAG AA compliant against #0E1217)
BG_COLOR = (14, 18, 23)        # #0E1217 - near-black charcoal canvas
HEADER_COLOR = (22, 27, 34)    # #161B22 - window header
BORDER_COLOR = (39, 46, 56)    # #272E38 - subtle window hairline
HEADER_TEXT = (125, 139, 153)  # #7D8B99 - window title & metadata
DOT_INACTIVE = (48, 54, 61)    # #30363D - minimal window controls
DOT_ACTIVE = (80, 110, 95)     # #506E5F - subtle sage window control
SAGE_ACCENT = (126, 168, 149)  # #7EA895 - primary sage green
TEXT_PRIMARY = (240, 244, 248) # #F0F4F8 - warm off-white (headings)
TEXT_SECONDARY = (230, 237, 243) # #E6EDF3 - high-contrast body
TEXT_MUTED = (145, 155, 166)   # #919BA6 - muted gray
TRACK_BG = (28, 34, 42)        # #1C222A - progress track background

# Font Paths
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT_REGULAR_PATH = os.path.join(WORKSPACE_ROOT, "assets", "fonts", "JetBrainsMono-Regular.ttf")
FONT_BOLD_PATH = os.path.join(WORKSPACE_ROOT, "assets", "fonts", "JetBrainsMono-Bold.ttf")

# Fallback to system fonts if needed
if not os.path.exists(FONT_REGULAR_PATH):
    FONT_REGULAR_PATH = "/usr/share/fonts/jetbrains-mono-fonts/JetBrainsMono-Regular.otf"
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = "/usr/share/fonts/jetbrains-mono-fonts/JetBrainsMono-Bold.otf"

font_header = ImageFont.truetype(FONT_REGULAR_PATH, 13)
font_badge = ImageFont.truetype(FONT_BOLD_PATH, 13)
font_title = ImageFont.truetype(FONT_BOLD_PATH, 28)
font_subtitle = ImageFont.truetype(FONT_BOLD_PATH, 20)
font_body = ImageFont.truetype(FONT_REGULAR_PATH, 20)
font_prompt = ImageFont.truetype(FONT_BOLD_PATH, 20)


def draw_frame_shell(scene_idx, total_scenes=8):
    """Renders the outer terminal bezel, header, and timeline progress scrubber."""
    im = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(im)

    # 1px subtle hairline border
    draw.rectangle([(0, 0), (WIDTH - 1, HEIGHT - 1)], outline=BORDER_COLOR, width=1)

    # Header bar
    draw.rectangle([(1, 1), (WIDTH - 2, 34)], fill=HEADER_COLOR)

    # Minimal window control dots
    draw.ellipse([(16, 12), (26, 22)], fill=DOT_INACTIVE)
    draw.ellipse([(32, 12), (42, 22)], fill=DOT_INACTIVE)
    draw.ellipse([(48, 12), (58, 22)], fill=DOT_ACTIVE)

    # Session title & Scene counter badge
    draw.text((72, 9), "JOURNEY.LOG // CH_JASWANTH_KUMAR", font=font_header, fill=HEADER_TEXT)
    draw.text((WIDTH - 65, 9), f"[{scene_idx}/{total_scenes}]", font=font_badge, fill=SAGE_ACCENT)

    # Timeline progress scrubber bar
    bar_y = 34
    draw.line([(1, bar_y), (WIDTH - 2, bar_y)], fill=TRACK_BG, width=2)
    segment_w = (WIDTH - 2) / total_scenes
    active_x1 = 1 + (scene_idx - 1) * segment_w
    active_x2 = 1 + scene_idx * segment_w
    draw.line([(active_x1, bar_y), (active_x2, bar_y)], fill=SAGE_ACCENT, width=2)

    return im, draw


def render_scene(scene_idx, badge, title, subtitle, line1, line2, prompt=None, cursor=True):
    """Renders a unified scene with a clear headline and at most two concise supporting lines."""
    im, draw = draw_frame_shell(scene_idx)
    x = 24
    draw.text((x, 56), badge, font=font_badge, fill=SAGE_ACCENT)
    draw.text((x, 90), title, font=font_title, fill=TEXT_PRIMARY)
    draw.text((x, 138), subtitle, font=font_subtitle, fill=SAGE_ACCENT)

    if prompt:
        draw.text((x, 184), line1, font=font_body, fill=TEXT_SECONDARY)
        draw.text((x, 222), line2, font=font_body, fill=TEXT_MUTED)
        draw.text((x, 264), prompt, font=font_prompt, fill=SAGE_ACCENT)
        if cursor:
            bbox = draw.textbbox((x, 264), prompt, font=font_prompt)
            draw.text((bbox[2] + 4, 264), "▌", font=font_prompt, fill=SAGE_ACCENT)
    else:
        draw.text((x, 192), line1, font=font_body, fill=TEXT_SECONDARY)
        draw.text((x, 234), line2, font=font_body, fill=TEXT_MUTED)

    return im


def generate_animation_frames():
    """Generates the 8 sequential timeline scenes with calibrated reading durations."""
    frames = []
    durations = []

    # Scene 1: Foundations (2200ms)
    frames.append(render_scene(
        1, "01 // THE FOUNDATIONS", "Computer Science @ GITAM", "Full-Stack & Systems Architecture",
        "• Bounded automation & deterministic math services", "• Moving software from demo to dependable"
    ))
    durations.append(2200)

    # Scene 2: MerchantOS (2400ms)
    frames.append(render_scene(
        2, "02 // FLAGSHIP BUILD", "MerchantOS", "Autonomous Revenue Engine · 107 Automated Tests",
        "• Profit-bounded discount engine for commerce", "• Deterministic pricing guards protect margin math"
    ))
    durations.append(2400)

    # Scene 3: Memra (2200ms)
    frames.append(render_scene(
        3, "03 // CLIENT-SIDE ARCHITECTURE", "Memra", "In-Browser PDF Engine · Zero Cloud Storage",
        "• In-browser memory books with zero cloud storage", "• Client-side PDF generation via native Web APIs"
    ))
    durations.append(2200)

    # Scene 4: AI Visibility Tracker (2200ms)
    frames.append(render_scene(
        4, "04 // APPLIED AI & BENCHMARKING", "AI Visibility Tracker", "Cross-Model Brand Presence Analytics",
        "• Benchmarking brand presence across 4 LLMs", "• spaCy entity recognition & citation auditing"
    ))
    durations.append(2200)

    # Scene 5: Barabari Collective (2300ms)
    frames.append(render_scene(
        5, "05 // COLLABORATIVE ENGINEERING", "Barabari Collective", "JPMorgan Chase Code for Good 2026",
        "• Operational platform built for artisan teams", "• Isolated RAG with Gemini & MongoDB Vector Search"
    ))
    durations.append(2300)

    # Scene 6: Professional Experience (2400ms)
    frames.append(render_scene(
        6, "06 // PROFESSIONAL EXPERIENCE", "Professional Experience", "Frontend & Full-Stack Systems Delivery",
        "• Xentro (Frontend) · Toji Labs (Co-founder & Eng)", "• Webbheads (Full-Stack) · CRM modules & REST APIs"
    ))
    durations.append(2400)

    # Scene 7: Recognition & Communities (2300ms)
    frames.append(render_scene(
        7, "07 // RECOGNITION & COMMUNITIES", "Recognition & Communities", "Hackathons & Technical Leadership",
        "• IdeaSprint 3.0 Winner · AWS Student Builders", "• Technical Core Team @ GDG GITAM & AWS Cloud Club"
    ))
    durations.append(2300)

    # Scene 8: The Next Chapter (3000ms total, subtle blinking prompt cursor)
    frames.append(render_scene(
        8, "08 // THE NEXT CHAPTER", "THE NEXT CHAPTER", "Dependable Systems & Autonomous Workflows",
        "• Seeking software engineering internships", "• Focus: Scalable distributed systems & bounded AI",
        prompt="> journey --continue", cursor=True
    ))
    durations.append(1200)

    frames.append(render_scene(
        8, "08 // THE NEXT CHAPTER", "THE NEXT CHAPTER", "Dependable Systems & Autonomous Workflows",
        "• Seeking software engineering internships", "• Focus: Scalable distributed systems & bounded AI",
        prompt="> journey --continue", cursor=False
    ))
    durations.append(400)

    frames.append(render_scene(
        8, "08 // THE NEXT CHAPTER", "THE NEXT CHAPTER", "Dependable Systems & Autonomous Workflows",
        "• Seeking software engineering internships", "• Focus: Scalable distributed systems & bounded AI",
        prompt="> journey --continue", cursor=True
    ))
    durations.append(1400)

    return frames, durations


def save_optimized_gif(frames, durations, output_path):
    """Converts RGB frames into an optimized palette GIF."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate an adaptive 32-color palette across all frames
    palette_sample = Image.new("RGB", (WIDTH, HEIGHT * len(frames)))
    for idx, f in enumerate(frames):
        palette_sample.paste(f, (0, idx * HEIGHT))

    sample_p = palette_sample.quantize(colors=32, method=Image.Quantize.MEDIANCUT)

    palette_frames = []
    for f in frames:
        p_frame = f.quantize(palette=sample_p, dither=Image.Dither.NONE)
        palette_frames.append(p_frame)

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
    print(f"  Scenes/Frames: {len(frames)}")
    print(f"  Duration: {total_dur_sec:.2f}s")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}")
    print(f"  Size: {size_kb:.2f} KB")


def main():
    output_gif = os.path.join(WORKSPACE_ROOT, "assets", "developer-reel.gif")
    print("Generating Polished Cinematic Developer Timeline frames (8 scenes)...")
    frames, durations = generate_animation_frames()
    print("Optimizing and saving GIF...")
    save_optimized_gif(frames, durations, output_gif)


if __name__ == "__main__":
    main()
