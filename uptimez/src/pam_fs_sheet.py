"""PAM, "First Search": look sheet v1 (pam_fs). Before (The Best Candidate: the chain, the brooch), this episode at
the start (no chain, no brooch), after Mom's candy (the sleeves shoved up, at work).
python3 pam_fs_sheet.py [out_dir] -> fs_pam_v1.png"""
import os
import sys
import cairo
import kit
import brand
import pam_bc as pb
import acts_ob as ac
import pam_fs as pf
from charsheets import corp, wrap


def main(d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 760)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.95, 0.93, 0.88); c.paint()
    corp(c, "PAM  ·  First Search  ·  look v1", 40, 62, 34, brand.NAVY, True)
    wrap(c, "One chain and one brooch in the room, and they are Mom's. Pam keeps her glasses; after Mom holds the candy "
            "out to her, she shoves her sleeves up and gets to work. As the robot retries, she tugs them down (the loop).",
         40, 102, 19, 1000)
    cols = [("BEFORE", "The Best Candidate: chain, brooch", None, ("stand", "happy")),
            ("START", "no chain, no brooch", False, ("stand", "happy")),
            ("AFTER THE CANDY", "sleeves up: she works", True, ("stand", "neutral")),
            ("AT WORK", "typing, sleeves up", True, ("typing", None))]
    for i, (t, sub, sl, (pose, face)) in enumerate(cols):
        x = 150 + i * 260
        if sl is None:
            pb.pam(k, x, 640, 1.35, pose, face)
        else:
            with pf.look(sl):
                if face is None:
                    ac.pam(k, x, 640, 1.35, pose)
                else:
                    pb.pam(k, x, 640, 1.35, pose, face)
        corp(c, t, x - 110, 690, 21, brand.NAVY, True)
        corp(c, sub, x - 110, 716, 15, (0.35, 0.35, 0.4))
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "fs_pam_v1.png")
    s.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
