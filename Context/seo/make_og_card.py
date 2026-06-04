#!/usr/bin/env python3
"""Generate the default social share card (1200x630) for dimagi.com.

On-brand: white Dimagi wordmark + tagline on the deep-purple -> indigo
hero gradient (same direction as the homepage hero overlay). Output is a
real local asset, assets/images/og-default.png, used as the fallback
og:image / twitter:image across core pages.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOGO = os.path.join(ROOT, "assets", "dimagi-logo.png")
OUT = os.path.join(ROOT, "assets", "images", "og-default.png")

W, H = 1200, 630
DEEP_PURPLE = (22, 0, 109)   # #16006D
INDIGO = (56, 67, 208)       # #3843D0

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

# Diagonal gradient: top-left deep-purple -> bottom-right indigo (~145deg)
bg = Image.new("RGB", (W, H))
px = bg.load()
for y in range(H):
    for x in range(W):
        t = (x / W + y / H) / 2.0
        px[x, y] = lerp(DEEP_PURPLE, INDIGO, t)

card = bg.convert("RGBA")

# White wordmark from the logo's alpha channel
logo = Image.open(LOGO).convert("RGBA")
alpha = logo.split()[-1]
white = Image.new("RGBA", logo.size, (255, 255, 255, 0))
white.putalpha(alpha)
target_w = 392
scale = target_w / logo.size[0]
white = white.resize((target_w, round(logo.size[1] * scale)), Image.LANCZOS)
card.alpha_composite(white, (96, 188))

draw = ImageDraw.Draw(card)

def font(path, size):
    return ImageFont.truetype(path, size)

HELV = "/System/Library/Fonts/HelveticaNeue.ttc"
tag_font = font(HELV, 58)
sub_font = font(HELV, 30)

# Tagline
draw.text((98, 360), "Digital Solutions for", font=tag_font, fill=(255, 255, 255, 255))
draw.text((98, 432), "Frontline Work", font=tag_font, fill=(255, 255, 255, 255))

# Subtle accent rule + url
draw.line([(100, 540), (148, 540)], fill=(254, 175, 49, 255), width=4)  # marigold accent
draw.text((164, 524), "dimagi.com", font=sub_font, fill=(208, 213, 246, 255))

card.convert("RGB").save(OUT, "PNG", optimize=True)
print("wrote", OUT, card.size)
