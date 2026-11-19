#!/usr/bin/env python3
"""Render entry.png: a one-page newspaper front page summing up
Thursday 19 November 2026. Every picture element is drawn in code
with PIL — no photographs, no copied artwork. Output is 1024x1024
and deterministic: same code, same bytes, every run.

Layout, top to bottom:
  * navy masthead with the paper name and the date
  * four story panels in a 2x2 grid, each with its own small
    vector illustration at the top
  * a strip of eight shorter items in two columns
  * a sources line along the bottom edge

Revision 2: the short-items strip is shortened to one measured line
per item (ellipsis guard so nothing can run into the other column
or off the page), the sources line gets its own clear band, and the
Vice City "VI" sign is filled so the letters stay legible.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (248, 244, 236)      # warm newsprint
NAVY = (18, 32, 60)
GOLD = (206, 158, 58)
CRIMSON = (172, 32, 32)
INK = (26, 26, 26)
MUTED = (96, 96, 96)
WHITE = (255, 255, 255)
SKY = (148, 178, 205)
SEA = (24, 84, 112)
DUSK = (52, 42, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, cx, y, text, fnt, colour):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y),
              text, font=fnt, fill=colour)


canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
pen = ImageDraw.Draw(canvas)

# ---------------------------------------------------------------- masthead
pen.rectangle([0, 0, PAGE, 150], fill=NAVY)
pen.rectangle([0, 150, PAGE, 154], fill=GOLD)
centred(pen, PAGE // 2, 16, "THE WORLD IN ONE DAY",
        load(SERIF_BOLD, 56), WHITE)
centred(pen, PAGE // 2, 86, "THURSDAY  ·  19 NOVEMBER 2026",
        load(SANS_BOLD, 29), GOLD)
centred(pen, PAGE // 2, 124, "One day. One picture. Every story that mattered.",
        load(SERIF, 19), (198, 204, 216))

# ---------------------------------------------------------------- stories
STORIES = [
    {
        "kicker": "SHENZHEN  ·  APEC",
        "label": "SUMMIT",
        "headline": "Three leaders, one table",
        "body": ("Trump, Xi and Putin hold their first-ever trilateral "
                 "summit in Shenzhen, on the sidelines of APEC — a room "
                 "no one thought would happen."),
        "art": "summit",
    },
    {
        "kicker": "GULF  ·  IRAN  ·  U.S.",
        "label": "ESCALATION",
        "headline": "Gulf on alert as US–Iran fire widens",
        "body": ("US jets struck a missile site on Iran's Qeshm Island on "
                 "17 Nov after Iran hit a US radar in Bahrain. On 18 Nov "
                 "Iran widened the attacks to a US base in Kuwait and "
                 "struck Bahrain again."),
        "art": "gulf",
    },
    {
        "kicker": "GAMING  ·  VICE CITY",
        "label": "RELEASE",
        "headline": "Vice City opens its gates",
        "body": ("After a 13-year wait, Grand Theft Auto VI begins its "
                 "global rollout today. Gamers finally enter Vice City."),
        "art": "vicecity",
    },
    {
        "kicker": "WASHINGTON  ·  CONGRESS",
        "label": "HISTORY",
        "headline": "Jeffries set to make history",
        "body": ("Democrats nominate Hakeem Jeffries to be the first "
                 "African-American Speaker of the US House. Peltola wins "
                 "Alaska as Democrats take 56 Senate seats."),
        "art": "capitol",
    },
]

PANEL_W, PANEL_H = 488, 344
PANEL_X = (16, 520)
PANEL_Y = (166, 526)
ART_H = 118


def art_summit(x, y, w, h):
    """Shenzhen skyline at dusk with three flags flying above it."""
    pen.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    pen.rectangle([x, y + h - 26, x + w, y + h], fill=(96, 108, 96))
    towers = [(0, 52, 46, 92), (56, 30, 40, 92), (106, 62, 52, 92),
              (168, 22, 38, 92), (216, 48, 44, 92), (270, 34, 42, 92),
              (322, 58, 46, 92), (378, 26, 40, 92), (428, 54, 44, 92)]
    for tx, ty, tw, th in towers:
        pen.rectangle([x + tx, y + ty, x + tx + tw, y + th], fill=(58, 66, 88))
        for wy in range(ty + 8, th - 6, 12):
            for wx in range(tx + 6, tx + tw - 6, 12):
                pen.rectangle([x + wx, y + wy, x + wx + 4, y + wy + 5],
                              fill=(240, 214, 120))
    # three flag poles: US, China, Russia
    for i, (fx, colours) in enumerate((
            (60, [(178, 34, 34), WHITE, (178, 34, 34)]),
            (230, [(222, 41, 16), (222, 41, 16), (222, 41, 16)]),
            (400, [(255, 255, 255), (0, 57, 166), (213, 0, 50)]))):
        pen.rectangle([x + fx, y + 8, x + fx + 3, y + 52], fill=(40, 40, 40))
        for j, c in enumerate(colours):
            pen.rectangle([x + fx + 3, y + 8 + j * 7, x + fx + 33, y + 15 + j * 7],
                          fill=c)
        pen.ellipse([x + fx - 2, y + 3, x + fx + 8, y + 13], fill=GOLD)


def art_gulf(x, y, w, h):
    """The Gulf: sea, Qeshm Island, jets overhead, missile streaks."""
    pen.rectangle([x, y, x + w, y + h], fill=SEA)
    pen.polygon([(x + 150, y + 96), (x + 215, y + 60), (x + 305, y + 56),
                 (x + 355, y + 92), (x + 320, y + 116), (x + 190, y + 118)],
                fill=(198, 166, 112))
    pen.text((x + 222, y + 80), "QESHM", font=load(SANS_BOLD, 15),
             fill=(92, 62, 22))
    # two jets crossing the sky
    for jx, jy in ((58, 26), (300, 16)):
        pen.polygon([(x + jx, y + jy + 6), (x + jx + 52, y + jy),
                     (x + jx + 60, y + jy + 6), (x + jx + 38, y + jy + 12),
                     (x + jx + 12, y + jy + 14)], fill=(228, 228, 228))
    # streaks from the jets down to the island
    for yy in (32, 42, 52):
        pen.line([x + 118, y + yy, x + 208, y + 66], fill=(255, 200, 60),
                 width=3)
    # alert ring around the island
    pen.ellipse([x + 140, y + 46, x + 366, y + 126], outline=(255, 200, 60),
                width=3)
    pen.text((x + 14, y + 94), "BAHRAIN", font=load(SANS_BOLD, 13),
             fill=(220, 230, 238))
    pen.text((x + 372, y + 22), "KUWAIT", font=load(SANS_BOLD, 13),
             fill=(220, 230, 238))


def art_vicecity(x, y, w, h):
    """Vice City at night: neon towers and a palm-lined boulevard."""
    pen.rectangle([x, y, x + w, y + h], fill=DUSK)
    pen.ellipse([x + 390, y + 10, x + 448, y + 68], fill=(244, 214, 130))
    towers = [(0, 58, 52), (60, 34, 46), (114, 66, 58), (180, 26, 44),
              (232, 52, 50), (290, 40, 46), (344, 62, 52), (404, 30, 48)]
    for tx, ty, tw in towers:
        pen.rectangle([x + tx, y + ty, x + tx + tw, y + h - 22],
                      fill=(28, 24, 52))
        for wy in range(ty + 8, h - 30, 14):
            for wx in range(tx + 6, tx + tw - 6, 13):
                pen.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 6],
                              fill=(255, 120, 200) if (wx + wy) % 26 == 0
                              else (120, 220, 255))
    pen.rectangle([x, y + h - 22, x + w, y + h], fill=(18, 16, 36))
    # neon "VI" sign
    pen.rectangle([x + 196, y + 60, x + 292, y + 98], fill=(28, 24, 52),
                  outline=(255, 80, 180), width=3)
    pen.text((x + 218, y + 64), "VI", font=load(SANS_BOLD, 30),
             fill=(255, 120, 200))
    # palm silhouettes along the boulevard
    for px in (30, 90, 360, 430):
        pen.line([x + px, y + h - 22, x + px, y + h - 52], fill=(10, 60, 30),
                 width=4)
        for dx, dy in ((-16, -8), (-8, -14), (0, -16), (8, -14), (16, -8)):
            pen.line([x + px, y + h - 52, x + px + dx, y + h - 52 + dy],
                     fill=(10, 60, 30), width=3)


def art_capitol(x, y, w, h):
    """The US Capitol dome in silhouette against a pale sky."""
    pen.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    pen.rectangle([x, y + h - 18, x + w, y + h], fill=(120, 128, 110))
    # dome
    pen.pieslice([x + 178, y + 6, x + 310, y + 96], 180, 360, fill=WHITE)
    pen.rectangle([x + 196, y + 88, x + 292, y + h - 18], fill=WHITE)
    pen.rectangle([x + 238, y - 2, x + 250, y + 14], fill=WHITE)
    pen.ellipse([x + 238, y - 8, x + 250, y + 4], fill=GOLD)
    # columns
    for cx in range(204, 292, 22):
        pen.rectangle([x + cx, y + 96, x + cx + 8, y + h - 18],
                      fill=(170, 178, 188))
    # flanking wings
    pen.rectangle([x + 96, y + 66, x + 178, y + h - 18], fill=(226, 232, 240))
    pen.rectangle([x + 310, y + 66, x + 392, y + h - 18], fill=(226, 232, 240))
    # flags on the wings
    for fx in (128, 348):
        pen.rectangle([x + fx, y + 40, x + fx + 3, y + 66], fill=(40, 40, 40))
        pen.rectangle([x + fx + 3, y + 40, x + fx + 27, y + 52],
                      fill=(178, 34, 34))
        pen.rectangle([x + fx + 3, y + 52, x + fx + 27, y + 58],
                      fill=WHITE)


ARTISTS = {"summit": art_summit, "gulf": art_gulf,
           "vicecity": art_vicecity, "capitol": art_capitol}

for idx, story in enumerate(STORIES):
    px = PANEL_X[idx % 2]
    py = PANEL_Y[idx // 2]
    pen.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=WHITE,
                  outline=(200, 196, 186), width=2)
    ARTISTS[story["art"]](px + 2, py + 2, PANEL_W - 4, ART_H)
    text_top = py + ART_H + 14
    pen.text((px + 16, text_top), story["kicker"], font=load(SANS_BOLD, 15),
             fill=CRIMSON)
    pen.text((px + PANEL_W - 16 - pen.textlength(story["label"],
             font=load(SANS_BOLD, 15)), text_top), story["label"],
             font=load(SANS_BOLD, 15), fill=MUTED)
    head_lines = wrap_text(pen, story["headline"], load(SERIF_BOLD, 27),
                           PANEL_W - 32)
    hy = text_top + 26
    for line in head_lines:
        pen.text((px + 16, hy), line, font=load(SERIF_BOLD, 27), fill=INK)
        hy += 32
    body_lines = wrap_text(pen, story["body"], load(SANS, 18),
                           PANEL_W - 32)
    by = hy + 6
    for line in body_lines:
        pen.text((px + 16, by), line, font=load(SANS, 18), fill=(52, 52, 52))
        by += 23

# ---------------------------------------------------------------- short items
STRIP = [
    ("CYCLONE AKVAN", "landfall due between Machilipatnam and Puri"),
    ("EU", "proposes a €45 billion loan for Ukraine"),
    ("NVIDIA", "Huang out; Kress acting CEO; China H-chip sales halted"),
    ("NASA", "Voyager 1 reaches one light-day from Earth"),
    ("KERCH BRIDGE", "road arch collapses after Ukrainian strikes"),
    ("EBOLA", "DR Congo outbreak passes 11,000 cases"),
    ("AUSTRALIA", "sanctions Israeli settlers over West Bank expansion"),
    ("PEW", "Islam on track to be the world's largest religion by 2035"),
]

strip_y = 886
pen.rectangle([0, strip_y - 10, PAGE, 1000], fill=(238, 232, 220))
pen.line([0, strip_y - 10, PAGE, strip_y - 10], fill=GOLD, width=3)
centred(pen, PAGE // 2, strip_y - 6, "—  ALSO TODAY  —",
        load(SANS_BOLD, 16), CRIMSON)
for i, (lead, rest) in enumerate(STRIP):
    cx = 16 if i % 2 == 0 else 520
    cy = strip_y + 20 + (i // 2) * 24
    # One line per item: shrink the tail with an ellipsis rather than
    # ever letting it run into the other column or off the page.
    head = "•  " + lead + " — "
    head_fnt, rest_fnt = load(SANS_BOLD, 14), load(SANS, 14)
    head_w = pen.textlength(head, font=head_fnt)
    while rest and pen.textlength(rest, font=rest_fnt) > 496 - 8 - head_w:
        rest = rest[:-4].rstrip() + "…"
    pen.text((cx, cy), head, font=head_fnt, fill=NAVY)
    pen.text((cx + head_w, cy), rest, font=rest_fnt, fill=INK)

# ---------------------------------------------------------------- sources
centred(pen, PAGE // 2, 1006,
        "Sources: Reuters, AP, BBC, WHO reporting of 19 November 2026",
        load(SANS, 14), MUTED)

canvas.save("entry.png", optimize=True)
print("saved entry.png", canvas.size)
