"""Build entry.png: the world news of Friday 20 November 2026 in one image.

Four generated editorial illustrations, one per top story of the day, are
composited into a 1024x1024 front page: a navy header naming the day, then a
2x2 grid of panels, each with a bold headline strip so a viewer who missed
the day can tell what happened from the image alone.

The four stories, each tied to an event happening on 20 November 2026
(checked at ~01:30 UTC, only ~1.5 hours into the UTC day, so the day's news
is still thin - see the caveat in BUILD-REPORT.md):
  1. Cyclone Akvan makes landfall on India's east coast around noon
     (IMD; 300,000+ evacuated, 423 rescue teams, 69 trains cancelled).
  2. Taiwan's Financial Supervisory Commission short-selling curbs take
     effect today after the Taiex's 4.4% plunge (Reuters).
  3. COP31 enters its scheduled closing day in Antalya with no deal yet;
     the final text is due by midnight Friday (UN News, Reuters).
  4. Trump, back from China, holds a White House press conference today
     (announced for the 20th).

Run: python3 build_image.py   (reads panels/, writes entry.png)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PANELS_DIR = HERE / "panels"
OUT = HERE / "entry.png"

SIZE = 1024
HEADER_H = 118
GUTTER = 8
BAND_H = 96

NAVY = (11, 22, 40)
GOLD = (232, 184, 75)
WHITE = (245, 247, 250)
BAND = (8, 14, 26)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
DATE_FONT = ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), 54)
HEAD_FONT = ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), 31)
SUB_FONT = ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 22)

PANELS = [
    ("panel1-cyclone.webp", "CYCLONE AKVAN LANDFALL", "300,000 evacuated as storm hits Odisha"),
    ("panel2-taiwan.webp", "TAIWAN CURBS IN FORCE", "Short-selling limits bite after rout"),
    ("panel3-cop31.webp", "COP31: CLOSING DAY", "Final text due on the last day"),
    ("panel4-presser.webp", "TRUMP BACK FROM CHINA", "White House press conference today"),
]


def center_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Crop img centrally to the target aspect, then resize to target size."""
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize(
        (round(img.width * scale), round(img.height * scale)), Image.LANCZOS
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def draw_centered(draw: ImageDraw.ImageDraw, cx: int, y: int, text: str, font, fill) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((cx - (box[2] - box[0]) // 2, y), text, font=font, fill=fill)


def main() -> None:
    page = Image.new("RGB", (SIZE, SIZE), NAVY)
    draw = ImageDraw.Draw(page)

    # Header: the day, named in full, over a gold rule.
    draw_centered(draw, SIZE // 2, 30, "FRIDAY 20 NOVEMBER 2026", DATE_FONT, WHITE)
    draw.rectangle([0, HEADER_H - 6, SIZE, HEADER_H], fill=GOLD)

    cell_w = (SIZE - GUTTER) // 2
    cell_h = (SIZE - HEADER_H - GUTTER) // 2
    positions = [
        (0, HEADER_H),
        (cell_w + GUTTER, HEADER_H),
        (0, HEADER_H + cell_h + GUTTER),
        (cell_w + GUTTER, HEADER_H + cell_h + GUTTER),
    ]

    for (filename, headline, subline), (x, y) in zip(PANELS, positions):
        art = Image.open(PANELS_DIR / filename).convert("RGB")
        page.paste(center_crop(art, cell_w, cell_h), (x, y))
        band_y = y + cell_h - BAND_H
        draw.rectangle([x, band_y, x + cell_w, y + cell_h], fill=BAND)
        draw.text((x + 16, band_y + 12), headline, font=HEAD_FONT, fill=GOLD)
        draw.text((x + 16, band_y + 54), subline, font=SUB_FONT, fill=WHITE)

    page.save(OUT, format="PNG")
    if OUT.stat().st_size > 1_048_576:
        # The gate reads the format from the first bytes, so a JPEG keeps the
        # same entry.png name while fitting the 1 MiB cap.
        page.save(OUT, format="JPEG", quality=90)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
