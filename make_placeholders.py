#!/usr/bin/env python3
"""Generate cream placeholder images so the layout reads correctly before the
real photography lands. Never overwrites a real file. Delete a placeholder and
drop the real photo in at the same path when you have it."""
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).parent
CREAM, RULE, FAINT = (239, 234, 226), (221, 213, 202), (138, 130, 124)

TARGETS = [
    ("photos/hero.jpg", 1600, 900, "HERO IMAGE"),
    ("photos/founder.jpg", 800, 1000, "FOUNDER PORTRAIT"),
]

for path, w, h, label in TARGETS:
    p = ROOT / path
    if p.exists():
        print(f"have  {path}")
        continue
    im = Image.new("RGB", (w, h), CREAM)
    d = ImageDraw.Draw(im)
    d.rectangle([24, 24, w - 25, h - 25], outline=RULE, width=2)
    tw = d.textlength(label)
    d.text(((w - tw) / 2, h / 2 - 6), label, fill=FAINT)
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, quality=88)
    print(f"made  {path} ({w}x{h})")
