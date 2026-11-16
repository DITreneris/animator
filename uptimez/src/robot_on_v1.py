"""The robot, "Office Noir", v1: the witness with the footage. Built on robot_ss (untouched):
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
FOOT_ZOOM = 1.9                  # how far the screen is zoomed into the footage frame
FOOT_FOCUS = (0.50, 0.50)        # which point of the footage frame sits at the screen centre (fractions)


def _screen(k, state, look=(0, 0), talk=0.0, side=1, seed=0, t=0.0):
    if state != "cctv" or _FOOTAGE["surf"] is None:
        rs.screen(k, state, look, talk, side, seed, t)
        return
    c = k.c
    sf = _FOOTAGE["surf"]
    ellipse(k, 0, 0, rm.SRX, rm.SRY, w.SCREEN, seed, shadow=False, lw=2)
    c.save()
    c.new_path(); c.save(); c.scale(rm.SRX - 3, rm.SRY - 3); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
    fw, fh = sf.get_width(), sf.get_height()
    sc = (2 * rm.SRX) / fw * FOOT_ZOOM                             # zoomed on the action; the ellipse crops the rest
    c.translate(-fw * sc * FOOT_FOCUS[0], -fh * sc * FOOT_FOCUS[1])
    c.scale(sc, sc)
    c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint()
    c.restore()


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
    if cap:
        hx, hy = out["head"]
        watch_cap(k, hx, hy - 50 * s, 1.05 * s, seed + 5)
        c = k.c                                                    # the antenna through the crown
        c.set_source_rgb(*INK); c.set_line_width(2.4 * s)
        c.move_to(hx, hy - 82 * s); c.line_to(hx, hy - 94 * s); c.stroke()
        ellipse(k, hx, hy - 97 * s, 5.5 * s, 5.5 * s, (0.98, 0.80, 0.25), seed + 6, shadow=False, lw=1.6 * s)
    return out
