"""FIRST SEARCH (episode 10): the set sheet v2 (fs_set_sheet_v1.py = v1, kept), after the audit of v1 (18 Nov):
the tighter master and the larger screen (fs_set LAYOUT v2), frame 0 and the hook at phone size, the red-to-green
sweep in four drawings, one phone template, the portrait, the background props, and which action uses each prop.
Writes fs_set_v2.png at 2400 x 1860."""
import sys
import cairo
import kit
import brand
import set_ob as st
import fs_set as fs
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v2"
W2, H2 = 1200, 930
GREY = (0.35, 0.40, 0.50)


def frame(state):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s); k = Ctx(c, 0)
    c.save(); fs.cam2(c); fs.master(k, state); c.restore()
    return s


def put(c, surf, x, y, sc, w=540, h=960):
    c.save(); c.translate(x, y); c.scale(sc, sc); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w * sc, h * sc); c.stroke()


def panel(c, x, y, w, h, draw, bg=None):
    c.set_source_rgb(*(bg or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
    c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def main(out):
    fs.LAYOUT[0] = "v2"
    try:
        _main(out)
    finally:
        fs.LAYOUT[0] = "v1"


def _main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "FIRST SEARCH", 68, 44, 28, bold=True)
    corp(c, "episode 10  ·  the set: one master, inserts for information, faces for the comedy", 290, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · SET SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    f0, fr = frame("query"), frame("red")
    put(c, f0, 24, 84, 0.55)
    y = 84 + 960 * 0.55 + 14
    corp(c, "FRAME 0 = THE LAST FRAME  ·  the master, zoom 1.25", 24, y, 11, bold=True)
    wrap(c, "Three things lead: the screen over the door, the portrait right above Don's head, Don. The Client in the "
         "doorway, Sofía at Don's side, the robot with its remote. Pam and Mom are background at the counter.",
         24, y + 15, 9.4, 540 * 0.55 - 4, col=GREY)
    x1 = 24 + 540 * 0.55 + 16
    put(c, f0, x1, 84, 0.5)                                                   # 270 px wide: frame 0
    corp(c, "AT 270 PX  ·  frame 0", x1, 84 + 480 + 14, 11, bold=True)
    put(c, fr, x1, 84 + 480 + 30, 0.25)                                       # and the hook, at 0.7 s, half again
    wrap(c, "0.7 s, the hook, at 270 (shown at half). \"0 RESULTS\" is 15 px high, the red fills the screen, and "
         "the portrait hangs over Don: the joke reads before it falls.", x1 + 135 + 10, 84 + 480 + 34, 9.4, 270 - 145, col=GREY)
    px0 = x1 + 270 + 18
    pw = W2 - 24 - px0
    # the sweep
    sw_h = 112
    panel(c, px0, 84, pw, sw_h, lambda: [fs.screen(k, "wipe%.2f" % p_, px0 + 10 + i * (pw - 20) / 4.0, 84 + 22,
                                                   (pw - 20) / 4.0 - 10, ((pw - 20) / 4.0 - 10) * 0.62, cursor=False)
                                         for i, p_ in enumerate((0.0, 0.35, 0.7, 1.0))])
    corp(c, "4.5  ·  RED TO GREEN: the colour sweeps, the 0 never changes; the paddle snaps up green on the last drawing", px0, 84 + sw_h + 13, 9.4, bold=True)
    # the phones
    y2 = 84 + sw_h + 30
    ph = 200
    panel(c, px0, y2, pw, ph, lambda: [fs.phone2(k, px0 + 60 + i * (pw - 40) / 4.0, y2 + ph / 2, 1.0, kd)
                                       for i, kd in enumerate(("bank", "paid", "post", "complete"))], bg=(0.93, 0.92, 0.89))
    corp(c, "ONE PHONE  ·  1.3 FRI · BANK  ·  3.2 PREMIUM · PAID  ·  4.7 the post  ·  8.1 100% COMPLETE", px0, y2 + ph + 13, 9.4, bold=True)
    corp(c, "the same frame every time, at most four lines, no letter under 9 px; the post is DON TAGGED YOU, the photo, the caption, Pam", px0, y2 + ph + 26, 8.2, col=GREY)
    # portrait and background props
    y3 = y2 + ph + 44
    cw = (pw - 24) / 3.0
    cells = [
        ("THE PORTRAIT", "plastered (frame 0)  ·  cracked after the bonk", lambda x, yy: (
            fs.portrait(k, x + cw * 0.27, yy + 60, 0.72), fs.portrait(k, x + cw * 0.73, yy + 60, 0.72, patch=False))),
        ("BACKGROUND: PAM'S PLAN", "read once, held up in 7.1-7.2", lambda x, yy: fs.plan_taped(k, x + cw / 2, yy + 70, 0.9)),
        ("BACKGROUND: MOM'S PLACE", "read once, in her close-up 6.1", lambda x, yy: (
            c.save(), c.translate(x + cw / 2 - 30, yy + 100), c.scale(1.5, 1.5), fs.counter_plate(k, 0, 0), c.restore())),
    ]
    for i, (lab, note, fn) in enumerate(cells):
        x = px0 + i * (cw + 12)
        panel(c, x, y3, cw, 150, lambda x=x, fn=fn: fn(x, y3))
        corp(c, lab, x, y3 + 150 + 13, 9.4, bold=True)
        corp(c, note, x, y3 + 150 + 26, 8.0, col=GREY)
    # what each prop does
    y4 = y3 + 150 + 44
    rows = [("The portrait", "1.1 falls on Don · 3.1 swings, he ducks · 3.4 Sofía's plaster · 5.2 over the Client as he towers"),
            ("The screen", "1.1 red, the buzz · 3.1 red again · 4.5 the sweep to green · 8.2 RETRY UNTIL FRIDAY, the loop"),
            ("The phone", "1.3 the deadline · 3.2 he paid · 4.7 Pam's comment, his face drops · 8.1 COMPLETE stops him"),
            ("Sofía's tablet", "2.2 the sale, thumb 1 · 3.1 handed back blind · 5.3 slid behind her back"),
            ("Pam's plan", "4.4 thumb 3, the tape · 7.1-7.2 the near-shred, pulled back"),
            ("Mom's place", "6.1 ASSISTANT TO DON and baby Don: who she is, before \"Young man.\"")]
    corp(c, "EVERY PROP HAS ITS ACTION", px0, y4, 10, bold=True)
    for i, (a, b) in enumerate(rows):
        corp(c, a, px0, y4 + 18 + i * 15, 9.0, bold=True)
        corp(c, b, px0 + 96, y4 + 18 + i * 15, 9.0, col=GREY)
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    main("%s/fs_set_%s.png" % (d, V))
    print("wrote", d)
