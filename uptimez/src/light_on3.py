"""OFFICE NOIR 3: light, a trial, v1 (20 Nov). Tomas: "why did Office Noir 1 and 2 look better; the lighting? Look at how
we can fit the lighting; maybe we find a good way." Measured: this film is brighter (mean 0.41 against 0.30 and 0.33),
48% of it mid grey (34%), and it calls none of the first two films' lighting tools; in them light falls ON the figures
and the frame is finished after the noir pass. Here: light put on a FINISHED frame (after the noir pass, as Noir 2 did),
from what the film already knows: where each tracked head is (motion_on3.CLOCK["heads"]) and one source a scene.
  A  "Noir 2": a pool of light where the scene's source falls, the rest sinks; the side away from the source shaded; vignette
  B  "Noir 1": A, and: the brim's / hood's shadow across each face's eyes; the body's far side dark; blinds' bars thrown
     across figures indoors; grain
Nothing in the film uses this yet. trial() -> ../office-noir-3/on3_light_trial_v1.png"""
import math
import cairo
import numpy as np

W, H = 540, 960
# a scene: (source x, y on the frame; pool rx, ry; how dark outside; which side is away from the light; blinds)
SCENES = {
    "street": dict(src=(270, 120), pool=(270, 610, 250, 330), dark=0.62, side=0, blinds=False),
    "alley": dict(src=(-40, 300), pool=(200, 600, 330, 300), dark=0.50, side=1, blinds=False),
    "office": dict(src=(520, 200), pool=(300, 430, 300, 360), dark=0.50, side=-1, blinds=True),
    "ring": dict(src=(270, 60), pool=(270, 560, 300, 400), dark=0.58, side=0, blinds=False),
    "close": dict(src=(420, 80), pool=(270, 430, 300, 420), dark=0.45, side=-1, blinds=False),
}


def _pool(c, x, y, rx, ry, dark):
    """Everything outside an ellipse of light sinks; soft at the edge."""
    c.save(); c.translate(x, y); c.scale(rx, ry)
    g = cairo.RadialGradient(0, 0, 0.55, 0, 0, 1.35)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, dark)
    c.set_source(g); c.paint(); c.restore()


def _side(c, side, a=0.34):
    if not side:
        return
    x0, x1 = (W * 0.45, W) if side > 0 else (W * 0.55, 0)
    g = cairo.LinearGradient(x0, 0, x1, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, a); c.set_source(g); c.paint()


def _vignette(c, a=0.34):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.30, W / 2, H / 2, H * 0.72)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, a); c.set_source(g); c.paint()


def _figures(c, heads, src):
    """On each tracked figure: a shadow across the eyes from above (a brim, a hood, a lamp overhead), and the half of
    the body away from the source dark. Soft; drawn over the figure's own box only."""
    for hx, hy, sc in heads:
        r = 62 * sc
        away = 1 if src[0] < hx else -1
        g = cairo.LinearGradient(0, hy - r * 1.15, 0, hy + r * 0.15)                         # the eyes, in shadow
        g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(0.75, 0, 0, 0, 0.42); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
        c.save(); c.translate(hx, hy - r * 0.45); c.scale(r * 1.05, r * 0.75); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source(g); c.fill()
        bx0, bx1 = (hx, hx + away * r * 1.5)
        g = cairo.LinearGradient(bx0, 0, bx1, 0)                                              # the far side of the body
        g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(0.5, 0, 0, 0, 0.36); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
        c.save(); c.translate(hx + away * r * 0.75, hy + r * 2.4); c.scale(r * 0.85, r * 3.3); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source(g); c.fill()


def _blinds(c, heads, angle=-0.2, gap=40, band=17, a=0.30):
    """The blinds' bars, thrown across the figures in the room (not the wall: the wall has its own)."""
    for hx, hy, sc in heads:
        r = 62 * sc
        c.save(); c.translate(hx, hy + r * 1.6); c.scale(r * 1.6, r * 3.6); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
        c.translate(hx, hy); c.rotate(angle); c.set_source_rgba(0, 0, 0, a)
        y = -700
        while y < 900:
            c.rectangle(-700, y, 1400, band); y += gap
        c.fill(); c.identity_matrix(); c.reset_clip()


_GRAIN = []


def _grain(surf, a=10.0, seed=0):
    if not _GRAIN:
        rng = np.random.default_rng(3)
        _GRAIN.extend(rng.normal(0, 1, (H, W)).astype(np.float32) for _ in range(4))
    buf = np.frombuffer(surf.get_data(), np.uint8).reshape(H, surf.get_stride() // 4, 4)
    n = (_GRAIN[seed % 4] * a)[:, :, None]
    lum = buf[:, :W, :3].astype(np.float32)
    red = (lum[:, :, 2:3] - lum[:, :, 1:2]) > 60                                              # the key red is left clean
    buf[:, :W, :3] = np.clip(lum + np.where(red, 0, n), 0, 255).astype(np.uint8)
    surf.mark_dirty()


def light(surf, scene, heads=(), kind="B", seed=0):
    """-> a new 540 x 960 frame, lit. heads: [(x, y, scale)] on this frame."""
    p = SCENES[scene]
    out = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(out)
    c.set_source_surface(surf, 0, 0); c.paint()
    if kind == "B":
        _figures(c, heads, p["src"])
        if p["blinds"]:
            _blinds(c, heads)
    _pool(c, *p["pool"], p["dark"])
    _side(c, p["side"])
    _vignette(c)
    if kind == "B":
        out.flush(); _grain(out, seed=seed)
    return out


def trial(out="../office-noir-3/on3_light_trial_v1.png"):
    import film_on3 as f
    from PIL import Image, ImageDraw
    D = dict((a, c_) for a, b_, c_ in f.FILM)
    shots = [("2.6", 1.3, "street"), ("3.4d", 0.4, "alley"), ("4.3", 0.5, "office"), ("4.4c", 0.4, "close"), ("5.1a", 0.6, "ring"), ("7.2", 0.5, "ring"), ("7.3", 0.3, "ring")]
    rows = [[], [], []]; stats = [[], [], []]
    for n, t, sc in shots:
        s0 = D[n](t)
        heads, zoom = list((f.mo.CLOCK.get("heads") or {}).values()), f.mo.CLOCK.get("zoom")
        if zoom:
            (fx, fy), z = zoom
            heads = [(fx + (x - fx) * z, fy + (y - fy) * z, s_ * z) for x, y, s_ in heads]
        for i, sf_ in enumerate((s0, light(s0, sc, heads, "A"), light(s0, sc, heads, "B"))):
            sf_.write_to_png("/tmp/_l.png"); im = Image.open("/tmp/_l.png").convert("RGB"); rows[i].append(im.resize((270, 480)))
            g = np.asarray(im.convert("L"), dtype=float) / 255; stats[i].append((g.mean(), ((g > 0.25) & (g < 0.75)).mean()))
    sheet = Image.new("RGB", (270 * len(shots) + 70, 480 * 3), "white"); d = ImageDraw.Draw(sheet)
    for i, lab in enumerate(("NOW", "A", "B")):
        d.text((8, 480 * i + 230), lab, fill="black")
        for j, im in enumerate(rows[i]):
            sheet.paste(im, (70 + 270 * j, 480 * i))
    sheet.save(out)
    return [(round(float(np.mean([a for a, _ in st])), 2), round(float(np.mean([b for _, b in st])), 2)) for st in stats]


if __name__ == "__main__":
    print(trial())
