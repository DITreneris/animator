"""SOFÍA, "First Search" (episode 10): her look sheet v1 (sofia_fs v1). The figure in the episode's poses, her faces,
the details (earrings swinging, belt, phone case, boots), episode 9's Sofía beside her, and the master wide at phone
size. Writes fs_sofia_v1.png at 2400 x 1860."""
import sys
import cairo
import kit
import brand
import set_ob as st
import fs_set as fs
import sofia_fs_v1 as sfs                                          # pinned: this sheet is v1
import sofia_ob as so
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v1"
W2, H2 = 1200, 930
GREY = (0.35, 0.40, 0.50)


def box(c, x, y, w, h, bg=None):
    c.set_source_rgb(*(bg or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def clip(c, x, y, w, h, draw, bg=None):
    box(c, x, y, w, h, bg)
    c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "First Search (episode 10)  ·  winter chic in fuchsia", 168, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · LOOK SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # the hero, large, with episode 9 beside her
    clip(c, 24, 84, 330, 560, lambda: (so.sofia(k, 92, 600, 0.95, "hold", "smile", look=(0.3, 0)),
                                        sfs.sofia(k, 236, 626, 1.55, "hold", "smile", look=(-0.3, 0), lag=(-3, 0), sparkle=1.0)))
    corp(c, "EPISODE 9  ·  EPISODE 10", 24, 84 + 560 + 14, 11, bold=True)
    wrap(c, "A wrap coat-dress in fuchsia with a soft roll collar, a wide black patent belt with a square gold buckle, "
         "knee-high boots, gold geometric drop earrings, the hair slicked back into a high ponytail with a gold cuff. "
         "No pearls in this film. Fuchsia stays clear of the episode's signals: the red and the green zero.",
         24, 84 + 560 + 29, 9.6, 326, col=GREY)

    # the poses
    x0 = 370
    clip(c, x0, 84, 806, 270, lambda: [sfs.sofia(k, x0 + 80 + i * 160, 84 + 262, 0.78, p_, f_, look=(-0.5, 0), lag=l_)
                                        for i, (p_, f_, l_) in enumerate((("stand", "smile", (0, 0)), ("hold", "knowing", (-5, 0)),
                                                                          ("phone", "tiny", (4, 1)), ("plaster", "smile", (0, 0)),
                                                                          ("behind", "unimpressed", (-3, 0))))])
    labels = (("stand", "frame 0"), ("hold", "her tablet, his old print"), ("phone", "the luxe case"),
              ("plaster", "3.4: the patch"), ("behind", "5.3: \"not me\""))
    for i, (a, b) in enumerate(labels):
        corp(c, a.upper(), x0 + 40 + i * 160, 84 + 270 + 13, 9.6, bold=True)
        corp(c, b, x0 + 40 + i * 160, 84 + 270 + 26, 8.2, col=GREY)

    # the faces
    y2 = 84 + 270 + 44
    faces = (("smile", "at the Client"), ("tiny", "the patch: better"), ("knowing", "the one glance"),
             ("neutral", "5.1: the smile drops"), ("unimpressed", "\"We fixed the red.\""), ("closed", "Mom rescues him"))
    fw = 806 / 6.0
    for i, (f_, note) in enumerate(faces):
        xx = x0 + i * fw
        clip(c, xx, y2, fw - 6, 150, lambda xx=xx, f_=f_: sfs.sofia(k, xx + (fw - 6) / 2 - 6, y2 + 440, 1.35, "stand", f_,
                                                                   look=(-0.4, 0), lag=(0, 0)))
        corp(c, f_.upper(), xx, y2 + 150 + 13, 9.4, bold=True)
        corp(c, note, xx, y2 + 150 + 26, 8.0, col=GREY)

    # the details
    y3 = y2 + 150 + 44
    dw = 806 / 4.0

    def earrings():
        for i, lg in enumerate((-6, 0, 6)):
            sfs.earring(k, x0 + 40 + i * 52, y3 + 40, lg * 1.0, 1.0 if i == 1 else 0.0, 50 + i)
            c.save(); c.translate(x0 + 40 + i * 52, y3 + 40); c.scale(1.8, 1.8); c.restore()

    def big_earrings():
        c.save(); c.translate(x0 + 18, y3 + 10); c.scale(1.9, 1.9)
        for i, lg in enumerate((-6, 0, 6)):
            sfs.earring(k, 14 + i * 32, 10, lg, 1.0 if i == 1 else 0.0, 50 + i)
        c.restore()

    def belt():
        c.save(); c.translate(x0 + dw + dw / 2 - 6, y3 + 70); c.scale(2.6, 2.6)
        kit.cut(k, [(-30, -20), (30, -20), (34, 20), (-34, 20)], sfs.FUCHSIA, shadow=False, lw=1.6)
        kit.rect(k, -30, -8, 60, 15, sfs.PATENT, 1, shadow=False, lw=1.4)
        kit.rect(k, -11, -12, 22, 23, kit.WALL if False else (0.80, 0.55, 0.12), 2, shadow=False, lw=1.4)
        kit.rect(k, -6, -7, 12, 13, sfs.PATENT, 3, shadow=False, lw=1.0)
        c.restore()

    def phone():
        c.save(); c.translate(x0 + 2 * dw + dw / 2 - 6, y3 + 70); c.scale(2.8, 2.8)
        kit.rect(k, -11, -20, 22, 40, sfs.ROSE_GOLD, 4, lw=1.4)
        kit.rect(k, -7.5, -16, 15, 32, sfs.CASE_PINK, 5, shadow=False, lw=1.0)
        c.set_source_rgb(*sfs.ROSE_GOLD); c.arc(0, 0, 4, 0, 6.3); c.fill()
        c.restore()

    def boots():
        c.save(); c.translate(x0 + 3 * dw + dw / 2 - 6, y3 + 136); c.scale(1.3, 1.3)
        sfs.sofia(k, 0, 0, 1.0, "stand", "smile", badge=False)
        c.restore()
    for i, (fn, lab, note) in enumerate(((big_earrings, "EARRINGS", "gold geometric drops; they swing"),
                                         (belt, "THE BELT", "black patent, a square gold buckle"),
                                         (phone, "THE PHONE", "rose gold, a pink inlay, no logo"),
                                         (boots, "THE BOOTS", "knee-high, a slim heel, a shine"))):
        xx = x0 + i * dw
        clip(c, xx, y3, dw - 6, 140, fn)
        corp(c, lab, xx, y3 + 140 + 13, 9.4, bold=True)
        corp(c, note, xx, y3 + 140 + 26, 8.0, col=GREY)

    # the ponytail and the phone-size check
    y4 = y3 + 140 + 44
    clip(c, x0, y4, 396, 130, lambda: [sfs.sofia(k, x0 + 70 + i * 130, y4 + 450, 1.25, "stand", "smile", look=(-0.3, 0),
                                                 lag=(lg, 0)) for i, lg in enumerate((-8, 0, 8))])
    corp(c, "THE PONYTAIL  ·  lag -8, 0, +8", x0, y4 + 130 + 13, 9.4, bold=True)
    corp(c, "it swings on every turn of her head", x0, y4 + 130 + 26, 8.0, col=GREY)
    fs.SOFIA_FS[0] = "sofia_fs_v1"
    try:
        f0 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        cc = cairo.Context(f0); kk = Ctx(cc, 0)
        cc.save(); st.cam(cc); fs.master(kk); cc.restore()
    finally:
        fs.SOFIA_FS[0] = False
    xx = x0 + 412
    c.save(); c.rectangle(xx, y4, 394, 130); c.clip()
    c.translate(xx + 197 - 200, y4 + 4 - 262); c.scale(0.5, 0.5); c.set_source_surface(f0, 0, 0); c.paint()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(xx, y4, 394, 130); c.stroke()
    corp(c, "AT PHONE SIZE  ·  in the master wide, 270 px", xx, y4 + 130 + 13, 9.4, bold=True)
    corp(c, "fuchsia pops off the beige wall and Don's navy", xx, y4 + 130 + 26, 8.0, col=GREY)
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    main("%s/fs_sofia_%s.png" % (d, V))
    print("wrote", d)
