"""v2 (20 Nov), from the first motion test (two cold viewers, cs_test_v1): the handshake wasn't seen ("pushing his arm
out", "pointing") and the mic read as an adjustment but a cold one ("shush", "do your job"). So: the handshake framed
waist-up on the two men, Pam at the edge, a big clasp and a bigger pump; Pam's face fond from the start and smiling after;
the lift slower (5 drawings); the tap marks off his face (one viewer saw a wink); Don talks with his eyes kept shut
(v1's "grin" popped his eyes three times: "surprised").
ONE STAR (episode 11, folder customer-success): motion, test shots first (20 Nov, Tomas: "plan detailed ... proceed").
Two beats that failed as stills in four rounds of cold viewers, animated so a cold viewer can judge them in motion:
  5.4a  the handshake: Don pumps the Client's hand with both of his; the Client looks away at Pam, then pulls free;
  5.4b  the mic: Don's headset boom hangs crooked; Pam's fingers lift it, it overshoots, springs back, settles at his
        mouth; a tap; her hand leaves; Don never looks;
  5.4c  Don says "Customer success." into the mic she fixed (the reorder: she sets him up to take the credit).
  3.5b  the set-up: Don's flash of panic jerks his head and the boom swings loose (from here it hangs crooked).
Drawn at 12 drawings a second on episode 10's set (the storyboard code, board v7's cameras), output at 30 fps.
  python3 cs_anim.py test [out_dir]  ->  cs_test_v1.mp4 (5.3 > 5.4a > 5.4b > 5.4c > 6.1, no sound, no captions),
                                        cs_test_v1_strip.png (every drawing, numbered) and cs_test_v1_feed.png (270 px)
  python3 cs_anim.py setup [out_dir] ->  cs_test_v1_setup.png (3.5b, the boom swinging loose)"""
import math
import os
import subprocess
import sys
import cairo
import fs_storyboard as sb
import cs_props as cp
import cs_board as b1
import cs_board2 as b2
import cs_board3 as b3
from cs_board import S, at, base
from cs_board2 import pam_at, phone_in
from kit import Ctx, INK, ellipse

V = "v2"
# v4 (20 Nov, Tomas and an outside review of test v3): Pam's arm is a real arm, from her own shoulder, two segments of
# fixed length bent at the elbow (IK), redrawn over Don; she stands close enough to reach and leans in; one hand with a
# thumb pinching the boom; she pulls back elbow first. Don's open mouth covers his smile (v3 showed two mouths). Don
# talks with his arms down (the vest pose looped). The Client holds his phone in his hand (v3's floated). The contact
# card shows Pam herself (cs_props.REAL_PAM). cs_anim_v2.py is v1-v3.
HI = [1]                                                   # 2 = native 1080 (drawn at 2x with set_device_scale)
CUT_HANDSHAKE = [False]                                    # v3 (Tomas): the handshake failed 4 of 4 cold viewers: cut                                                   # cs_anim_v1.py is the v1 test, kept
DPS = 12                                                   # drawings per second
SKIN_PAM = (0.96, 0.82, 0.70)
PURPLE = (0.40, 0.26, 0.55)
BOOM = (0.45, 0.45, 0.50)
CROOKED = (47, 10, 72, 22, 84, 48, 78, 78)                 # the boom, head-local: hanging out and down at his collar
CROOKED4 = (47, 10, 62, 20, 68, 38, 62, 58)                # v4: shorter (a viewer: "stretched to her shoulder")
MOUTH = (47, 10, 40, 40, 18, 40, 10, 32)                   # at his mouth (fs_storyboard.don_signs "down")
UP = (47, 10, 58, -4, 58, -26, 52, -40)                    # along his head ("up")


def kit_skin_don():
    import kit
    return kit.PEOPLE["DON"]["skin"]


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def boom_pts(t, frm=CROOKED, to=MOUTH):
    """t 0 = frm, 1 = to; past 1 it overshoots along the same path."""
    return lerp(frm, to, t)


class Don:
    """Draws Don's signs with a boom given as points (instead of "up"/"down") for the shot being drawn."""
    def __init__(self, pts, talk=0.0):
        self.pts, self.talk = pts, talk

    def __enter__(self):
        self.orig = sb.don_signs
        pts, talk = self.pts, self.talk

        def signs(k, head, s, mic, hair):
            c = k.c
            hx, hy = head
            c.save(); c.translate(hx, hy); c.scale(s, s); c.set_line_cap(1)
            if talk:                                                          # v4: the smile covered, one open mouth
                ellipse(k, 0, 33, 19, 11, kit_skin_don(), 713, shadow=False, outline=False)
                ellipse(k, 0, 32, 10, 4 + 6 * talk, (0.45, 0.12, 0.12), 712, shadow=False, lw=2)
            for w, col in ((6, INK), (3.2, BOOM)):
                c.set_source_rgb(*col); c.set_line_width(w)
                c.move_to(pts[0], pts[1]); c.curve_to(*pts[2:]); c.stroke()
            ellipse(k, pts[6], pts[7], 6.5, 5, (0.12, 0.12, 0.14), 711, shadow=False, lw=1.6)
            c.set_source_rgb(*INK); c.set_line_width(4.6)                    # his one hair, curled
            c.move_to(2, -50); c.curve_to(0, -74, 24, -84, 20, -67); c.curve_to(17, -57, 7, -64, 14, -70); c.stroke()
            c.restore()
        sb.don_signs = signs
        return self

    def __exit__(self, *e):
        sb.don_signs = self.orig


# ---- 5.4a the handshake --------------------------------------------------------------------------------------------------

def m5_4a(k, d):
    """19 drawings (1.6 s). d 0 Don steps in, hands out; 2 the grab; 3-14 three pumps of 4; 15-18 the Client pulls free,
    eyes down to his phone; Don still pumping air, eyes shut, delighted."""
    free = d >= 15
    pump = (0, -1, 0, 1)[(d - 3) % 4] if 3 <= d < 15 else 0                # up, mid, down, mid
    reach = min(1.0, d / 2.0)
    du = -40 - 25 * reach + 20 * pump                                      # Don's two arms to the middle, pumping
    dpose = (du, 30 - 10 * reach, -38 - 20 * reach + 20 * pump, -60)
    cpose = (-10, 5, 10, -5) if free else (-10, 5, 55, 15)                 # his right hand out (limp), or back
    st = {}

    def ex(k_, o):
        c = k_.c
        dh = sorted(o["don"]["hands"])
        mx, my = (dh[0][0] + dh[1][0]) / 2 - 4, (dh[0][1] + dh[1][1]) / 2
        if free:
            for (px, py) in dh:                                            # pumping nothing
                ellipse(k_, px, py, 7, 7, (0.96, 0.80, 0.66), 990, lw=1.6)
            return
        ch = max(o["client"]["hands"])                                     # his limp forearm up to the clasp
        c.set_line_cap(1)
        for w, col in ((14, INK), (10.5, (0.42, 0.44, 0.24))):
            c.set_source_rgb(*col); c.set_line_width(w); c.move_to(*ch); c.line_to(mx - 6, my + 2); c.stroke()
        if d >= 2:
            ellipse(k_, mx - 6, my + 2, 12, 11, (0.86, 0.66, 0.50), 983, lw=2)       # his hand, inside Don's two
            for (px, py) in dh:
                ellipse(k_, px, py, 11.5, 10.5, (0.96, 0.80, 0.66), 984 + int(px), lw=2)
        if 3 <= d < 15:                                                    # the shake: arcs above and below the clasp
            c.set_source_rgb(*INK); c.set_line_width(2.6)
            for sy in (-1, 1):
                c.new_path(); c.arc(mx - 4, my, 30, 3.7, 5.7) if sy < 0 else c.arc(mx - 4, my, 30, 0.6, 2.5); c.stroke()
        st["head"] = o["client"]["head"]

    S(k, (372, 712, 2.1), auto=False, mic="down", portrait=False, extra=ex,
      pre=pam_at(282, front=True, face="pleased", look=(1, 0), glasses="up"),
      **base(rb=False, sf=False, pm=False, mm=False,
             cl=at("client", x=362, pose=cpose, face="warm" if not free else "plain", look=(-1, 0) if not free else (0.4, 1)),
             dn=at("don", x=458, pose=dpose, face="happy", look=(-1, -0.3))))
    if free:
        phone_in(k, "client", dx=0.8, dy=1.6, lit=True, s=1.0)


# ---- 5.4b the mic --------------------------------------------------------------------------------------------------------

BOOM_T = [0, 0, 0, 0, 0, 0.15, 0.40, 0.70, 1.0, 1.25, 0.85, 1.07, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]   # v2: a slower lift
REACH = [0, 0, 0.45, 0.85, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.9, 0.6, 0.3, 0, 0]


MIC_CAM = (445, 590, 2.6)                                  # v6: the plaque whole and under the bar, the portrait above it
BREATH = 1.5                                               # v6 (lesson 72): everyone breathes, a 1.5 s cycle


def breath(d, phase=0.0, amp=0.008):
    return 1.0 + amp * math.sin(2 * math.pi * (d / float(DPS) / BREATH + phase))


class Breathe:
    """Scales a character's drawing a hair taller and back about its feet (the chest rises), by patching its draw
    function in fs_storyboard for one shot."""
    def __init__(self, name, sy):
        self.name, self.sy = name, sy

    def __enter__(self):
        self.orig = getattr(sb, self.name)
        orig, sy = self.orig, self.sy

        def w(k, x, feet, *a, **kw):
            c = k.c
            c.save(); c.translate(x, feet); c.scale(1.0, sy); c.translate(-x, -feet)
            try:
                return orig(k, x, feet, *a, **kw)
            finally:
                c.restore()
        setattr(sb, self.name, w)
        return self

    def __exit__(self, *e):
        setattr(sb, self.name, self.orig)                                  # v5: the room in shot: OUR FIRST CLIENT over Don (was a bare wall)
PAM_X, PAM_LEAN = 526, (0, 0, -2, -3, -5, -6, -6, -6, -6, -6, -6, -6, -6, -5, -3, -2, 0, 0, 0)   # v4: no head on his shoulder
LN = 48                                                    # kit.arm: upper arm and forearm, fixed
REACH = [0, 0, 0.25, 0.6, 0.9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.75, 0.45, 0.2, 0, 0]


def _ease(t):
    return t * t * (3 - 2 * t)


def _don_head():
    """Where Don's head is in this shot (a dry run of the same scene)."""
    cam = MIC_CAM7 if V7[0] else MIC_CAM
    if _don_head.__dict__.get("cam") != cam:
        _don_head.__dict__.pop("head", None); _don_head.cam = cam
    if "head" not in _don_head.__dict__:
        got = {}
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4); k = Ctx(cairo.Context(s), 0)
        with b3._ep11v3(), Don(CROOKED4):
            S(k, cam, auto=False, mic="down", portrait="hang", extra=lambda k_, o: got.update(h=o["don"]["head"]),
              **base(cl=False, rb=False, sf=False, mm=False, pm=False, dn=at("don", x=450, pose="stand", face="happy", look=(-1, 0))))
        _don_head.head = got["h"]
    return _don_head.head


def _pam_arm(d, pts):
    """Her near (screen-left) arm: shoulder angles from IK, the hand on the boom's middle, or at rest at her side."""
    from cand_bc import ik
    hx, hy = _don_head()
    sd = sb.SC["don"]
    q = pts
    gx = 0.125 * q[0] + 0.375 * q[2] + 0.375 * q[4] + 0.125 * q[6]
    gy = 0.125 * q[1] + 0.375 * q[3] + 0.375 * q[5] + 0.125 * q[7]
    grip = (hx + gx * sd, hy + gy * sd)                                         # in the scene
    s, feet, lean = sb.SC["pam"], sb.F + 6, math.radians(PAM_LEAN[d])
    import kit
    bt = -300 * kit.PEOPLE["PAM"]["h"] + 78
    sh = (-40, bt + 14)
    vx, vy = grip[0] - PAM_X, grip[1] - feet                                    # the grip in her own (unleaned, unscaled) frame
    lx = (vx * math.cos(-lean) - vy * math.sin(-lean)) / s
    ly = (vx * math.sin(-lean) + vy * math.cos(-lean)) / s
    rest = (sh[0] + math.sin(math.radians(-8)) * 2 * LN, sh[1] + math.cos(math.radians(-8)) * 2 * LN)
    r = _ease(REACH[d])
    tx, ty = lerp(rest, (lx, ly), r)
    a1, a2 = ik(sh[0], sh[1], tx, ty, LN, LN, -1)                              # the elbow toward Don, below the boom
    return (a1, a2), sh, s, feet, PAM_LEAN[d]


def m5_4b(k, d):
    """19 drawings, tight on Don's head, Pam close at his side. d 0-1 crooked, Don beaming at the Client off frame;
    2-4 her arm comes up from her side, elbow bending; 5-13 she pinches the boom's middle and lifts it, it overshoots,
    springs back, settles at his mouth; 13 a tap; 14-18 she lets go and her arm comes back down, elbow first."""
    import pam_bc as pb
    t = BOOM_T[d]
    pts = boom_pts(t, frm=CROOKED4)
    (a1, a2), sh, s, feet, lean = _pam_arm(d, pts)
    pose = (a1, a2, 8, 0)

    def pam_pre(k_):
        c_ = k_.c
        c_.save(); c_.translate(PAM_X, feet); c_.scale(1.0, breath(d, 0.5)); c_.translate(-PAM_X, -feet)
        pb.pam(k_, PAM_X, feet, s, pose, "pleased", (-1, -0.3), glasses="up", lean=lean)
        c_.restore()

    def ex(k_, o):                                                               # the same arm again, over Don
        if REACH[d] <= 0:
            return
        c = k_.c
        c.save(); c.translate(PAM_X, feet); c.rotate(math.radians(lean)); c.scale(s, s); c.set_line_cap(1)
        dd = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
        ex_, ey_ = sh[0] + dd(a1)[0] * LN, sh[1] + dd(a1)[1] * LN
        wx, wy = ex_ + dd(a1 + a2)[0] * LN, ey_ + dd(a1 + a2)[1] * LN
        from kit import cut
        for (ax, ay, bx, by), col in (((sh[0], sh[1], ex_, ey_), PURPLE), ((ex_, ey_, wx, wy), SKIN_PAM)):   # sleeve up to the elbow
            ang = math.atan2(by - ay, bx - ax); nx, ny = -math.sin(ang) * 8.5, math.cos(ang) * 8.5
            cut(k_, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
        c.set_source_rgb(*PURPLE); c.set_line_width(0)
        ellipse(k_, ex_, ey_, 9, 9, PURPLE, 997, shadow=False, lw=2)                  # the elbow, the shoved-up cuff
        ang = math.atan2(wy - ey_, wx - ex_)
        ellipse(k_, wx, wy, 11, 9.5, SKIN_PAM, 999, shadow=False, lw=2)                # the hand
        if REACH[d] >= 1 and 5 <= d <= 13:                                            # thumb and finger round the boom
            px, py = -math.sin(ang), math.cos(ang)
            ellipse(k_, wx + px * 9, wy + py * 9, 5, 4, SKIN_PAM, 996, shadow=False, lw=1.6)
            ellipse(k_, wx - px * 9, wy - py * 9, 5, 4, SKIN_PAM, 995, shadow=False, lw=1.6)
        c.restore()
        if d == 13:                                                               # the tap: marks below the boom, off his face
            hx, hy = o["don"]["head"]; sd = sb.SC["don"]
            c.set_source_rgb(*INK); c.set_line_width(1.2)
            for a_ in (14, 24):
                c.move_to(hx + a_ * sd, hy + 44 * sd); c.line_to(hx + (a_ + 3) * sd, hy + 52 * sd); c.stroke()

    with Don(pts), Breathe("don", breath(d)):
        S(k, MIC_CAM7 if V7[0] else MIC_CAM, auto=False, mic="down", portrait="hang", extra=ex, pre=pam_pre,
          **base(cl=False, rb=False, sf=False, mm=False, pm=False, dn=at("don", x=450, pose="stand", face=_m5_4b_face[0], look=(-1, 0))))


# ---- 5.4c "Customer success." -------------------------------------------------------------------------------------------

def m5_4c(k, d):
    """16 drawings (1.3 s): the same framing, the boom at his mouth; he swells and speaks into it (mouth on twos)."""
    talk = (0.0, 1.0, 0.5, 1.0)[(d // 2) % 4] if 3 <= d < 14 else 0.0       # v2: the mouth on twos, eyes shut
    face = "happy"
    with Don(MOUTH, talk), Breathe("don", breath(d + 19, 0.0, 0.012 if 3 <= d < 14 else 0.008)):
        S(k, MIC_CAM7 if V7[0] else MIC_CAM, auto=False, mic="down", portrait="hang",
          pre=lambda k_: __import__("pam_bc").pam(k_, PAM_X, sb.F + 6, sb.SC["pam"], "stand", "pleased", (-1, -0.3), glasses="up"),
          **base(cl=False, rb=False, sf=False, mm=False, pm=False, dn=at("don", x=450, pose="stand", face=face, look=(-1, 0))))


# ---- 3.5b the set-up: the boom swings loose -----------------------------------------------------------------------------

SWING = [0.0, 0.0, -0.4, 0.55, 1.15, 0.85, 1.0, 1.0]       # from "down" (at his mouth) to CROOKED, with a bounce


def m3_5b(k, d):
    pts = lerp(MOUTH, CROOKED4, SWING[d])
    with Don(pts):
        S(k, (452, 640, 3.0), auto=False, mic="down", portrait=False,
          **base(cl=False, sf=False, rb=False, pm=False, mm=False,
                 dn=at("don", face="panic" if d >= 2 else "smug", look=(-1, 0) if d < 2 else (-1, -0.3))))


# ---- the test clip ------------------------------------------------------------------------------------------------------

def m6_1(k, d):
    """At the door, his phone held in front of his chest in both hands, eyes down on it (v6: v5 held it off to the side
    and looked at us); he breathes."""
    def ex(k_, o):
        (lx, ly), (rx, ry) = sorted(o["client"]["hands"])
        mx, my = (lx + rx) / 2, (ly + ry) / 2 - 6
        c = k_.c
        c.save(); c.translate(mx, my); c.rotate(-0.05)
        c.set_source_rgba(0.6, 0.9, 1.0, 0.30); c.arc(0, -10, 26, 0, 6.3); c.fill()
        from kit import rect as rect_
        rect_(k_, -11, -22, 22, 36, (0.10, 0.11, 0.14), 997, lw=1.6)
        c.set_source_rgb(*cp.LIGHT); c.rectangle(-9, -19, 18, 30); c.fill()
        c.restore()
        for hx, hy in ((lx, ly), (rx, ry)):
            ellipse(k_, hx, hy, 7, 6.5, (0.86, 0.66, 0.50), 998 + int(hx), lw=1.6)
    with Breathe("client", breath(d)):
        S(k, (232, 600, 2.7), auto=False, portrait=False, extra=ex,
          **base(rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", pose=(-30, 125, 30, -125), face="plain", look=(0.1, 1))))


def m5_3(k, d):
    """v6: the card is live: SAVE (grey) for 4 drawings, then his thumb taps it and it turns green, SAVED."""
    cp.phone(k, "contact3")
    c = k.c
    if d < 5:
        from kit import rect as rect_
        rect_(k, 118, 650, 304, 90, (0.72, 0.74, 0.78) if d < 4 else (0.55, 0.80, 0.60), 990, shadow=False, lw=2)
        cp.T(c, "SAVE", 270, 710, 42, col=(1, 1, 1))
    if 2 <= d <= 5:                                                             # his thumb comes down on it
        sb.thumb(k, 300, 690 + (0 if d >= 4 else 40), 1.5, sb.SKIN_CL, oil=True, ang=2.6, who="client")


def m6_1b(k, d):
    """v6, insert: his oily thumb types the UPDATE (thumb 3), the struck line and "Pam found it." on screen."""
    old = cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0]
    cp.REPLY_BIG[0] = cp.SAME_LAYOUT[0] = cp.GARAGE_LOGO[0] = True
    try:
        cp.phone2(k, "update")
    finally:
        cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0] = old
    tx = (300, 330, 280, 320)[(d // 2) % 4]
    sb.thumb(k, tx, 760 - (8 if d % 2 else 0), 1.6, sb.SKIN_CL, oil=True, ang=2.7, who="client")


# ---- v7 (outside review, the four points that correlate; v6 is kept in cs_anim_v6.py) ------------------------------------

V7 = [False]
MIC_CAM7 = (458, 600, 2.4)                                 # v7: Pam whole in frame (v6 cut her in half at the right edge)
M7 = [0, 0, 0, 0] + list(range(1, 19)) + [18, 18, 18]       # v7 5.4b: crooked held 5 drawings, then straight held after she lets go
TAP7 = 13                                                  # from the tap on, Don reacts (not before the contact)


def m5_4b7(k, d):
    """v7: 25 drawings. The crooked boom holds long enough to read; Don only reacts after her tap (he swells, smug);
    the straight boom holds after her hand is gone: before, contact, result."""
    s = M7[d]
    smug = s >= TAP7 and d > 4
    with Breathe("don", 1.0 + (0.02 if smug else 0.0)):
        _m5_4b_face[0] = "smug" if smug else "happy"
        try:
            m5_4b(k, s)
        finally:
            _m5_4b_face[0] = "happy"


_m5_4b_face = ["happy"]


def m6_1_7(k, d):
    """v7: 12 drawings. The phone is IN his hands (fists on its sides, thumbs on its face), no rings, no glow on his face;
    eyes down on it, then the phone comes up a hair and he glances up, guilty, and back down."""
    up = 4 <= d <= 8
    look = (-0.5, -0.4) if up else (0.0, 1.0)
    pose = (10, 110, -10, -110)
    lift = (0, 0, 0, 0, -3, -5, -5, -5, -4, -2, 0, 0)[d]

    def ex(k_, o):
        (lx, ly), (rx, ry) = sorted(o["client"]["hands"])
        mx, my = (lx + rx) / 2, (ly + ry) / 2 + lift
        c = k_.c
        from kit import rect as rect_
        c.save(); c.translate(mx, my - 14); c.rotate(-0.04)
        rect_(k_, -13, -22, 26, 40, (0.10, 0.11, 0.14), 997, lw=1.6)
        c.set_source_rgb(*cp.LIGHT); c.rectangle(-10.5, -19, 21, 33); c.fill()
        c.restore()
        skin = (0.86, 0.66, 0.50)
        for i, (hx, sgn) in enumerate(((lx, 1), (rx, -1))):
            ellipse(k_, hx, my, 9, 10, skin, 980 + i, lw=1.6)                    # the fist on the phone's side
            ellipse(k_, hx + sgn * 6, my - 12, 3.6, 5.5, skin, 984 + i, lw=1.3)   # the thumb on its face
    with Breathe("client", breath(d)):
        S(k, (232, 600, 2.7), auto=False, portrait=False, extra=ex,
          **base(rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", pose=pose, face="plain", look=look)))


def m6_1b7(k, d):
    """v7 insert, 31 drawings (2.6 s): the change happens on screen. d 0-3 the old post (lawyer in red); 4-6 the line
    is struck through; 7-8 UPDATE:; 9-12 "Pam found it." types on; 13-30 held (1.5 s). The company's old reply is
    dimmed, so the eye goes to her name. His thumb types below the text and leaves before the hold."""
    c = k.c
    sway = SWAY8[0]
    if sway:                                                  # v8 (lesson 72): the phone drifts in his hand, breathing rhythm
        c.set_source_rgb(0.24, 0.22, 0.20); c.paint()
        ph = 2 * math.pi * d / float(DPS) / BREATH
        c.save(); c.translate(270, 480); c.rotate(math.radians(0.35 * math.sin(ph))); c.translate(-270 + 1.5 * math.sin(ph * 0.5), -480 + 2.0 * math.sin(ph))
    old = cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0]
    cp.REPLY_BIG[0] = cp.SAME_LAYOUT[0] = cp.GARAGE_LOGO[0] = True
    try:
        cp.phone2(k, "update")
    finally:
        cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0] = old
    try:
        _m6_1b7_text(k, d)
    finally:
        if sway:
            c.restore()


SWAY8 = [False]


def _m6_1b7_text(k, d):
    c = k.c
    x0, top, L, Z, ry = 58, 360, 44, 36, 650
    c.set_source_rgb(*cp.LIGHT); c.rectangle(x0 + 2, top - 40, 420, ry - top + 36); c.fill()   # the text area, redrawn by stage
    struck = min(1.0, max(0.0, (d - 3) / 3.0))
    for i, s_ in enumerate(("“Paid $999.", "They lost my", "blueprint.")):
        cp.T(c, s_, x0 + 30, top + i * L, Z, col=cp.INK if struck == 0 else cp.GREY, bold=False, center=False)
    for i, s_ in enumerate(("My lawyer", "will call.”")):
        ex = cp.T(c, s_, x0 + 30, top + (3 + i) * L, Z, col=cp.RED if struck == 0 else cp.GREY, bold=True, center=False)
        if struck > 0:
            c.set_source_rgb(*cp.RED); c.set_line_width(5)
            c.move_to(x0 + 24, top + (3 + i) * L - 12); c.line_to(x0 + 24 + (12 + ex) * struck, top + (3 + i) * L - 12); c.stroke()
    if d >= 7:
        cp.T(c, "UPDATE:", x0 + 250, top + 3 * L, 30, col=cp.GRN, center=False)
    if d >= 9:
        txt = "Pam found it."
        n = len(txt) if d >= 12 else (4, 8, 11)[d - 9]
        cp.T(c, txt[:n], x0 + 30, top + 5 * L + 14, 46, col=(0.55, 0.16, 0.46), center=False)
    c.set_source_rgba(*cp.LIGHT, 0.6); c.rectangle(x0 + 10, ry, 404, 140); c.fill()               # the old reply steps back
    if d <= 15:                                                                                 # the thumb, below the text
        y = 850 + (10 if (4 <= d <= 12 and d % 2) else 0) + max(0, d - 12) * 60
        sb.thumb(k, 360, y, 1.6, sb.SKIN_CL, oil=True, ang=2.7, who="client")


CLIP7 = [("5.3", 12, m5_3), ("5.4b", 25, m5_4b7), ("5.4c", 16, m5_4c), ("6.1", 12, m6_1_7), ("6.1b", 31, m6_1b7)]


CLIP = [("5.3", 12, m5_3),
        ("5.4a", 19, m5_4a),                               # dropped when CUT_HANDSHAKE
        ("5.4b", 19, m5_4b),
        ("5.4c", 16, m5_4c),
        ("6.1", 8, m6_1),
        ("6.1b", 10, m6_1b)]


def draw(fn, d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * HI[0], 960 * HI[0])
    if HI[0] > 1:
        s.set_device_scale(HI[0], HI[0])
    c = cairo.Context(s); k = Ctx(c, 0)
    sb.bg(c); sb.HEADS.clear(); sb.AVOID.clear()
    old = cp.PROPS4[0], cp.REAL_PAM[0]; cp.PROPS4[0] = cp.REAL_PAM[0] = True
    try:
        with b3._ep11v3():
            fn(k, d)
    finally:
        cp.PROPS4[0], cp.REAL_PAM[0] = old
    return s


def strip(tiles, out, tw, cols, label=True):
    th = tw * 960 // 540
    rows = (len(tiles) + cols - 1) // cols
    S_ = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (tw + 6) + 6, rows * (th + (24 if label else 6)) + 6)
    c = cairo.Context(S_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, f) in enumerate(tiles):
        x, y = 6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + (24 if label else 6))
        c.save(); c.translate(x, y); c.scale(tw / 540.0, th / 960.0)
        p = cairo.SurfacePattern(f); p.set_filter(cairo.FILTER_GOOD); c.set_source(p); c.paint(); c.restore()
        if label:
            c.select_font_face("Inter", 0, 1); c.set_font_size(13); c.set_source_rgb(1, 1, 1)
            c.move_to(x + 2, y + th + 17); c.show_text(name)
    S_.write_to_png(out)


def test(out_dir):
    tmp = "/tmp/cs_test"; os.makedirs(tmp, exist_ok=True)
    tiles, lst, n = [], open(tmp + "/list.txt", "w"), 0
    for shot, nd, fn in (CLIP7 if V7[0] else CLIP):
        if CUT_HANDSHAKE[0] and shot == "5.4a":
            continue
        for d in range(nd):
            f = draw(fn, d)
            p = "%s/d%03d.png" % (tmp, n); f.write_to_png(p)
            lst.write("file '%s'\nduration %.6f\n" % (p, 1.0 / DPS))
            tiles.append(("#%d  %.2f s" % (n + 1, n / float(DPS)), f, shot)); n += 1
    lst.write("file '%s'\n" % p); lst.close()
    out = os.path.join(out_dir, "cs_test_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/t.part.mp4"], check=True)
    os.replace(tmp + "/t.part.mp4", out)
    strip([t[:2] for t in tiles], os.path.join(out_dir, "cs_test_%s_strip.png" % V), 180, 10)
    if HI[0] > 1:                                                   # the real feed size: every drawing of the mic at 270 px
        mic = [t for t in tiles if t[2] == "5.4b"]
        strip([(t[0].split()[0], t[1]) for t in mic], os.path.join(out_dir, "cs_test_%s_mic270.png" % V), 270, 7)
    else:
        strip([(t[0].split()[0], t[1]) for t in tiles], os.path.join(out_dir, "cs_test_%s_feed.png" % V), 135, 13)
    print("wrote", out, "%d drawings, %.2f s" % (n, n / float(DPS)))


def setup(out_dir):
    strip([("#%d" % (d + 1), draw(m3_5b, d)) for d in range(len(SWING))],
          os.path.join(out_dir, "cs_test_%s_setup.png" % V), 180, 8)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "test"
    if what == "test3":                                            # v3: no handshake, native 1080
        V, HI[0], CUT_HANDSHAKE[0], what = "v3", 2, True, "test"
    if what == "test8":                                            # v8: v7 + the UPDATE screen sways (lesson 72)
        V, HI[0], CUT_HANDSHAKE[0], V7[0], SWAY8[0], what = "v8", 2, True, True, True, "test"
    if what == "test7":                                            # v7: the review's four correlating points
        V, HI[0], CUT_HANDSHAKE[0], V7[0], what = "v7", 2, True, True, "test"
    if what == "test6":                                            # v6: G3 sign, breathing, live card, 6.1 phone and thumb
        V, HI[0], CUT_HANDSHAKE[0], what = "v6", 2, True, "test"
    if what == "test5":                                            # v5: the mic shot with the room's dressing
        V, HI[0], CUT_HANDSHAKE[0], what = "v5", 2, True, "test"
    if what == "test4":                                            # v4: the arm rig, one mouth, the phone in hand
        V, HI[0], CUT_HANDSHAKE[0], what = "v4", 2, True, "test"
    d = sys.argv[2] if len(sys.argv) > 2 else "../customer-success"
    {"test": test, "setup": setup}[what](d)
