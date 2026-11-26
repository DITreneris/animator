"""THE DOUBLE AGENT (episode 15): the set's additions and the establishing frame, v3 (26 Nov: canon depth, colours, shadows; two reviews P0-P1).

The canon (DITreneris/uptimez CANON.md): the 9:16 room from episode 10 on is the front desk v4
(series/front-desk-set.md, fs_set4.py), with episode 14's pieces (ps_set: the tape at x 560, the throne, the blinds).
Nothing in fs_set4, set_ob or ps_set changes; this file draws on top of ps_set.room().

New for 15 (concept v3, §8): DON's office gets a glass front with blinds. It sits in the bare wall of zone C,
behind the counter, left of DON's door (which stays as built, x 896): so Don, on his side of the tape, looks over
the counter into his own office, and Mom, standing at her end of the counter, is between him and the glass.

  python3 da_set.py [out_dir]   ->  da_establish_v3.png (540x960 x2)  +  da_establish_v3_world.png (the whole room)
"""
import os
import sys
import math
import cairo
import kit
import ps_set as pss
import fs_set4 as s4
import fs_storyboard_v17 as sbv
import don_ps as dp
import pm_ps as pm
import sofia_ps as sp
import client_ps as cps
import dh_cast as dc
from kit import Ctx, INK, rect

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "the-double-agent")
F = pss.F                                                   # the floor line, 800
WIN = (606, 300, 278, 300)                                  # the office glass: x 606-884, y 300-600 (its sill at the counter top)
# colours from the canon only (kit.WALL / kit.FLOOR; the glass #8CAAB9 of the 16:9 set page; the wood of DON's door):
IN_WALL = tuple(v * 0.86 for v in kit.WALL)                 # inside: the office wall one step darker = one plane deeper
IN_FLOOR = tuple(v * 0.85 for v in kit.FLOOR)
DESK, DESK_D = (0.56, 0.39, 0.24), (0.44, 0.30, 0.18)       # Don's desk: the wood of his own door
GLASS = (0.55, 0.67, 0.73)                                  # #8CAAB9, "cool glass"
pss.NO_SCREEN[0] = True
SC = dict(don=0.60, pam=0.54, mom=0.54)                     # ps_scenes' scales (the series' proportions)
S_IN = 0.40                                                 # inside, behind the wall: one step deeper


def _blinds_on_window(k, state="up", u=0.0):
    """ps_set.blinds drawn on the office glass instead of the street door (its globals swapped, then restored)."""
    keep = (pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R)
    x, y, w, h = WIN
    pss.GX0, pss.GY0, pss.GW, pss.GH = x, y, w, h
    pss.CORD_L, pss.CORD_R = x + 10, x + w - 8
    try:
        pss.blinds(k, state, u, seed=5200, cords=True)
    finally:
        pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R = keep


def _self_portrait(k, x, y, s):
    """Don's framed portrait of himself on his office's back wall (gold, bigger than OUR FIRST CLIENT)."""
    c = k.c
    w, h = 74 * s, 88 * s
    rect(k, x - w / 2 - 7 * s, y - 7 * s, w + 14 * s, h + 14 * s, (0.83, 0.66, 0.24), 5301, shadow=False, lw=2)
    rect(k, x - w / 2, y, w, h, (0.72, 0.82, 0.90), 5302, shadow=False, lw=1.5)
    c.save(); c.rectangle(x - w / 2, y, w, h); c.clip()
    dp.don(k, x, y + h + 96 * s * 0.9, 0.34 * s, "stand", "smug" if "smug" in getattr(dp, "FACES", ()) else "neutral")
    c.restore()


def office_inside(k, cast=True):
    """What the glass shows: the back wall, Don's portrait, Father in Don's chair behind Don's desk, the Client, Sofía."""
    c = k.c
    x, y, w, h = WIN
    heads = {}
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*IN_WALL); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*IN_FLOOR); c.rectangle(x, y + h - 26, w, 26); c.fill()
    cx = x + w * 0.50
    _self_portrait(k, cx, y + 54, 0.66)                      # over his own chair, the CEO's wall
    rect(k, cx - 36, y + 120, 72, 110, (0.12, 0.12, 0.14), 5310, shadow=False, lw=2)   # Don's chair: a tall black back
    if cast:
        o = cps.client(k, x + 36, 560, S_IN * 0.92, pose="open", face="bored", look=(1, 0))   # standing, left
        heads["client"] = o["head"]
        o = dc.father(k, cx, 590, S_IN * 0.92 * 1.19, face="hard", look=(0, 0.3))           # in Don's chair (seated: lower);
        heads["father"] = o["head"]                                                       # 1.19x the Client, as in 14's booth
        o = sp.sofia(k, x + w - 34, 556, S_IN * 0.95, "hold", "smile", look=(-1, 0))
        heads["sofia"] = o["head"]
    # Don's desk across the bottom of the glass: it hides everyone from the waist down
    rect(k, x - 4, y + h - 112, w + 8, 14, DESK, 5320, shadow=False, lw=2)
    rect(k, x + 6, y + h - 100, w - 12, 100, DESK_D, 5321, shadow=False, lw=2)
    # (v2: Father's shoes on the desk are left to their own shot, 0:04: here they read as "two black ovals")
    c.set_source_rgba(*IN_WALL, 0.14); c.rectangle(x, y, w, h); c.fill()   # v2: the room behind the glass 14 % less contrast
    c.restore()
    # the glass: a cool tint, two reflections, the frame
    c.set_source_rgba(*GLASS, 0.14); c.rectangle(x, y, w, h); c.fill()
    c.save(); c.rectangle(x, y + h - 112, w, 112); c.clip()     # review P1: the reflections only on the desk, off the people
    c.set_source_rgba(1, 1, 1, 0.13); c.set_line_width(7)
    for dx in (40, 58):
        c.move_to(x + dx, y + h); c.line_to(x + dx + 70, y); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(3.5); c.rectangle(x, y, w, h); c.stroke()
    rect(k, x - 8, y + h, w + 16, 10, (0.80, 0.80, 0.77), 5340, shadow=False, lw=2)          # the sill
    return heads


def room(k, blind="up", u=0.0, inside=True, behind=()):
    """The front desk with the tape (ps_set, as episode 14 ends) plus the office glass. The glass is in the wall, so it
    is drawn in fs_set4's pam_back hook: after the wall, before Pam and Mom and the counter. behind: callables drawn
    after the glass, behind the counter (Pam, Mom)."""
    heads = {}
    orig = pss.s4.draw_set

    def back(k_):
        heads.update(office_inside(k_, cast=inside))
        _blinds_on_window(k_, blind, u)
        for fn in behind:
            heads.update(fn(k_) or {})
    pss.s4.draw_set = lambda k_, cast="home", **kw: orig(k_, {"pam_back": back}, **kw)
    try:
        pss.room(k, blind="rehung", tape=True, phone=None)
    finally:
        pss.s4.draw_set = orig
    return heads


def establish(k):
    """The blocking frame: Don on his side of the tape, looking at his own office; Pam and Mom at the counter;
    Father, the Client and Sofía behind the glass."""
    def mom(k_):
        return {"mom": pm.mom(k_, 824, F - 70, SC["mom"], "folded", "unimpressed", look=(-1, 0))["head"]}
    heads = room(k, behind=(mom,))
    _tape_seam(k.c)
    s4.shadow(k, 650, F + 36, 30)                            # canon: everyone gets a contact shadow
    o = pm.pam(k, 650, F + 34, SC["pam"], "cup_mid", "neutral", look=(-1, 0))     # in front of the counter's left end,
    heads["pam"] = o["head"]                                                     # Father's side, her thermos cup in hand
    s4.shadow(k, 522, F + 332, 48)                           # forward, below the throne and the DON mark (review P0: the
    o = dp.don(k, 522, F + 330, SC["don"], "stand", "neutral", look=(1, -0.5), hands=("quiet", "relax"))
    heads["don"] = o["head"]
    return heads


def _floor_on(c):
    """ps_scenes._floor_on (copied, not imported: importing it switches episode 14's set flags): the floor and the tape
    run on below the world's edge (y 960) for the low framings."""
    c.set_source_rgb(0.72, 0.63, 0.50); c.rectangle(-2000, F, 5000, 3000); c.fill()
    x0 = pss.LINE_X

    def at(y):
        return x0 + 34 * (y - F) / 160, 8.5 + 11.5 * (y - F) / 160
    (ca, ha), (cb_, hb) = at(958), at(1600)
    c.new_path(); c.move_to(ca - ha, 958); c.line_to(ca + ha, 958); c.line_to(cb_ + hb, 1600); c.line_to(cb_ - hb, 1600)
    c.close_path(); c.set_source_rgb(*pss.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(2.4)
    c.stroke()


def _tape_seam(c):
    """Covers the stroke across the tape where the room's tape ends (y 960) and the floor's runs on: fill over it and
    stroke the two long edges only."""
    x0 = pss.LINE_X

    def at(y):
        return x0 + 34 * (y - F) / 160, 8.5 + 11.5 * (y - F) / 160
    (ca, ha), (cb_, hb) = at(944), at(976)
    c.new_path(); c.move_to(ca - ha + 1.2, 944); c.line_to(ca + ha - 1.2, 944); c.line_to(cb_ + hb - 1.2, 976)
    c.line_to(cb_ - hb + 1.2, 976); c.close_path(); c.set_source_rgb(*pss.TAPE); c.fill()
    c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(2.4)
    for sgn in (-1, 1):
        c.move_to(ca + sgn * ha, 944); c.line_to(cb_ + sgn * hb, 976); c.stroke()


def frame(cam, out, scale=2, world=False):
    W, H = (960, 960) if world else (540, 960)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * scale, H * scale)
    c = cairo.Context(surf); c.scale(scale, scale); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save()
    if not world:
        sbv.view(c, *cam)
        _floor_on(c)
    heads = establish(k)
    c.restore()
    surf.write_to_png(out)
    return heads


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    os.makedirs(out, exist_ok=True)
    CAM = (659, 700, 0.90)
    h = frame(CAM, os.path.join(out, "da_establish_v3.png"))
    frame(None, os.path.join(out, "da_establish_v3_world.png"), scale=1, world=True)
    for n, v in h.items():
        print(n, tuple(round(a) for a in v[:2]))


# --- S8: inside DON's office, looking out through the glass (the final image, 8.1) ------------------------------------
# Tomas 26 Nov (/grill-me): a still now, before the script. Frame units (540x960), no world camera: the office is a new
# room. Mirror rule: seen from inside, the floor is reversed, so Don's side (with the throne) is on screen RIGHT of the
# tape, Father's side (the counter, right outside the glass) is in front of it.
MUG = (0.86, 0.66, 0.16)                                    # Pam's mug: mustard (Tomas 26 Nov), one silhouette
G8 = (34, 120, 472, 400)                                    # the glass in frame units: x 34-506, y 120-520


def pam_mug(k, x, y, s=1.0):
    """Pam's mug: a tall mustard mug with a big round handle on the right (the same silhouette in every shot)."""
    c = k.c
    rect(k, x - 13 * s, y - 30 * s, 26 * s, 30 * s, MUG, 5501, shadow=False, lw=2)
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(x + 4 * s, y - 28 * s, 8 * s, 27 * s); c.fill()      # its shaded side
    c.set_source_rgba(1, 1, 1, 0.35); c.rectangle(x - 9 * s, y - 27 * s, 3 * s, 24 * s); c.fill()     # a highlight
    c.set_source_rgb(*INK); c.set_line_width(4.5 * s); c.new_path()
    c.arc(x + 15 * s, y - 15 * s, 8 * s, -1.5, 1.5); c.stroke()
    c.set_source_rgb(*MUG); c.set_line_width(2.4 * s); c.new_path()
    c.arc(x + 15 * s, y - 15 * s, 8 * s, -1.5, 1.5); c.stroke()


def _floor_through_glass(k, don_pose="salute", strip=True):
    """What the glass shows from inside: the far (camera-side) wall, the floor, the tape receding, Don at his line
    facing us, the throne's back on his side, the counter's back right outside the glass."""
    c = k.c
    x, y, w, h = G8
    hz = y + 150                                             # the far wall meets the floor
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, hz - y); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(x, hz, w, y + h - hz); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(x, hz); c.line_to(x + w, hz); c.stroke()
    # the tape: near (bottom of the glass) wide, far narrow; DON on his side (screen right)
    tn, tf = (250, y + h), (300, hz)
    c.new_path(); c.move_to(tn[0] - 22, tn[1]); c.line_to(tn[0] + 22, tn[1]); c.line_to(tf[0] + 6, tf[1]); c.line_to(tf[0] - 6, tf[1])
    c.close_path(); c.set_source_rgb(*pss.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(1.8); c.stroke()
    # Don at his line, facing the office: saluting, the strip stuck to his saluting hand
    s4.shadow(k, 330, hz + 92, 28)
    o = dp.don(k, 330, hz + 90, 0.34, don_pose, "pleased" if hasattr(dp, "don") else "neutral", look=(-0.4, 0.2))
    if strip and o.get("hands"):                              # the peeled strip hanging from his raised hand
        hx, hy = max(o["hands"], key=lambda p: -p[1])
        c.save(); c.translate(hx, hy + 4); c.rotate(0.12)
        rect(k, -4, 0, 8, 46, pss.TAPE, 5510, shadow=False, lw=1.4)
        c.restore()
    return o


def s8_final(k):
    """8.1: the meeting at Don's desk, nobody looks up; through the glass, Don saluting at his line."""
    c = k.c
    c.set_source_rgb(*IN_WALL); c.paint()
    x, y, w, h = G8
    c.save(); c.rectangle(x, y, w, h); c.clip()
    heads = {"don": _floor_through_glass(k)["head"]}
    # the counter's back, right outside the glass (its top and the backs of Pam's monitor and Mom's nameplate)
    rect(k, x - 4, y + h - 46, w + 8, 50, (0.80, 0.72, 0.58), 5520, shadow=False, lw=2)
    c.restore()
    c.set_source_rgba(*GLASS, 0.14); c.rectangle(x, y, w, h); c.fill()
    keep = (pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R)
    pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R = x, y, w, h, x + 10, x + w - 8
    try:
        pss.blinds(k, "up", 0.0, seed=5530, cords=True)
    finally:
        pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R = keep
    c.set_source_rgb(*INK); c.set_line_width(4); c.rectangle(x, y, w, h); c.stroke()
    # the meeting, at the desk, in front of the glass: the Client left, Pam, Father in Don's chair, Sofía right
    rect(k, 226, 500, 92, 220, (0.12, 0.12, 0.14), 5540, shadow=False, lw=2)                # Don's chair, its tall back
    heads["client"] = cps.client(k, 86, 846, 0.66, pose="open", face="bored", look=(1, 0.3))["head"]
    heads["father"] = dc.father(k, 272, 840, 0.66 * 1.19, face="hard", look=(0, 0.5))["head"]
    heads["sofia"] = sp.sofia(k, 466, 830, 0.62, "hold", "smile", look=(-1, 0.3))["head"]
    heads["pam"] = pm.pam(k, 176, 840, 0.62, "stand", "neutral", look=(0.3, 0.8))["head"]
    # Don's desk across the bottom: the blueprint open in front of Pam, her mug, Don's photo face down, his white mug
    rect(k, -10, 760, 560, 30, DESK, 5550, shadow=False, lw=2.4)
    rect(k, -10, 788, 560, 180, DESK_D, 5551, shadow=False, lw=2.4)
    import acts_ob as ac
    c.save(); c.translate(184, 772); c.scale(1, 0.55); ac.plan_open(k, 0, 0, 0.95); c.restore()
    pam_mug(k, 108, 776, 1.0)
    rect(k, 330, 760, 70, 12, (0.83, 0.66, 0.24), 5560, shadow=False, lw=1.8)               # Don's gold photo, face down
    rect(k, 420, 744, 22, 26, (0.97, 0.97, 0.95), 5561, shadow=False, lw=1.8)                # his white office mug
    return heads


def s8_still(out):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920)
    c = cairo.Context(surf); c.scale(2, 2); k = Ctx(c, 0)
    h = s8_final(k)
    surf.write_to_png(out)
    return h
