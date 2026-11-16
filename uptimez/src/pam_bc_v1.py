"""v1, pinned (the current file is v2). PAM, "The Best Candidate", v1: the lead, on the interview panel. Her Secret Santa look (pam_ss v2: the purple
cardigan, the reading glasses on the gold bead chain) with this episode's touches (grill, 16 Nov):
- fresh lipstick, a shade bolder than the dusty rose (lips="berry"; "rose" and None still work): she dressed up
  because Don runs the panel;
- a small lilac flower brooch on her screen-left chest. Mom wears a flower brooch on the other side, and both
  wear glasses on a chain: side by side they mirror each other, which is the last joke of the film.
Poses: POSE_YES (the paddle up beside her head), POSE_LOWER (the paddle coming down, slowly: she disagrees with Don
and stays loyal), POSE_WRITE (the notepad up in one hand, the pen on it), POSE_ASK (pen hand raised: "Any family
in the company?"), POSE_MIRROR (hands together in front, the notepad held like Mom's handbag).
Extras: paddle="YES"/"NO" in her screen-right hand, note="KIND" on the notepad in her screen-left hand (with
POSE_WRITE or POSE_MIRROR), pen=True.
Every pam_ss / pam_mf face works: "peer" is her cool look over the glasses at the macho, "fade" is the paddle
coming down, "hurt" is after the "No."; new here: "mirror", Mom's sweet act copied (eyes shut in a smile, a closed
smile, a blush).
pam_ss.py, pam_mf.py, kit and every earlier Pam are untouched (the lip colour is swapped for one call and restored).
Usage: o = pam(k, x, feet, s, pose, face, look, glasses="low", lips="berry", mouth=None, lean=0, paddle=None,
               note=None, pen=False, brooch=True)  -> {"head", "hands"}"""
import math
import kit
import pam_mf as pm
import pam_ss as ps
import props_bc as props
from kit import INK, ellipse

BT, HY, SKIN = pm.BT, pm.HY, pm.SKIN
BERRY = (0.78, 0.27, 0.43)
BERRY_LINE = (0.40, 0.10, 0.20)
LILAC = (0.74, 0.64, 0.90)
LILAC_DARK = (0.52, 0.42, 0.72)
POSE_YES = (-8, 0) + pm.ik(1, 58, BT - 16)
POSE_LOWER = (-8, 0) + pm.ik(1, 56, BT + 58)
POSE_WRITE = pm.ik(-1, -26, BT + 76) + pm.ik(1, 2, BT + 70)
POSE_ASK = pm.ik(-1, -26, BT + 104) + pm.ik(1, 34, BT + 8)
POSE_MIRROR = pm.ik(-1, -11, BT + 96) + pm.ik(1, 11, BT + 96)
POSE_TABLE = pm.POSE_TABLE


def brooch_flower(c, x, y, rr, rot=0.0):
    for i in range(5):
        a = rot + i * 2 * math.pi / 5
        c.new_path(); c.arc(x + math.cos(a) * rr * 0.75, y + math.sin(a) * rr * 0.75, rr * 0.55, 0, 2 * math.pi)
        c.set_source_rgb(*LILAC); c.fill_preserve(); c.set_source_rgb(*LILAC_DARK); c.set_line_width(1.0); c.stroke()
    c.new_path(); c.arc(x, y, rr * 0.38, 0, 2 * math.pi); c.set_source_rgb(*pm.GOLD); c.fill()


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=40, glasses="low", lips="berry", mouth=None,
        lean=0.0, paddle=None, note=None, pen=False, brooch=True, badge=True):
    c = k.c
    if lean:                                               # tip the whole figure, extras included (points returned unleaned)
        c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
        try:
            return pam(k, x, feet, s, pose, face, look, seed, glasses, lips, mouth, 0.0, paddle, note, pen, brooch, badge)
        finally:
            c.restore()
    old = (ps.ROSE, ps.ROSE_LINE)
    if lips == "berry":
        ps.ROSE, ps.ROSE_LINE = BERRY, BERRY_LINE
    try:
        out = ps.pam(k, x, feet, s, pose, "happy" if face == "mirror" else face, look, seed, badge, glasses,
                     "rose" if lips else None, False, mouth, 0.0)
    finally:
        ps.ROSE, ps.ROSE_LINE = old
    if face == "mirror" and not mouth:                     # Mom's smile, borrowed: closed, wide, a blush
        c.save(); c.translate(x, feet); c.scale(s, s)
        ellipse(k, 0, HY + 29, 19, 12, SKIN, seed + 70, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(7.4); c.set_line_cap(1)
        c.move_to(-13, HY + 24); c.curve_to(-6, HY + 34, 6, HY + 34, 13, HY + 24); c.stroke()
        c.set_source_rgb(*(BERRY if lips else INK)); c.set_line_width(4.6)
        c.move_to(-13, HY + 24); c.curve_to(-6, HY + 34, 6, HY + 34, 13, HY + 24); c.stroke()
        for sx in (-1, 1):
            c.save(); c.translate(sx * 33, HY + 17); c.scale(9, 5.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0.93, 0.52, 0.60, 0.5); c.fill()
        c.restore()
    if brooch:
        c.save(); c.translate(x, feet); c.scale(s, s)
        brooch_flower(c, -25, BT + 34, 8.5, 0.3)
        c.restore()
    h0, h1 = out["hands"]
    if note is not None:
        if pose == POSE_MIRROR:                            # held in both hands, low, like a handbag
            props.notepad(k, x, feet + (BT + 122) * s, 0.72 * s, 0.0, note, seed + 80)
            for q in (h0, h1):
                ellipse(k, q[0], q[1], 10 * s, 10 * s, SKIN, seed + 82, shadow=False, lw=2 * s)
        else:
            props.notepad(k, h0[0] + 6 * s, h0[1] - 22 * s, 0.86 * s, -0.10, note, seed + 80)
            ellipse(k, h0[0] - 2 * s, h0[1] + 8 * s, 10 * s, 10 * s, SKIN, seed + 82, shadow=False, lw=2 * s)
    if pen:
        props.ballpen(k, h1[0] - 10 * s, h1[1] + 10 * s, 0.85 * s, 0.75)
        ellipse(k, h1[0], h1[1], 10 * s, 10 * s, SKIN, seed + 83, shadow=False, lw=2 * s)
    if paddle:
        ang = 0.10 if pose != POSE_LOWER else 0.95
        props.paddle(k, h1[0], h1[1] - 2 * s, 0.9 * s, ang, paddle, seed + 90)
        ellipse(k, h1[0], h1[1], 10 * s, 10 * s, SKIN, seed + 91, shadow=False, lw=2 * s)
    return out
