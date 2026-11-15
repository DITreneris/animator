"""v2 (don_sheet_mf_v1.py writes v1 from don_mf_v1.py). Acting fixes for shots 5, 7, 11 and 12: the panic face
and stiff pose for 12, the cap airborne in 11c, Pam's sleeve and shoulder anchoring the chain in every yank beat,
a higher arm cross and bigger pout (5), a two-handed hug of the star and an offended face (7), and the phone check
seated in one order (Sofía, Don, Pam).
DON model sheet for "Mandatory Fun" (don_mf.py). Writes don_sheet_mf_v2.png at 2400x1560 (drawn at
1200x780, 2x): the AI Police kit, faces and poses by shot, the cap / star / belt-cuff details, the yank in three
beats, and a phone-size check with Sofia and Pam."""
import sys
import math
import cairo
import kit
import brand
import don_v4 as dv
import don_tg as dt
import don_mf as dm
import pam_mf as pm
import sofia_mf as sm
import props_mf as pr
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.92, 0.97)
LABELS = []
HY = dm.HY


def boxed(c, x, y, w, h, label=None, fill=(1, 1, 1)):
    c.set_source_rgb(*fill); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(x, y, w, h); c.stroke()
    LABELS.append((x, y, w, h, label))


def flush(c):
    for x, y, w, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 17, w - 2, 16); c.fill()
            corp(c, label, x + 6, y + h - 5, 9, col=GREY)
    LABELS.clear()


def table(c, x, y, w, h=60):
    c.set_source_rgb(0.55, 0.36, 0.22); c.rectangle(x, y, w, 14); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w, 14); c.stroke()
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y + 14, w, h); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 14, w, h); c.stroke()


def head_at(k, cx, cy, s, face, look=(0, 0), mouth=None):
    dm.don(k, cx, cy - HY * s, s, "stand", face, look=look, mouth=mouth)


def motion(c, pts, col=GREY, w=1.6):
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1)
    for (x0, y0, x1, y1) in pts:
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "DON", 68, 44, 28, bold=True)
    corp(c, "\"Mandatory Fun\"  ·  self-appointed AI Police  ·  wants admiration, not responsibility", 140, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · MANDATORY FUN v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    dm.don(k, 144, 512, 1.06, "stand", "hero", seed=71)
    corp(c, "FRONT · OFFICE v4 + THE AI POLICE KIT", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. office / Thanksgiving / Mandatory Fun
    corp(c, "OFFICE v4  ·  THANKSGIVING v2  ·  MANDATORY FUN", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    dv.don(k, 345, 300, 0.52, seed=72)
    dt.don(k, 449, 300, 0.52, "stand", "neutral", seed=72)
    dm.don(k, 553, 300, 0.52, "stand", "neutral", seed=72)
    c.restore()
    corp(c, "His office look, no tie. Added: toy cap a size too small, giant gold star, yellow toy cuffs.", 290, 322,
         9, col=GREY)

    # 3. faces by shot
    corp(c, "FACES, BY SHOT  (big, broad, always performing)", 284, 348, 10, bold=True)
    faces = [("hero", (0, 0), "3: entrance"), ("wink", (-0.8, 0.4), "4: \"arrest\""),
             ("smug", (-0.6, 0.2), "4: \"attention\""), ("pout", (-1, 0), "5: the sulk"),
             ("indignant", (0.6, 0), "7: \"a cop!\"")]
    for i, (e, lk, lab) in enumerate(faces):
        x, y = 284 + i * 66, 354
        boxed(c, x, y, 63, 92, lab, fill=(1.0, 0.94, 0.92) if e == "pout" else (1, 1, 1))
        c.save(); c.rectangle(x, y, 63, 92); c.clip()
        head_at(k, x + 31, y + 46, 0.36, e, lk)
        c.restore()
    corp(c, "THE YANK + THE END  ·  MOUTHS (\"AI Police!\" A · \"cop!\" O)", 284, 466, 9, col=GREY, bold=True)
    row2 = [("snap", (0, 0), None, "11: yanked"), ("collapse", (0, 0), None, "11: back down"),
            ("panic", (0, 0), None, "12: panic"), ("hero", (0, 0), "A", "\"AI Police!\""),
            ("indignant", (0.6, 0), "O", "\"cop!\"")]
    for i, (e, lk, m, lab) in enumerate(row2):
        x, y = 284 + i * 66, 472
        boxed(c, x, y, 63, 60, lab)
        c.save(); c.rectangle(x, y, 63, 60); c.clip()
        head_at(k, x + 31, y + 28, 0.36, e, lk, mouth=m)
        c.restore()

    # 4. poses
    corp(c, "POSES  (cuffs on his belt until the robot takes them in shot 8)", 634, 92, 10, bold=True)
    poses = [(dm.POSE_HERO, "hero", {}, "3: taps the star"),
             (dm.POSE_LEAN, "wink", dict(lean=-6, look=(-1, 0.5)), "4: leans in"),
             (dm.POSE_CROSS, "pout", dict(look=(-1, 0)), "5: arms folded"),
             (dm.POSE_CLUTCH, "indignant", dict(look=(1, 0)), "7: clutches it"),
             (dm.POSE_STIFF, "panic", dict(cuff="R", belt_cuffs_on=False), "12: panic, cuffed"),
             ("stand", "collapse", dict(belt_cuffs_on=False, cap=False), "loop: cap off")]
    poses = poses[:5]
    for i, (p, f, kw, lab) in enumerate(poses):
        x = 634 + i * 109
        boxed(c, x, 98, 105, 210, lab, fill=(1.0, 0.94, 0.92) if f in ("pout", "panic") else (1, 1, 1))
        c.save(); c.rectangle(x, 98, 105, 210); c.clip()
        o = dm.don(k, x + 52, 290, 0.44, p, f, seed=80 + i, **kw)
        if "cuff" in o:
            cx_, cy_ = o["cuff"]
            pr.chain(k, cx_, cy_, x + 106, cy_ + 10, 0.44, sag=0.25)
        c.restore()

    # 5. the yank, three beats (shot 11)
    corp(c, "THE YANK  (shot 11: lunge · taut · snap back, cap pops)", 634, 348, 10, bold=True)
    beats = [("lunge", "11a: lunges after her"), ("taut", "11b: the chain goes taut"), ("snap", "11c: snapped back")]
    for i, (b, lab) in enumerate(beats):
        x = 634 + i * 182
        boxed(c, x, 354, 178, 178, lab, fill=(1.0, 0.97, 0.88) if b == "taut" else (1, 1, 1))
        c.save(); c.rectangle(x, 354, 178, 160); c.clip()
        po = pm.pam(k, x + 172, 590, 0.5, (-100, 6, 8, 0), "neutral" if b != "snap" else "dinner",
                    look=(-1, 0), glasses="low" if b != "snap" else "up", cuff="L", seed=93)
        pl = po["cuff"]
        if b == "lunge":
            o = dm.don(k, x + 70, 520, 0.42, dm.POSE_LUNGE, "hero", lean=-12, look=(-1, 0), cuff="R",
                       belt_cuffs_on=False)
            pr.chain(k, *o["cuff"], *pl, 0.42, sag=0.35)
            motion(c, [(x + 118, 410, x + 138, 410), (x + 116, 420, x + 140, 420)])
        elif b == "taut":
            o = dm.don(k, x + 74, 520, 0.42, dm.POSE_LUNGE, "snap", lean=-20, look=(-1, 0), cuff="R",
                       belt_cuffs_on=False, cap=(-6, -6, -18))
            pr.chain(k, *o["cuff"], *pl, 0.42, sag=0.0)
            cx_, cy_ = o["cuff"]
            c.set_source_rgb(*INK); c.set_line_width(1.6)       # the twang
            for j in range(3):
                c.move_to(cx_ + 18 + j * 10, cy_ - 8); c.line_to(cx_ + 22 + j * 10, cy_ - 14); c.stroke()
        else:
            o = dm.don(k, x + 78, 548, 0.42, dm.POSE_SNAP, "snap", lean=12, cuff="R", belt_cuffs_on=False,
                       cap=(-6, -62, -28))
            hx_, hy_ = o["head"]
            c.set_source_rgb(*GREY); c.set_line_width(1.4)          # the cap's spin
            c.arc(hx_ + 4, hy_ - 64, 22, 1.1 * math.pi, 1.6 * math.pi); c.stroke()
            c.arc(hx_ + 4, hy_ - 64, 22, 0.1 * math.pi, 0.5 * math.pi); c.stroke()
            pr.chain(k, *o["cuff"], *pl, 0.42, sag=0.15)
            motion(c, [(x + 30, 400, x + 50, 404), (x + 26, 416, x + 48, 418), (x + 30, 432, x + 50, 432)])
        c.restore()

    # 6. phone-size check
    corp(c, "PHONE-SIZE CHECK  (one seating: Sofía, Don, Pam  ·  4: leans in  ·  5: sulks at Sofía  ·  12: she's happy, he panics)", 24,
         556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    sm.sofia(k, 76, 760, 0.42, "write", "neutral", look=(0, 0.6), seed=95)
    dm.don(k, 156, 770, 0.38, dm.POSE_LEAN, "wink", lean=-6, look=(-1, 0.5), seed=96)
    dm.don(k, 268, 770, 0.38, dm.POSE_CROSS, "pout", look=(-1, 0), seed=98)
    pm.pam(k, 352, 760, 0.42, pm.POSE_FINGER, "hopeful", finger=True, look=(-0.8, 0), seed=97)
    dm.don(k, 466, 770, 0.38, dm.POSE_STIFF, "panic", belt_cuffs_on=False, seed=99)
    pm.pam(k, 566, 760, 0.42, pm.POSE_TABLE, "happy", seed=100)
    c.restore()
    table(c, 24, 700, 590)
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    dhx, phx = 466 + 22, 566 - 22
    for hx_ in (dhx, phx):
        kit.ellipse(k, hx_, 703, 4.2, 4.2, pm.SKIN, 7, shadow=False, lw=1.2)
    a_ = pr.cuff(k, dhx - 3, 697, 0.5, 0.0, loop_side=1)
    b_ = pr.cuff(k, phx + 3, 697, 0.5, 0.0, loop_side=-1)
    pr.chain(k, a_[0], a_[1], b_[0], b_[1], 0.5, sag=0.15)
    c.restore()

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Office v4 underneath (vest, shirt, khakis, ketchup). The kit is cheap: plastic, toy-sized.",
             "Plant: the yellow cuffs on his belt (shot 3). The robot takes them (8), they end up on him (10).",
             "He only performs for Sofía: wink, smug. To Pam he never turns his head.",
             "5: arms folded high, big pout, eyes on Sofía (away from Pam). 7: offended, hugging the star.",
             "11: Pam anchors the chain in frame; lunge, taut twang, snapped back, cap airborne.",
             "12: Pam content, Don in real panic (no smile, stiff). Hold the contrast for a beat."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "don_sheet_mf_v2.png")
