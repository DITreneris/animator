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
cps.CLEAN[0] = True   # Tomas 28 Nov (/grill-me): in episode 15 the Client is the canon's garage owner, oil in the creases only
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
    import da_hand_gate as g_                                  # a picture on the wall: its hands are not the cast's
    with g_.paused():                                          # (28 Nov, the scene 1 gate: logged as LEGACY 'relax')
        dp.don(k, x, y + h + 96 * s * 0.9, 0.34 * s, "stand", "smug" if "smug" in getattr(dp, "FACES", ()) else "neutral")
    c.restore()


INSIDE_QUIET = [True]   # 28 Nov (the scene 3 hand gate): the people behind the glass rest their hands in the canon's
                        # 'quiet', not the legacy 'relax'; they are the other space's state, not this shot's cast, so the
                        # gate's job list doesn't count them (paused). False draws them as before.


def office_inside(k, cast=True):
    """What the glass shows: the back wall, Don's portrait, Father in Don's chair behind Don's desk, the Client, Sofía."""
    if not INSIDE_QUIET[0]:
        return _office_inside(k, cast)
    import hands_ps as hp_
    import da_hand_gate as g_
    keep = hp_.reset
    hp_.reset = lambda left="relax", right="relax": keep("quiet" if left == "relax" else left,
                                                         "quiet" if right == "relax" else right)
    try:
        with g_.paused():
            return _office_inside(k, cast)
    finally:
        hp_.reset = keep


def _office_inside(k, cast=True):
    c = k.c
    x, y, w, h = WIN
    heads = {}
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*IN_WALL); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*IN_FLOOR); c.rectangle(x, y + h - 26, w, 26); c.fill()
    cx = x + w * 0.50
    _self_portrait(k, cx, y + 54, 0.66)                      # over his own chair, the CEO's wall
    if EP15_SET[0]:                                            # 27 Nov: a plain low office chair (one throne only)
        rect(k, cx - 34, y + 176, 68, 54, (0.12, 0.12, 0.14), 5310, shadow=False, lw=2)
    else:
        rect(k, cx - 36, y + 120, 72, 110, (0.12, 0.12, 0.14), 5310, shadow=False, lw=2)   # Don's chair: a tall black back
    st = INSIDE[0]
    if cast and st is not None:                                # 27 Nov (the two spaces): the office in a given shot's state
        return _inside_state(k, st, x, y, w, h, cx, heads)
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


INSIDE = [None]      # opt-in (27 Nov, the two spaces): a dict giving the office's state behind the glass for a shot:
                     # client "stand" | "seated" | None, roll "none" | "held" (rolled in his hands), sofia True/False,
                     # mug True (Pam's mustard mug on Father's side of the desk), pam "hand_on_mug" | "with_plan" | None.
                     # None: establish v3's inside, as before.


def _inside_state(k, st, x, y, w, h, cx, heads):
    """office_inside's cast and props in one shot's state; the desk, the tint, the reflections and the sill as before."""
    c = k.c
    if st.get("client") == "stand":
        o = cps.client(k, x + 36, 560, S_IN * 0.92, pose="open", face="bored", look=st.get("client_look", (1, 0)))
        heads["client"] = o["head"]                            # client_look: opt-in (27 Nov, 6.6: at Pam, outside)
    elif st.get("client") == "seated":
        o = cps.client(k, x + 50, 600, S_IN * 0.92, pose="open", face="bored", look=(1, 0.3)); heads["client"] = o["head"]
    o = dc.father(k, cx, 590, S_IN * 0.92 * 1.19, face="hard", look=(0, 0.3)); heads["father"] = o["head"]
    if st.get("sofia", True):
        o = sp.sofia(k, x + w - 34, 556, S_IN * 0.95, "hold", "smile", look=(-1, 0)); heads["sofia"] = o["head"]
    if st.get("pam"):
        o = pm.pam(k, cx + 70, 572, S_IN, "stand", "neutral", look=(-1, 0.4), mug=False); heads["pam"] = o["head"]
    rect(k, x - 4, y + h - 112, w + 8, 14, DESK, 5320, shadow=False, lw=2)
    rect(k, x + 6, y + h - 100, w - 12, 100, DESK_D, 5321, shadow=False, lw=2)
    if st.get("mug"):                                          # her mustard mug on Father's side of the desk
        pam_mug(k, cx + 34, y + h - 110, 0.62)
        heads["mug"] = (cx + 34, y + h - 122, 10)
        if st.get("pam") == "hand_on_mug":
            kit.ellipse(k, cx + 46, y + h - 122, 6, 5, (0.99, 0.86, 0.66), 5330, shadow=False, lw=1.4)
    if st.get("roll") == "held":                                # the blueprint rolled, across the Client's hands
        hx, hy = heads.get("client", (x + 50, 480))[:2]
        kit.rect(k, hx - 26, hy + 46, 52, 9, (0.22, 0.42, 0.72), 5331, shadow=False, lw=1.6)
        heads["roll"] = (hx, hy + 50, 14)
    c.set_source_rgba(*IN_WALL, 0.14); c.rectangle(x, y, w, h); c.fill()
    c.restore()
    c.set_source_rgba(*GLASS, 0.14); c.rectangle(x, y, w, h); c.fill()
    c.save(); c.rectangle(x, y + h - 112, w, 112); c.clip()
    c.set_source_rgba(1, 1, 1, 0.13); c.set_line_width(7)
    for dx in (40, 58):
        c.move_to(x + dx, y + h); c.line_to(x + dx + 70, y); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(3.5); c.rectangle(x, y, w, h); c.stroke()
    rect(k, x - 8, y + h, w + 16, 10, (0.80, 0.80, 0.77), 5340, shadow=False, lw=2)
    return heads


EP15_SET = [False]   # opt-in (Tomas 27 Nov, /grill-me "too many badges and chairs"): in this episode the throne's back
                     # is bare (no OWNER: INVESTOR card, no price tag's blank back), no taped MY GARAGES plan on the
                     # counter, no shredder. Off: every earlier frame byte-identical.
NAME_BADGES = [True]  # opt-out (same day): the people's name badges off (the robot's HR stays: its role here)


class no_badges(object):
    """the people's name badges off while drawing (Don's staff badge, Pam's, Sofía's), the robot's HR kept. Patches
    the drawers for the duration only; NAME_BADGES on: nothing changes."""
    def __enter__(self):
        import don_v4 as dv
        import pm_ps
        import sofia_da as sd_
        self.keep = (dv.staff_badge, pm_ps.pb.pam, sd_.sofia)
        if NAME_BADGES[0]:
            return self
        sb_, pp, so_ = self.keep
        dv.staff_badge = lambda k_, name, *a, **kw: sb_(k_, name, *a, **kw) if name == "HR" else None

        def pam_(*a, **kw):
            try:
                return pp(*a, **dict(kw, badge=False))
            except TypeError:                                   # pam_fs passes its badge positionally, last
                a = list(a); a[-1] = False
                return pp(*a, **kw)

        def sofia_(*a, **kw):
            kw["badge"] = False
            return so_(*a, **kw)
        pm_ps.pb.pam, sd_.sofia = pam_, sofia_
        return self

    def __exit__(self, *e):
        import don_v4 as dv
        import pm_ps
        import sofia_da as sd_
        dv.staff_badge, pm_ps.pb.pam, sd_.sofia = self.keep


def room(k, blind="up", u=0.0, inside=True, behind=(), spun=False):
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
    keep = (pss.throne_back, pss.price_tag, pss.s4.shredder, pss.s4.fs.plan_taped)
    if EP15_SET[0]:
        tb, pt = pss.throne_back, pss.price_tag
        pss.throne_back = lambda k_, x, feet, s_, card=True: tb(k_, x, feet, s_, card=False)
        pss.price_tag = lambda *a, **kw: None if kw.get("back") else pt(*a, **kw)
        pss.s4.shredder = lambda *a, **kw: None
        pss.s4.fs.plan_taped = lambda *a, **kw: None
    try:
        pss.room(k, blind="rehung", tape=True, phone=None, **({"spun": True} if spun else {}))   # spun: opt-in (27 Nov,
    finally:                                                                                     # the layouts: the throne's
        pss.s4.draw_set = orig                                                                   # back to the street side)
        pss.throne_back, pss.price_tag, pss.s4.shredder, pss.s4.fs.plan_taped = keep
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


MUG_V2 = [False]   # opt-in (27 Nov, the props audit): a rim with a wall, the handle a closed loop joined to the body, a
                   # rounded foot. Same size, colour and side (one prop, one shape); off = S8 v7 and S8r v4 byte-identical.


def _mug_v2(k, x, y, s):
    """Pam's mug v2: 26 x 30 like v1, the handle on the right. The handle first (the body covers its joints), then the
    body with rounded bottom corners, then the open top: a rim ellipse, the wall's thickness, the dark inside."""
    c = k.c
    hx, hy = x + 12 * s, y - 15 * s
    c.new_path(); c.arc(hx, hy, 10.5 * s, -1.25, 1.25); c.arc_negative(hx, hy, 6.2 * s, 1.1, -1.1); c.close_path()
    c.set_source_rgb(*MUG); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2 * s ** 0.5); c.stroke()
    c.set_source_rgba(0, 0, 0, 0.18); c.new_path(); c.arc(hx, hy, 9.0 * s, -0.2, 1.2); c.arc_negative(hx, hy, 6.6 * s, 1.1, -0.1)
    c.close_path(); c.fill()
    w, h, r = 13 * s, 30 * s, 4 * s
    c.new_path(); c.move_to(x - w, y - h); c.line_to(x - w, y - r); c.curve_to(x - w, y, x - w + r, y, x - w + 2 * r, y)
    c.line_to(x + w - 2 * r, y); c.curve_to(x + w - r, y, x + w, y, x + w, y - r); c.line_to(x + w, y - h); c.close_path()
    c.set_source_rgb(*MUG); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(x + 4 * s, y - 27 * s, 8 * s, 25 * s); c.fill()      # its shaded side
    c.set_source_rgba(1, 1, 1, 0.35); c.rectangle(x - 9 * s, y - 26 * s, 3 * s, 22 * s); c.fill()     # a highlight
    for rx, ry, col in ((w, 3.4 * s, MUG), (w - 2.4 * s, 2.3 * s, (0.42, 0.30, 0.08))):          # the rim, then the inside
        c.save(); c.translate(x, y - h); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()


def pam_mug(k, x, y, s=1.0):
    """Pam's mug: a tall mustard mug with a big round handle on the right (the same silhouette in every shot)."""
    if MUG_V2[0]:
        return _mug_v2(k, x, y, s)
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
