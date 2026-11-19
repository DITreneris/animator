"""FIRST SEARCH (episode 10): the set sheet v1. Frame 0 in the master wide (episode 9's camera), the same frame at
phone size (270 px), and the new things in their states: the wall screen, the portrait, Mom's place at the counter,
Pam's taped plan, the Client's phone (four screens), the UPGRADE card. Writes fs_set_v1.png at 2400 x 1860."""
import sys
import cairo
import kit
import brand
import set_ob as st
import fs_set as fs
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v1"
W2, H2 = 1200, 930
GREY = (0.35, 0.40, 0.50)


def staged(c, x, y, sc, draw):
    c.save(); c.translate(x, y); c.scale(sc, sc); c.rectangle(0, 0, st.W, st.H); c.clip()
    draw()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(x, y, st.W * sc, st.H * sc); c.stroke()


def panel(c, x, y, w, h, draw, bg=None):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*(bg or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
    draw(x, y, w, h)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def frame0_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s)
    k = Ctx(c, 0)
    c.save(); st.cam(c); fs.master(k); c.restore()
    return s


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "FIRST SEARCH", 68, 44, 28, bold=True)
    corp(c, "episode 10  ·  the set: episode 9's front desk, and what's new", 290, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · SET SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    SC = 0.60
    staged(c, 24, 84, SC, lambda: (st.cam(c), fs.master(k)))
    y = 84 + st.H * SC + 14
    corp(c, "FRAME 0 = THE LAST FRAME  ·  the master wide", 24, y, 11, bold=True)
    wrap(c, "Three things to read: the robot's remote and the screen over the door (\"blueprint\"), the portrait, "
         "crooked and plastered, right above Don's bald head, and Don. The Client stands in the open doorway. Pam and "
         "Mom stand behind the counter: Pam with the taped plan, Mom by ASSISTANT TO DON and the baby photo.",
         24, y + 15, 9.6, st.W * SC - 4, col=GREY)

    x1 = 24 + st.W * SC + 18                                                    # phone size
    f0 = frame0_surface()
    c.save(); c.translate(x1, 84); c.scale(0.5, 0.5); c.set_source_surface(f0, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x1, 84, 270, 480); c.stroke()
    corp(c, "AT PHONE SIZE  ·  270 px", x1, 84 + 480 + 14, 11, bold=True)
    wrap(c, "The test the cold viewers get. The screen, the portrait and Don read; the plaster reads as a plaster; "
         "ASSISTANT TO DON is small here, so its close-up (6.1) carries it.", x1, 84 + 480 + 29, 9.6, 268, col=GREY)

    px0 = x1 + 270 + 18
    pw, ph = (W2 - 24 - px0 - 12) / 2.0, 150
    cells = [
        ("THE WALL SCREEN", "the query  ·  red  ·  green  ·  RETRY UNTIL FRIDAY", lambda x, yy, w, h: [
            fs.screen(k, s_, x + 6 + i * (w - 12) / 4.0, yy + 34, (w - 12) / 4.0 - 6, ((w - 12) / 4.0 - 6) * 0.64,
                      cursor=(s_ == "query")) for i, s_ in enumerate(("query", "red", "green", "retry"))]),
        ("THE PORTRAIT", "frame 0, plastered  ·  the bonk shows the crack  ·  crooked 8°", lambda x, yy, w, h: (
            fs.portrait(k, x + w * 0.28, yy + 62, 0.80), fs.portrait(k, x + w * 0.72, yy + 62, 0.80, patch=False))),
        ("MOM'S PLACE", "6.1: the plate and the baby photo, at the counter's end", lambda x, yy, w, h: (
            fs.counter_plate(k, x + w / 2 - 10, yy + h / 2 + 26) if False else _mom_close(k, x, yy, w, h))),
        ("PAM'S PLAN", "taped back from the strips, bay 7 a gap (for episode 11)", lambda x, yy, w, h: fs.plan_taped(k, x + w / 2, yy + h / 2 + 8, 1.05)),
        ("THE PHONE  ·  1.3, 3.2", "FRI · BANK, then PREMIUM · PAID", lambda x, yy, w, h: (
            fs.phone(k, x + w * 0.30, yy + h / 2, 0.80, "bank"), fs.phone(k, x + w * 0.70, yy + h / 2, 0.80, "paid"))),
        ("THE PHONE  ·  4.7", "DON TAGGED YOU, and Pam's comment", lambda x, yy, w, h: fs.phone(k, x + w / 2, yy + h / 2, 0.86, "post")),
        ("THE PHONE  ·  8.1", "the report, in the doorway", lambda x, yy, w, h: fs.phone(k, x + w / 2, yy + h / 2, 0.80, "complete")),
        ("SOFÍA'S TABLET  ·  2.2", "UPGRADE, and his old thumbprint", lambda x, yy, w, h: fs.tablet_upgrade(k, x + w / 2, yy + h / 2, 0.95)),
    ]
    for i, (lab, note, fn) in enumerate(cells):
        x0 = px0 + (i % 2) * (pw + 12); y0 = 84 + (i // 2) * (ph + 40)
        panel(c, x0, y0, pw, ph, fn, bg=(0.93, 0.92, 0.89) if lab.startswith("THE PHONE") or lab.startswith("SOF") else None)
        corp(c, lab, x0, y0 + ph + 13, 9.6, bold=True)
        corp(c, note, x0, y0 + ph + 26, 8.2, col=GREY)
    yb = 84 + 4 * (ph + 40) + 4
    wrap(c, "Continuity: episode 9 ends with the portrait lower by the door, small, tilted 4° (Pam hung it). Here it "
         "hangs above Don's spot, larger, at 8°: he moved it over himself. The network post has no logo and no name.",
         px0, yb, 9.2, W2 - 24 - px0, col=GREY)
    surf.write_to_png(out)


def _mom_close(k, x, y, w, h):
    import mom_bc
    c = k.c
    c.save(); c.rectangle(x, y, w, h); c.clip()
    mom_bc.mom(k, x + w * 0.66, y + h + 64, 0.62, "bag", "sweet", look=(-0.8, 0))
    c.set_source_rgb(*st.DESK); c.rectangle(x, y + h - 40, w, 40); c.fill()
    c.set_source_rgb(*st.DESK_DARK); c.rectangle(x, y + h - 44, w, 6); c.fill()
    c.save(); c.translate(x + w * 0.40, y + h - 44); c.scale(1.6, 1.6)
    fs.counter_plate(k, -28, 0)
    c.restore()
    c.restore()


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    main("%s/fs_set_%s.png" % (d, V))
    print("wrote", d)
