"""SOFÍA, "First Search" (episode 10): the acting sheet v2 (sofia_fs v2), after the audit of look sheet v1 (kept,
sofia_fs_sheet.py): the costume was approved; this sheet is the acting. Eight faces of her own and the freeze, each tied
to a moment of the script and shown again at phone size; five actions as three-drawing sequences; the three shot sizes
at 270 px; the rules every shot keeps. Writes fs_sofia_v2.png at 2400 x 1860."""
import sys
import cairo
import kit
import brand
import set_ob as st
import fs_set as fs
import sofia_fs as sfs
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v2"
W2, H2 = 1200, 930
GREY = (0.35, 0.40, 0.50)


def clip(c, x, y, w, h, draw, bg=None):
    c.set_source_rgb(*(bg or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
    c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def head(k, cx, cy, s, face, look=(-0.4, 0), lag=(0, 0)):
    """Her head with its centre at (cx, cy)."""
    hy = sfs.HY * s
    sfs.sofia(k, cx, cy - hy, s, "stand", face, look=look, lag=lag)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "First Search (episode 10)  ·  the acting: what she thinks, on mute", 168, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · ACTING SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # ---- the faces, and the same at phone size
    faces = (("charm", "to the Client", "1.3, 5.1"), ("fake", "the customer smile", "2.2"),
             ("drop", "the smile goes", "5.1"), ("better", "after the plaster", "3.4"),
             ("deadpan", "to camera, once", "optional"), ("sideeye", "\"not me\"", "5.3"),
             ("contempt", "\"We fixed the red.\"", "5.3"), ("resigned", "Mom rescues him", "6.2"),
             ("freeze", "the action, below", "—"))
    fw = (W2 - 48) / 9.0
    y1 = 82
    for i, (f_, note, shot) in enumerate(faces):
        x = 24 + i * fw
        clip(c, x, y1, fw - 6, 112, lambda x=x, f_=f_: head(k, x + (fw - 6) / 2 - 6, y1 + 52, 1.08, f_))
        corp(c, f_.upper(), x, y1 + 112 + 12, 9.6, bold=True)
        corp(c, note, x, y1 + 112 + 24, 8.0, col=GREY)
        corp(c, ("shot " + shot) if shot[0].isdigit() else shot, x, y1 + 112 + 35, 7.6, col=GREY)
    y1b = y1 + 112 + 44
    strip = cairo.ImageSurface(cairo.FORMAT_ARGB32, int((W2 - 48) * 2), 120)
    cc = cairo.Context(strip); cc.set_source_rgb(*kit.WALL); cc.paint(); kk = Ctx(cc, 0)
    for i, (f_, _, _) in enumerate(faces):
        head(kk, (i + 0.5) * fw * 2 - 10, 62, 1.30, f_)
    c.save(); c.translate(24, y1b); c.scale(0.25, 0.25)                    # a quarter: what 270 px gives a close-up
    c.set_source_surface(strip, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.0); c.rectangle(24, y1b, (W2 - 48) * 0.5, 30); c.stroke()
    corp(c, "THE SAME NINE AT A QUARTER: a close-up on a phone. The eyes and brows carry each one, not only the lips.",
         24 + (W2 - 48) * 0.5 + 12, y1b + 19, 9.4, bold=True)

    # ---- the actions: three drawings each
    y2 = y1b + 44
    aw = (W2 - 48) / 3.0
    acts = [
        ("THE PATCH  ·  3.4", "pinches the plaster, presses it on his face, smooths it: better", [
            dict(pose="pinch", face="charm", plaster=True), dict(pose="press", face="charm"), dict(pose="press", face="better")], True),
        ("\"NOT ME\"  ·  5.3", "the tablet slides from her chest to behind her back", [
            dict(pose="hold", face="drop"), dict(pose="stand", face="sideeye", slide=0.5), dict(pose="behind", face="sideeye")], False),
        ("THE GLANCE AT DON  ·  once", "her head turns, the ponytail and earrings lag, then settle", [
            dict(pose="hold", face="charm", look=(-0.6, 0), lag=(0, 0)), dict(pose="hold", face="charm", look=(0.8, 0), lag=(-9, 0)),
            dict(pose="hold", face="deadpan", look=(0, 0), lag=(4, 0))], False),
    ]
    acts2 = [
        ("THE POLITE LEAN  ·  to the Client", "hands clasp, she leans in a little too far", [
            dict(pose="stand", face="charm"), dict(pose="clasp", face="charm", lean=-6), dict(pose="clasp", face="fake", lean=-11)], False),
        ("THE FREEZE  ·  after Don's line", "everything stops but the earrings and the ponytail", [
            dict(pose="hold", face="fake"), dict(pose="freeze", face="freeze", lag=(9, 0)), dict(pose="freeze", face="freeze", lag=(-6, 0))], False),
    ]

    def act_cell(x, y, w, h, frames, glass):
        for j, f in enumerate(frames):
            fx = x + 40 + j * (w - 60) / 3.0 + 10
            if glass and f["pose"] in ("press",):                              # the portrait's corner, where she presses
                c.save(); c.translate(fx + 62, y + 52); c.rotate(fs.CROOK)
                kit.rect(k, -24, -30, 48, 60, (0.76, 0.60, 0.24), 3, lw=1.6)
                c.set_source_rgb(0.74, 0.84, 0.94); c.rectangle(-17, -23, 34, 46); c.fill()
                c.restore()
            sfs.sofia(k, fx, y + h - 6, 0.50, f["pose"], f["face"], look=f.get("look", (-0.4, 0)), lag=f.get("lag", (0, 0)),
                      lean=f.get("lean", 0.0), plaster=f.get("plaster"), slide=f.get("slide"))
            if glass and f["pose"] == "press":                                 # the plaster under her hand, on his face
                fs.plaster(c, fx + 62, y + 44, 0.55, ang=-0.12)
            if j < 2:
                c.set_source_rgb(*GREY); c.set_line_width(1.6)
                ax = fx + (w - 60) / 6.0 + 6
                c.move_to(ax - 6, y + h - 60); c.line_to(ax + 4, y + h - 60); c.stroke()
                c.move_to(ax + 1, y + h - 64); c.line_to(ax + 5, y + h - 60); c.line_to(ax + 1, y + h - 56); c.stroke()

    for i, (lab, note, frames, glass) in enumerate(acts):
        x = 24 + i * aw
        clip(c, x, y2, aw - 8, 176, lambda x=x, frames=frames, glass=glass: act_cell(x, y2, aw - 8, 176, frames, glass))
        corp(c, lab, x, y2 + 176 + 13, 9.6, bold=True)
        corp(c, note, x, y2 + 176 + 25, 8.0, col=GREY)
    y3 = y2 + 176 + 40
    for i, (lab, note, frames, glass) in enumerate(acts2):
        x = 24 + i * aw
        clip(c, x, y3, aw - 8, 176, lambda x=x, frames=frames, glass=glass: act_cell(x, y3, aw - 8, 176, frames, glass))
        corp(c, lab, x, y3 + 176 + 13, 9.6, bold=True)
        corp(c, note, x, y3 + 176 + 25, 8.0, col=GREY)

    # ---- the three shot sizes at 270 px
    x = 24 + 2 * aw
    fs.SOFIA_FS[0] = True
    try:
        f0 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        cc = cairo.Context(f0); kk = Ctx(cc, 0)
        cc.save(); st.cam(cc); fs.master(kk); cc.restore()
    finally:
        fs.SOFIA_FS[0] = False
    med = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    cc = cairo.Context(med); kk = Ctx(cc, 0)
    cc.set_source_rgb(*kit.WALL); cc.paint()
    sfs.sofia(kk, 270, 330 - sfs.HY * 2.4, 2.4, "hold", "charm", look=(-0.5, 0))
    clo = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    cc = cairo.Context(clo); kk = Ctx(cc, 0)
    cc.set_source_rgb(*kit.WALL); cc.paint()
    sfs.sofia(kk, 250, 470 - sfs.HY * 4.2, 4.2, "stand", "drop", look=(-0.3, 0))
    tw = (aw - 8 - 16) / 3.0
    for j, (sf_, lab) in enumerate(((clo, "CLOSE"), (med, "MEDIUM"), (f0, "WIDE"))):
        xx = x + 4 + j * (tw + 4)
        sc = tw / 540.0
        c.save(); c.translate(xx, y3); c.scale(sc, sc); c.set_source_surface(sf_, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.0); c.rectangle(xx, y3, tw, 960 * sc); c.stroke()
        corp(c, lab, xx, y3 + 960 * sc + 12, 8.6, bold=True)
    corp(c, "THE THREE SIZES  ·  at 270 px they read", x, y3 + 960 * (tw / 540.0) + 26, 8.0, col=GREY)

    # ---- the rules
    y4 = y3 + 960 * (tw / 540.0) + 50
    wrap(c, "RULES FOR EVERY SHOT  ·  The ponytail always falls to screen right. The earrings and the ponytail lag the "
         "head and settle after it; in the freeze they are the only thing still moving. The buckle is always centred. "
         "Long fuchsia sleeves with a darker cuff, the red nails always showing. No pearls in this film. Her comedy is "
         "restraint: no panic, no open disgust; the drop, the freeze and contempt are her cracks, and each is short. "
         "One look to camera (deadpan) per episode at most.", 24, y4, 9.6, W2 - 48, col=INK)
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    main("%s/fs_sofia_%s.png" % (d, V))
    print("wrote", d)
