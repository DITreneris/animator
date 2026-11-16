"""v4: opt-in hat_lift (0..1) tips the partner's fedora; robot_on_v3.py = v3. v3: opt-in partner=True (fedora, trench, silver badge) for storyboard v4; robot_on_v2.py = v2. The robot, "Office Noir", v2 (robot_on_v1.py = v1, kept). v2: the playback screen is brighter (FOOT_BRIGHT
lifts the footage) and zoomed on Don, so he is recognisable in the witness shot.
v1 notes: the witness with the footage. Built on robot_ss (untouched):
- a night-watchman's peaked cap (dark, a black peak, a small white badge), the antenna poking through the crown;
- screen state "cctv": the screen shows a frame of security footage (any cairo surface, cropped to fit),
  passed as footage=; the frame itself carries its own CCTV overlay (props_on.cctv_overlay);
- otherwise its Secret Santa screens and poses. Its red bow tie is not the key red, so it turns grey in noir.
Usage: o = robot_noir(k, x, feet, s, pose, state, look, cap=True, footage=None, ...)"""
import math
import cairo
import kit
import robot_ss as rs
import robot_mf as rm
import waiter_kit as w
from kit import INK, cut, rect, ellipse

CAP = (0.20, 0.21, 0.24)
PEAK = (0.06, 0.06, 0.07)
CAP_BADGE = (0.92, 0.92, 0.90)
_FOOTAGE = {"surf": None}
FOOT_BRIGHT = 0.28               # v2: white lift over the footage on its screen
FOOT_ZOOM = 2.3                  # how far the screen is zoomed into the footage frame
FOOT_FOCUS = (0.50, 0.50)        # which point of the footage frame sits at the screen centre (fractions)
LOGICAL_FOOTAGE = None           # opt-in (1080 release): the footage's size in drawing units, when its pixels are 2x


def _screen(k, state, look=(0, 0), talk=0.0, side=1, seed=0, t=0.0):
    if state != "cctv" or _FOOTAGE["surf"] is None:
        rs.screen(k, state, look, talk, side, seed, t)
        return
    c = k.c
    sf = _FOOTAGE["surf"]
    ellipse(k, 0, 0, rm.SRX, rm.SRY, w.SCREEN, seed, shadow=False, lw=2)
    c.save()
    c.new_path(); c.save(); c.scale(rm.SRX - 3, rm.SRY - 3); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
    fw, fh = LOGICAL_FOOTAGE or (sf.get_width(), sf.get_height())
    sc = (2 * rm.SRX) / fw * FOOT_ZOOM                             # zoomed on the action; the ellipse crops the rest
    c.translate(-fw * sc * FOOT_FOCUS[0], -fh * sc * FOOT_FOCUS[1])
    c.scale(sc, sc)
    c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint()
    c.restore()
    if FOOT_BRIGHT:
        c.save(); c.new_path(); c.save(); c.scale(rm.SRX - 3, rm.SRY - 3); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(1, 1, 1, FOOT_BRIGHT); c.fill(); c.restore()


def watch_cap(k, x, y, s=1.0, seed=0):
    """(x, y) = the middle of the band, sitting on top of the head."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-40, 0), (-46, -22), (-30, -34), (30, -34), (46, -22), (40, 0)], CAP, shadow=False, lw=2.2)   # crown
    rect(k, -40, -8, 80, 10, PEAK, seed + 1, shadow=False, lw=1.8)                                         # band
    c.new_path(); c.move_to(-34, 2); c.curve_to(-20, 16, 20, 16, 34, 2); c.close_path()                     # peak
    c.set_source_rgb(*PEAK); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    cut(k, [(0, -28), (8, -22), (6, -12), (-6, -12), (-8, -22)], CAP_BADGE, shadow=False, lw=1.4)          # badge
    c.restore()


def robot_noir(k, x, feet, s=1.0, pose="stand", state="eager", look=(0, 0), cap=True, footage=None, seed=900,
               **kw):
    old = rs.screen
    _FOOTAGE["surf"] = footage
    rm.screen = _screen
    try:
        out = rm.robot(k, x, feet, s, pose, state, look, kw.get("side", 1), kw.get("talk", 0.0), seed, False,
                       kw.get("head_dx"), kw.get("head_rot"), kw.get("wobble", 0.0), kw.get("t", 0.0))
    finally:
        rm.screen = rs.ORIG_SCREEN
        _FOOTAGE["surf"] = None
    if kw.get("partner"):                                          # v3 opt-in: Don's partner, not a guard
        partner_kit(k, out, s, seed, kw.get("hat_lift", 0.0))
    elif cap:
        hx, hy = out["head"]
        watch_cap(k, hx, hy - 50 * s, 1.05 * s, seed + 5)
        c = k.c                                                    # the antenna through the crown
        c.set_source_rgb(*INK); c.set_line_width(2.4 * s)
        c.move_to(hx, hy - 82 * s); c.line_to(hx, hy - 94 * s); c.stroke()
        ellipse(k, hx, hy - 97 * s, 5.5 * s, 5.5 * s, (0.98, 0.80, 0.25), seed + 6, shadow=False, lw=1.6 * s)
    return out


# ---- v3 (opt-in, partner=True): Don's partner. Robot_on_v2.py = v2 kept; without partner=True nothing changes. -----
BADGE_SILVER = (0.80, 0.81, 0.83)        # silver, not gold: gold belongs to Sofia's hoops and Pam's glasses


def partner_kit(k, out, s, seed=900, hat_lift=0.0):
    """A trench over the egg body (a V open on the bow tie), sleeves to the elbows, a belt, a silver star badge on
    the chest, his own fedora, the antenna poking through the crown. Head-relative, so it follows any pose."""
    import don_on as d
    c = k.c
    hx, hy = out["head"]
    for ax, ay in out["hands"]:                                         # the sleeves, shoulder to past the elbow
        sx = -1 if ax < hx else 1
        shx, shy = hx + sx * 47 * s, hy + 84 * s
        mx, my = shx + (ax - shx) * 0.62, shy + (ay - shy) * 0.62
        ln = math.hypot(mx - shx, my - shy) or 1
        nx, ny = -(my - shy) / ln * 9 * s, (mx - shx) / ln * 9 * s
        cut(k, [(shx + nx, shy + ny), (mx + nx * 1.15, my + ny * 1.15), (mx - nx * 1.15, my - ny * 1.15), (shx - nx, shy - ny)],
            d.TRENCH, shadow=False, lw=2.2 * s)
    for sx in (-1, 1):                                                  # the two coat panels, a V on the bow tie
        P = lambda u, v: (hx + sx * u * s, hy + v * s)
        cut(k, [P(11, 64), P(50, 70), P(61, 182), P(2, 182), P(2, 124)], d.TRENCH, shadow=False, lw=2.4 * s)
        cut(k, [P(11, 64), P(31, 69), P(19, 104), P(2, 124)], d.TRENCH_SHADE, shadow=False, lw=2.0 * s)   # lapel
        for v in (136, 160):
            ellipse(k, *P(10, v), 3.2 * s, 3.2 * s, d.TRENCH_SHADE, seed + v, shadow=False, lw=1.4 * s)
    rect(k, hx - 60 * s, hy + 142 * s, 120 * s, 10 * s, d.TRENCH_SHADE, seed + 40, shadow=False, lw=2 * s)   # the belt
    bx, by, r = hx - 33 * s, hy + 100 * s, 9 * s                        # the badge: a silver star
    c.new_path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        c.line_to(bx + math.cos(a) * rr, by + math.sin(a) * rr)
    c.close_path(); c.set_source_rgb(*BADGE_SILVER); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.6 * s); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.4 * s)                   # the antenna through the crown
    c.move_to(hx, hy - 70 * s); c.line_to(hx, hy - 88 * s); c.stroke()
    ellipse(k, hx, hy - 91 * s, 5.5 * s, 5.5 * s, (0.98, 0.80, 0.25), seed + 6, shadow=False, lw=1.6 * s)
    d.fedora(k, hx + 4 * hat_lift * s, hy - (34 + 16 * hat_lift) * s, 1.0 * s, tilt=-0.08 - 0.18 * hat_lift,
             seed=seed + 7)                                         # v4 opt-in: hat_lift 0..1, the tip of the hat
    c.set_source_rgb(*INK); c.set_line_width(2.4 * s)                   # the antenna again, over the crown
    top = 88 + 18 * hat_lift                                            # v4: the antenna pushes the hat up
    c.move_to(hx + 2 * hat_lift * s, hy - (72 + 16 * hat_lift) * s); c.line_to(hx + 2 * hat_lift * s, hy - top * s); c.stroke()
    ellipse(k, hx + 2 * hat_lift * s, hy - (top + 3) * s, 5.5 * s, 5.5 * s, (0.98, 0.80, 0.25), seed + 6, shadow=False,
            lw=1.6 * s)


def screen_text(c, out, s, text, size=26):
    """Overwrite the face screen with text (e.g. "YOU."): the partner says it with his face as well."""
    x, y = out["screen"]
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.save(); c.scale(40, 34); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(0.10, 0.13, 0.24); c.fill()
    c.select_font_face("DejaVu Sans Mono", 0, 1); c.set_font_size(size)
    e = c.text_extents(text)
    c.set_source_rgb(0.72, 0.96, 1.0); c.move_to(-e.x_advance / 2, e.height / 2); c.show_text(text)
    c.restore()
