"""Storyboard for "Office Noir", v3 (on_sb_v2.py = v2, on_sb_v1.py = v1, kept). v3 after the v2 audit: the CCTV
snag in three clean states at the same x4 framing (on the lapel / SNAG, the corner catches the tip / the heart stays
on the monitor, the lapel empty), then the exit wide with two CCTV circles (the heart on the monitor, the empty
lapel); shot 6 is the humiliation: eyes drop, the empty lapel, his eyes SNAP up (the mask cracks for 0.3 s), then
the cynic mask back on with a sweat drop (the 12 degree tilt is gone); Pam holds her fingertips on the lapel, then
his eyes go from her hand to her eyes; Don starts "Sofia-" in the lens POV and she cuts him off; the flask and the
informant are bigger in the montage, and the flask has a bendy straw (the twin of the milk carton's); 10B shows the
bunny sitting on the blanket and the strawberry milk on it, both whole; "DONNIE!" is shouted once, over the shadow
in shot 9, and 10A is "Up. Time for work."; the recovery is trimmed. About 31.6 s.
v2 notes: Storyboard for "Office Noir", v2 (on_sb_v1.py = v1, kept). v2 after the review: shot 1 opens on one lightning
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

W2, H2 = 1200, 1990
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
    if beat == 1:
        d.don_pj(kk, x, feet, s, face="frozen", lift=6, bunny=False)
    else:
        d.don_pj(kk, x, feet, s, face="deflated", look=(-0.6, 0.95), lift=6, bunny=False)
    st.sweat_drop(c, x + 46 * s, feet + (d.HY - 20) * s, 0.9 * s / 2)
    bl = HEART0[1] + 92                                                              # the blanket's edge
    if beat == 3:                                                                    # the toy magnifier going under
        pr.magnifier(c, 420, bl + 10, 34, rot=-2.4, toy=True)
        kit.ellipse(kk, 380, bl - 14, 26, 20, d.SKIN, 852, shadow=False, lw=2.4)
    rect(kk, -20, bl, 600, 300, (0.70, 0.84, 0.94), 811)
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(-20, bl, 600, 20); c.fill()                  # the sheet's fold
    pr.bunny(kk, 100, bl + 46, 1.9, mode="pink")                    # v3: the informant, whole, on the blanket
    pr.milk(kk, 486, bl + 34, 2.0)                                   # v3: the drink, whole, straw and all
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


# ---- v3 montage: the props bigger; the flask has a bendy straw (the milk carton's twin) ------------------------

def k_drink(kk):
    c = kk.c
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(260, 470, 20, 260, 470, 460)
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.9); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    rect(kk, -20, 700, 580, 400, (0.20, 0.17, 0.15), 901)
    s = 4.6
    c.save(); c.translate(270, 560); c.rotate(-0.08); c.scale(s, s)          # the straw first, out of the open neck
    c.set_line_cap(1)
    for col, w in ((INK, 8.5), ((0.92, 0.92, 0.92), 6.0)):
        c.set_source_rgb(*col); c.set_line_width(w)
        c.move_to(-1, -40); c.line_to(-1, -66); c.curve_to(-1, -74, 4, -78, 12, -78); c.line_to(22, -78); c.stroke()
    c.set_source_rgb(0.45, 0.45, 0.45); c.set_line_width(2.2)
    for yy in (-46, -54, -62):
        c.move_to(-4, yy); c.line_to(2, yy - 3); c.stroke()
    c.set_line_cap(0); c.restore()
    pr.flask(kk, 270, 560, s, open_=True, glove=True)
    psh.caption(c, "ONE DRINK.", 24, 40)


def k_informant(kk):
    c = kk.c
    c.set_source_rgb(0.04, 0.04, 0.05); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.LinearGradient(0, 960, 0, 220)
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.9); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0.0)
    c.set_source(g); c.move_to(70, 960); c.line_to(470, 960); c.line_to(350, 220); c.line_to(190, 220); c.close_path()
    c.fill()
    rect(kk, -20, 820, 580, 300, (0.18, 0.16, 0.15), 902)
    pr.bunny(kk, 270, 830, 4.1, mode="noir", menace=True)
    psh.caption(c, "ONE INFORMANT.", 24, 40)


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
    zc = (P.CORNER[0] + 10, P.CORNER[1] + 30)                         # v3: one x4 framing for all three states
    on = P.cctv(pr.enhance(P.frame5(0.0), zc, 3.2, 2, "ENHANCE x4"), "MON 08:59:15")
    snag = P.cctv(pr.enhance(P.frame5(0.33), zc, 3.2, 2, "ENHANCE x4"), "MON 08:59:15")
    sn = cairo.Context(snag)                                          # v3: the snag made loud: the tip pulled taut
    def scr(pt):
        return 270 + (pt[0] - zc[0]) * 3.2, 480 + (pt[1] - zc[1]) * 3.2
    lap = P.lapel_at(12)
    tip = scr((lap[0] + 0.95 * P.SIZE, lap[1] - 0.55 * P.SIZE)); cor = scr(P.CORNER)
    sn.set_line_cap(1)
    sn.set_source_rgb(0, 0, 0); sn.set_line_width(13); sn.move_to(*tip); sn.line_to(*cor); sn.stroke()
    sn.set_source_rgb(1, 1, 1); sn.set_line_width(8); sn.move_to(*tip); sn.line_to(*cor); sn.stroke()
    sn.set_source_rgb(0.95, 0.95, 0.95); sn.set_line_width(4)
    for a in (-2.2, -1.6, -1.0, 0.2, 0.8):
        sn.move_to(cor[0] + math.cos(a) * 26, cor[1] + math.sin(a) * 26)
        sn.line_to(cor[0] + math.cos(a) * 48, cor[1] + math.sin(a) * 48); sn.stroke()
    sn.set_line_cap(0)
    gone = P.cctv(pr.enhance(P.frame5(1.0), zc, 3.2, 2, "ENHANCE x4"), "MON 08:59:16")   # same lean: lapel empty
    stuck = pr.enhance(P.frame5(1.0, lean=4), (P.END[0] - 20, P.END[1] + 60), 1.25, 1, None)
    P.cctv(stuck, "MON 08:59:16", rec=False)
    cs = cairo.Context(stuck)
    cs.select_font_face("DejaVu Sans Mono", 0, 1); cs.set_font_size(26); cs.set_source_rgb(0.95, 0.95, 0.95)
    cs.move_to(380, 112); cs.show_text("II 0.6 s")
    P.bubble(cs, "Suspect\nidentified.", 250, 640, tail=(300, 120), size=36)
    exitf = P.cctv(P.frame5(1.0, walk=True), "MON 08:59:17")
    ce = cairo.Context(exitf)                                         # v3: the robot circles both ends of the crime
    ce.set_source_rgb(0.95, 0.95, 0.95); ce.set_line_width(3); ce.set_dash([10, 6])
    ce.arc(P.END[0], P.END[1], P.SIZE * 1.9, 0, 2 * math.pi); ce.stroke()
    lx, ly = 80 + d.LAPEL_HEART[0] * P.S, P.FEET + 30 + d.LAPEL_HEART[1] * P.S
    ce.arc(lx, ly, P.SIZE * 1.9, 0, 2 * math.pi); ce.stroke(); ce.set_dash([])
    ce.move_to(lx + P.SIZE * 1.4, ly - P.SIZE * 1.4); ce.line_to(P.END[0] - P.SIZE * 1.4, P.END[1] + P.SIZE * 1.4); ce.stroke()
    return wide, on, snag, gone, stuck, exitf


def b_shot4(footage):
    s4 = surf(); psh.shot4(Ctx(cairo.Context(s4), 0), footage); eng.accent_pass(s4, ACC); return s4


def k6(kk, beat):
    """v2: ECU of his eyes; ECU of the empty lapel; the 12 degree tilt with the brim coming down."""
    c = kk.c
    c.set_source_rgb(0.20, 0.20, 0.21); c.rectangle(0, 0, 540, 960); c.fill()
    if beat == "eyes":                                                # v3: still the cynic, the eyes drop
        s = 8.0; d.don_noir(kk, 270, 480 - d.HY * s, s, face="cynic", look=(0.3, 0.95), brim=0.3, outline=True)
    elif beat == "lapel":
        s = 7.0; d.don_noir(kk, 270 - d.LAPEL_HEART[0] * s, 480 - d.LAPEL_HEART[1] * s, s, face="neutral", brim=0.3,
                            outline=True)
    elif beat == "snap":                                              # v3: the eyes snap up, the mask cracks
        s = 8.0; d.don_noir(kk, 270, 470 - d.HY * s, s, face="frozen", brim=0.0, outline=True)
        c.set_source_rgb(0.95, 0.95, 0.95); c.set_line_width(7); c.set_line_cap(1)          # shock ticks
        for x0, y0, x1, y1 in ((40, 560, 8, 600), (40, 640, 4, 650), (500, 560, 532, 600), (500, 640, 536, 650)):
            c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        c.set_line_cap(0)
    elif beat == "mask":                                              # v3: the cynic mask back on, one drop gives him away
        s = 8.0; d.don_noir(kk, 270, 480 - d.HY * s, s, face="cynic", brim=0.6, outline=True)
        st.sweat_drop(c, 470, 330, 3.0)
    elif beat in ("down", "up"):                                      # v3: in 7B, her hand, then her eyes
        s = 8.0; d.don_noir(kk, 270, 480 - d.HY * s, s, face="neutral", brim=0.3, outline=True,
                            look=(-0.1, 0.95) if beat == "down" else (-0.5, -0.6))
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
    for beat in (1, 4):                                              # v3: beat 1 now held 1.0 s (her fingertips stay)
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


def shout(sf, text, size=64):
    """An off-screen shout: a jagged white burst with the word, top of the frame (the voice from outside the room)."""
    c = cairo.Context(sf)
    c.select_font_face(psh.TYPE, 0, 0); c.set_font_size(size)
    w = c.text_extents(text).x_advance
    cx, cy, rx, ry = 270, 150, w / 2 + 50, 70
    c.new_path()
    for i in range(24):
        a = i * math.pi / 12; r = 1.0 if i % 2 == 0 else 0.78
        c.line_to(cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r)
    c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(0, 0, 0); c.set_line_width(4); c.stroke()
    c.move_to(cx - w / 2, cy + size * 0.35); c.show_text(text)
    return sf


def two_cards(sf, a, b, size=34):
    c = cairo.Context(sf)
    psh.caption(c, a, 24, 36, size)
    psh.caption(c, b, 24, 36 + size * 1.9, size)
    return sf


def build():
    d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
    s1f = noir(k1, lambda c: (l1(c), st.flash(c, 0.5), st.blinds(c, 0, 120, 540, 700, -0.30, 22, 10, 0.5)))
    s1 = two_cards(noir(k1, l1), "Monday. Somebody", "left Pam a heart.")
    drink = noir(k_drink)
    inf = noir(k_informant)
    boss = noir(setsh.kboss, setsh.lboss)
    s2a, s2b, s2c = b_shot2()
    s2c = say(s2c, "Sof\u00eda\u2014", 300, 700, (70, 120), 40)
    s3 = b_shot3()
    wide, on, snag, gone, stuck, exitf = b_shot5()
    s4 = b_shot4(wide)
    s6a, s6b, s6c, s6d = b_shot6("eyes"), b_shot6("lapel"), b_shot6("snap"), b_shot6("mask")
    d.FEDORA_RIM = True
    s7d, s7u = b_shot6("down"), b_shot6("up")
    s7a, s7b1, s7b4 = b_shot7()
    d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
    s8 = say(noir(k8, l8), "I object to\nthat wording.", 40, 60, (110, 120), 36)
    s9a = two_cards(noir(lambda kk: k9(kk, 0.0), setsh.l9), "Nobody tells me", "what to—")
    s9b = noir(lambda kk: k9(kk, 1.0), setsh.l9)
    shout(s9b, "DONNIE!")                                              # v3: shouted once, over the shadow
    s10a = say(colour(setsh.k10a), "Up.\nTime for work.", 30, 50, (300, 110), 36)
    s10b1, s10b2, s10b3 = (colour(lambda kk: k10b(kk, 1)), colour(lambda kk: k10b(kk, 2)),
                           colour(lambda kk: k10b(kk, 3)))
    d.FEDORA_BAND, d.FEDORA_RIM = None, False
    P = [
        (0.0, 0.4, "1", "LIGHTNING: one flash, the heart lit", "thunder \u00b7 rain", s1f),
        (0.4, 3.0, "1", "frame 0 settles; push in on the heart", "VO 1 \u00b7 sting on \"Unsigned.\"", s1),
        (3.0, 3.9, "M", "ONE DRINK: the flask, bigger, a bendy straw", "VO M (one) \u00b7 a metal click", drink),
        (3.9, 4.8, "M", "ONE INFORMANT: bigger, lit from below", "VO M (two)", inf),
        (4.8, 5.7, "M", "ONE BOSS: the curler shadow", "VO M (three) \u00b7 sting", boss),
        (5.7, 6.3, "2", "the draw: hand inside the coat, like a gun", "\u2014 \u00b7 a metallic CLICK", s2a),
        (6.3, 7.2, "2", "...a magnifying glass. His eye, huge", "\u2014", s2b),
        (7.2, 8.2, "2", "through the lens: heart = her lips; he starts", "Don: \"Sof\u00eda\u2014\"", s2c),
        (8.2, 10.2, "3", "she cuts him off; files, never looks up", "2 Sof\u00eda", s3),
        (10.2, 11.8, "4", "the witness: a silent click", "\u2014 (click)", s4),
        (11.8, 12.8, "5", "CCTV wide: the lean", "\u2014", wide),
        (12.8, 13.3, "5", "x4 state 1: the heart on his lapel, the corner at it", "\u2014", on),
        (13.3, 14.0, "5", "x4 state 2: the corner catches the tip", "SNAG (sfx)", snag),
        (14.0, 14.7, "5", "x4 state 3: the heart stays, the lapel empty", "a soft pop", gone),
        (14.7, 15.7, "5", "snapped on: freeze", "3 robot", stuck),
        (15.7, 16.5, "5", "wide: he walks off; both ends circled", "\u2014", exitf),
        (16.5, 17.0, "6", "ECU: his eyes drop", "\u2014 (no music)", s6a),
        (17.0, 17.5, "6", "ECU: the empty lapel. Hold.", "\u2014", s6b),
        (17.5, 17.8, "6", "SNAP: eyes up, the mask cracks", "a dry click", s6c),
        (17.8, 18.3, "6", "the cynic mask back on; one drop", "\u2014", s6d),
        (18.3, 20.3, "7A", "she shows him the heart, calm", "4 Pam", s7a),
        (20.3, 21.3, "7B", "her fingertips stay on his lapel", "\u2014", s7b1),
        (21.3, 21.65, "7B", "his eyes: down to her hand...", "\u2014", s7d),
        (21.65, 22.0, "7B", "...up to her eyes", "\u2014", s7u),
        (22.0, 22.8, "7B", "pause, the corner of her mouth", "\u2014", s7b4),
        (22.8, 25.2, "8", "the finger; 0.4 s silence after", "5 Don", s8),
        (25.2, 25.9, "9", "low angle, hand in pocket: full noir again", "VO 6 starts", s9a),
        (25.9, 26.9, "9", "the shadow grows; cut off at his peak", "VO 6 cut off \u00b7 Mom: DONNIE!", s9b),
        (26.9, 28.5, "10A", "smash cut to colour: Mom looms", "7 Mom \u00b7 music cut dead", s10a),
        (28.5, 29.6, "10B", "in bed: the stare (HEART0 again)", "\u2014", s10b1),
        (29.6, 30.4, "10B", "a glance down at the bunny", "\u2014", s10b2),
        (30.4, 31.6, "10B", "he slides the pink toy magnifier under", "\u2014 \u2192 loops to frame 0", s10b3),
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
    corp(c, "UPTIMEZ INC. · STORYBOARD · OFFICE NOIR v3", 920, 34, 9.5, col=GREY, bold=True)
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
    t = main(sys.argv[1] if len(sys.argv) > 1 else "on_sb_sheet_v3.png",
             sys.argv[2] if len(sys.argv) > 2 else "on_sb_loop_v3.png")
    print("total", t)
