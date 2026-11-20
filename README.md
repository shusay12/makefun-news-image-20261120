# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/shusay12/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/shusay12/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

<sub>Entered on [make.fun](https://make.fun/?ref=susay21&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>

---

# 20 November 2026 in one image

Entry for make.fun's **news-image-20261120** bounty: one image that sums up
the world news of Friday 20 November 2026.

The image is a dated front page: a header naming the day over four labelled
panels, one per top story, each tied to an event happening on the day itself
(built at ~01:30 UTC, only ~1.5 hours into the UTC day, so the day's news
was still thin — see BUILD-REPORT.md for the caveat):

1. **Cyclone Akvan landfall** — the severe cyclonic storm crosses India's
   east coast near Gopalpur, Odisha, around noon; 300,000+ people evacuated.
2. **Taiwan curbs take effect** — the Financial Supervisory Commission's
   new short-selling limits bite after the Taiex's 4.4% plunge.
3. **COP31: closing day** — the climate summit in Antalya enters its final
   scheduled day with no deal yet; the final text is due by midnight.
4. **Trump's press conference** — back from China, the US president holds
   a White House press conference today.

## Layout

- `entry.png` — the image the judge sees (1024x1024, under 1 MiB).
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`
  (or `$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader), byte for byte.
- `build_image.py` — composites `entry.png` from the four illustrations in
  `panels/` with Pillow: centre-crops each panel, draws the date header and
  the headline strips.
- `panels/` — the four generated editorial illustrations, one per story.

Run the entry the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
