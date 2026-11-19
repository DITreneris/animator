"""MOM, "First Search": the switch test v2 (fs_mom_test_v1.py = v1, kept), after its cold test (3/5 for both viewers,
the character read; beats 2 and 4 misread the same way). Fixes: Pam's monitor on the counter: she disappears behind it
(she isn't looking) and leans out of it to Mom (she is); the dish only drops, no prop swap, and the blank face is
harder; the shredder is there from the start; the point is an arm straight out with a finger; Sofía looks at the
shredder and then works it; Mom and Pam apart (the curler read as Pam's purple object); the candy dish bigger.
MOM, "First Search": the 8-second switch test (the design audit's), as five stills for two cold viewers, before
she goes into storyboard v9. No dialogue. Candy for Pam (Tomas's pick: candy is Pam's only).
0-2 s  Mom holds the candy out to Pam, a huge sugary smile; Pam takes one.
2-3 s  Pam turns back to her screen: Mom's smile is gone at once.
3-5 s  Sofía comes in: Mom straightens, fists on her hips, chin up, the glare over the frames.
5-7 s  Sofía freezes: Mom slowly points at the overflowing shredder.
7-8 s  Pam turns back: the sugar again, the candy out. Behind, Sofía empties the shredder.
python3 fs_mom_test.py [out_dir] -> fs_mom_test_v2/ (frames), fs_mom_test_v2.png (sheet), fs_mom_test_v2_270.png"""
import os
import sys
import cairo
import kit
import fs_set as fs
import fs_storyboard_v8 as sb                                 # pinned: the switch tests were drawn on board v8
import mom_fs as mf
import pam_bc as pb
import acts_ob as ac

F = sb.F
CAM = (300, 650, 1.6)
MX, PX, SX, SHX = 410, 250, 160, 206
kit.ARM_POSES["_bin"] = (-8, 0, 40, 30)                  # Sofía: a hand down on the shredder
BLUE = (0.30, 0.55, 0.85)


def monitor(k, x, y):
    """Pam's monitor on the counter: big enough to hide her face."""
    c = k.c
    kit.rect(k, x - 46, y - 74, 92, 64, (0.15, 0.16, 0.20), 501, lw=2.4)
    kit.rect(k, x - 40, y - 68, 80, 52, BLUE, 502, shadow=False, lw=1.4)
    c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(2)
    for i in range(4):
        c.move_to(x - 32, y - 58 + i * 11); c.line_to(x + 22 - (i % 2) * 14, y - 58 + i * 11); c.stroke()
    kit.rect(k, x - 8, y - 10, 16, 10, (0.15, 0.16, 0.20), 503, shadow=False, lw=1.6)
    kit.rect(k, x - 24, y, 48, 6, (0.15, 0.16, 0.20), 504, shadow=False, lw=1.6)


def frame(k, t):
    looking = t in (1, 5)

    def back(k):
        px, pf, ps = sb.P["pam"]
        if looking:                                        # she leans out from behind her monitor, to Mom
            pb.pam(k, PX + 52, pf, ps, "stand", "happy", look=(1, 0.2), lean=10)
        else:                                              # behind it: not looking
            pb.pam(k, PX, pf, ps, "stand", "neutral", look=(-1, 0.3))

    def pre(k):
        monitor(k, PX, sb.F - 176)

    def ex(k, o):
        ac.shredder(k, SHX, F, 0.9, fill=1.0)
        if t == 1:
            mf.mom(k, MX, F + 16, 0.66, "offer", "sweet", lean=-4, tilt=-12, candy_dish=True, candy_s=1.8)
        elif t == 2:
            mf.mom(k, MX, F + 16, 0.66, "low", "stern", look=(0, 0.4), tilt=0, candy_dish=True, candy_s=1.8)
        elif t == 3:
            mf.mom(k, MX, F + 16, 0.66, "fists", "glare", look=(-1, 0.6), chin=True)
        elif t == 4:
            mf.mom(k, MX, F + 16, 0.66, "point", "glare", look=(-1, 0.6), chin=True, finger=True)
        else:
            mf.mom(k, MX, F + 16, 0.66, "offer", "sweet", lean=-4, tilt=-12, candy_dish=True, candy_s=1.8)
    sf = False
    if t == 3:
        sf = dict(x=SX, face="charm", pose="stand", look=(1, 0))
    elif t == 4:
        sf = dict(x=SX, face="freeze", pose="freeze", look=(1, 0.8))
    elif t == 5:
        sf = dict(x=SX, face="resigned", pose="_bin", look=(1, 0.8))
    sb.scene(k, cam=CAM, cl=False, dn=False, rb=False, mm=False, pm=False, back=back, pre=pre, sf=sf, extra=ex,
             counter_plan=False)


def main(d):
    fs.LAYOUT[0] = "v2"; fs.REMOTE_BIG[0] = True; fs.BABY_DON[0] = True
    out = os.path.join(d, "fs_mom_test_v2")
    os.makedirs(out, exist_ok=True)
    paths = []
    try:
        for t in range(1, 6):
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
            c = cairo.Context(s); k = kit.Ctx(c, 0)
            sb.bg(c); frame(k, t)
            p = os.path.join(out, "%d.png" % t); s.write_to_png(p); paths.append(p)
    finally:
        fs.LAYOUT[0] = "v1"; fs.REMOTE_BIG[0] = False; fs.BABY_DON[0] = False
    for w, name in ((540, "fs_mom_test_v2.png"), (270, "fs_mom_test_v2_270.png")):
        sh = cairo.ImageSurface(cairo.FORMAT_ARGB32, w * 5 + 40, int(w * 16 / 9) + 20)
        c = cairo.Context(sh); c.set_source_rgb(1, 1, 1); c.paint()
        for i, p in enumerate(paths):
            im = cairo.ImageSurface.create_from_png(p)
            c.save(); c.translate(8 + i * (w + 8), 10); c.scale(w / 540.0, w / 540.0)
            c.set_source_surface(im, 0, 0); c.paint(); c.restore()
            c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(14 if w < 540 else 22)
            c.move_to(14 + i * (w + 8), 34 if w >= 540 else 26); c.show_text(str(i + 1))
        sh.write_to_png(os.path.join(d, name))
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
