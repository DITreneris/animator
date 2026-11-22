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
from kit import Ctx, INK

F = sb.F
DON = (452, F + 26, sb.SC["don"])
GS = 0.56
FS = 0.62


def hd(x, feet, s):                                        # a head on Don's rig: (x, y, r) in set coordinates
    return (x, feet - 302 * s, 50 * s)


def hc(x, feet, s):                                        # a head on the Client's rig (the bodyguards, the repairman)
    return (x, feet - 372 * s, 55 * s)


def shot(name, heads, draw, note, rb=False, dn=False, chair=True, machine="broken", zmax=None, cam=None, **kw):
    return dict(name=name, heads=heads, draw=draw, note=note, rb=rb, dn=dn, chair=chair, machine=machine, zmax=zmax,
                cam=cam, kw=kw)


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
    cam = clear_signs(cam, sh["heads"])

    def back(k_):
        cs_cal.wall(k_, cs_cal.FRI)
        if sh["chair"]:
            dp.ceo_chair(k_, *dp.CHAIR)

    def extra(k_, o):
        dp.coffee_machine(k_, dp.MACHINE[0], dp.MACHINE[1], dp.MACHINE[2], sh["machine"])
        sh["draw"](k_, o)
    rb = dict(x=RX, x4=True, arm="none") if sh["rb"] else False
    cb.S(k, cam, auto=False, back=back, extra=extra, portrait=dict(ang=0.0),
         **cb.base(cl=False, sf=False, pm=False, mm=False, dn=False, rb=rb, door=0.9 if sh["name"].startswith("9") else 0.0))
    return cam


def main(out="../daddys-home/dh_blocking_v2.png"):
    os.makedirs("../daddys-home/dh_blocking", exist_ok=True)
    cols = 4; tw, th = 405, 720
    rows = (len(SHOTS) + cols - 1) // cols
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * (tw + 20) + 20, rows * (th + 96) + 70)
    sc = cairo.Context(sheet); sc.set_source_rgb(0.97, 0.95, 0.90); sc.paint()
    sc.set_source_rgb(*INK); sc.select_font_face("Inter", 0, 1); sc.set_font_size(26)
    sc.move_to(20, 40); sc.show_text("DADDY'S HOME · blocking v2 · the filter (7.1a to 7.3b) and the arrival (9.1 to 10.6)")
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
        ok = (rmax >= 60 or not faces) and not rail and not cut and not signs
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
