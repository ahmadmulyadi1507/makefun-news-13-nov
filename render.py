#!/usr/bin/env python3
"""Render the news-image-01 entry: a one-page front-page infographic summing up
Friday 13 November 2026's world news. Drawn from scratch with PIL (flat shapes,
no photos, no copied artwork). Output: entry.png, 1024x1024, well under 1 MiB."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
INK = (24, 28, 36)
GREY = (107, 101, 88)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(draw, cx, cy, r_out, r_in, points, fill):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def dashed_circle(draw, cx, cy, r, fill, dash=10, gap=7):
    import math
    step = 2 * math.pi / 90
    seg = []
    for i in range(91):
        a = i * step
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if (i % (dash + gap)) < dash:
            seg.append(p)
        else:
            if len(seg) > 1:
                draw.line(seg, fill=fill, width=3)
            seg = []
    if len(seg) > 1:
        draw.line(seg, fill=fill, width=3)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- header ----------------
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 116, W, 121], fill=GOLD)
f_date = font(FONT_BOLD, 25)
f_title = font(FONT_BOLD, 54)
t = "FRIDAY  -  13 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f_date)) / 2, 14), t, font=f_date, fill=GOLD)
t = "THE WORLD IN A DAY"
d.text(((W - d.textlength(t, font=f_title)) / 2, 46), t, font=f_title, fill=(255, 255, 255))

# ---------------- story cards ----------------
# (accent, headline, fact, pictogram key)
STORIES = [
    ((178, 34, 34), "UKRAINE'S 1,200-DRONE NIGHT",
     "Largest drone barrage of the war as peace talks widen to Europe", "drones"),
    ((20, 80, 110), "DRONES DOWNED OVER BAHRAIN",
     "US intercepts two Iranian drones; tankers hit in the Strait of Hormuz", "gulf"),
    ((196, 120, 20), "FAA HALTS ALL US DEPARTURES",
     "Nationwide ground stop for 4+ hours after a communications failure", "faa"),
    ((0, 120, 190), "MICROSOFT 365 DOWN, DAY TWO",
     "Outlook, Teams and Copilot offline worldwide", "cloud"),
    ((150, 40, 40), "CHINA'S DRILLS RING TAIWAN",
     "Large unannounced Pacific exercise, Taipei says", "taiwan"),
    ((120, 60, 140), "QATAR-TURKEY SIGN DEFENCE PACT",
     "Mutual defence deal sealed in Istanbul", "pact"),
]

CARD_W, CARD_H, GAP, MARGIN = 480, 269, 16, 24
f_head = font(FONT_BOLD, 31)
f_fact = font(FONT_REG, 20)
f_num = font(FONT_BOLD, 22)


def pic_drones(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(27, 42, 74))
    for sx, sy in [(40, 26), (120, 55), (200, 18), (300, 60), (380, 30), (440, 70)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255))
    # drones: small quadcopter silhouettes
    for dx, dy, s in [(90, 34, 1.3), (230, 58, 1.1), (330, 30, 1.4)]:
        cx, cy = x0 + dx, y0 + dy
        d.rectangle([cx - 12 * s, cy - 4, cx + 12 * s, cy + 4], fill=(200, 205, 215))
        d.line([cx - 20 * s, cy - 8, cx + 20 * s, cy - 8], fill=(200, 205, 215), width=3)
        d.line([cx - 20 * s, cy + 8, cx + 20 * s, cy + 8], fill=(200, 205, 215), width=3)
    # explosion starburst
    ex, ey = x0 + w - 70, y0 + h - 34
    star(d, ex, ey, 30, 13, 8, (255, 176, 32))
    star(d, ex, ey, 18, 8, 8, (255, 110, 30))


def pic_gulf(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(242, 227, 198))
    d.ellipse([x0 + w - 92, y0 + 10, x0 + w - 52, y0 + 50], fill=(255, 196, 66))
    d.rectangle([x0, y0 + 62, x0 + w, y0 + h], fill=(20, 80, 110))
    d.line([x0, y0 + 62, x0 + w, y0 + 62], fill=(255, 255, 255), width=2)
    # tanker
    d.rectangle([x0 + 60, y0 + 78, x0 + 300, y0 + 96], fill=(30, 30, 36))
    d.rectangle([x0 + 250, y0 + 58, x0 + 300, y0 + 78], fill=(30, 30, 36))
    for i, c in enumerate([(200, 60, 60), (60, 160, 90), (240, 180, 40)]):
        d.rectangle([x0 + 80 + i * 52, y0 + 62, x0 + 126 + i * 52, y0 + 78], fill=c)
    # radar arcs
    for r in (14, 26, 38):
        d.arc([x0 + w - 90 - r, y0 + 78 - r, x0 + w - 90 + r, y0 + 78 + r],
              start=270, end=90, fill=(255, 255, 255), width=3)
    d.ellipse([x0 + w - 94, y0 + 74, x0 + w - 86, y0 + 82], fill=(255, 255, 255))


def pic_faa(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(220, 233, 245))
    d.rectangle([x0, y0 + 74, x0 + w, y0 + h], fill=(90, 100, 112))
    for i in range(9):
        d.rectangle([x0 + 14 + i * 52, y0 + 88, x0 + 40 + i * 52, y0 + 94], fill=(255, 255, 255))
    # plane silhouette
    px, py = x0 + 150, y0 + 46
    d.ellipse([px - 70, py - 10, px + 90, py + 10], fill=NAVY)
    d.polygon([(px + 30, py - 8), (px + 90, py - 34), (px + 104, py - 34),
               (px + 60, py - 4)], fill=NAVY)
    d.polygon([(px - 10, py + 6), (px + 40, py + 30), (px + 56, py + 30),
               (px + 16, py + 8)], fill=NAVY)
    d.polygon([(px - 70, py - 2), (px - 96, py - 14), (px - 96, py + 2)], fill=NAVY)
    # red stop octagon
    ox, oy, r = x0 + w - 62, y0 + 44, 26
    oct_pts = []
    import math
    for i in range(8):
        a = math.pi / 8 + i * math.pi / 4
        oct_pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
    d.polygon(oct_pts, fill=(178, 34, 34), outline=(255, 255, 255), width=3)


def pic_cloud(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 241, 250))
    cx, cy = x0 + 150, y0 + 52
    d.ellipse([cx - 95, cy - 30, cx - 15, cy + 30], fill=(255, 255, 255))
    d.ellipse([cx - 45, cy - 48, cx + 45, cy + 30], fill=(255, 255, 255))
    d.ellipse([cx + 15, cy - 28, cx + 95, cy + 30], fill=(255, 255, 255))
    d.rectangle([cx - 95, cy + 4, cx + 95, cy + 30], fill=(255, 255, 255))
    # lightning bolt
    bx, by = x0 + 330, y0 + 30
    d.polygon([(bx + 18, by), (bx - 12, by + 44), (bx + 6, by + 44),
               (bx - 8, by + 78), (bx + 30, by + 30), (bx + 10, by + 30)],
              fill=(255, 176, 32))


def pic_taiwan(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(127, 179, 200))
    # island
    ix, iy = x0 + 150, y0 + 54
    d.polygon([(ix - 34, iy - 26), (ix - 6, iy - 34), (ix + 26, iy - 18),
               (ix + 36, iy + 10), (ix + 12, iy + 30), (ix - 24, iy + 26),
               (ix - 40, iy + 4)], fill=(74, 140, 74))
    dashed_circle(d, ix, iy, 52, (178, 34, 34))
    # ships
    for sx in (330, 390):
        d.rectangle([x0 + sx, y0 + 72, x0 + sx + 56, y0 + 84], fill=(60, 66, 76))
        d.rectangle([x0 + sx + 34, y0 + 58, x0 + sx + 46, y0 + 72], fill=(60, 66, 76))


def pic_pact(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(240, 234, 220))
    # Qatar flag (maroon, serrated white band)
    qx, qy = x0 + 70, y0 + 24
    d.rectangle([qx, qy, qx + 130, qy + 60], fill=(138, 21, 56))
    serr = [(qx, qy)]
    for i in range(5):
        serr.append((qx + 34, qy + i * 12))
        serr.append((qx, qy + i * 12 + 6))
    serr.append((qx, qy + 60))
    d.polygon(serr, fill=(255, 255, 255))
    d.line([qx, qy, qx, qy + 60], fill=(120, 110, 96), width=3)
    # Turkey flag (red, crescent + star)
    tx, ty = x0 + 280, y0 + 24
    d.rectangle([tx, ty, tx + 130, ty + 60], fill=(227, 10, 23))
    d.ellipse([tx + 34, ty + 12, tx + 82, ty + 48], fill=(255, 255, 255))
    d.ellipse([tx + 44, ty + 17, tx + 84, ty + 43], fill=(227, 10, 23))
    star(d, tx + 92, ty + 30, 10, 4, 5, (255, 255, 255))
    # gold ribbon joining them
    d.arc([x0 + 190, y0 + 62, x0 + 290, y0 + 108], start=180, end=360,
          fill=GOLD, width=5)


PICS = {"drones": pic_drones, "gulf": pic_gulf, "faa": pic_faa,
        "cloud": pic_cloud, "taiwan": pic_taiwan, "pact": pic_pact}

for i, (accent, headline, fact, key) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = MARGIN + col * (CARD_W + GAP)
    y0 = 136 + row * (CARD_H + GAP)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + CARD_H], fill=CARD, outline=BORDER, width=1)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + 6], fill=accent)
    PICS[key](x0, y0 + 6, CARD_W, 108)
    # number badge
    bx, by = x0 + 14, y0 + 20
    d.ellipse([bx, by, bx + 34, by + 34], fill=accent)
    d.text((bx + 17 - d.textlength(str(i + 1), font=f_num) / 2, by + 4),
           str(i + 1), font=f_num, fill=(255, 255, 255))
    # headline + fact
    lines = wrap(d, headline, f_head, CARD_W - 32)
    ty = y0 + 126
    for ln in lines[:2]:
        d.text((x0 + 16, ty), ln, font=f_head, fill=INK)
        ty += 38
    fact_lines = wrap(d, fact, f_fact, CARD_W - 32)
    ty = y0 + 126 + 76
    for ln in fact_lines[:2]:
        d.text((x0 + 16, ty), ln, font=f_fact, fill=GREY)
        ty += 24

# ---------------- footer ----------------
f_foot = font(FONT_REG, 18)
t = "Six stories, one day  -  reported Friday 13 November 2026  -  Sources: AP, Reuters, IEA"
d.text(((W - d.textlength(t, font=f_foot)) / 2, 988), t, font=f_foot, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
