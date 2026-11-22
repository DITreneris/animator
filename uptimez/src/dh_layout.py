"""Daddy's Home: blocking for the two hardest beats (plan stage 6, gate G2b), as real camera frames on the front desk.
The arrival (9.1 to 10.6) and the filter (7.1a to 7.3b). Every camera comes from cs_frame.face_cam (the series' scale
rule); the sheet prints each frame's biggest face radius, and what is under the bottom line or the button rail.
  python3 dh_layout.py  -> ../daddys-home/dh_blocking_v1.png and dh_blocking/<shot>.png"""
import os
import sys
import math
import cairo
import kit
import fs_storyboard as sb
import cs_board as cb
import cs_frame as cf
import cs_cal
import dh_cast as dc
import dh_props as dp
import dh_poses as dq
import pam_bc as pb
import sofia_cs as scs
import sofia_dh as sdh
from kit import Ctx, INK

F = sb.F
DON = (452, F + 26, sb.SC["don"])
GS = 0.56
FS = 0.62


def hd(x, feet, s):                                        # a head on Don's rig: (x, y, r) in set coordinates
    return (x, feet - 302 * s, 50 * s)


def hc(x, feet, s):                                        # a head on the Client's rig (the bodyguards, the repairman)
    return (x, feet - 372 * s, 55 * s)


def shot(name, heads, draw, note, rb=False, dn=False, chair=True, machine="broken", zmax=None, cam=None, ymin=276, **kw):
    return dict(name=name, heads=heads, draw=draw, note=note, rb=rb, dn=dn, chair=chair, machine=machine, zmax=zmax,
                cam=cam, ymin=ymin, kw=kw)


def _guards(k, xl, xr, feet=F - 6):
    dc.guard(k, xl, feet, GS); dc.guard(k, xr, feet, GS, flip=True)


RX = 232                                                   # v2: the robot at its station by the door (front-desk-set.md)
ROBOT = (RX, F - 150, 50 * 0.40)


def s9_1(k, o):
    _guards(k, 70, 180)


def s9_2(k, o):                                            # the end of the push-in: he is the frame; they are its edges
    _guards(k, -22, 272)
    dc.father(k, 125, F + 22, FS, look=(0.3, 0.1))


def s9_3(k, o):
    dc.father(k, 130, F + 16, FS, look=(1, 0))
    c = k.c                                                # the scanner beam, from the robot's visor across his chest
    rx, ry = o["robot"]["screen"]
    c.set_source_rgba(0.95, 0.15, 0.15, 0.55); c.set_line_width(5)
    c.move_to(rx - 14, ry); c.line_to(130 + 22, F + 16 - 250 * FS); c.stroke()


def s9_4(k, o):
    dc.father(k, 330, F + 20, FS, look=(1, 0))
    sb.don(k, 452, F + 26, sb.SC["don"], (-8, 0, 60, 100), "neutral", look=(-1, 0))


def s10_4a(k, o):
    dc.father(k, 330, F + 20, FS, face="brow", look=(0.6, 0))


def s10_4b(k, o):
    _guards(k, 180, 290, F - 10)
    c = k.c                                                # they straighten: two marks over each head
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
    for gx in (180, 290):
        for dx in (-16, 16):
            c.move_to(gx + dx, F - 10 - 452 * GS); c.line_to(gx + dx * 1.3, F - 10 - 474 * GS); c.stroke()


def s10_6(k, o):
    sb.don(k, 440, F + 30, sb.SC["don"], (-95, 10, 95, -10), "panic", look=(-1, 0))


def s7_1a(k, o):
    c = k.c
    dc.repairman(k, 648, F + 14, GS, pose=(-6, 3, 8, -4), case=False, look=(1, 0.2))
    dc.tool_case(k, 712, F - 216, 0.62)                    # on the counter top, by its handle
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)   # BANG
    for a_ in (-2.5, -2.0, -1.1, -0.6):
        c.move_to(712 + math.cos(a_) * 44, F - 196 + math.sin(a_) * 30); c.line_to(712 + math.cos(a_) * 64, F - 196 + math.sin(a_) * 46); c.stroke()


def s7_3(k, o):
    d = sb.don(k, 452, F + 26, sb.SC["don"], "stand", "neutral", look=(0, 0))
    dp.coffee_run(k, d["head"], sb.SC["don"])
    dp.wet_filter(k, d["head"][0], d["head"][1] - 48 * sb.SC["don"], 0.80, -0.12)


def nothing(k, o):
    pass


SHOTS = [
    shot("7.1a", [hc(648, F + 14, GS)], s7_1a, "BANG: the case on the counter", cam=(728, 650, 2.2)),
    shot("7.2", [], nothing, "one big POP", machine="pop", cam=(770, 560, 3.0)),
    shot("7.3", [hd(452, F + 26, 0.60)], s7_3, "the filter lands; he doesn't move"),
    shot("7.3b", [ROBOT], nothing, "\"Workplace incident recorded.\"", rb=True, zmax=3.6, chair=False),
    shot("9.1", [hc(70, F - 6, GS), hc(180, F - 6, GS)], s9_1, "two bodyguards fill the door", chair=False),
    shot("9.2", [hd(125, F + 22, FS)], s9_2, "they part; the camera pushes in: Father", chair=False),
    shot("9.3", [hd(130, F + 16, FS), ROBOT], s9_3, "\"Unregistered visitor.\"", rb=True, chair=False),
    shot("9.4", [hd(330, F + 20, FS), hd(452, F + 26, 0.60)], s9_4, "the thumb goes down. \"Approved.\""),
    shot("10.4a", [hd(330, F + 20, FS)], s10_4a, "\"Good. Find my money.\" The eyebrow"),
    shot("10.4b", [hc(180, F - 10, GS), hc(290, F - 10, GS)], s10_4b, "0.4 s: both straighten", chair=False),
    shot("10.5a", [ROBOT], nothing, "the robot's head turns", rb=True, zmax=3.6, chair=False),
    shot("10.5b", [], nothing, "what it sees: the throne", cam=(452, 724, 2.3)),
    shot("10.6", [hd(440, F + 30, 0.60)], s10_6, "he steps into its view; it slides to see past him", cam=(470, 724, 2.3)),
]


# ---- v3: beats 0 to 6 and 8, one key frame a shot --------------------------------------------------------------------
PS, SS, MS = sb.SC["pam"], sb.SC["sofia"], sb.SC["mom"]
CH = dp.CHAIR
FLOOR = CH[1]


def hp(x, feet, s):                                        # Pam's and Sofía's heads
    return (x, feet - 272 * s, 50 * s)


def hm(x, feet, s):                                        # Mom's
    return (x, feet - 294 * s, 50 * s)


def h_seat(sunk=False):
    return (CH[0], FLOOR - (180 if not sunk else 152), 30)


def s0_2a(k, o):
    import acts_ob as ac
    dq.don_seated(k, CH[0], FLOOR, CH[2])
    ac.shredder(k, CH[0] + 190 * CH[2], FLOOR, 0.62, fill=0.4)


def s0_2b(k, o):
    dq.don_seated(k, CH[0], FLOOR, CH[2], sunk=True, puff=True)


def s1_1(k, o):
    scs.sofia(k, 566, F + 4, SS, "hold", "interested", look=(-1, 0))
    pb.pam(k, 652, F + 6, PS, "stand", "neutral", look=(-1, 0), glasses="up")


def s1_2(k, o):
    d = sb.don(k, 452, F + 26, 0.60, (-100, -30, 100, 30), "happy", look=(0.6, 0))
    c = k.c
    hx, hy = d["head"]
    for dx, dy in ((-16, -34), (20, -30)):
        c.save(); c.translate(hx + dx, hy + dy); c.scale(0.7, 0.7)
        c.move_to(0, -8); c.curve_to(6, 0, 5, 6, 0, 6); c.curve_to(-5, 6, -6, 0, 0, -8); c.close_path()
        c.set_source_rgb(0.62, 0.84, 0.95); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.5); c.stroke()
        c.restore()


def s1_3(k, o):
    scs.sofia(k, 566, F + 4, SS, "hold", "interested", look=(-0.8, -0.3))


def s2_1(k, o):
    q = scs.sofia(k, 566, F + 4, SS, "chest", "deadpan", look=(-1, 0))
    c = k.c
    hx, hy = min(q["hands"], key=lambda h_: h_[1])
    c.save(); c.translate(hx, hy - 6); c.rotate(-0.06)
    kit.rect(k, -32, -30, 64, 46, (0.86, 0.72, 0.36), 3301, lw=2)
    kit.text(k, "REPORTS", 0, -4, 11, INK)
    c.restore()


def s2_3(k, o):
    dp.ceo_chair(k, 530, FLOOR, CH[2], lean=0.05)
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)        # it is rolling back towards him
    for yy in (F - 60, F - 36, F - 12):
        c.move_to(600, yy); c.line_to(626, yy); c.stroke()
    sb.don(k, 420, F + 26, 0.60, "stand", "smug", look=(-1, 0))


def s2_4(k, o):
    pb.pam(k, 598, F + 6, PS, "stand", "neutral", look=(-1, 0.1), glasses="up")


def s3_1(k, o):
    sb.don(k, 330, F + 26, 0.60, (-70, -20, 8, 0), "smug", look=(-1, 0))
    rx, ry = o["robot"]["screen"]
    dp.star_screen(k, rx + 6, ry - 84, 112, green=False)


def s3_5(k, o):
    sb.don(k, 330, F + 26, 0.60, "vest", "smug", look=(1, 0))


def s4_1(k, o):
    dp.ceo_chair(k, CH[0], FLOOR, CH[2])
    scs.sofia(k, 476, F + 10, SS, "hold", "caught", look=(-1, 0))
    sb.mfs.mom(k, 384, F + 8, MS, "wipe", "sweet", look=(0.6, 0.6))


def s5_1(k, o):
    dc.repairman(k, 128, F + 8, GS, look=(0.6, 0))


def s5_2(k, o):
    sb.mfs.mom(k, 408, F + 8, MS, "stand", "sweet", look=(-1, 0))
    scs.sofia(k, 534, F + 4, SS, "hold", "smile", look=(-1, 0))
    sb.don(k, 470, F + 26, 0.60, "vest", "happy", look=(-1, 0))


def s5_4(k, o):
    q = pb.pam(k, 598, F + 6, PS, (-8, 0, 60, 110), "neutral", look=(0.2, 0.9), glasses="up")
    c = k.c
    hx, hy = q["hands"][1]
    c.save(); c.translate(hx + 2, hy - 12); c.rotate(2.6)                    # her cup, tipped: nothing comes out
    kit.cut(k, [(-9, -11), (9, -11), (7, 11), (-7, 11)], (0.97, 0.96, 0.92), shadow=False, lw=2)
    c.restore()


def s6_1(k, o):
    dc.repairman(k, 300, F + 8, GS, case=True, look=(1, -0.2))
    d = sb.don(k, 408, F + 26, 0.60, (-70, -30, 8, 0), "happy", look=(-1, 0))
    hx, hy = d["hands"][0]
    kit.rect(k, hx - 20, hy - 9, 30, 19, dp.GOLD, 3302, lw=1.8)
    kit.text(k, "PREMIUM", hx - 5, hy + 2, 5.2, INK)


def s8_2(k, o):
    d = sb.don(k, 452, F + 26, 0.60, "stand", "neutral", look=(0, 0))
    dp.coffee_run(k, d["head"], 0.60)
    sb.mfs.mom(k, 372, F + 8, MS, "lick", "sweet", look=(0.8, -0.4))
    dp.wet_filter(k, 338, F - 70, 0.7, 0.4)                                 # in her other hand, peeled off


def s8_3(k, o):
    dq.don_zipped(k, 452, F + 26, 0.60, face="confused", look=(-0.6, 0.4))


def s8_4a(k, o):
    sdh.sofia(k, 560, F + 4, SS, "lapel", "interested", look=(-0.8, 0))


def s8_4b(k, o):
    sb.mfs.mom(k, 392, F + 8, MS, "hip", "sweet", look=(1, 0))
    pb.pam(k, 456, F + 6, PS, "stand", "neutral", look=(0.6, 0), glasses="up")
    dq.don_zipped(k, 520, F + 26, 0.60, look=(-0.6, 0))


def s9_6(k, o):
    dc.guard(k, 286, F - 2, GS)
    sdh.sofia(k, 392, F + 4, SS, "stand", "tight", look=(-1, 0))
    sdh.cv(k, 338, F - 96, 0.7, 0.1)


SHOTS_NEW = [
    shot("0.2a", [h_seat()], s0_2a, "DAD rings: Don in the throne, feet up", chair=False),
    shot("0.2b", [h_seat(True)], s0_2b, "PSSSH: it sinks under him", chair=False),
    shot("1.1", [hp(566, F + 4, SS), hp(652, F + 6, PS)], s1_1, "they stare at him", chair=False),
    shot("1.2", [hd(452, F + 26, 0.60)], s1_2, "\"Good news, everyone!\"; the sweat"),
    shot("1.3", [hp(566, F + 4, SS)], s1_3, "\"Is he coming alone?\"", chair=False),
    shot("2.1", [hp(566, F + 4, SS)], s2_1, "REPORTS", chair=False),
    shot("2.3", [hd(420, F + 26, 0.60)], s2_3, "\"The money was invested.\" It rolls back", chair=False, cam=(470, 700, 2.1)),
    shot("2.4", [hp(598, F + 6, PS)], s2_4, "\"Into what?\"", chair=False),
    shot("3.1", [hd(330, F + 26, 0.60), ROBOT], s3_1, "\"Make it green.\"", rb=True, chair=False),
    shot("3.5", [hd(330, F + 26, 0.60)], s3_5, "\"He won't count.\"", chair=False),
    shot("4.1", [hm(384, F + 8, MS), hp(476, F + 10, SS)], s4_1, "Mom scrubs the arm; Sofía is up", chair=False),
    shot("5.1", [hc(128, F + 8, GS)], s5_1, "a knock: a big man in black, a case", chair=False),
    shot("5.2", [hm(408, F + 8, MS), hd(470, F + 26, 0.60), hp(534, F + 4, SS)], s5_2, "they snap into a line", chair=True, ymin=240),
    shot("5.4", [hp(598, F + 6, PS)], s5_4, "her empty cup; she says nothing", chair=False),
    shot("6.1", [hc(300, F + 8, GS), hd(408, F + 26, 0.60)], s6_1, "\"Lifetime Premium. On us.\"", chair=False, ymin=215),
    shot("8.2", [hm(372, F + 8, MS), hd(452, F + 26, 0.60)], s8_2, "\"Mom! I'm the CEO!\""),
    shot("8.3", [hd(452, F + 26, 0.60)], s8_3, "the zip, to his chin"),
    shot("8.4a", [hp(560, F + 4, SS)], s8_4a, "Sofía walks back in, changed", chair=False),
    shot("8.4b", [hm(392, F + 8, MS), hp(456, F + 6, PS), hd(520, F + 26, 0.60)], s8_4b, "Mom stands Pam beside him", chair=False, ymin=240),
    shot("9.6", [hc(286, F - 2, GS), hp(392, F + 4, SS)], s9_6, "the CV, pocketed", chair=False, ymin=188),
]
SHOTS_BLOCKING = SHOTS


def clear_signs(cam, heads, y_min=276):
    """A wall sign cut by the top of the frame is pushed out of it: the camera comes down until the sign is gone, as long
    as the faces stay at or below y_min (the top bar is at 96)."""
    cx, cy, z = cam
    need = cy
    for n in ("portrait+plaque", "calendar"):
        b = cf.SIGNS[n]
        if cf.sign_state((cx, cy, z), b) == "CUT" and 270 + (b[2] - cx) * z > 2 and 270 + (b[0] - cx) * z < 538:
            need = max(need, b[3] + 484.0 / z)
    if need > cy and heads:
        fy = min(480 + (h[1] - need) * z for h in heads)
        if fy < y_min:
            need -= (y_min - fy) / z
    return (cx, round(max(cy, need), 1), z)


def draw(sh, k):
    cam = sh["cam"] or cf.face_cam(sh["heads"], z_max=sh["zmax"])
    cam = clear_signs(cam, sh["heads"], sh.get("ymin", 276))

    def back(k_):
        cs_cal.wall(k_, cs_cal.FRI)
        if sh["chair"]:
            dp.ceo_chair(k_, *dp.CHAIR)

    def extra(k_, o):
        dp.coffee_machine(k_, dp.MACHINE[0], dp.MACHINE[1], dp.MACHINE[2], sh["machine"])
        sh["draw"](k_, o)
    rb = dict(x=RX, x4=True, arm="none") if sh["rb"] else False
    k.c.save(); k.c.identity_matrix(); k.c.set_source_rgb(*kit.FLOOR); k.c.paint(); k.c.restore()   # the floor goes on under the set's own edge
    cb.S(k, cam, auto=False, back=back, extra=extra, portrait=dict(ang=0.0),
         **cb.base(cl=False, sf=False, pm=False, mm=False, dn=False, rb=rb, door=0.9 if sh["name"].startswith("9") else 0.0))
    return cam


def main(out="../daddys-home/dh_layout_v3.png", shots=None):
    os.makedirs("../daddys-home/dh_blocking", exist_ok=True)
    SHOTS = shots or SHOTS_NEW
    cols = 4; tw, th = 405, 720
    rows = (len(SHOTS) + cols - 1) // cols
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * (tw + 20) + 20, rows * (th + 96) + 70)
    sc = cairo.Context(sheet); sc.set_source_rgb(0.97, 0.95, 0.90); sc.paint()
    sc.set_source_rgb(*INK); sc.select_font_face("Inter", 0, 1); sc.set_font_size(26)
    sc.move_to(20, 40); sc.show_text("DADDY'S HOME · layout v3 · beats 0 to 6, 8 and 9.6 (the filter and the arrival are in blocking v2)")
    for i, sh in enumerate(SHOTS):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); c = cairo.Context(surf); c.scale(2, 2)
        cam = draw(sh, Ctx(c, 0))
        surf.write_to_png("../daddys-home/dh_blocking/%s.png" % sh["name"])
        z = cam[2]
        faces = [(270 + (x - cam[0]) * z, 480 + (y - cam[1]) * z, r * z) for x, y, r in sh["heads"]]
        rmax = max([f[2] for f in faces] or [0])
        rail = [f for f in faces if f[0] + f[2] > cf.RAIL[0] and cf.RAIL[1] < f[1] < cf.RAIL[2]]
        cut = [f for f in faces if f[0] - f[2] < 0 or f[0] + f[2] > 540]
        verdict = "r %d" % round(rmax) + (" · %d face(s) in the rail" % len(rail) if rail else "") + (" · %d face(s) cut" % len(cut) if cut else "")
        signs = [n for n in ("portrait+plaque", "calendar") if cf.sign_state(cam, cf.SIGNS[n]) == "CUT"]
        verdict += (" · CUT: " + ", ".join(signs)) if signs else ""
        ok = (rmax >= (56 if len(faces) >= 3 else 60) or not faces) and not rail and not cut and not signs
        print("%-5s cam %-22s %s  %s" % (sh["name"], cam, verdict, "ok" if ok else "LOOK"), flush=True)
        x0, y0 = 20 + (i % cols) * (tw + 20), 60 + (i // cols) * (th + 96)
        sc.save(); sc.translate(x0, y0); sc.scale(tw / 1080.0, th / 1920.0); sc.set_source_surface(surf, 0, 0); sc.paint(); sc.restore()
        sc.set_source_rgba(0.9, 0.1, 0.1, 0.55); sc.set_line_width(1.5); sc.set_dash([6, 4])       # the bottom line and the rail
        sc.move_to(x0, y0 + 720 * th / 960.0); sc.line_to(x0 + tw, y0 + 720 * th / 960.0); sc.stroke()
        sc.rectangle(x0 + 470 * tw / 540.0, y0 + 380 * th / 960.0, 70 * tw / 540.0, 480 * th / 960.0); sc.stroke(); sc.set_dash([])
        sc.set_source_rgb(*INK); sc.set_line_width(2); sc.rectangle(x0, y0, tw, th); sc.stroke()
        sc.select_font_face("Inter", 0, 1); sc.set_font_size(19); sc.move_to(x0, y0 + th + 26); sc.show_text("%s  %s" % (sh["name"], sh["note"]))
        sc.select_font_face("Inter", 0, 0); sc.set_font_size(16)
        sc.set_source_rgb(*((0.1, 0.45, 0.2) if ok else (0.8, 0.1, 0.1)))
        sc.move_to(x0, y0 + th + 50); sc.show_text(("OK  " if ok else "LOOK  ") + verdict + "  ·  zoom %.2f" % z)
    sheet.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    main()
