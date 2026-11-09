"""Colour emoji as cairo surfaces (Noto Color Emoji via PIL). Same renderer as s134.py, without its episode imports."""
import numpy as np
import cairo
from PIL import Image, ImageDraw, ImageFont

EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
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

