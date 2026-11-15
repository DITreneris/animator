"""Cafeteria set sheet for "I Will Replace You": the wide as framed, the 12 camera frames on the set, key
framings at phone size, props (burgers at full and phone size), bubble styles, new poses, and measured
checks. Writes cafe_set_v1.png at 2400x1560 (drawn at 1200x780, 2x) and prints the measurements."""
import sys
import math
import cairo
import kit
import brand
import anim
import pt42
import waiter_kit_v1 as w
import cafe_kit_v1 as ck
import sofia_v4 as sf
import don_v4 as dv
from kit import Ctx, INK
from charsheets import corp, wrap
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)

# planned cameras (world cx, cy, zoom) for the 12 shots of concept v3; the storyboard starts from these
CAMS = {
    1: (245, 640, 1.32, "two-shot"), 2: (115, 640, 2.40, "Sofía"), 3: (270, 640, 1.15, "robot arrives"),
    4: (270, 640, 1.20, "\"sir?\""), 5: (335, 600, 0.88, "WIDE"), 6: (290, 735, 3.00, "insert"),
    7: (420, 630, 2.40, "Don CU"), 8: (305, 640, 2.40, "robot CU"), 9: (200, 640, 1.60, "point"),
    10: (365, 640, 1.90, "whisper"), 11: (420, 630, 2.30, "Approved."), 12: (115, 615, 2.90, "Sofía CU"),
}


def world(k, robot="table", rpose="serve", rface="eager", rlook=(1, 0), tray=None, burgers=0, sof_face="neutral",
          sof_pose="stand", don_face="smug", don_pose="stand", don_look=(-0.6, 0), sof_look=(0.6, 0)):
    """The set. robot: 'table' (behind the table, between them) | 'wide' (rolling back from the counter) | None."""
    ck.room(k)
    ck.menu_board(k, 80, 330)
    pt42.wall_sign(k, 310, 340, 30)
    ck.counter(k, 760)
    ck.pam_corner(k)
    out = {}
    ck.chair_back(k, ck.SOF[0], ck.SOF[1] - 214, 1250)
    ck.chair_back(k, ck.DON[0], ck.DON[1] - 244, 1251)
    if robot == "table":
        out["robot"] = w.robot(k, ck.ROBOT[0], ck.ROBOT[1], 1.0, rpose, rface, look=rlook, tray=tray, seed=1501)
    out["sof"] = ck.seated(k, lambda: sf.sofia(k, ck.SOF[0], ck.SOF[1], 1.0, sof_pose, sof_face, look=sof_look,
                                               folder="none"))
    out["don"] = ck.seated(k, lambda: dv.don(k, ck.DON[0], ck.DON[1], 1.0, don_pose, don_face, look=don_look))
    ck.table(k)
    if robot == "wide":                       # front plane, rolling back from the counter with the food
        out["robot"] = w.robot(k, 560, 975, 1.0, "travel", "eager", tray="dome", wobble=-0.06, side=-1, seed=1500)
    if burgers:
        ck.bolt_burger(k, 252, ck.TABLE_TOP - 6, 0.7)
        ck.bolt_burger(k, 330, ck.TABLE_TOP - 6, 0.7, wrench_out=False)
    return out


def frame_box(c, x, y, wbox, cam):
    """Sets up a 9:16 box at (x, y), wbox wide, looking through camera cam; returns the screen scale."""
    hbox = wbox * 16 / 9
    c.save(); c.rectangle(x, y, wbox, hbox); c.clip()
    sc = wbox / 540
    c.translate(x + wbox / 2, y + hbox / 2); c.scale(sc * cam[2], sc * cam[2]); c.translate(-cam[0], -cam[1])
    return sc


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "CAFETERIA SET", 68, 44, 28, bold=True)
    corp(c, "One table, the robot between them, Pam at the back, counter off right", 300, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    tw = c.text_extents("UPTIMEZ INC. · I WILL REPLACE YOU · SET SHEET v1").x_advance
    corp(c, "UPTIMEZ INC. · I WILL REPLACE YOU · SET SHEET v1", W2 - 24 - tw, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. the wide, as framed (shot 5)
    corp(c, "SHOT 5 · THE ONE WIDE (9:16, as framed)", 24, 92, 10, bold=True)
    frame_box(c, 24, 98, 220, CAMS[5])
    world(k, robot="wide")
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(24, 98, 220, 220 * 16 / 9); c.stroke()

    # 2. camera map
    corp(c, "THE 12 CAMERAS ON THE SET", 264, 92, 10, bold=True)
    mx, my, mw, mh = 264, 98, 420, 300
    boxed(c, mx, my, mw, mh)
    c.save(); c.rectangle(mx, my, mw, mh); c.clip()
    ms = 0.36
    c.translate(mx + mw / 2, my + mh / 2); c.scale(ms, ms); c.translate(-330, -600)
    world(k, robot="table", tray="empty")
    cols = [(0.85, 0.15, 0.15), (0.10, 0.45, 0.80), (0.10, 0.60, 0.30), (0.75, 0.40, 0.05)]
    for n, (cx, cy, z, lbl) in CAMS.items():
        fw, fh = 540 / z, 960 / z
        c.set_source_rgb(*cols[n % 4]); c.set_line_width(4 / ms * 0.5)
        c.rectangle(cx - fw / 2, cy - fh / 2, fw, fh); c.stroke()
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(26)
        tx, ty = cx - fw / 2 + 6, cy - fh / 2 + 28 + (n % 3) * 26 if z < 2 else cy - fh / 2 + 28
        c.move_to(tx, ty); c.show_text(str(n))
    c.restore()
    corp(c, "Numbers = shots of concept v3. Two-shots are wide in 9:16; singles and close-ups are tight.",
         270, 412, 9, col=GREY)

    # 3. key framings at phone size
    corp(c, "KEY FRAMINGS AT PHONE SIZE", 704, 92, 10, bold=True)
    keys = [(1, dict(robot=None, sof_face="eyebrow", don_face="happy"), "1 the pun"),
            (4, dict(robot="table", rpose="serve", rface="eager", tray="empty", sof_pose="finger", sof_face="neutral"),
             "4 ignored"),
            (6, dict(robot=None, burgers=1), "6 the reveal"),
            (9, dict(robot="table", rpose="lock", rface="stern", rlook=(-1, 0), sof_face="horrified"), "9 the point"),
            (10, dict(robot="table", rpose="lean", rface="timid", sof_face="horrified"), "10 whisper"),
            (12, dict(robot=None, sof_face="neutral", sof_look=(0, 0)), "12 to camera")]
    fwid = 76
    for i, (n, kw, lbl) in enumerate(keys):
        x, y = 704 + (i % 6) * (fwid + 4), 98
        frame_box(c, x, y, fwid, CAMS[n])
        o = world(k, **kw)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, y, fwid, fwid * 16 / 9); c.stroke()
        corp(c, lbl, x, y + fwid * 16 / 9 + 12, 8, col=GREY)
    # bubbles on two of them, at phone size
    corp(c, "Frames shown at about the size a phone shows a feed video in a grid; bubbles are tested below.",
         704, 258, 9, col=GREY)

    # 4. props
    corp(c, "PROPS", 704, 290, 10, bold=True)
    boxed(c, 704, 296, 472, 150)
    c.save(); c.rectangle(704, 296, 472, 136); c.clip()
    w.dome_tray(k, 760, 400, w=90, dome=1.0)
    corp(c, "dome", 742, 424, 8, col=GREY)
    ck.bolt_burger(k, 880, 400, 1.2)
    corp(c, "bolt burger, full size", 846, 424, 8, col=GREY)
    ck.bolt_burger(k, 990, 400, 0.38)
    corp(c, "at phone size", 966, 424, 8, col=GREY)
    ck.wrench(k, 1060, 330, 0.8, 0.3)
    ck.bolt(k, 1130, 380, 1.2, -0.3)
    corp(c, "wrench, bolt", 1060, 424, 8, col=GREY)
    c.restore()

    # 5. bubbles
    corp(c, "BUBBLES", 704, 466, 10, bold=True)
    boxed(c, 704, 472, 472, 150)
    c.save(); c.rectangle(704, 472, 472, 136); c.clip()
    c.translate(704, 472); c.scale(0.5, 0.5)
    ck.thought(k, "Replace him.", (150, 250), 170, 110, size=30)
    ck.shout(k, "I WILL\nREPLACE YOU!", (560, 260), 560, 110, size=40)
    ck.whisper(k, "If that's okay, sir?", (760, 260), 755, 205, size=30)
    c.restore()
    corp(c, "thought: cloud + dots   ·   shout: biggest, spiky   ·   whisper: normal size, dotted", 710, 618, 8,
         col=GREY)

    # 6. new poses
    corp(c, "NEW POSES", 24, 520, 10, bold=True)
    boxed(c, 24, 526, 660, 150)
    c.save(); c.rectangle(24, 526, 660, 136); c.clip()
    c.translate(24, 526); c.scale(0.42, 0.42)
    sf.sofia(k, 110, 330, 1.0, "finger", "neutral", look=(0.5, 0), folder="none")
    sf.sofia(k, 300, 330, 1.0, "stand", "horrified", look=(0.6, 0), folder="none")
    p = dv.don(k, 520, 330, 1.0, anim.key(dv.POSE_THUMB), "happy", look=(-1, 0)); dv.thumbs_up(k, p["hands"][1])
    p = dv.don(k, 760, 330, 1.0, anim.key(dv.POSE_WRENCH), "shock"); ck.wrench(k, p["hands"][1][0], p["hands"][1][1] - 30, 0.9, 0.2)
    dv.don(k, 1000, 330, 1.0, anim.key(dv.POSE_CHEST), "pleased")
    dv.don(k, 1240, 330, 1.0, "stand", "neutral", look=(-1, 0))
    c.restore()
    for i, lbl in enumerate(["Sofía: finger up", "Sofía: horrified", "Don: thumbs-up", "Don: wrench",
                             "Don: flattered", "Don: glance"]):
        corp(c, lbl, 30 + i * 102, 672, 8, col=GREY)

    # 7. measured checks
    corp(c, "MEASURED", 24, 700, 10, bold=True)
    wrap(c, MEASURE_TEXT, 24, 716, 9, 1150)
    flush_labels(c)
    surf.write_to_png(out)


def measure():
    """Head size per camera, the robot's pointing reach vs Sofía's face and torso."""
    lines = []
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
    k = Ctx(cairo.Context(surf), 0)
    rb = w.robot(k, ck.ROBOT[0], ck.ROBOT[1], 1.0, "lock", "stern", look=(-1, 0))
    hx, hy = rb["hands"][0]
    tip = hx - 18
    so = sf.sofia(k, ck.SOF[0], ck.SOF[1], 1.0, "stand", "horrified", folder="none")
    face_r = so["head"][0] + 72            # her hair's outer edge at chest height
    body_top = ck.SOF[1] - 300 * sf.H + 78
    lines.append(f"Point: fingertip x {tip:.0f}, y {hy:.0f}; Sofía's head edge x {face_r:.0f}, her chest y "
                 f"{body_top:.0f}-{ck.TABLE_TOP}: the fingertip is {tip - face_r:+.0f} px from her hair edge, aimed "
                 f"{'at her upper torso' if body_top <= hy <= ck.TABLE_TOP else 'OFF her torso'}.")
    sizes = ", ".join(f"{n}: 1/{960 / (100 * z):.1f}" for n, (cx, cy, z, l) in CAMS.items())
    lines.append(f"Head height as a share of frame height, per shot: {sizes}. Singles and close-ups 1/4 or more; "
                 f"two-shots (1, 3, 4) about 1/7 to 1/8 because 9:16 is narrow.")
    return lines, (tip, hy, face_r, body_top)


MEASURE_TEXT = ""

if __name__ == "__main__":
    ls, nums = measure()
    MEASURE_TEXT = "  ".join(ls)
    print("\n".join(ls))
    main(sys.argv[1] if len(sys.argv) > 1 else "cafe_set_v1.png")
