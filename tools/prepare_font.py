#!/usr/bin/env python3
"""
tools/prepare_font.py
Downloads JetBrains Mono Regular and Bold, subsets them to ASCII printable characters
using fonttools pyftsubset (woff2), generates base64 strings, and saves OFL.txt.
"""
import os
import sys
import base64
import urllib.request
import subprocess

FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
OFL_URL = "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/OFL.txt"
REGULAR_URL = "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Regular.ttf"
BOLD_URL = "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Bold.ttf"

def download_file(url, target_path):
    print(f"Downloading {url} -> {target_path}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(target_path, "wb") as f:
        f.write(resp.read())
    print(f"Saved {target_path} ({os.path.getsize(target_path)} bytes)")

def subset_font(input_ttf, output_woff2):
    print(f"Subsetting {input_ttf} -> {output_woff2}...")
    # pyftsubset with ASCII printable characters U+0020-007E
    cmd = [
        sys.executable, "-m", "fontTools.subset",
        input_ttf,
        f"--output-file={output_woff2}",
        "--flavor=woff2",
        "--unicodes=U+0020-007E",
        "--layout-features=*",
        "--desubroutinize",
        "--no-hinting",
    ]
    subprocess.check_call(cmd)
    size = os.path.getsize(output_woff2)
    print(f"Generated {output_woff2} ({size} bytes)")
    return size

def main():
    os.makedirs(FONT_DIR, exist_ok=True)
    ofl_path = os.path.join(FONT_DIR, "OFL.txt")
    if not os.path.exists(ofl_path):
        download_file(OFL_URL, ofl_path)

    reg_ttf = os.path.join(FONT_DIR, "JetBrainsMono-Regular.ttf")
    bold_ttf = os.path.join(FONT_DIR, "JetBrainsMono-Bold.ttf")
    reg_woff2 = os.path.join(FONT_DIR, "JetBrainsMono-Regular.subset.woff2")
    bold_woff2 = os.path.join(FONT_DIR, "JetBrainsMono-Bold.subset.woff2")

    if not os.path.exists(reg_ttf):
        download_file(REGULAR_URL, reg_ttf)
    if not os.path.exists(bold_ttf):
        download_file(BOLD_URL, bold_ttf)

    subset_font(reg_ttf, reg_woff2)
    subset_font(bold_ttf, bold_woff2)

    with open(reg_woff2, "rb") as f:
        reg_b64 = base64.b64encode(f.read()).decode("ascii")
    with open(bold_woff2, "rb") as f:
        bold_b64 = base64.b64encode(f.read()).decode("ascii")

    css_path = os.path.join(FONT_DIR, "fonts_embedded.css")
    with open(css_path, "w") as f:
        f.write(f"""@font-face {{
  font-family: 'JetBrains Mono';
  font-style: normal;
  font-weight: 400;
  src: url('data:font/woff2;charset=utf-8;base64,{reg_b64}') format('woff2');
}}
@font-face {{
  font-family: 'JetBrains Mono';
  font-style: normal;
  font-weight: 700;
  src: url('data:font/woff2;charset=utf-8;base64,{bold_b64}') format('woff2');
}}
""")
    print(f"Saved {css_path} ({os.path.getsize(css_path)} bytes)")

if __name__ == "__main__":
    main()
