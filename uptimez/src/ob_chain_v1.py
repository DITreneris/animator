"""v1, pinned. THE ONBOARDING: the reaction chain, a storyboard strip (v1). Beats 03 and 06 of concept v9 as fourteen frames, in
the order the second performance audit asked for: her action, Don's reaction, her recovery, and what it costs.
Drawn with the sheets' own modules, so a frame here is what the film will draw. Don's face in frame 7 is a
storyboard note (two brows over his sheet face); his own sheet comes later.
Writes ob_chain_v1.png (with captions) and ob_chain_v1_mute.png (numbers only: for the cold mute test)."""
import sys
import cairo
import kit
import brand
import sofia_ob as so
import client_ob as co
import don_v4 as dv
import pam_bc as pb
from kit import Ctx, INK
from charsheets import corp, wrap
import ob_sofia_sheet as sh

V = "v1"
FW, FH, GAP, COLS = 172, 306, 8, 7
GREY = (0.35, 0.40, 0.50)
DOWN, UP = (-0.8, 1.0), (-0.8, -0.2)
EYES = (0, so.HY + 12)
BUST = (0, so.HY + 22)


def don(k, cx, cy, look, knows=False):
    o = dv.don(k, cx, cy + 300, 1.25, "stand", "neutral", look=look)
    if knows:                                              # a storyboard note: the brows come down in the middle
        c = k.c
        hx, hy = o["head"]
        c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(1)
        c.move_to(hx - 44, hy - 30); c.line_to(hx - 12, hy - 18); c.stroke()
        c.move_to(hx + 44, hy - 30); c.line_to(hx + 12, hy - 18); c.stroke()


def frames(k, c):
    A = sh.at
    return [
        ("03", "She reads him.", "", lambda x, y: A(k, x, y - 8, 2.3, EYES, "low", "appraise", look=DOWN)),
        ("03", "She likes what she read.", "", lambda x, y: A(k, x, y - 8, 2.3, EYES, "low", "interested", look=(-0.9, -0.2))),
        ("03", "One pearl.", "SOFÍA: \"Oh...\"", lambda x, y: A(k, x, y + 10, 2.2, (6, so.BODY_TOP + 12), "necklace", "oh",
                                                             look=(-0.9, -0.2))),
        ("03", "Don sees the pearl.", "", lambda x, y: don(k, x, y, (-1, 0.5))),
        ("03", "She catches him seeing it.", "", lambda x, y: A(k, x, y - 4, 1.7, BUST, "necklace", "sideeye", look=(1.0, 0.1))),
        ("03", "Professional again, a moment too late.", "", lambda x, y: A(k, x, y - 4, 1.7, BUST, "low", "recover",
                                                                          look=(-0.8, -0.1))),
        ("03", "He knows.", "", lambda x, y: don(k, x, y, (-1, 0.0), knows=True)),
        ("03", "The Client saw none of it.", "CLIENT: \"Can it find this when I lose it?\"",
         lambda x, y: co.client(k, x + 24, y - 20 - (co.HY + 10) * 0.74, 0.74, "arrive", "confident", look=(0.7, 0.0))),
        ("06", "Pam has the form done.", "", lambda x, y: (pb.pam(k, x, y + 300, 1.15, "stand", "neutral", look=(-0.6, 0.4)),
                                                           so.tablet(k, x - 2, y + 96, -0.06, "form", 3))),
        ("06", "Sofía takes it. Her clipboard goes under her arm.", "SOFÍA: \"Tap here.\"",
         lambda x, y: so.sofia(k, x + 26, y + 150, 0.86, "show", "recover", look=(-0.9, -0.15), lean=2)),
        ("06", "One button.", "", lambda x, y: sh.device_insert(c, k, x - 8, y - 6, 0.95)),
        ("06", "One tap. His thumb, in oil.", "CLIENT: \"That worked.\"", lambda x, y: sh.device_insert(c, k, x - 8, y - 6, 0.95,
                                                                                                    done=True)),
        ("06", "Her smile turns real. Half a second.", "", lambda x, y: A(k, x, y - 4, 1.7, BUST, "low", "real", look=(-0.6, 0.0))),
        ("06", "She presses it back, and checks who noticed.", "SOFÍA: \"Everything you need is in there.\"",
         lambda x, y: A(k, x, y - 4, 1.7, BUST, "low", "tiny", look=(1.0, 0.0))),
    ]


def main(out, mute=False):
    rows = 2
    W = 40 + COLS * FW + (COLS - 1) * GAP + 40
    cap = 26 if mute else 88
    H = 86 + rows * (FH + cap) + (0 if mute else 56)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * 2, H * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    if not mute:
        brand.mark(c, 40, 20, 34, zzz=False)
        corp(c, "THE ONBOARDING", 84, 44, 28, bold=True)
        corp(c, "the reaction chain  ·  beats 03 and 06  ·  storyboard " + V, 346, 44, 13, col=GREY)
        c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(40, 64); c.line_to(W - 40, 64); c.stroke()
    for i, (beat, what, line, fn) in enumerate(frames(k, c)):
        x0 = 40 + (i % COLS) * (FW + GAP)
        y0 = (86 if not mute else 30) + (i // COLS) * (FH + cap)
        c.save(); c.rectangle(x0, y0, FW, FH); c.clip()
        c.set_source_rgb(*kit.WALL); c.rectangle(x0, y0, FW, FH); c.fill()
        fn(x0 + FW / 2, y0 + FH / 2)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(x0, y0, FW, FH); c.stroke()
        corp(c, "%d" % (i + 1), x0, y0 + FH + 15, 10.5, bold=True)
        if not mute:
            corp(c, "beat " + beat, x0 + 18, y0 + FH + 15, 8.6, col=GREY)
            yy = wrap(c, what, x0, y0 + FH + 30, 9.6, FW - 4)
            if line:
                wrap(c, line, x0, yy + 15, 9.0, FW - 4, col=GREY)
    if not mute:
        wrap(c, "The order is the point: we see what she does before we see Don see it, and we see her notice him before "
             "she covers it. She hides the feeling, not her calm. After frame 2 she never returns to the plain smile.",
             40, H - 40, 10, W - 80, col=GREY)
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_chain_%s.png" % (d, V))
    main("%s/ob_chain_%s_mute.png" % (d, V), mute=True)
    print("wrote", d)
