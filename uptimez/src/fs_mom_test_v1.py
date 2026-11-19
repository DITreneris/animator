"""(pinned: switch test v1) MOM, "First Search": the 8-second switch test (the design audit's), as five stills for two cold viewers, before
she goes into storyboard v9. No dialogue. Candy for Pam (Tomas's pick: candy is Pam's only).
0-2 s  Mom holds the candy out to Pam, a huge sugary smile; Pam takes one.
2-3 s  Pam turns back to her screen: Mom's smile is gone at once.
3-5 s  Sofía comes in: Mom straightens, fists on her hips, chin up, the glare over the frames.
5-7 s  Sofía freezes: Mom slowly points at the overflowing shredder.
7-8 s  Pam turns back: the sugar again, the candy out. Behind, Sofía empties the shredder.
python3 fs_mom_test.py [out_dir] -> fs_mom_test_v1/ (frames), fs_mom_test_v1.png (sheet), fs_mom_test_v1_270.png"""
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
CAM = (288, 650, 1.85)
MX, PX = 372, 300


def frame(k, t):
    def back(k):
        px, pf, ps = sb.P["pam"]
        if t in (1, 5):
            pb.pam(k, PX, pf, ps, "stand", "happy", look=(1, 0.2))
        else:
            ac.pam(k, PX, pf, ps, "typing")

    def ex(k, o):
        if t in (4, 5):
            ac.shredder(k, 246, F, 0.9, fill=1.0)
        if t == 1:
            mf.mom(k, MX, F + 16, 0.66, "offer", "sweet", lean=-4, tilt=-12, candy_dish=True)
        elif t == 2:
            mf.mom(k, MX, F + 16, 0.66, "bag", "unimpressed", look=(-1, 0.3), tilt=0)
        elif t == 3:
            mf.mom(k, MX, F + 16, 0.66, "fists", "glare", look=(-1, 0.6), chin=True)
        elif t == 4:
            mf.mom(k, MX, F + 16, 0.66, "thread", "glare", look=(-1, 0.6), chin=True, bag=False)
        else:
            mf.mom(k, MX, F + 16, 0.66, "offer", "sweet", lean=-4, tilt=-12, candy_dish=True)
    sf = False
    if t == 3:
        sf = dict(x=180, face="charm", pose="stand", look=(1, 0))
    elif t == 4:
        sf = dict(x=180, face="freeze", pose="freeze", look=(1, 0))
    elif t == 5:
        sf = dict(x=180, face="resigned", pose="stand", look=(1, 0.5))
    sb.scene(k, cam=CAM, cl=False, dn=False, rb=False, mm=False, pm=False, back=back, sf=sf, extra=ex, counter_plan=False)


def main(d):
    fs.LAYOUT[0] = "v2"; fs.REMOTE_BIG[0] = True; fs.BABY_DON[0] = True
    out = os.path.join(d, "fs_mom_test_v1")
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
    for w, name in ((540, "fs_mom_test_v1.png"), (270, "fs_mom_test_v1_270.png")):
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
