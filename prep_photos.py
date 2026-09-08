#!/usr/bin/env python3
"""Turn the originals in photos/ig/ into the sized files the site actually uses.

Originals stay untouched. Re-run after adding a new source photo:
  python prep_photos.py
"""
import pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "photos/ig"
OUT = ROOT / "photos"
THUMBS = OUT / "thumbs"
THUMBS.mkdir(parents=True, exist_ok=True)

# source file -> published name
MAP = {
    "eliteeye_02_CdywXTBvr6r_01.jpg": "hero.jpg",
    "eliteeye_01_CdyxDjfvyLl_01.jpg": "work-chanel-personalized.jpg",
    "eliteeye_03_CdywAtEPJKs_01.jpg": "work-ysl-paris.jpg",
    "eliteeye_04_CXj43TTs1jo_01.jpg": "work-casino-night.jpg",
    "eliteeye_05_CXjytS8puJu_01.jpg": "work-relaxation-set.jpg",
    "eliteeye_03_CdywAtEPJKs_02.jpg": "work-louis-vuitton-cards.jpg",
    "eliteeye_03_CdywAtEPJKs_03.jpg": "work-dior-necklace.jpg",
    "eliteeye_07_CWOs-syP4R6_01.jpg": "work-elite-eye-box.jpg",
    "eliteeye_02_CdywXTBvr6r_02.jpg": "work-gucci-night.jpg",
    "eliteeye_06_CWwRVNUPRRY_01.jpg": "logo.jpg",
}

# Licensed stock from Pexels, used for section atmosphere only. Her own
# photography carries the credibility; these are texture. Credits in
# photos/pexels/CREDITS.json.
STOCK = {
    "stock-writing-hand.jpg": ("service-private-gift-consulting.jpg", (1600, 900)),
    "stock-wax-seals.jpg": ("service-corporate-executive-gifting.jpg", (1600, 900)),
    "stock-bride-ribbons.jpg": ("service-weddings-and-milestones.jpg", (1600, 900)),
    "stock-ribbons-flatlay.jpg": ("service-custom-luxury-gift-boxes.jpg", (1600, 900)),
    "stock-sheer-fabric.jpg": ("band-sheer.jpg", (2400, 1000)),
}

HERO_BOX = (2000, 1200)   # wide crop for the hero
FULL_BOX = (1400, 1400)   # longest edge for gallery originals
THUMB = 800               # square thumbnails


def save(im, path, quality=86):
    im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)


for src_name, out_name in MAP.items():
    src = SRC / src_name
    if not src.exists():
        print(f"MISSING {src_name}")
        continue
    im = ImageOps.exif_transpose(Image.open(src))

    if out_name == "hero.jpg":
        save(ImageOps.fit(im, HERO_BOX, Image.LANCZOS, centering=(0.5, 0.5)), OUT / out_name, 88)
    elif out_name == "logo.jpg":
        save(ImageOps.contain(im, (900, 900), Image.LANCZOS), OUT / out_name, 90)
    else:
        full = im.copy()
        full.thumbnail(FULL_BOX, Image.LANCZOS)
        save(full, OUT / out_name)
        save(ImageOps.fit(im, (THUMB, THUMB), Image.LANCZOS, centering=(0.5, 0.45)), THUMBS / out_name)
    print(f"{out_name:34s} <- {src_name}")

for src_name, (out_name, box) in STOCK.items():
    src = ROOT / "photos/pexels" / src_name
    if not src.exists():
        print(f"MISSING {src_name}")
        continue
    im = ImageOps.exif_transpose(Image.open(src))
    save(ImageOps.fit(im, box, Image.LANCZOS, centering=(0.5, 0.5)), OUT / out_name, 86)
    print(f"{out_name:40s} <- {src_name}")
