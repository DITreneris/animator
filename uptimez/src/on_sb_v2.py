"""Storyboard for "Office Noir", v2 (on_sb_v1.py = v1, kept). v2 after the review: shot 1 opens on one lightning
flash (two bright frames, then it decays: no flicker), the heart bigger and the line on two cards; shot 2 is the
fake-out (he reaches into his coat, a metallic click, draws... a magnifying glass; his eye huge in the lens; his
POV through the lens: the heart's red lines up with Sofia's lips); the CCTV peel at x4 gets 1.2 s, the exit 0.7 s;
shot 6 is an ECU of his eyes, the empty lapel, a 12 degree tilt; hard-edged split light in 6, 7B and 8; shot 9's
shadow grows until it nearly swallows him; 10B shows the bed (headboard, pillow, blanket), the fedora stays on,
and ends on the gag: he slides a pink toy magnifier under the blanket.
v1 notes: Storyboard for "Office Noir", v1 (grill, 16 Nov: every beat as a panel; the loop is a true match cut, the heart
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

W2, H2 = 1200, 1560
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
ACC = setsh.ACC
HEART0 = (330.0, 830.0, 58.0)                     # v2: bigger; x, y, size in frame 0 and the last frame


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

MON1 = (390, 1110, 2.2)


def k1(kk):
    """The heart on Pam's monitor at HEART0 in the foreground; Don behind on the left; the agency door and the rain."""
    st.office_back(kk, t=0.0, door_x=330, window_x=24)
    d.don_noir(kk, 150, 1180, 1.9, face="cynic", brim=1.0, outline=True)
    kit.cut(kk, [(-20, 1060), (560, 1060), (560, 980), (-20, 980)], (0.40, 0.32, 0.25))
    pr.monitor(kk, *MON1)
    d.heart(kk.c, HEART0[0], HEART0[1], HEART0[2])


def l1(c):
    st.blinds(c, 0, 120, 280, 620, angle=-0.30, amount=0.32)
    eng.side_light(c, 0, 0, 540, 960, from_left=True, amount=0.30)
    st.vignette(c, 0.35)
    st.key_light(c, 150, 1180 + d.HY * 1.9, 160, 0.30)


# ---- 10B: the last frame, the heart on his pocket at HEART0 --------------------------------------------------

def k10b(kk, beat=1):
    """The last frame: the heart on his pocket at HEART0. v2: the bed reads (headboard, pillow, blanket); the
    fedora stays on. beat 1 the stare; beat 2 the glance down; beat 3 he slides the pink toy magnifier under the
    blanket."""
    c = kk.c
    st.bedroom(kk)
    s = HEART0[2] / 13.0
    x = HEART0[0] - 25 * s
    feet = HEART0[1] - (d.BT + 48) * s
    hy = feet + d.HY * s
    rect(kk, -20, hy - 150, 580, 330, (0.24, 0.52, 0.54), 850)                       # a teal headboard
    c.set_source_rgb(0.18, 0.40, 0.42); c.set_line_width(3)
    for xx in range(30, 540, 70):
        c.move_to(xx, hy - 140); c.line_to(xx, hy + 170); c.stroke()
    kit.ellipse(kk, x, hy + 40, 210, 120, (0.98, 0.95, 0.88), 851)                  # the pillow behind his head
    rect(kk, 440, 600, 140, 260, (0.62, 0.45, 0.30), 812)
    pr.milk(kk, 512, 600, 1.4)
    if beat == 1:
        d.don_pj(kk, x, feet, s, face="frozen", lift=6, bunny=True)
    else:
        d.don_pj(kk, x, feet, s, face="deflated", look=(-0.6, 0.95), lift=6, bunny=True)
    bx, by = x - 28 * s, feet + (d.BT + 92) * s
    for i in range(3):
        kit.ellipse(kk, bx + (-14 + i * 12) * s * 0.62, by - 16 * s * 0.62, 5 * s * 0.6, 8 * s * 0.6, d.SKIN,
                    840 + i, shadow=False, lw=1.6 * s * 0.6)
    st.sweat_drop(c, x + 46 * s, feet + (d.HY - 20) * s, 0.9 * s / 2)
    bl = HEART0[1] + 92                                                              # the blanket's edge
    if beat == 3:                                                                    # the toy magnifier going under
        pr.magnifier(c, 420, bl + 10, 34, rot=-2.4, toy=True)
        kit.ellipse(kk, 380, bl - 14, 26, 20, d.SKIN, 852, shadow=False, lw=2.4)
    rect(kk, -20, bl, 600, 300, (0.70, 0.84, 0.94), 811)
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(-20, bl, 600, 20); c.fill()                  # the sheet's fold
    if beat == 3:
        kit.ellipse(kk, 380, bl + 4, 24, 14, d.SKIN, 853, shadow=False, lw=2.4)                    # fingers on the fold


# ---- shot 8 ------------------------------------------------------------------------------------------------------

def k8(kk):
    c = kk.c
    c.set_source_rgb(0.22, 0.22, 0.23); c.rectangle(0, 0, 540, 960); c.fill()
    d.don_noir(kk, 270, 1560, 4.0, pose=d.POSE_OBJECT, face="indignant", brim=0.0, outline=False)
    d.heart(c, 270 + 24 * 4.0, 1560 + (d.BT + 26) * 4.0, 16 * 4.0 * 0.72)


def l8(c):
    st.key_light(c, 270, 1560 + d.HY * 4.0, 220, 0.22)
    st.hard_side(c, 300, angle=0.08, amount=0.55, right=True)                    # v2: a hard split, not a gradient


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


def k6(kk, beat):
    """v2: ECU of his eyes; ECU of the empty lapel; the 12 degree tilt with the brim coming down."""
    c = kk.c
    c.set_source_rgb(0.20, 0.20, 0.21); c.rectangle(0, 0, 540, 960); c.fill()
    if beat == "eyes":
        s = 8.0; d.don_noir(kk, 270, 480 - d.HY * s, s, face="neutral", look=(0.3, 0.95), brim=0.3, outline=True)
    elif beat == "lapel":
        s = 7.0; d.don_noir(kk, 270 - d.LAPEL_HEART[0] * s, 480 - d.LAPEL_HEART[1] * s, s, face="neutral", brim=0.3,
                            outline=True)
    else:
        c.save(); c.translate(270, 480); c.rotate(math.radians(12)); c.translate(-270, -480)
        d.don_noir(kk, 290, 1560, 4.0, face="drop", look=(0, 0.2), brim=1.0, outline=True)
        c.restore()


def b_shot6(beat):
    sf = noir(lambda kk: k6(kk, beat), lambda c: st.hard_side(c, 300, 0.10, 0.5))
    return sf


POSE_REACH = (-10, 4) + dm.ik(1, 6, d.BT + 58)                       # his hand inside the coat, at his chest


def k2a(kk):
    """The draw: low angle, his hand goes inside the trench like a gun. (Sound: a metallic click.)"""
    dsh.lamp_wall(kk, 540, 960, 120, 160)
    o = d.don_noir(kk, 290, 1380, 3.2, pose=POSE_REACH, face="cynic", brim=0.6, outline=True)
    hx, hy = o["hands"][1]
    s = 3.2
    kit.cut(kk, [(hx - 30 * s, hy - 26 * s), (hx + 8 * s, hy - 30 * s), (hx + 12 * s, hy + 14 * s), (hx - 26 * s, hy + 18 * s)],
            d.TRENCH_SHADE, shadow=False, lw=2 * s)                                # the lapel over his hidden hand


def k2b_base(kk):
    dsh.lamp_wall(kk, 540, 960, 120, 160)
    d.don_noir(kk, 270, 1420, 3.6, face="cynic", brim=0.4, outline=True)


def b_shot2():
    a = noir(k2a, lambda c: st.hard_side(c, 330, 0.1, 0.45))
    base = surf(); k2b_base(Ctx(cairo.Context(base), 0)); eng.accent_pass(base, ACC)
    b = surf(); cb = cairo.Context(b); cb.set_source_surface(base, 0, 0); cb.paint()
    ex, ey = 270 + 17 * 3.6, 1420 + d.HY * 3.6                                         # his screen-right eye
    pr.lens_view(cb, base, ex, ey, 92, zoom=1.9, rot=1.1)                              # the eye, huge in the lens
    st.hard_side(cb, 360, 0.1, 0.35)
    pov = surf(); ssh.shot2_pov(Ctx(cairo.Context(pov), 0)); eng.accent_pass(pov, ssh.ACC)
    lens = surf(); cl = cairo.Context(lens); cl.set_source_surface(pov, 0, 0); cl.paint()
    cl.set_source_rgba(0, 0, 0, 0.45); cl.rectangle(0, 0, 540, 960); cl.fill()
    pr.lens_view(cl, pov, 280, 405, 165, zoom=1.12, rot=1.25)                         # heart and lips in one lens
    return a, b, lens


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
        st.hard_side(cairo.Context(sf), 340, 0.08, 0.5)                          # v2: a hard split
        bs.append(sf)
    d.FEDORA_RIM = False
    return a, bs[0], bs[1]


def k9(kk, grow):
    """v2: the shadow grows during the shot until it nearly swallows him."""
    st.office_back(kk, t=1.2, door_x=700, window_x=24)
    sc = 1.5 + 1.1 * grow
    st.mom_shadow(kk, 430 - 60 * grow, 700 + 330 * grow, sc, skew=0.10, alpha=0.92, head=1.5, big=True)
    o = d.don_noir(kk, 175, 1320, 2.6, pose=setsh.POSE_POCKET, face="cynic", brim=1.0, outline=True)
    s = 2.6
    hx, hy = o["hands"][0]
    kit.ellipse(kk, hx + 2 * s, hy + 2 * s, 15 * s, 11 * s, d.TRENCH_SHADE, 331, shadow=False, lw=1.6 * s)
    rect(kk, hx - 15 * s, hy - 12 * s, 32 * s, 12 * s, d.TRENCH, 330, shadow=False, lw=2 * s)


def two_cards(sf, a, b, size=34):
    c = cairo.Context(sf)
    psh.caption(c, a, 24, 36, size)
    psh.caption(c, b, 24, 36 + size * 1.9, size)
    return sf


def build():
    d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
    s1f = noir(k1, lambda c: (l1(c), st.flash(c, 0.5), st.blinds(c, 0, 120, 540, 700, -0.30, 22, 10, 0.5)))
    s1 = two_cards(noir(k1, l1), "Monday. Somebody", "left Pam a heart.")
    drink = surf(); psh.drink(Ctx(cairo.Context(drink), 0)); eng.accent_pass(drink, ACC)
    inf = surf(); psh.informant(Ctx(cairo.Context(inf), 0)); eng.accent_pass(inf, ACC)
    boss = noir(setsh.kboss, setsh.lboss)
    s2a, s2b, s2c = b_shot2()
    s3 = b_shot3()
    wide, catch, peel, stuck, exitf = b_shot5()
    s4 = b_shot4(wide)
    s6a, s6b, s6c = b_shot6("eyes"), b_shot6("lapel"), b_shot6("tilt")
    s7a, s7b1, s7b4 = b_shot7()
    d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
    s8 = say(noir(k8, l8), "I object to\nthat wording.", 40, 60, (110, 120), 36)
    s9a = two_cards(noir(lambda kk: k9(kk, 0.0), setsh.l9), "Nobody tells me", "what to—")
    s9b = noir(lambda kk: k9(kk, 1.0), setsh.l9)
    s10a = say(colour(setsh.k10a), "DONNIE! Up.\nTime for work.", 30, 50, (300, 110), 36)
    s10b1, s10b2, s10b3 = (colour(lambda kk: k10b(kk, 1)), colour(lambda kk: k10b(kk, 2)),
                           colour(lambda kk: k10b(kk, 3)))
    d.FEDORA_BAND, d.FEDORA_RIM = None, False
    P = [
        (0.0, 0.4, "1", "LIGHTNING: one flash, the heart lit", "thunder \u00b7 rain", s1f),
        (0.4, 3.2, "1", "frame 0 settles; push in on the heart", "VO 1 \u00b7 sting on \"Unsigned.\"", s1),
        (3.2, 4.2, "M", "ONE DRINK: he flips the flask open", "VO M (one) \u00b7 a metal click", drink),
        (4.2, 5.2, "M", "ONE INFORMANT: lit from below", "VO M (two)", inf),
        (5.2, 6.2, "M", "ONE BOSS: the curler shadow", "VO M (three) \u00b7 sting", boss),
        (6.2, 6.9, "2", "the draw: hand inside the coat, like a gun", "\u2014 \u00b7 a metallic CLICK", s2a),
        (6.9, 7.9, "2", "...a magnifying glass. His eye, huge", "\u2014", s2b),
        (7.9, 9.0, "2", "through the lens: heart = her lips", "\u2014 (smug point)", s2c),
        (9.0, 11.3, "3", "the lamp: she files, never looks up", "2 Sof\u00eda", s3),
        (11.3, 13.3, "4", "the witness: a silent click", "\u2014 (click)", s4),
        (13.3, 14.5, "5", "CCTV wide: the lean", "\u2014", wide),
        (14.5, 15.3, "5", "ENHANCE x2: the corner hooks it", "\u2014", catch),
        (15.3, 16.5, "5", "ENHANCE x4: the peel (1.2 s)", "\u2014", peel),
        (16.5, 17.4, "5", "snapped on: freeze 0.6 s", "3 robot", stuck),
        (17.4, 18.1, "5", "wide: he walks off (0.7 s)", "\u2014", exitf),
        (18.1, 18.6, "6", "ECU: his eyes drop", "\u2014 (no music)", s6a),
        (18.6, 19.0, "6", "ECU: the empty lapel", "\u2014", s6b),
        (19.0, 19.5, "6", "the 12 degree tilt, brim down", "\u2014", s6c),
        (19.5, 21.6, "7A", "she shows him the heart", "4 Pam", s7a),
        (21.6, 22.3, "7B", "her fingertips; he looks down", "\u2014", s7b1),
        (22.3, 24.0, "7B", "pause, eyes up, the corner (0.8\u20131 s)", "\u2014", s7b4),
        (24.0, 27.2, "8", "the finger; 0.4 s silence after", "5 Don", s8),
        (27.2, 28.0, "9", "low angle, hand in pocket", "VO 6 starts", s9a),
        (28.0, 29.2, "9", "the shadow grows over him", "VO 6 cut off \u00b7 DONNIE! starts", s9b),
        (29.2, 31.2, "10A", "smash cut to colour: Mom looms", "7 Mom \u00b7 music cut dead", s10a),
        (31.2, 32.4, "10B", "in bed: the stare (HEART0 again)", "\u2014", s10b1),
        (32.4, 33.4, "10B", "a glance down at the bunny", "\u2014", s10b2),
        (33.4, 34.6, "10B", "he slides the pink toy magnifier under", "\u2014 \u2192 loops to frame 0", s10b3),
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
    corp(c, "UPTIMEZ INC. · STORYBOARD · OFFICE NOIR v2", 920, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()
    cols, w, gx, gy = 7, 152, 14, 108
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
    lc = loop_check(P[1][5], P[-1][5])
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
    t = main(sys.argv[1] if len(sys.argv) > 1 else "on_sb_sheet_v2.png",
             sys.argv[2] if len(sys.argv) > 2 else "on_sb_loop_v2.png")
    print("total", t)
