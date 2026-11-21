#!/usr/bin/env python3
"""Render the travel poster for MIRELL, the isle above the clouds.

A place that does not exist: a floating island with a lighthouse and a
waterfall that pours into a sea of clouds, at golden dusk. Everything is
drawn with PIL from scratch -- no borrowed images, no network, no
randomness (fully deterministic).

Rebuilt 2026-11-21 in the post-opening session: stronger lighthouse
beams, a fuller two-ribbon waterfall with mist at its base, rock strata
and sun-side rim light, a tighter sun, crisper cloud tops, and a balloon
highlight.

Usage: python3 poster.py [output-path]   (default: entry.png next to this file)
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

W, H = 1024, 1024
FRAME = 14                      # cream border around the whole poster
BAND_TOP = 800                  # title band starts here
BAND_BOTTOM = H - FRAME

# ---------------------------------------------------------------- palette
INK_DEEP = (15, 46, 56)         # title band teal
CREAM = (247, 234, 208)
GOLD = (232, 176, 106)
GOLD_BRIGHT = (249, 205, 122)
CORAL = (217, 95, 75)
ROCK = (34, 65, 74)
ROCK_DARK = (20, 44, 54)
ROCK_LIGHT = (52, 92, 99)
GRASS = (46, 93, 79)
CLOUD_CREAM = (247, 231, 200)
CLOUD_PEACH = (240, 193, 147)

SKY_STOPS = [  # (fraction down the art region, RGB)
    (0.00, (26, 43, 77)),
    (0.30, (62, 62, 110)),
    (0.55, (122, 90, 122)),
    (0.75, (198, 122, 96)),
    (0.90, (232, 158, 104)),
    (1.00, (242, 176, 110)),
]


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def sky_color(frac):
    for i in range(len(SKY_STOPS) - 1):
        f0, c0 = SKY_STOPS[i]
        f1, c1 = SKY_STOPS[i + 1]
        if f0 <= frac <= f1:
            return lerp(c0, c1, (frac - f0) / (f1 - f0))
    return SKY_STOPS[-1][1]


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def draw_tracked(draw, cx, y, text, fnt, fill, tracking):
    """Draw text centred on cx, with `tracking` px between glyphs."""
    widths = []
    total = 0
    for ch in text:
        w = draw.textlength(ch, font=fnt)
        widths.append(w)
        total += w
    total += tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def soft_layer(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


# ------------------------------------------------------------------ scene
def render(path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    art_top, art_bottom = FRAME, BAND_TOP
    art_h = art_bottom - art_top

    # Sky gradient, row by row.
    for y in range(art_top, art_bottom):
        d.line([(FRAME, y), (W - FRAME, y)],
               fill=sky_color((y - art_top) / art_h))

    # Stars in the upper sky.
    stars = [(120, 90, 2), (240, 60, 1), (330, 120, 2), (470, 70, 1),
             (620, 90, 2), (760, 60, 1), (880, 110, 2), (950, 180, 1),
             (60, 200, 1), (180, 160, 1), (540, 130, 1), (700, 150, 2),
             (830, 220, 1), (420, 180, 1), (60, 320, 1), (950, 300, 2)]
    for x, y, r in stars:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214))

    # Sun with a soft glow, low on the horizon, left of the island.
    # Tighter than before: a smaller disc and glow so the sky keeps its
    # dusk gradient instead of washing out.
    glow = soft_layer((W, H))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([330 - 140, 560 - 140, 330 + 140, 560 + 140],
               fill=(249, 205, 122, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(32))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([330 - 84, 560 - 84, 330 + 84, 560 + 84], fill=GOLD_BRIGHT)
    d.ellipse([330 - 68, 560 - 68, 330 + 68, 560 + 68], fill=(251, 219, 150))

    # Hot-air balloon, upper left, drifting toward the island.
    bx, by = 205, 215
    bal = soft_layer((W, H))
    bd = ImageDraw.Draw(bal)
    bd.ellipse([bx - 52, by - 62, bx + 52, by + 42], fill=CORAL + (255,))
    bd.ellipse([bx - 52, by - 62, bx + 52, by + 42], outline=(247, 234, 208, 255), width=3)
    bd.ellipse([bx - 20, by - 62, bx + 20, by + 42], fill=(247, 234, 208, 255))
    bd.ellipse([bx - 7, by - 62, bx + 7, by + 42], fill=CORAL + (255,))
    bd.polygon([(bx - 34, by + 38), (bx + 34, by + 38),
                (bx + 18, by + 78), (bx - 18, by + 78)], fill=(120, 84, 58, 255))
    # small soft sheen on the sun-facing side of the envelope
    bd.ellipse([bx - 42, by - 52, bx - 26, by - 28], fill=(255, 244, 228, 210))
    bd.line([(bx - 40, by + 40), (bx - 16, by + 76)], fill=(120, 84, 58, 255), width=2)
    bd.line([(bx + 40, by + 40), (bx + 16, by + 76)], fill=(120, 84, 58, 255), width=2)
    bal = bal.filter(ImageFilter.GaussianBlur(1))
    img.paste(Image.alpha_composite(img.convert("RGBA"), bal).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # Birds.
    for x, y, s in [(120, 330, 14), (170, 300, 11), (880, 260, 12),
                    (920, 300, 9), (90, 420, 10)]:
        d.arc([x - s, y - s // 2, x, y + s // 2], 200, 340, fill=(30, 48, 66), width=3)
        d.arc([x, y - s // 2, x + s, y + s // 2], 200, 340, fill=(30, 48, 66), width=3)

    # ---- Floating island -------------------------------------------------
    # Rock mass: flat grassy top, underside tapering to a soft point.
    rock = [(470, 392), (880, 392), (868, 430), (840, 470), (800, 520),
            (740, 575), (690, 620), (665, 640), (640, 615), (600, 565),
            (555, 520), (515, 475), (488, 435)]
    isl = soft_layer((W, H))
    idr = ImageDraw.Draw(isl)
    idr.polygon(rock, fill=ROCK + (255,))
    # soft shade: darker toward the right face of the rock, masked to it
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon(rock, fill=255)
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gpx = grad.load()
    for x in range(470, 881):
        a = int(95 * max(0, (x - 600) / 280))
        for y in range(392, 641):
            gpx[x, y] = ROCK_DARK + (a,)
    isl = Image.alpha_composite(isl, Image.composite(grad, soft_layer((W, H)), mask))
    idr = ImageDraw.Draw(isl)
    # warm rim light along the top edge
    idr.line([(470, 392), (880, 392)], fill=GOLD_BRIGHT + (255,), width=4)
    # strata: thin ledges across the rock face so it reads as stone, not
    # a flat triangle; each chord stays inside the tapering outline
    for (x0, x1, y) in [(530, 820, 470), (575, 775, 530), (630, 718, 585)]:
        idr.line([(x0, y), (x1, y)], fill=ROCK_LIGHT + (110,), width=3)
    # sun-side rim light down the left underside edge
    idr.line([(490, 438), (555, 520), (600, 565), (640, 615), (665, 640)],
             fill=GOLD_BRIGHT + (150,), width=3, joint="curve")
    # grassy top
    idr.rectangle([470, 384, 880, 396], fill=GRASS + (255,))
    idr.ellipse([470, 378, 880, 398], fill=GRASS + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), isl).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # Cypress trees on the island.
    for tx, th in [(500, 46), (540, 34), (840, 40)]:
        d.polygon([(tx, 392 - th), (tx - 13, 392), (tx + 13, 392)],
                  fill=(24, 64, 52))
        d.rectangle([tx - 2, 392 - 6, tx + 2, 392], fill=(60, 44, 30))

    # Little houses with lit windows.
    for hx, hw, hh in [(576, 44, 30), (628, 36, 24), (790, 40, 26)]:
        d.rectangle([hx, 392 - hh, hx + hw, 392], fill=(247, 234, 208))
        d.polygon([(hx - 3, 392 - hh), (hx + hw // 2, 392 - hh - 16),
                   (hx + hw + 3, 392 - hh)], fill=(150, 66, 52))
        d.rectangle([hx + hw // 2 - 4, 392 - 14, hx + hw // 2 + 4, 392 - 6],
                    fill=(249, 205, 122))

    # Lighthouse: white tower, gold lamp, beams over the cloud sea.
    # Beams are now strong enough to read as the poster's landmark glow.
    lx = 716
    beam = soft_layer((W, H))
    bdr = ImageDraw.Draw(beam)
    bdr.polygon([(lx, 300), (lx - 250, 262), (lx - 250, 338)],
                fill=(249, 205, 122, 72))
    bdr.polygon([(lx, 300), (lx + 250, 268), (lx + 250, 332)],
                fill=(249, 205, 122, 72))
    beam = beam.filter(ImageFilter.GaussianBlur(6))
    img.paste(Image.alpha_composite(img.convert("RGBA"), beam).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(lx - 16, 392), (lx - 11, 306), (lx + 11, 306), (lx + 16, 392)],
              fill=(247, 234, 208))
    d.rectangle([lx - 14, 300, lx + 14, 312], fill=(30, 48, 66))
    d.rectangle([lx - 11, 288, lx + 11, 300], fill=GOLD_BRIGHT)
    d.polygon([(lx - 15, 288), (lx, 272), (lx + 15, 288)], fill=(150, 66, 52))
    d.ellipse([lx - 26, 288, lx + 26, 312], fill=(249, 205, 122))
    d.ellipse([lx - 16, 292, lx + 16, 308], fill=(255, 238, 190))

    # ---- Waterfall pouring off the island into the clouds ---------------
    # Two ribbon cascades leaving the rock's lower edge, widening as they
    # fall and dissolving into the cloud sea below, with mist where the
    # water meets the clouds.
    falls = soft_layer((W, H))
    fd = ImageDraw.Draw(falls)

    def ribbon(cx, y0, y1, half0, half1, alpha):
        pts = []
        for y in range(y0, y1, 6):
            t = (y - y0) / (y1 - y0)
            wob = 7 * math.sin(y / 24.0)
            half = half0 + (half1 - half0) * t
            pts.append((cx + wob - half, y))
        for y in range(y1 - 1, y0 - 1, -6):
            t = (y - y0) / (y1 - y0)
            wob = 7 * math.sin(y / 24.0)
            half = half0 + (half1 - half0) * t
            pts.append((cx + wob + half, y))
        fd.polygon(pts, fill=(246, 232, 200, alpha))

    ribbon(580, 540, 745, 18, 34, 225)   # main fall, off the left edge
    ribbon(652, 632, 740, 10, 20, 210)   # second fall, off the rock tip
    for i, (fx, fw) in enumerate([(568, 4), (582, 5), (596, 4)]):
        pts = []
        y = 540
        while y < 730:
            pts.append((fx + 6 * math.sin((y - 540) / 26.0 + i), y))
            y += 8
        fd.line(pts, fill=(255, 246, 224, 245), width=fw, joint="curve")
    # bright lip where the water leaves the rock
    fd.ellipse([556, 530, 604, 548], fill=(255, 246, 224, 240))
    fd.ellipse([636, 624, 668, 640], fill=(255, 246, 224, 230))
    # mist where the falls meet the cloud sea
    fd.ellipse([520, 716, 640, 756], fill=(247, 231, 200, 200))
    fd.ellipse([610, 712, 700, 748], fill=(247, 231, 200, 180))
    falls = falls.filter(ImageFilter.GaussianBlur(2))
    img.paste(Image.alpha_composite(img.convert("RGBA"), falls).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # ---- Sea of clouds ----------------------------------------------------
    clouds = soft_layer((W, H))
    cd = ImageDraw.Draw(clouds)
    puffs = [
        # (cx, cy, rx, ry, color, alpha)
        (180, 700, 190, 46, CLOUD_PEACH, 235), (420, 730, 230, 52, CLOUD_CREAM, 255),
        (700, 705, 220, 48, CLOUD_CREAM, 255), (920, 735, 180, 50, CLOUD_PEACH, 235),
        (90, 760, 150, 40, CLOUD_CREAM, 255), (330, 765, 200, 44, CLOUD_PEACH, 220),
        (580, 765, 210, 46, CLOUD_CREAM, 255), (830, 770, 200, 44, CLOUD_CREAM, 245),
        (1024 - 60, 690, 140, 38, CLOUD_CREAM, 230),
        (250, 640, 150, 34, CLOUD_CREAM, 200), (760, 645, 160, 32, CLOUD_PEACH, 190),
        (60, 660, 120, 30, CLOUD_PEACH, 180),
    ]
    for cx, cy, rx, ry, col, a in puffs:
        cd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col + (a,))
    clouds = clouds.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.alpha_composite(img.convert("RGBA"), clouds).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # Crisp cloud tops: a second, lightly blurred layer of smaller puffs
    # along the sea's upper edge, so the horizon reads as cloud, not fog.
    tops = soft_layer((W, H))
    td = ImageDraw.Draw(tops)
    for cx, cy, rx, ry in [(150, 668, 120, 26), (380, 682, 140, 28),
                           (640, 678, 150, 28), (880, 685, 130, 26),
                           (985, 700, 100, 24), (40, 690, 90, 22)]:
        td.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                   fill=CLOUD_CREAM + (130,))
    tops = tops.filter(ImageFilter.GaussianBlur(4))
    img.paste(Image.alpha_composite(img.convert("RGBA"), tops).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # ---- Title band -------------------------------------------------------
    d.rectangle([FRAME, BAND_TOP, W - FRAME, BAND_BOTTOM], fill=INK_DEEP)
    d.line([(FRAME, BAND_TOP), (W - FRAME, BAND_TOP)], fill=GOLD, width=3)

    title_font = font("LiberationSerif-Bold.ttf", 148)
    tag_font = font("LiberationSans-Bold.ttf", 30)
    draw_tracked(d, W // 2, 822, "MIRELL", title_font, CREAM, tracking=26)
    # small gold diamonds flanking the tagline, clear of the lettering
    tag_w = draw_tracked(d, W // 2, 962, "THE ISLE ABOVE THE CLOUDS", tag_font, GOLD, tracking=8)
    for dx in (-(tag_w / 2 + 30), tag_w / 2 + 30):
        cx = W // 2 + dx
        d.polygon([(cx, 962), (cx + 8, 970), (cx, 978), (cx - 8, 970)],
                  fill=GOLD)

    # Frame: cream border + thin gold inner line.
    d.rectangle([0, 0, W - 1, H - 1], outline=CREAM, width=FRAME)
    d.rectangle([FRAME - 2, FRAME - 2, W - FRAME + 1, H - FRAME + 1],
                outline=GOLD, width=2)

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    render(out)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")
