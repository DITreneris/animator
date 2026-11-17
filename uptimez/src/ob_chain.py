"""THE ONBOARDING: the reaction chain, storyboard strip v2 (ob_chain_v1.py = v1, kept), after the cold mute test of v1.
Two fresh viewers could not tell whom she was looking at, read the hand on the pearls as pointing at herself, put
Don's anger down to his ketchup stain, and thought it was her finger on the button. v1 was all singles: nobody shared
a frame with anybody. v2 gives the chain its geography:
  - an establishing three-shot, and an insert of what her eyes are on (his hand on the roll);
  - the pearl is held between finger and thumb (sofia_ob "pinch");
  - Don is IN her frame when he sees it, and when she catches him; his stain is below the frame line;
  - the thumb on the button is the Client's, large, with oil on it; then his face;
  - the last frame has Don in it again: who noticed.
Drawn with the sheets' own modules. Don's brows in frames 7 and 16 are a storyboard note.
Writes ob_chain_v2.png (with captions), ob_chain_v2_mute.png (numbers only), and with a third argument a folder of
contact sheets for the cold mute test."""
import os
import sys
import math
import cairo
import kit
import brand
import sofia_ob as so
import client_ob as co
import don_v4 as dv
import pam_bc as pb
from kit import Ctx, INK, cut, rect, ellipse
from charsheets import corp, wrap
import ob_sofia_sheet as sh

V = "v2"
FW, FH, GAP, COLS = 172, 306, 8, 7
WIDE = FW * 2 + GAP
GREY = (0.35, 0.40, 0.50)
FLOOR = (0.72, 0.63, 0.50)
EYES = (0, so.HY + 12)
BUST = (0, so.HY + 22)
A = sh.at


def don(k, x, head_y, s, look, knows=False):
    o = dv.don(k, x, head_y + 302 * s, s, "stand", "neutral", look=look)
    if knows:                                              # a storyboard note: the brows come down in the middle
        c = k.c
        hx, hy = o["head"]
        c.set_source_rgb(*INK); c.set_line_width(5 * s); c.set_line_cap(1)
        c.move_to(hx - 44 * s, hy - 30 * s); c.line_to(hx - 12 * s, hy - 18 * s); c.stroke()
        c.move_to(hx + 44 * s, hy - 30 * s); c.line_to(hx + 12 * s, hy - 18 * s); c.stroke()


def his_hand(c, k, x, y, s):
    """What her eyes are on: his hand round the blue roll. Big, oil in the creases, no ring."""
    J = co.LOOKS["B"]["jacket"]
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-0.30)
    co.blueprint_roll(k, 0, 0, 0.0, 250, 17, 71)
    cut(k, [(-34, 96), (34, 96), (30, 30), (-30, 30)], J, lw=2.4)                       # the sleeve
    cut(k, [(-30, 34), (30, 34), (30, 20), (-30, 20)], co.SHIRT, shadow=False, lw=2)     # the shirt cuff
    cut(k, [(-28, 22), (28, 22), (30, -6), (-30, -6)], co.SKIN, shadow=False, lw=2.2)    # the back of the hand
    for i, fx in enumerate((-30, -15, 0, 15)):                                          # four fingers over the roll
        cut(k, [(fx, -4), (fx + 14, -4), (fx + 14, -30), (fx, -30)], co.SKIN, shadow=False, lw=2)
        c.set_source_rgba(*co.OIL, 0.75); c.set_line_width(1.6); c.set_line_cap(1)
        c.move_to(fx + 3, -12); c.line_to(fx + 11, -12); c.stroke()
        c.move_to(fx + 3, -19); c.line_to(fx + 11, -19); c.stroke()
    ellipse(k, 31, 4, 9, 15, co.SKIN, 75, shadow=False, lw=2)                           # the thumb
    c.restore()


def his_thumb(c, k, x, y, ang, s):
    """The Client's thumb, coming in from screen left: broad, a short nail, oil in the creases."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-150, -30), (-20, -27), (8, -22), (22, -8), (22, 8), (8, 22), (-20, 27), (-150, 30)], co.SKIN, lw=2.6)
    cut(k, [(-8, -17), (10, -13), (16, 0), (10, 12), (-8, 15)], (0.93, 0.80, 0.70), shadow=False, lw=1.6)
    c.set_source_rgba(*co.OIL, 0.8); c.set_line_width(2.2); c.set_line_cap(1)
    for dx in (-46, -40, -72):
        c.move_to(dx, -22); c.curve_to(dx + 5, -8, dx + 5, 8, dx, 22); c.stroke()
    c.restore()


def frames(k, c):
    def establish(x0, y0, w, h):
        F = y0 + h - 22
        c.set_source_rgb(*FLOOR); c.rectangle(x0, F - 6, w, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1.4); c.move_to(x0, F - 6); c.line_to(x0 + w, F - 6); c.stroke()
        co.client(k, x0 + 92, F, 0.56, "arrive", "confident", look=(0.8, 0.0))
        so.sofia(k, x0 + 214, F, 0.56, "hold", "smile", look=(-0.8, -0.2))
        dv.don(k, x0 + 306, F, 0.56, "stand", "neutral", look=(-1, 0))

    def pair(pose, face, look, dlook, knows):
        def fn(x0, y0, w, h):
            cy = y0 + h / 2
            A(k, x0 + 112, cy - 6, 1.5, BUST, pose, face, look=look)
            don(k, x0 + 290, cy + 34, 0.98, dlook, knows)
        return fn

    def pam(x0, y0, w, h):
        cx, cy = x0 + w / 2, y0 + h / 2
        pb.pam(k, cx, cy + 300, 1.15, "stand", "neutral", look=(-0.6, 0.4))
        so.tablet(k, cx - 2, cy + 96, -0.06, "form", 3)
        skin = getattr(pb, "SKIN", so.SKIN)
        for sx in (-1, 1):                                 # her hands on it
            ellipse(k, cx - 2 + sx * 25, cy + 108, 9, 11, skin, 90 + sx, shadow=False, lw=2)

    def press(done):
        def fn(x0, y0, w, h):
            cx, cy = x0 + w / 2, y0 + h / 2
            sh.device_insert(c, k, cx + 6, cy - 6, 0.95, done=done)
            if done:
                his_thumb(c, k, x0 + 30, cy + 78, -0.5, 0.78)
            else:
                his_thumb(c, k, cx - 8, cy + 30, -0.42, 0.78)
        return fn
    one = lambda fn: (lambda x0, y0, w, h: fn(x0 + w / 2, y0 + h / 2))
    return [
        (2, "03", "Who is where. She is looking at the visitor; Don is looking at her.", "", establish),
        (1, "03", "Her eyes go down him.", "", one(lambda x, y: A(k, x, y - 8, 2.3, EYES, "low", "appraise", look=(-0.8, 1.0)))),
        (1, "03", "What she is reading: his hand. No ring.", "CLIENT: \"I live alone.\"",
         lambda x0, y0, w, h: his_hand(c, k, x0 + w / 2 - 6, y0 + h / 2 + 16, 1.25)),
        (1, "03", "Her eyes come back up, and her face answers.", "", one(lambda x, y: A(k, x, y - 8, 2.3, EYES, "low", "interested",
                                                                                     look=(-0.9, -0.2)))),
        (1, "03", "One pearl, held.", "SOFÍA: \"Oh...\"", one(lambda x, y: A(k, x, y + 12, 2.2, (8, so.BODY_TOP + 10), "pinch", "oh",
                                                                           look=(-0.9, -0.2)))),
        (2, "03", "Don sees the pearl.", "", pair("pinch", "oh", (-0.9, -0.2), (-1, 0.1), False)),
        (2, "03", "She catches him seeing it, and looks straight back. He knows.", "",
         pair("pinch", "sideeye", (1.0, 0.1), (-1, -0.1), True)),
        (1, "03", "Professional again, a moment too late.", "", one(lambda x, y: A(k, x, y - 4, 1.7, BUST, "low", "recover",
                                                                                 look=(-0.8, -0.1)))),
        (1, "03", "The visitor saw none of it.", "CLIENT: \"Can it find this when I lose it?\"",
         lambda x0, y0, w, h: co.client(k, x0 + w / 2 + 24, y0 + h / 2 - 20 - (co.HY + 10) * 0.74, 0.74, "arrive", "confident",
                                        look=(0.7, 0.0))),
        (1, "06", "Pam has the form done.", "", pam),
        (1, "06", "Sofía takes it. Her clipboard goes under her arm.", "SOFÍA: \"Tap here.\"",
         lambda x0, y0, w, h: so.sofia(k, x0 + w / 2 + 26, y0 + h / 2 + 150, 0.86, "show", "recover", look=(-0.9, -0.15), lean=2)),
        (1, "06", "One button. His thumb.", "", press(False)),
        (1, "06", "A tick, and his thumbprint in oil.", "", press(True)),
        (1, "06", "He is pleased with a result.", "CLIENT: \"That worked.\"",
         lambda x0, y0, w, h: co.client(k, x0 + w / 2 + 4, y0 + h / 2 - 10 - (co.HY + 10) * 1.05, 1.05, "open", "warm", look=(0.6, 0.0))),
        (1, "06", "Her smile turns real. Half a second.", "", one(lambda x, y: A(k, x, y - 4, 1.7, BUST, "low", "real", look=(-0.6, 0.0)))),
        (2, "06", "She presses it back, and checks who noticed. Don did.", "SOFÍA: \"Everything you need is in there.\"",
         pair("low", "tiny", (1.0, 0.0), (-1, -0.1), True)),
    ]


def layout(fr, top, cap):
    out, col, row = [], 0, 0
    for span, *_ in fr:
        if col + span > COLS:
            col, row = 0, row + 1
        out.append((40 + col * (FW + GAP), top + row * (FH + cap), FW if span == 1 else WIDE))
        col += span
    return out, row + 1


def main(out, mute=False):
    surf0 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 8, 8)
    fr = frames(None, None)
    cap = 26 if mute else 88
    top = 30 if mute else 86
    pos, rows = layout(fr, top, cap)
    W = 40 + COLS * FW + (COLS - 1) * GAP + 40
    H = top + rows * (FH + cap) + (0 if mute else 56)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * 2, H * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    if not mute:
        brand.mark(c, 40, 20, 34, zzz=False)
        corp(c, "THE ONBOARDING", 84, 44, 28, bold=True)
        corp(c, "the reaction chain  ·  beats 03 and 06  ·  storyboard " + V, 346, 44, 13, col=GREY)
        c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(40, 64); c.line_to(W - 40, 64); c.stroke()
    for i, ((span, beat, what, line, fn), (x0, y0, w)) in enumerate(zip(frames(k, c), pos)):
        c.save(); c.rectangle(x0, y0, w, FH); c.clip()
        c.set_source_rgb(*kit.WALL); c.rectangle(x0, y0, w, FH); c.fill()
        fn(x0, y0, w, FH)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(x0, y0, w, FH); c.stroke()
        corp(c, "%d" % (i + 1), x0, y0 + FH + 15, 10.5, bold=True)
        if not mute:
            corp(c, "beat " + beat, x0 + 22, y0 + FH + 15, 8.6, col=GREY)
            yy = wrap(c, what, x0, y0 + FH + 30, 9.6, w - 4)
            if line:
                wrap(c, line, x0, yy + 15, 9.0, w - 4, col=GREY)
    if not mute:
        wrap(c, "v1 was all singles and failed the cold mute test. Here every reaction shares a frame with its cause: "
             "her eyes and his hand, the pearl and Don, the button and his thumb, her smile and who saw it.", 40, H - 40, 10,
             W - 80, col=GREY)
    surf.write_to_png(out)
    return [(x0 * 2, y0 * 2, w * 2) for x0, y0, w in pos]


def sheets(src, pos, folder):
    """Contact sheets for the cold mute test: the numbered frames only, four columns' worth to a sheet, and one small."""
    from PIL import Image
    os.makedirs(folder, exist_ok=True)
    im = Image.open(src).convert("RGB")
    tiles = [im.crop((x - 6, y - 6, x + w + 6, y + FH * 2 + 44)) for x, y, w in pos]
    groups, cur, width = [], [], 0
    for i, t in enumerate(tiles):
        if width + t.width > 1500 and cur:
            groups.append(cur); cur, width = [], 0
        cur.append(i); width += t.width + 10
    groups.append(cur)
    bg = (247, 245, 237)
    for n, g in enumerate(groups):
        s = Image.new("RGB", (sum(tiles[i].width + 10 for i in g) + 10, tiles[0].height + 20), bg)
        x = 10
        for i in g:
            s.paste(tiles[i], (x, 10)); x += tiles[i].width + 10
        s.save("%s/sheet_%d_frames_%02d-%02d.png" % (folder, n + 1, g[0] + 1, g[-1] + 1))
    small = im.resize((int(im.width * 270 / 344.0), int(im.height * 270 / 344.0)))
    small.save("%s/sheet_%d_all_frames_small.png" % (folder, len(groups) + 1))
    return sorted(os.listdir(folder))


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_chain_%s.png" % (d, V))
    pos = main("%s/ob_chain_%s_mute.png" % (d, V), mute=True)
    if len(sys.argv) > 2:
        print(sheets("%s/ob_chain_%s_mute.png" % (d, V), pos, sys.argv[2]))
    print("wrote", d)
