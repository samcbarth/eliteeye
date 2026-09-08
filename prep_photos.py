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

# Mood strip. Reference imagery only - these are licensed stock and are kept
# well away from the work gallery, which is entirely her own photography.
MOOD = [
    "mood-perfume", "mood-lv-flowers", "mood-watch-box", "mood-watch-leather",
    "mood-champagne", "mood-leather-bag", "mood-pearls", "mood-pearl-necklaces",
    "mood-diamond-ring", "mood-gold-necklaces", "mood-perfume-box",
    "mood-gold-round-box",
]
# Tiles render at roughly 270px wide, so 600px covers a 2x screen.
MOOD_BOX = (600, 600)

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

# Founder portrait. The only usable frame is from a 2020 graduation set, so it
# is cropped to head and shoulders and pushed to a warm monochrome: the green
# gown fought the palette, and mono reads editorial rather than commencement.
# Replace PORTRAIT_SRC with a real headshot when one exists and drop the tint.
PORTRAIT_SRC = "photos/rachel/instagram_rachelscott_2020-12-15_05.jpg"
PORTRAIT_CROP = (150, 15, 590, 565)

portrait_src = ROOT / PORTRAIT_SRC
if portrait_src.exists():
    from PIL import ImageEnhance
    im = ImageOps.exif_transpose(Image.open(portrait_src))
    im = im.crop(PORTRAIT_CROP).resize((800, 1000), Image.LANCZOS).convert("RGB")
    grey = ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.08)
    duo = ImageOps.colorize(grey, black="#1b1714", white="#f4efe7", mid="#9c9086")
    save(ImageEnhance.Sharpness(duo).enhance(1.15), OUT / "founder.jpg", 92)
    print(f"{'founder.jpg':34s} <- {pathlib.Path(PORTRAIT_SRC).name} (cropped, warm mono)")


for src_name, (out_name, box) in STOCK.items():
    src = ROOT / "photos/pexels" / src_name
    if not src.exists():
        print(f"MISSING {src_name}")
        continue
    im = ImageOps.exif_transpose(Image.open(src))
    save(ImageOps.fit(im, box, Image.LANCZOS, centering=(0.5, 0.5)), OUT / out_name, 86)
    print(f"{out_name:40s} <- {src_name}")

for name in MOOD:
    src = ROOT / "photos/pexels" / f"{name}.jpg"
    if not src.exists():
        print(f"MISSING {name}")
        continue
    im = ImageOps.exif_transpose(Image.open(src))
    save(ImageOps.fit(im, MOOD_BOX, Image.LANCZOS, centering=(0.5, 0.5)), OUT / f"{name}.jpg", 78)
    print(f"{name + '.jpg':40s} <- pexels/{name}.jpg")
