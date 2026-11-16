"""Storyboard for "Office Noir", v1 (grill, 16 Nov: every beat as a panel; the loop is a true match cut, the heart
at the same screen position and size in the first and last frames; plan to about 33.5 s, the measured voice
takes decide the final cut; no title, no branding on screen).
HEART0 is the heart's place and size in frame 0 (on Pam's monitor) and in the last frame (on Don's pyjama
pocket). Each panel is a 540x960 frame built from the approved character, props and set modules, lit as on the
sets sheet, with the line in its bubble or caption card. PANELS lists (start, end, shot, label, line, builder).
Writes on_sb_sheet_v1.png and on_sb_loop_v1.png (the match check, both frames overlaid)."""
import sys
import math
import cairo
import kit
import brand
import don_on as d
import don_mf as dm
import pam_on as pn
import mom_on as mo
import sofia_on as so
import props_on as pr
import on_set as st
import engine_on as eng
import on_set_sheet as setsh
import props_sheet_on as psh
import don_sheet_on as dsh
import sofia_sheet_on as ssh
import pam_sheet_on as pms
from kit import Ctx, INK, rect
from charsheets import corp, wrap

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
ACC = setsh.ACC
HEART0 = (330.0, 760.0, 46.0)                     # x, y, size: frame 0 and the last frame


def surf():
    return cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)


def noir(draw, light=None):
    sf = surf(); draw(Ctx(cairo.Context(sf), 0)); eng.accent_pass(sf, ACC)
    if light:
        light(cairo.Context(sf))
    return sf


def colour(draw):
    sf = surf(); draw(Ctx(cairo.Context(sf), 0)); return sf


def vo(sf, text, size=30):
    psh.caption(cairo.Context(sf), text, 24, 40, size)
    return sf


def say(sf, text, x=40, y=60, tail=(120, 110), size=34):
    psh.bubble(cairo.Context(sf), text, x, y, tail, size)
    return sf


# ---- shot 1: frame 0 -----------------------------------------------------------------------------------------

MON1 = (390, 1060, 2.2)


def k1(kk):
    """The heart on Pam's monitor at HEART0 in the foreground; Don behind on the left; the agency door and the rain."""
    st.office_back(kk, t=0.0, door_x=330, window_x=24)
    d.don_noir(kk, 150, 1180, 1.9, face="cynic", brim=1.0, outline=True)
    kit.cut(kk, [(-20, 1000), (560, 1000), (560, 980), (-20, 980)], (0.40, 0.32, 0.25))
    pr.monitor(kk, *MON1)
    d.heart(kk.c, HEART0[0], HEART0[1], HEART0[2])


def l1(c):
    st.blinds(c, 0, 120, 280, 620, angle=-0.30, amount=0.32)
    eng.side_light(c, 0, 0, 540, 960, from_left=True, amount=0.30)
    st.vignette(c, 0.35)
    st.key_light(c, 150, 1180 + d.HY * 1.9, 160, 0.30)


# ---- 10B: the last frame, the heart on his pocket at HEART0 --------------------------------------------------

def k10b(kk, beat=1):
    st.bedroom(kk)
    rect(kk, 440, 560, 140, 260, (0.62, 0.45, 0.30), 812)
    pr.milk(kk, 500, 560, 1.6)
    s = HEART0[2] / 13.0                                     # don_pj's pocket heart is 13 units
    x = HEART0[0] - 25 * s
    feet = HEART0[1] - (d.BT + 48) * s
    if beat == 1:
        d.don_pj(kk, x, feet, s, face="frozen", lift=6, bunny=True)
    else:
        d.don_pj(kk, x, feet, s, face="deflated", look=(-0.6, 0.95), lift=6, bunny=True)
    bx, by = x - 28 * s, feet + (d.BT + 92) * s
    for i in range(3):
        kit.ellipse(kk, bx + (-14 + i * 12) * s * 0.62, by - 16 * s * 0.62, 5 * s * 0.6, 8 * s * 0.6, d.SKIN,
                    840 + i, shadow=False, lw=1.6 * s * 0.6)
    st.sweat_drop(kk.c, x + 46 * s, feet + (d.HY - 20) * s, 0.9 * s / 2)


# ---- shot 8 ------------------------------------------------------------------------------------------------------

def k8(kk):
    c = kk.c
    c.set_source_rgb(0.22, 0.22, 0.23); c.rectangle(0, 0, 540, 960); c.fill()
    d.don_noir(kk, 270, 1560, 4.0, pose=d.POSE_OBJECT, face="indignant", brim=0.0, outline=False)
    d.heart(c, 270 + 24 * 4.0, 1560 + (d.BT + 26) * 4.0, 16 * 4.0 * 0.72)


def l8(c):
    eng.side_light(c, 0, 0, 540, 960, from_left=False, amount=0.4)
    st.key_light(c, 270, 1560 + d.HY * 4.0, 220, 0.25)


# ---- builders for the beats --------------------------------------------------------------------------------------

def b_shot3():
    s3 = surf()
    ssh.shot3(Ctx(cairo.Context(s3), 0)); eng.accent_pass(s3, ssh.ACC); ssh.relight3(s3)
    c3 = cairo.Context(s3)
    hx, hy = ssh.HEAD3["head"]; s_ = 2.5
    c3.save(); c3.new_path(); c3.arc(hx, hy, 50 * s_, 0, 2 * math.pi); c3.clip()
    c3.set_source_rgba(0, 0, 0, 0.25); c3.rectangle(hx + 8 * s_, hy - 60 * s_, 70 * s_, 120 * s_); c3.fill(); c3.restore()
    st.key_light(c3, hx - 6 * s_, hy + 30 * s_, 26 * s_, 0.22)
    c3.set_source_rgb(1, 1, 1); c3.arc(hx - 18 * s_ + 3 * s_, hy + 1 * s_, 2.6 * s_, 0, 2 * math.pi); c3.fill()
    return say(s3, "I sign my work,\ndarling.", 150, 40, (120, 110), 34)


def b_shot5():
    P = psh
    wide = P.cctv(P.frame5(0.0), "MON 08:59:14")
    catch = P.cctv(pr.enhance(P.frame5(0.33), P.CORNER, 2.0, 1, "ENHANCE x2"), "MON 08:59:15")
    peel = P.cctv(pr.enhance(P.frame5(0.66, lean=7), P.CORNER, 4.0, 5, "ENHANCE x4"), "MON 08:59:15")
    stuck = pr.enhance(P.frame5(1.0, lean=4), (P.END[0] - 20, P.END[1] + 60), 1.25, 1, None)
    P.cctv(stuck, "MON 08:59:16", rec=False)
    cs = cairo.Context(stuck)
    cs.select_font_face("DejaVu Sans Mono", 0, 1); cs.set_font_size(26); cs.set_source_rgb(0.95, 0.95, 0.95)
    cs.move_to(380, 112); cs.show_text("II 0.6 s")
    P.bubble(cs, "Suspect\nidentified.", 250, 640, tail=(300, 120), size=36)
    exitf = P.cctv(P.frame5(1.0, walk=True), "MON 08:59:17")
    return wide, catch, peel, stuck, exitf


def b_shot4(footage):
    s4 = surf(); psh.shot4(Ctx(cairo.Context(s4), 0), footage); eng.accent_pass(s4, ACC); return s4


def b_shot6(beat):
    sf = surf(); psh.shot6(Ctx(cairo.Context(sf), 0), beat); eng.accent_pass(sf, ACC)
    st.key_light(cairo.Context(sf), 290, 1560 + d.HY * 4.0, 220, 0.2)
    return sf


def b_shot2():
    s2 = dsh.noir_frame(dsh.shot2, light=0.55)
    pov = surf(); ssh.shot2_pov(Ctx(cairo.Context(pov), 0)); eng.accent_pass(pov, ssh.ACC)
    return s2, pov


def b_shot7():
    d.FEDORA_RIM = True
    a = surf(); pms.shot7a(Ctx(cairo.Context(a), 0)); eng.accent_pass(a, ACC)
    ca = cairo.Context(a)
    pms.soft_light(ca, 165, 1010 + pn.HY * 2.0, 230, 0.30)
    eng.side_light(ca, 300, 0, 240, 960, from_left=True, amount=0.45)
    psh.bubble(ca, "You left me\nyour heart.", 40, 60, tail=(60, 120), size=36)
    bs = []
    for beat in (1, 4):
        sf = surf(); pms.shot7b(Ctx(cairo.Context(sf), 0), beat); eng.accent_pass(sf, ACC)
        eng.side_light(cairo.Context(sf), 0, 0, 540, 960, from_left=True, amount=0.35)
        bs.append(sf)
    d.FEDORA_RIM = False
    return a, bs[0], bs[1]


def build():
    d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
    s1 = vo(noir(k1, l1), "Monday. Somebody left Pam a heart.", 24)
    drink = surf(); psh.drink(Ctx(cairo.Context(drink), 0)); eng.accent_pass(drink, ACC)
    inf = surf(); psh.informant(Ctx(cairo.Context(inf), 0)); eng.accent_pass(inf, ACC)
    boss = noir(setsh.kboss, setsh.lboss)
    s2, pov = b_shot2()
    s3 = b_shot3()
    wide, catch, peel, stuck, exitf = b_shot5()
    s4 = b_shot4(wide)
    s6a, s6b = b_shot6("a"), b_shot6("b")
    s7a, s7b1, s7b4 = b_shot7()
    d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
    s8 = say(noir(k8, l8), "I object to\nthat wording.", 40, 60, (110, 120), 36)
    s9 = vo(noir(setsh.k9, setsh.l9), "Nobody tells me what to—", 24)
    s10a = say(colour(setsh.k10a), "DONNIE! Up.\nTime for work.", 30, 50, (300, 110), 36)
    s10b1, s10b2 = colour(lambda kk: k10b(kk, 1)), colour(lambda kk: k10b(kk, 2))
    d.FEDORA_BAND, d.FEDORA_RIM = None, False
    P = [
        (0.0, 3.2, "1", "frame 0: the heart (HEART0); push in", "VO 1 · sting on \"Unsigned.\"", s1),
        (3.2, 4.2, "M", "ONE DRINK: he flips the flask open", "VO M (one)", drink),
        (4.2, 5.2, "M", "ONE INFORMANT: lit from below", "VO M (two)", inf),
        (5.2, 6.2, "M", "ONE BOSS: the curler shadow", "VO M (three) · sting", boss),
        (6.2, 7.4, "2", "low angle: the heart up to his eye", "—", s2),
        (7.4, 8.5, "2", "his POV: the heart lines up with her lips", "— (smug point)", pov),
        (8.5, 10.8, "3", "the lamp: she files, never looks up", "2 Sofía", s3),
        (10.8, 12.8, "4", "the witness: a silent click", "— (click)", s4),
        (12.8, 14.0, "5", "CCTV wide: the lean", "—", wide),
        (14.0, 14.8, "5", "ENHANCE x2: the corner hooks it", "—", catch),
        (14.8, 15.6, "5", "ENHANCE x4: the peel", "—", peel),
        (15.6, 16.5, "5", "snapped on: freeze 0.6 s", "3 robot", stuck),
        (16.5, 17.6, "5", "wide: he walks off unaware", "—", exitf),
        (17.6, 18.2, "6", "eyes drop to the empty lapel", "— (silence)", s6a),
        (18.2, 18.9, "6", "the tilt, the brim down", "—", s6b),
        (18.9, 21.0, "7A", "she shows him the heart", "4 Pam", s7a),
        (21.0, 21.7, "7B", "her fingertips; he looks down", "—", s7b1),
        (21.7, 23.4, "7B", "pause, eyes up, the corner (0.8–1 s)", "—", s7b4),
        (23.4, 26.6, "8", "the finger; 0.4 s silence after", "5 Don", s8),
        (26.6, 28.6, "9", "low angle, hand in pocket, Mom's shadow", "VO 6, cut off · DONNIE! starts", s9),
        (28.6, 30.6, "10A", "smash cut to colour: Mom looms", "7 Mom · music cut dead", s10a),
        (30.6, 31.8, "10B", "the stare (HEART0 again)", "—", s10b1),
        (31.8, 33.6, "10B", "a glance down at the bunny; hold", "— → loops to frame 0", s10b2),
    ]
    return P


def loop_check(first, last):
    """Both frames at 50 % with a crosshair on HEART0: the heart must sit on the cross in both."""
    sf = surf(); c = cairo.Context(sf)
    c.set_source_surface(first, 0, 0); c.paint_with_alpha(1.0)
    c.set_source_surface(last, 0, 0); c.paint_with_alpha(0.5)
    x, y, r = HEART0
    c.set_source_rgb(0, 0.8, 0.3); c.set_line_width(3)
    c.move_to(x - r * 2, y); c.line_to(x + r * 2, y); c.stroke(); c.move_to(x, y - r * 2); c.line_to(x, y + r * 2); c.stroke()
    c.arc(x, y, r * 1.3, 0, 2 * math.pi); c.stroke()
    return sf


def main(out, loop_out):
    P = build()
    total = P[-1][1]
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(sheet); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "STORYBOARD", 68, 44, 26, bold=True)
    corp(c, "\"Office Noir: The Red Heart\"  ·  every beat  ·  %.1f s  ·  loops on the heart" % total, 266, 44, 13,
         col=GREY)
    corp(c, "UPTIMEZ INC. · STORYBOARD · OFFICE NOIR v1", 920, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()
    cols, w, gx, gy = 8, 132, 14, 100
    h = w * 960 / 540
    for i, (t0, t1, shot, lab, line, sf) in enumerate(P):
        col, row = i % cols, i // cols
        x0, y0 = 24 + col * (w + gx), 84 + row * (h + gy)
        c.save(); c.translate(x0, y0); c.scale(w / 540, w / 540)
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, y0, w, h); c.stroke()
        corp(c, "%s  %.1f–%.1f s" % (shot, t0, t1), x0, y0 + h + 14, 9.5, bold=True)
        yy = wrap(c, lab, x0, y0 + h + 28, 8.5, w, col=(0.25, 0.28, 0.36))
        wrap(c, line, x0, yy + 13, 8.5, w, col=(0.55, 0.20, 0.25))
    lc = loop_check(P[0][5], P[-1][5])
    i = len(P)
    col, row = i % cols, i // cols
    x0, y0 = 24 + col * (w + gx), 84 + row * (h + gy)
    c.save(); c.translate(x0, y0); c.scale(w / 540, w / 540); c.set_source_surface(lc, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, y0, w, h); c.stroke()
    corp(c, "LOOP CHECK", x0, y0 + h + 14, 9.5, bold=True)
    wrap(c, "frame 0 + the last frame at 50 %: the heart on the cross in both", x0, y0 + h + 28, 8.5, w,
         col=(0.25, 0.28, 0.36))
    sheet.write_to_png(out)
    lc.write_to_png(loop_out)
    return total


if __name__ == "__main__":
    t = main(sys.argv[1] if len(sys.argv) > 1 else "on_sb_sheet_v1.png",
             sys.argv[2] if len(sys.argv) > 2 else "on_sb_loop_v1.png")
    print("total", t)
