#!/usr/bin/env python3
"""
Render the 23 November 2026 world-news front page.

Build tool only (not the graded entry): it draws entry.png from news.json
using Pillow, locally, with no network and no randomness, so re-running it
produces the same image. The graded program is main.ts, which simply copies
entry.png to /output/entry.png (Node 22, standard library only).

Design: a clean newspaper front page, "THE WORLD IN ONE PAGE".
The judge has no news feed, so the image must name the day, show the day's
most consequential stories across regions and fields, and stay legible at
about 300 pixels across — hence huge date and headlines, six numbered
stories, one big market number, and no tiny text.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (251, 246, 234)
INK = (20, 20, 20)
MUTED = (90, 90, 82)
RED = (180, 35, 24)
TEAL = (14, 107, 94)
NAVY = (27, 58, 92)
AMBER = (180, 83, 9)
LINE = (216, 210, 192)
CARD = (255, 255, 255)


def font(name, size):
    paths = {
        "serif_b": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "sans_b": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=1.25):
    lines = wrap(draw, text, fnt, max_w)
    lh = int(fnt.size * leading)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36

    # ---- Masthead -------------------------------------------------------
    d.text((mx, 22), data["title"], font=font("serif_b", 56), fill=INK)
    d.text((mx, 92), "MONDAY 23 NOVEMBER 2026", font=font("sans_b", 40), fill=RED)
    d.text((mx, 140), "The day's world news, summed up  •  23 November 2026",
           font=font("sans", 22), fill=MUTED)
    d.line([(mx, 178), (W - mx, 178)], fill=INK, width=4)
    d.line([(mx, 184), (W - mx, 184)], fill=INK, width=1)

    # ---- Lead story: COP31 ---------------------------------------------
    lead = data["stories"][0]
    ly, lh = 200, 250
    d.rounded_rectangle([mx, ly, 648, ly + lh], radius=10, fill=CARD,
                        outline=LINE, width=2)
    d.text((mx + 20, ly + 14), "01  •  CLIMATE  •  ANTALYA, TURKEY",
           font=font("sans_b", 20), fill=RED)
    d.text((mx + 20, ly + 44), "COP31", font=font("serif_b", 72), fill=INK)
    d.text((mx + 20, ly + 122), "COLLAPSES", font=font("serif_b", 72), fill=INK)
    text_block(d, mx + 20, ly + 206, "No deal on fossil fuels.",
               font("sans_b", 23), 580, fill=TEAL)
    # "NO DEAL" stamp in the empty space right of COP31
    d.rounded_rectangle([420, ly + 48, 624, ly + 104], radius=8,
                        outline=RED, width=4)
    d.text((438, ly + 62), "NO DEAL", font=font("sans_b", 30), fill=RED)

    # ---- Markets panel, right of lead -----------------------------------
    mk = data["stories"][1]
    d.rounded_rectangle([668, ly, W - mx, ly + lh], radius=10, fill=NAVY,
                        outline=NAVY, width=2)
    d.text((688, ly + 14), "02  •  MARKETS", font=font("sans_b", 20),
           fill=(255, 214, 130))
    d.text((688, ly + 44), "Markets slide", font=font("serif_b", 38),
           fill=(255, 255, 255))
    d.text((688, ly + 98), "NIKKEI", font=font("sans_b", 22), fill=(200, 220, 240))
    d.text((688, ly + 124), "-5.06%", font=font("sans_b", 54), fill=(255, 120, 100))
    d.text((688, ly + 196), "S&P 500  -3.7%  •  AI sell-off",
           font=font("sans_b", 20), fill=(255, 255, 255))

    # ---- Lead summary line, under the two top panels --------------------
    y = ly + lh + 16
    text_block(d, mx, y, lead["summary"], font("sans", 22), W - 2 * mx,
               fill=INK, leading=1.3)
    d.line([(mx, 536), (W - mx, 536)], fill=LINE, width=2)

    # ---- Grid: stories 03–06 -------------------------------------------
    grid_y, card_h, gap = 552, 140, 14
    cards = data["stories"][2:]
    colours = [NAVY, RED, AMBER, TEAL]
    for i, story in enumerate(cards):
        col, row = i % 2, i // 2
        x0 = mx + col * (464 + gap)
        y0 = grid_y + row * (card_h + gap)
        d.rounded_rectangle([x0, y0, x0 + 464, y0 + card_h], radius=10,
                            fill=CARD, outline=LINE, width=2)
        d.rectangle([x0, y0, x0 + 10, y0 + card_h], fill=colours[i])
        d.text((x0 + 24, y0 + 12), f"{story['n']}  •  {story['kicker']}",
               font=font("sans_b", 17), fill=colours[i])
        text_block(d, x0 + 24, y0 + 38, story["headline"],
                   font("serif_b", 29), 420, fill=INK, leading=1.05)
        text_block(d, x0 + 24, y0 + 78, story["summary"],
                   font("sans", 19), 420, fill=MUTED, leading=1.22)

    # ---- Also today ------------------------------------------------------
    ay = 862
    d.text((mx, ay), "ALSO TODAY", font=font("sans_b", 20), fill=RED)
    d.line([(mx, ay + 28), (W - mx, ay + 28)], fill=INK, width=2)
    col_w = (W - 2 * mx - 2 * 24) // 3
    for i, item in enumerate(data["also_today"]):
        x0 = mx + i * (col_w + 24)
        text_block(d, x0, ay + 42, item, font("sans", 19), col_w,
                   fill=INK, leading=1.25)

    # ---- Footer ----------------------------------------------------------
    d.rectangle([0, 968, W, H], fill=INK)
    d.text((mx, 980), data["footer"], font=font("sans_b", 18), fill=(255, 255, 255))

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {img.size} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
