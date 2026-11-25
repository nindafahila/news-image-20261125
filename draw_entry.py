#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125.

A one-page newspaper front page summing up the world news of
Wednesday 25 November 2026: lead story (Ukraine's sea drones sink
the Russian corvette Merkury off Libya) illustrated with a small
drawn scene, six more stories as cards with drawn icons, and a
footer ticker. Pure Pillow, deterministic, no network, no random
numbers: the same script always writes the same bytes.

Run: python3 draw_entry.py   (writes entry.png next to this file)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (20, 33, 61)           # deep navy
INK_SOFT = (58, 68, 92)
GOLD = (201, 162, 39)
RED = (178, 34, 24)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
CARD = (255, 255, 255)
RULE = (20, 33, 61)
SKY = (214, 226, 235)
SEA = (28, 68, 110)
ORANGE = (232, 122, 26)
YELLOW = (245, 197, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def para(draw, xy, text, fnt, max_w, leading, fill):
    """Draw wrapped paragraph; returns y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_ship_scene(draw, box):
    """Small drawn scene: warship at anchor, drones above, blast."""
    x0, y0, x1, y1 = box
    # sky
    draw.rectangle(box, fill=SKY)
    # sun haze
    draw.ellipse([x1 - 78, y0 + 14, x1 - 34, y0 + 58], fill=(250, 238, 200))
    # distant headland
    draw.polygon([(x0, y1 - 96), (x0 + 90, y1 - 128), (x0 + 190, y1 - 96)],
                 fill=(168, 186, 200))
    # sea
    draw.rectangle([x0, y1 - 88, x1, y1], fill=SEA)
    for wy, ww in ((y1 - 70, 60), (y1 - 48, 84), (y1 - 26, 56)):
        draw.arc([x0 + 18, wy, x0 + 18 + ww, wy + 18], 180, 360,
                 fill=(255, 255, 255), width=3)
        draw.arc([x0 + 150, wy + 6, x0 + 150 + ww, wy + 24], 180, 360,
                 fill=(255, 255, 255), width=3)
    # hull
    hull = [(x0 + 26, y1 - 92), (x0 + 252, y1 - 92),
            (x0 + 228, y1 - 58), (x0 + 52, y1 - 58)]
    draw.polygon(hull, fill=(52, 58, 66))
    draw.rectangle([x0 + 26, y1 - 96, x0 + 252, y1 - 92], fill=(70, 76, 84))
    # superstructure + mast
    draw.rectangle([x0 + 96, y1 - 132, x0 + 168, y1 - 96], fill=(86, 92, 100))
    draw.rectangle([x0 + 118, y1 - 152, x0 + 146, y1 - 132], fill=(86, 92, 100))
    draw.line([x0 + 132, y1 - 178, x0 + 132, y1 - 152], fill=(52, 58, 66), width=4)
    draw.polygon([(x0 + 132, y1 - 178), (x0 + 156, y1 - 172), (x0 + 132, y1 - 166)],
                 fill=RED)
    # blast above the bow
    cx, cy = x0 + 216, y1 - 168
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 34 if i % 2 == 0 else 16
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE)
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=YELLOW)
    # smoke puffs
    for sx, sy, sr in ((x0 + 178, y1 - 196, 12), (x0 + 196, y1 - 208, 15),
                       (x0 + 220, y1 - 200, 11)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 126, 134))
    # three drones with dotted trails
    for dx, dy in ((x0 + 44, y0 + 34), (x0 + 96, y0 + 58), (x0 + 150, y0 + 26)):
        for k in range(4):
            tx = dx - 14 - k * 10
            draw.ellipse([tx - 2, dy - 2, tx + 2, dy + 2], fill=(90, 96, 104))
        draw.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(30, 34, 40))
        draw.line([dx - 8, dy - 5, dx + 8, dy - 5], fill=(30, 34, 40), width=2)
        draw.line([dx - 8, dy + 5, dx + 8, dy + 5], fill=(30, 34, 40), width=2)
    draw.rectangle(box, outline=INK, width=2)


def icon(draw, kind, box, color):
    """Tiny geometric icon inside a square chip."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "shield":  # cyber
        draw.polygon([(cx, y0 + 4), (x1 - 5, y0 + 10), (x1 - 5, cy + 2),
                      (cx, y1 - 4), (x0 + 5, cy + 2), (x0 + 5, y0 + 10)],
                     outline=color, width=3)
        draw.line([cx - 7, cy, cx - 2, cy + 6, cx + 8, cy - 7],
                  fill=color, width=3)
    elif kind == "court":  # courts: pediment + columns + base
        draw.polygon([(cx - 14, y0 + 12), (cx + 14, y0 + 12), (cx, y0 + 4)],
                     fill=color)
        draw.rectangle([x0 + 5, y0 + 14, x1 - 5, y0 + 17], fill=color)
        for bx in (x0 + 8, cx - 2, x1 - 12):
            draw.rectangle([bx, y0 + 19, bx + 4, y1 - 10], fill=color)
        draw.rectangle([x0 + 5, y1 - 9, x1 - 5, y1 - 5], fill=color)
    elif kind == "tower":  # gulf
        draw.polygon([(cx - 7, y1 - 4), (cx - 5, y0 + 12), (cx + 5, y0 + 12),
                      (cx + 7, y1 - 4)], fill=color)
        draw.line([cx, y0 + 12, cx, y0 + 4], fill=color, width=3)
        for wy in (y0 + 20, y0 + 28):
            draw.line([cx - 4, wy, cx + 4, wy], fill=PAPER, width=2)
    elif kind == "cross":  # health
        draw.rectangle([cx - 4, y0 + 5, cx + 4, y1 - 5], fill=color)
        draw.rectangle([x0 + 5, cy - 4, x1 - 5, cy + 4], fill=color)
    elif kind == "ball":  # sport
        draw.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=color, width=3)
        draw.polygon([(cx, cy - 6), (cx + 6, cy - 1), (cx + 4, cy + 6),
                      (cx - 4, cy + 6), (cx - 6, cy - 1)], fill=color)
    elif kind == "bars":  # toll
        for i, hgt in enumerate((10, 18, 26)):
            bx = x0 + 6 + i * 11
            draw.rectangle([bx, y1 - 5 - hgt, bx + 8, y1 - 5], fill=color)


def card(draw, box, kicker, color, icon_kind, headline, body):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=(190, 184, 170), width=1)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=color)
    ix0, iy0 = x0 + 16, y0 + 20
    draw.rectangle([ix0, iy0, ix0 + 40, iy0 + 40], fill=(238, 234, 224))
    icon(draw, icon_kind, (ix0, iy0, ix0 + 40, iy0 + 40), color)
    tx = ix0 + 54
    draw.text((tx, iy0 + 2), kicker, font=F_SANS_B(15), fill=color)
    hy = para(draw, (tx, iy0 + 24), headline, F_SANS_B(20),
              x1 - 16 - tx, 26, INK)
    para(draw, (x0 + 16, y0 + 78), body, F_SANS(15),
         x1 - x0 - 32, 20, INK_SOFT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band ----
    d.rectangle([0, 0, W, 118], fill=INK)
    mast = "THE WORLD IN ONE PICTURE"
    mw = d.textlength(mast, font=F_SERIF_B(52))
    d.text(((W - mw) / 2, 16), mast, font=F_SERIF_B(52), fill=(255, 255, 255))
    date = "WEDNESDAY  ·  25 NOVEMBER 2026"
    dw = d.textlength(date, font=F_SANS_B(20))
    d.text(((W - dw) / 2, 82), date, font=F_SANS_B(20), fill=GOLD)
    d.rectangle([0, 118, W, 122], fill=GOLD)

    # ---- lead story ----
    lx0, ly0, lx1, ly1 = 28, 136, 996, 436
    d.rectangle([lx0, ly0, lx1, ly1], fill=CARD, outline=(190, 184, 170), width=1)
    d.rectangle([lx0, ly0, lx1, ly0 + 5], fill=RED)
    tx = lx0 + 24
    d.text((tx, ly0 + 20), "THE LEAD — MEDITERRANEAN", font=F_SANS_B(16), fill=RED)
    hy = para(d, (tx, ly0 + 48), "SEVEN DRONES SINK A RUSSIAN WARSHIP",
              F_SERIF_B(40), 596, 48, INK)
    deck = ("Ukraine says its sea drones sank the corvette Merkury at anchor "
            "in Benghazi and hit the cargo ship Angara. Zelenskyy also "
            "confirmed the strike on the Sparta II in the Gulf of Finland.")
    hy = para(d, (tx, hy + 10), deck, F_SERIF(19), 596, 26, INK_SOFT)
    d.text((tx, ly1 - 34),
           "BENGHAZI — 7 Ukrainian-made sea drones · corvette commissioned 2023",
           font=F_SANS_B(13), fill=INK_SOFT)
    draw_ship_scene(d, (672, 156, 972, 416))

    # ---- six story cards ----
    cards = [
        ("CYBER", RED, "shield",
         "CIA and spy office breached",
         "Hackers hit an unclassified system shared by the CIA and the "
         "Director of National Intelligence, days after breaches at the FBI "
         "and the farm payments system."),
        ("COURTS", INK, "court",
         "Huawei convicted in New York",
         "A Brooklyn jury found the Chinese telecom giant guilty on 10 of 12 "
         "counts — bank fraud, wire fraud, stealing trade secrets. It was "
         "cleared of racketeering."),
        ("GULF", TEAL, "tower",
         "Houthis hit Riyadh tower",
         "A drone strike on the Saudi capital's tallest skyscraper wounded "
         "11 people — the second hit in under a week. The Saudi-led "
         "coalition vowed a decisive response."),
        ("HEALTH", GREEN, "cross",
         "Ebola teams flee Congo hospital",
         "WHO staff were evacuated from a hospital in Akwe, Ituri, after "
         "sheltering three days in the maternity ward. The outbreak has "
         "reached 11,762 cases and 5,775 deaths."),
        ("SPORT", (146, 110, 8), "ball",
         "Madrid 5–1 PSV: Bellingham stuns",
         "Jude Bellingham came off the bench to score a wonder goal and "
         "Kylian Mbappé struck twice as Real Madrid came from behind — a "
         "fifth straight Champions League win."),
        ("WAR TOLL", (122, 28, 20), "bars",
         "Russia's dead put past 700,000",
         "Leaked Rosstat records counted 490,000 Russian military deaths "
         "registered by the end of September; with the missing included, "
         "the toll is put at about 720,000."),
    ]
    gx, gy = 28, 452
    cw, ch, gap = 476, 148, 16
    for i, (kick, col, ic, head, body) in enumerate(cards):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        card(d, (cx, cy, cx + cw, cy + ch), kick, col, ic, head, body)

    # ---- ticker ----
    d.rectangle([0, 934, W, 978], fill=INK)
    tick = ("SPAIN VOTES IN 4 DAYS   •   US MARKETS SHUT THURSDAY   •   "
            "SENEGAL'S AFCON TITLE RESTORED")
    tw = d.textlength(tick, font=F_SANS_B(15))
    d.text(((W - tw) / 2, 950), tick, font=F_SANS_B(15), fill=(255, 255, 255))
    src = "Sources: Reuters · AP · NYT · UEFA · WHO — drawn from verified reports of 25 November 2026"
    sw = d.textlength(src, font=F_SANS(14))
    d.text(((W - sw) / 2, 992), src, font=F_SANS(14), fill=INK_SOFT)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
