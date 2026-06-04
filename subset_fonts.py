#!/usr/bin/env python3
"""
Rebuild the GenWanMin (源雲明體) woff2 subsets used by the site.

Collects every character that appears in the site's HTML/QMD sources
(including the footer and the bilingual data-en/data-zh attributes and
the JS strings in _header.html), then subsets the full OTFs down to just
those glyphs. Run this whenever you add new text (especially new Chinese
characters) so the subset fonts don't show missing glyphs (tofu).

Requires: fonttools, brotli   ->   pip install fonttools brotli

Usage:  python3 subset_fonts.py
"""
import glob
import html
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
FONT_DIR = ROOT / "fonts"

# weight suffix in source OTF  ->  output subset name
WEIGHTS = {
    "R": "GenWanMin2TW-R",
    "M": "GenWanMin2TW-M",
    "SB": "GenWanMin2TW-SB",
}

SAFETY = ''.join(chr(c) for c in range(0x20, 0x7f)) + '©·–—…“”‘’「」『』（）、，。：；！？％　'


def collect_chars() -> str:
    chars = set(SAFETY)
    sources = glob.glob(str(ROOT / "*.html")) + glob.glob(str(ROOT / "*.qmd"))
    sources += [str(ROOT / "_header.html"), str(ROOT / "_footer.html")]
    for f in sources:
        p = pathlib.Path(f)
        if not p.exists():
            continue
        text = html.unescape(p.read_text(encoding="utf-8", errors="ignore"))
        chars.update(ch for ch in text if ch not in "\n\r\t")
    return ''.join(sorted(chars))


def main() -> None:
    chars = collect_chars()
    cjk = sum(1 for c in chars if ord(c) > 0x2e7f)
    print(f"Collected {len(chars)} unique chars ({cjk} CJK).")

    # Write the char list to the system temp dir (avoids touching the repo /
    # cloud-synced folder, which may disallow deleting hidden files).
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".txt", delete=False
    ) as tf:
        tf.write(chars)
        chars_file = tf.name

    try:
        for src, base in WEIGHTS.items():
            otf = FONT_DIR / f"GenWanMin2TW-{src}.otf"
            out = FONT_DIR / f"{base}-sub.woff2"
            if not otf.exists():
                print(f"  ! missing source {otf.name}, skipped")
                continue
            subprocess.run([
                "pyftsubset", str(otf),
                f"--text-file={chars_file}",
                "--flavor=woff2",
                "--layout-features=*",
                f"--output-file={out}",
            ], check=True)
            print(f"  built {out.name} ({out.stat().st_size // 1024} KB)")
    finally:
        pathlib.Path(chars_file).unlink(missing_ok=True)
    print("Done.")


if __name__ == "__main__":
    sys.exit(main())
