#!/usr/bin/env python3
"""Rebuild the 20 November 2026 front page from its four panels.

Composes ``entry.png`` (1024x1024): a navy masthead naming the day, a
gold rule, then a 2x2 grid of illustrations.  Each cell pairs its
picture with a dark caption strip carrying a gold headline and a
one-line white summary.

Usage:  python3 build_image.py [output-path]
The output defaults to ``repro-entry.png`` next to this script, so a
plain run never clobbers the judged ``entry.png``.

Requires Pillow.  No network access; everything is read from ``panels/``.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PANEL_DIR = HERE / "panels"
DEFAULT_OUTPUT = HERE / "repro-entry.png"

# --- canvas geometry (pixels, measured off the finished front page) ---
CANVAS = (1024, 1024)
MASTHEAD_HEIGHT = 112
RULE_HEIGHT = 6
CELL_WIDTH = 508
PICTURE_HEIGHT = 353
STRIP_HEIGHT = 100
ROW_PITCH = 457  # cell (453) plus a 4 px navy gap between the rows
COLUMN_PITCH = 516  # cell (508) plus an 8 px navy gutter
# Panels are first shrunk to 672 px wide (448 tall), then the top
# 508x353 window is cut out, centred horizontally.
PANEL_PREVIEW_WIDTH = 672

# --- palette ---
NAVY_MASTHEAD = (11, 22, 40)
NAVY_STRIP = (8, 14, 26)
GOLD = (233, 184, 74)
WHITE = (255, 255, 255)

MASTHEAD_TEXT = "FRIDAY 20 NOVEMBER 2026"

# (panel file, headline, one-line summary), reading order.
STORIES = (
    ("panel1-cyclone.webp", "CYCLONE AKVAN LANDFALL",
     "300,000 evacuated as storm hits Odisha"),
    ("panel2-taiwan.webp", "TAIWAN CURBS IN FORCE",
     "Short-selling limits bite after rout"),
    ("panel3-cop31.webp", "COP31: CLOSING DAY",
     "Final text due on the last day"),
    ("panel4-presser.webp", "TRUMP BACK FROM CHINA",
     "White House press conference today"),
)

FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
)


def pick_font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    """Find a DejaVu (or fallback Liberation) face at the given size."""
    wanted = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    alternates = ("LiberationSans-Bold.ttf",) if bold else ("LiberationSans-Regular.ttf",)
    for folder in FONT_DIRS:
        for name in (wanted, *alternates):
            candidate = Path(folder) / name
            if candidate.is_file():
                return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def cover_fit(picture: Image.Image, width: int, height: int) -> Image.Image:
    """Shrink ``picture`` to a 672 px wide preview, then cut the top
    ``width`` x ``height`` window out of it, centred horizontally.

    The preview keeps the panel's aspect ratio; the window always
    starts at the top edge, so the skyline / horizon of each
    illustration stays where the front page shows it.
    """
    preview_height = round(picture.height * PANEL_PREVIEW_WIDTH / picture.width)
    preview = picture.resize(
        (PANEL_PREVIEW_WIDTH, preview_height), Image.LANCZOS
    )
    left = (preview.width - width) // 2
    return preview.crop((left, 0, left + width, height))


def draw_cell(canvas: Image.Image, origin_x: int, origin_y: int,
              panel_file: str, headline: str, summary: str,
              headline_font, summary_font) -> None:
    """Paste one picture plus its caption strip at the given cell origin."""
    picture = Image.open(PANEL_DIR / panel_file).convert("RGB")
    canvas.paste(
        cover_fit(picture, CELL_WIDTH, PICTURE_HEIGHT),
        (origin_x, origin_y),
    )

    strip_top = origin_y + PICTURE_HEIGHT
    strip_height = STRIP_HEIGHT
    canvas.paste(
        Image.new("RGB", (CELL_WIDTH, strip_height), NAVY_STRIP),
        (origin_x, strip_top),
    )

    pen = ImageDraw.Draw(canvas)
    text_x = origin_x + 16
    # Headline sits near the top of the strip, summary below it.
    pen.text((text_x, strip_top + 41), headline, font=headline_font,
             fill=GOLD, anchor="ls")
    pen.text((text_x, strip_top + 75), summary, font=summary_font,
             fill=WHITE, anchor="ls")


def build_page() -> Image.Image:
    """Assemble the whole front page and return it."""
    page = Image.new("RGB", CANVAS, NAVY_MASTHEAD)
    pen = ImageDraw.Draw(page)

    masthead_font = pick_font(bold=True, size=54)
    pen.text((CANVAS[0] // 2, 81), MASTHEAD_TEXT, font=masthead_font,
             fill=WHITE, anchor="ms")

    pen.rectangle(
        [(0, MASTHEAD_HEIGHT),
         (CANVAS[0], MASTHEAD_HEIGHT + RULE_HEIGHT)],
        fill=GOLD,
    )

    headline_font = pick_font(bold=True, size=31)
    summary_font = pick_font(bold=False, size=22)

    grid_top = MASTHEAD_HEIGHT + RULE_HEIGHT
    for index, (panel_file, headline, summary) in enumerate(STORIES):
        column, row = index % 2, index // 2
        draw_cell(
            page,
            column * COLUMN_PITCH,
            grid_top + row * ROW_PITCH,
            panel_file, headline, summary,
            headline_font, summary_font,
        )
    return page


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    page = build_page()
    page.save(output, format="PNG")
    print(f"wrote {output} ({output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
