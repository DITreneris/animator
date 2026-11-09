"""Saved to Cloud S1v3.4 - S1v3.3 with simpler name cards: a speech-bubble tag with the name and
three emoji, pointing at the character; freezes shortened from 1.3 s to 1.0 s.
New module only: patches s133 at runtime; s133.py and earlier are unchanged.
Render with engine_v.py: s134 (sniff tag) or s134n (ends on DON)."""
import os
import numpy as np
import cairo
from PIL import Image, ImageDraw, ImageFont
import kit
import s133
from kit import cut, rough_rect_pts, ease, clamp

EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
TAGS = [  # name, emoji, tag target (tail tip), bubble centre
    ("DON", ["\U0001F451", "\U0001F648", "\U0001F4C1"], (150, 545), (190, 400)),        # crown, see-no-evil, folder
    ("PAM", ["\U0001F4BE", "\U0001F4BE", "\U0001F607"], (430, 585), (370, 440)),        # floppy, floppy, halo
    ("CLOUD", ["☁️", "\U0001F634", "\U0001F927"], (290, 335), (270, 205)),    # cloud, sleeping, sneezing
]
_cache = {}


def emoji_surface(ch):
    if ch not in _cache:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        im = im.crop(im.getbbox())
        a = np.array(im).astype(np.float32)
        al = a[..., 3:4] / 255.0
        bgra = np.concatenate([a[..., 2:3] * al, a[..., 1:2] * al, a[..., 0:1] * al, a[..., 3:4]], axis=2).astype(np.uint8)
        bgra = np.ascontiguousarray(bgra)
        surf = cairo.ImageSurface.create_for_data(memoryview(bgra).cast("B"), cairo.FORMAT_ARGB32, im.width, im.height)
        _cache[ch] = (surf, bgra, im.width, im.height)
    return _cache[ch]


def draw_emoji(c, ch, cx, cy, size):
    surf, _keep, w, h = emoji_surface(ch)
    sc = size / max(w, h)
    c.save()
    c.translate(cx - w * sc / 2, cy - h * sc / 2)
    c.scale(sc, sc)
    c.set_source_surface(surf, 0, 0)
    c.paint()
    c.restore()


def tag(k, i, u):
    name, emo, (tx, ty), (bx, by) = TAGS[i]
    c = k.c
    pop = 0.6 + 0.4 * (1 + 2.6 * (clamp(u / 0.16) - 1) ** 3 + 1.6 * (clamp(u / 0.16) - 1) ** 2)   # pop with overshoot
    w, h = 250, 150
    x0, y0 = bx - w / 2, by - h / 2
    c.save()
    c.translate(bx, by)
    c.scale(max(0.02, pop), max(0.02, pop))
    c.translate(-bx, -by)
    tail = [(bx - 18, y0 + h - 3), (tx, ty), (bx + 18, y0 + h - 3)] if ty > by else \
           [(bx - 18, y0 + 3), (tx, ty), (bx + 18, y0 + 3)]
    cut(k, tail, (1, 1, 1))
    cut(k, rough_rect_pts(k, x0, y0, w, h, 990 + i, j=1.6), (1, 1, 1))
    c.select_font_face(kit.FONT)
    c.set_font_size(46)
    e = c.text_extents(name)
    c.move_to(bx - e.width / 2 - e.x_bearing, y0 + 58)
    c.set_source_rgb(*kit.INK)
    c.show_text(name)
    for j, ch in enumerate(emo):
        draw_emoji(c, ch, bx + (j - 1) * 66, y0 + 108, 52)
    c.restore()


s133.FREEZE = 1.0
s133.card = tag
s133.CARDS = [(1.1, "DON", "", []), (3.75, "PAM", "", []), (4.85, "CLOUD", "", [])]
DURATION = s133.duration(21.5)
RAW_T = 0.0


def frame(k, t, tl):
    s133.RAW_T = RAW_T
    s133.frame(k, t, tl)


PANELS = [(0.0, DURATION, frame)]
shake = s133.shake
overlay = s133.overlay
