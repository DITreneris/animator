"""The Double Agent (episode 15), 3.2: the push 9.1, S8 -> S8r (plan v2 §3.2; script v4 9.1, 1.8 s).

The camera dollies through Don's office glass into the tug on the floor. One zoom about a fixed point, so the far
plane (the wall, the glass, the room behind it) grows as a plane; the meeting and the desk are nearer, so they grow
faster (parallax) and leave the frame at the bottom. The blinds' rail leaves at the top, a sheen slides off the glass,
the glass's tint fades, and the far room hands over to S8r, which is placed in the glass at the rect the push ends on.
The last frame is S8r's frame 0 as 1.1 draws it (da_s8r.still writes it: lessons 57, 183), not a copy.

Nothing shared changes: S8 is drawn by da_s8's own layer functions with v8's flags; the glass's tint and sheen are
drawn here (da_s8.glass draws them fixed), its jambs, sill and blinds by the same geometry.

  python3 da_s8r.py                (writes da_s8r_frame0_v4.png: 1.1's frame 0)
  python3 da_push91.py [out_dir]   -> da_push91_strip_v2.png (10 fps, 18 frames) and the seam check
"""
import math
import os
import sys

import cairo
from PIL import Image

import kit
from kit import Ctx
import da_set as ds
import da_s8 as s8

W, H = 540, 960
SCALE = 2
FPS, DUR = 30, 1.8
N = int(round(FPS * DUR))                                      # 54 frames; the last is frame 0
V = s8.S8R_IN_GLASS                                            # where S8r sits in the glass (S8 v9 draws it there)
R_END = V[2] / float(W)                                        # 0.370: the view's size at the end, in frame units
FX = V[0] / (1 - R_END)                                        # the fixed point of the zoom (279, 165)
FY = V[1] / (1 - R_END)
FG_POW = 2.6                                                   # the near plane (the meeting, the desk): the far plane's ** this
WIN_POW = 1.6                                                  # the window plane (the wall, the glass, the blinds, the sill)
FATHER_POW = 2.3                                               # Father in Don's chair: behind the desk, nearer than the glass
                                                               # (the audit 8.8: the chair "came in too hard" with the desk)
ACC, DEC = 0.25, 0.17                                          # the dolly's speed-up and settle, as parts of 1.8 s


def smooth(a, b, x):
    t = min(1.0, max(0.0, (x - a) / float(b - a)))
    return t * t * (3 - 2 * t)


def ease(t):
    """the dolly: speeds up over ACC, crosses the glass at one speed, settles over DEC into frame 0's hold (CLAUDE.md
    G5: frame 0 is held; 1.1 opens still). Position along log-zoom, 0..1."""
    v = 1.0 / (1 - ACC / 2.0 - DEC / 2.0)
    if t < ACC:
        return v * t * t / (2 * ACC)
    if t > 1 - DEC:
        return 1 - v * (1 - t) ** 2 / (2 * DEC)
    return v * (ACC / 2.0 + (t - ACC))


def view(c, r):
    """frame units: the rect (FX + (0 - FX) r, ...) of size (W r, H r) fills the frame."""
    c.translate(FX, FY); c.scale(1.0 / r, 1.0 / r); c.translate(-FX, -FY)


def glass_layer(k, fade, sheen):
    """da_s8.glass, split: the tint, the fixed sheen and the frame's reflection at `fade` (1 = as S8), a sheen band at
    `sheen` (0..1 across the glass, None = none); the jambs, sill and blinds as S8."""
    c = k.c
    x, y, w, h = s8.G
    c.save(); c.rectangle(x, y, w, h); c.clip()
    if fade > 0:
        c.push_group()
        g_ = s8.GLASS_SOFT[0]
        c.set_source_rgba(*ds.GLASS, 0.12 * g_); c.rectangle(x, y, w, h); c.fill()
        g = cairo.LinearGradient(x, y, x + w, y + h)
        g.add_color_stop_rgba(0.00, 1, 1, 1, 0.0); g.add_color_stop_rgba(0.30, 1, 1, 1, 0.10 * g_)
        g.add_color_stop_rgba(0.38, 1, 1, 1, 0.0); g.add_color_stop_rgba(0.80, 1, 1, 1, 0.0)
        g.add_color_stop_rgba(0.86, 1, 1, 1, 0.07 * g_); g.add_color_stop_rgba(0.90, 1, 1, 1, 0.0)
        c.set_source(g); c.paint()
        c.set_source_rgba(1, 1, 1, 0.10 * g_); c.set_line_width(5); c.rectangle(x + 14, y + 22, w - 28, h - 40); c.stroke()
        c.pop_group_to_source(); c.paint_with_alpha(fade)
    if sheen is not None:                                      # a sheen sliding off the glass, faint (the audit: <= 0.2)
        p = x - 200 + (w + 400) * sheen
        my = y + h / 2.0
        g = cairo.LinearGradient(p - 70, my - 35, p + 70, my + 35)
        a = 0.16 * fade * math.sin(math.pi * sheen)
        g.add_color_stop_rgba(0.0, 1, 1, 1, 0); g.add_color_stop_rgba(0.5, 1, 1, 1, a); g.add_color_stop_rgba(1.0, 1, 1, 1, 0)
        c.set_source(g); c.paint()
    c.restore()
    cut = kit.cut
    J = s8.JAMB
    cut(k, [(x - J, y - J), (x, y), (x, y + h), (x - J, y + h + J * 0.6)], (0.80, 0.76, 0.68), shadow=False, lw=2)
    cut(k, [(x + w, y), (x + w + J, y - J), (x + w + J, y + h + J * 0.6), (x + w, y + h)], (0.62, 0.58, 0.52), shadow=False, lw=2)
    cut(k, [(x - J, y - J), (x + w + J, y - J), (x + w, y), (x, y)], (0.70, 0.66, 0.58), shadow=False, lw=2)
    kit.rect(k, x - J - 6, y + h, w + 2 * J + 12, 14, (0.88, 0.85, 0.78), 5660, lw=2)
    c.set_source_rgba(0, 0, 0, 0.14); c.rectangle(x - J - 6, y + h + 14, w + 2 * J + 12, 7); c.fill()
    s8.blinds_tidy(k, 8)


def draw(k, t, img, near_layers):
    draw_e(k, ease(t), img, near_layers)


def draw_e(k, e, img, near_layers):
    """three planes, one camera: the far room (S8r) ends on frame 0; the window plane, nearer, grows faster and leaves
    (jambs, rail, sill); the meeting and the desk, nearest, leave first."""
    c = k.c
    r = R_END ** e                                             # the far plane
    rw = r ** WIN_POW                                          # the window plane
    q = glass_cover(rw)                                        # how much of the frame the opening fills, 0..1
    cool = 1 - smooth(0.35, 1.0, q)                            # the glass's grade, tint, sheen and the office's light go
    fade = 1 - smooth(0.50, 1.0, q)                            # with the glass itself: gone when its edges leave the frame
    sheen = smooth(0.25, 0.95, q) if 0.25 < q < 0.95 else None
    x, y, w, h = s8.G
    c.save(); view(c, rw); s8.office_wall(k); c.restore()
    c.save()
    c.save(); view(c, rw); c.rectangle(x, y, w, h); c.restore(); c.clip()     # the opening, on the window plane
    view(c, r); s8.far_room(k, cool=cool)                      # the far plane, through the opening
    c.restore()
    c.save(); view(c, rw); glass_layer(k, fade, sheen); c.restore()
    rf = r ** FATHER_POW
    if rf > 0.08:
        c.save(); view(c, rf); father_layer(k); c.restore()
    rn = r ** FG_POW
    if rn > 0.08:                                              # the near plane: past the camera, it is gone
        c.save(); view(c, rn); near_layers(k); c.restore()
    if fade > 0:
        c.push_group(); s8.light(k); c.pop_group_to_source(); c.paint_with_alpha(fade)


def glass_cover(rw):
    """the share of the frame inside the glass's opening (below the blinds' bottom bar, above the sill), the window
    plane at zoom rw."""
    x, y, w, h = s8.G
    vx0, vy0 = FX * (1 - rw), FY * (1 - rw)
    vx1, vy1 = vx0 + W * rw, vy0 + H * rw
    gx0, gy0, gx1, gy1 = x, 155.0, x + w, y + h
    ix = max(0.0, min(vx1, gx1) - max(vx0, gx0)); iy = max(0.0, min(vy1, gy1) - max(vy0, gy0))
    return ix * iy / ((vx1 - vx0) * (vy1 - vy0))


def _hands_on():
    import hands_ps as hp
    import hands_v4 as hv
    hv.enable(); kit.HAND[0] = hp.hand
    return hp, hv


def father_layer(k):
    """da_s8.meeting's first half (V5): Don's chair, its side light, Father resting in it."""
    c = k.c
    s8.chair(k, 336, 378, 1.0)                                # CHAIR_VARIANT (default "D": v9 as before)
    g = cairo.RadialGradient(300, 470, 10, 300, 470, 120)
    g.add_color_stop_rgba(0, 0.95, 0.85, 0.70, 0.22); g.add_color_stop_rgba(1, 0.95, 0.85, 0.70, 0.0)
    c.save(); c.rectangle(264, 378, 144, 280); c.clip(); c.set_source(g); c.paint(); c.restore()
    hp, hv = _hands_on()
    try:
        hp.reset("quiet", "quiet")
        s8.seated(k, lambda: s8._father_rest(k))
    finally:
        hv.disable(); kit.HAND[0] = None


def near_layers(k):
    """da_s8.meeting's second half (Sofía reading, Pam), then frame()'s desk, props, hands and the Client; v9's flags."""
    import sofia_da as sd
    hp, hv = _hands_on()
    try:
        hp.reset("quiet", "quiet")
        keep5 = sd.LOOK_V5[0]; sd.LOOK_V5[0] = s8.S8_SOFIA_V5[0]      # as da_s8.meeting (v12: Sofía v5)
        try:
            s8.seated(k, lambda: sd.with_board(k, 444, 748, 0.66, "binder", face_kind="interested", look=(-1.0, 0.9), lift=62))
        finally:
            sd.LOOK_V5[0] = keep5
    finally:
        hv.disable(); kit.HAND[0] = None
    s8.seated(k, lambda: s8.pam_taking(k))
    s8.desk(k); s8.props(k)
    s8.pam_hands_over(k)
    s8.client_over_desk(k)


def render_e(e, img):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * SCALE, H * SCALE)
    c = cairo.Context(surf); c.scale(SCALE, SCALE)
    with ds.no_badges():
        draw_e(Ctx(c, 0), e, img, near_layers)
    surf.flush()
    return surf


def to_pil(s):
    return Image.frombuffer("RGB", (s.get_width(), s.get_height()), bytes(s.get_data()), "raw", "BGRX", 0, 1).copy()


def _diff(a, b):
    import numpy as np
    d = np.abs(np.asarray(a, dtype=np.int16) - np.asarray(b, dtype=np.int16))
    return d.mean(), np.percentile(d, 99)


def strip(frames, out, tag):
    idx = list(range(0, len(frames), 3)) + ([len(frames) - 1] if (len(frames) - 1) % 3 else [])
    tw, th = 180, 320
    cols = 7
    rows = (len(idx) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 6), rows * (th + 24)), (255, 255, 255))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(sheet)
    for n, i in enumerate(idx):
        x0, y0 = (n % cols) * (tw + 6), (n // cols) * (th + 24)
        sheet.paste(frames[i].resize((tw, th), Image.LANCZOS), (x0, y0 + 20))
        dr.text((x0 + 4, y0 + 4), "%s %d  %.1fs" % (tag, i, i / float(FPS)), fill=(0, 0, 0))
    sheet.save(out)
    print("wrote", out)


V = ["v11"]                                                    # 27 Nov (Tomas: one throne, only the robot's HR): S8 v10 +
                                                               # S8r v5; "v9": S8 v9 + S8r v4, as built before
FILES = {"v9": ("da_s8_final_v9.png", "da_s8r_frame0_v4.png", "da_push91_strip_v2.png", "da_pull81_strip_v1.png"),
         "v10": ("da_s8_final_v10.png", "da_s8r_frame0_v5.png", "da_push91_strip_v3.png", "da_pull81_strip_v2.png"),
         "v11": ("da_s8_final_v11.png", "da_s8r_frame0_v5.png", "da_push91_strip_v4.png", "da_pull81_strip_v3.png"),
         "v12": ("da_s8_final_v12.png", "da_s8r_frame0_v5.png", "da_push91_strip_v5.png", "da_pull81_strip_v4.png"),
         "v13": ("da_s8_final_v13.png", "da_s8r_frame0_v5.png", "da_push91_strip_v6.png", "da_pull81_strip_v5.png")}


def setup(out_dir):
    import da_arms
    da_arms.setup()
    s8.V5[0] = s8.V6[0] = s8.V8[0] = s8.V9[0] = True; ds.MUG_V2[0] = True
    if V[0] in ("v10", "v11", "v12", "v13"):
        s8.CHAIR_VARIANT[0] = "L"; ds.NAME_BADGES[0] = False; s8.S8R_FILE[0] = FILES[V[0]][1]
    if V[0] in ("v11", "v12", "v13"):
        s8.GLASS_SOFT[0] = 0.62
    if V[0] == "v13":                                          # v12 + the big mug before Pam, steaming (story chain fix E)
        import da_cups as cu
        s8.S8_SOFIA_V5[0] = True
        s8.MUG_FN[0] = lambda k, x, y, s_: cu.mug(k, x, y, s_, handle=-1, state="rest")
        s8.MUG_AT[0] = s8.V13_MUG; s8.MUG_STEAM[0] = True
    if V[0] == "v12":                                          # (28 Nov, the rough-cut re-render: Sofía v5, the ceramic mug;
        import da_cups as cu                                   # the Client without the rag comes from da_set)
        s8.S8_SOFIA_V5[0] = True
        s8.MUG_FN[0] = lambda k, x, y, s_: cu.mug(k, x, y, s_, handle=1, state="rest")
    f0 = os.path.join(out_dir, FILES[V[0]][1])
    return f0, cairo.ImageSurface.create_from_png(f0)           # 1.1's frame 0, as da_s8r.still wrote it


def main(out_dir="../the-double-agent"):
    """9.1: S8 v9 -> S8r; its last drawing is frame 0 itself."""
    f0, img = setup(out_dir)
    s9 = os.path.join(out_dir, FILES[V[0]][0])
    frames = [Image.open(s9).convert("RGB")]                   # 8.1's held still IS 9.1's first drawing
    frames += [to_pil(render_e(ease(i / float(N - 1)), img)) for i in range(1, N - 1)]
    frames.append(Image.open(f0).convert("RGB"))
    print("9.1 in:  frame 1 vs S8 v9: mean %.2f, 99th pct %d (levels)" % _diff(frames[1], frames[0]))
    print("9.1 seam: frame %d vs frame 0: mean %.2f, 99th pct %d (levels)" % ((N - 2,) + _diff(frames[-2], frames[-1])))
    strip(frames, os.path.join(out_dir, FILES[V[0]][2]), "9.1")
    return frames


PULL_DUR = 1.5                                                  # inside 8.1's 4.0 s (Tomas 27 Nov): 1.5 s back, 2.5 s held


def pull81(out_dir="../the-double-agent"):
    """8.1's opening (Tomas 27 Nov, /grill-me: 7.4 cuts to S8r, then the camera pulls back through the glass into the
    office and holds on the final image): 9.1's dolly played backwards, at 1.5 s. Its first drawing is frame 0 (the
    file), its last S8 v9 (the file): the hold that follows is that still."""
    f0, img = setup(out_dir)
    n = int(round(FPS * PULL_DUR))
    s9 = os.path.join(out_dir, FILES[V[0]][0])
    frames = [Image.open(f0).convert("RGB")]
    frames += [to_pil(render_e(ease(1 - i / float(n - 1)), img)) for i in range(1, n - 1)]
    frames.append(Image.open(s9).convert("RGB"))
    print("8.1 in:  frame 1 vs frame 0: mean %.2f, 99th pct %d" % _diff(frames[1], frames[0]))
    print("8.1 out: frame %d vs S8 v9: mean %.2f, 99th pct %d" % ((n - 2,) + _diff(frames[-2], frames[-1])))
    strip(frames, os.path.join(out_dir, FILES[V[0]][3]), "8.1")
    return frames


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pull":
        pull81(*sys.argv[2:])
    else:
        main(*sys.argv[1:])
