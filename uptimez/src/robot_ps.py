"""THE ROBOT in "Pick a Side" (episode 14): the HR robot at the office scale of 13 (0.66), with this episode's parts.
Tomas, 23 Nov, /grill-me:
- the selfie: a TELESCOPIC arm out of its side with a phone clamped at the end; FLASH; it turns the phone to Don with
  the photo and PUBLIC POST? on it, then #TeamDon (one prop carries the photo, the question and the post);
- its ONE wheel balances ON the tape like a tightrope walker, arms out; each push knocks it off and it rolls back on;
- visor icons in its own cyan, line pictograms like 13's WITHOUT HIM: a sun (the room went dark), a striped barrier
  with one red light (Border breach);
- when it bumps Don it keeps its usual smile: never sly, never aggressive.
Nothing in its rig changes: the parts are drawn over dh_poses.rm.robot's figure, at its own screen and hand points.
  robot(k, x, feet, s, arms=None, tilt=0.0, visor=None, selfie=0.0, phone=None, turn=0.0)
  phone_screen(k, x, y, s, kind)     kind: "photo", "public", "posted" (the insert of 3.2/3.3/3.5)
  python3 robot_ps.py [out_dir]  ->  ps_robot_v2.png (sheet), ps_robot_phone_v2.png (phone check); v1: robot_ps_v1.py"""
import math
import os
import sys
import cairo
import kit
import of_cast as oc
from kit import Ctx, INK, cut, rect, ellipse

dq = oc.dq
CYAN = (0.45, 0.92, 1.0)
VISOR = (0.09, 0.12, 0.24)
TAPE = (0.95, 0.78, 0.15)
STEEL, STEEL_D = (0.72, 0.74, 0.78), (0.50, 0.52, 0.56)
S_OFFICE = 0.66                                            # 13's office scale (lesson 138), 95 % of Don


UI_KIT = [False]                                            # opt-in (Pick a Side, 25 Nov): the screens via ps_ui / of_ui
PAD_THUMB = [True]                                          # opt-in off (3.4's gag): Don's own rig thumb presses the pad; a drawn-in
                                                            # thumb as well is a second hand (one hand per wrist)
HEART = [False]                                             # opt-in (ep 14 v4): the posted screen's heart drawn, not the missing glyph
SUN_UP = [False]                                            # opt-in (ep 14 scenes, 24 Nov): the sun with an up-arrow beside it,
                                                            # "more light": two cold viewers read the plain sun as a gear


def oil_can(k, x, y, s=1.0, ang=0.0, drop=True, label=True):
    """The treat (ep 14, 5.3; Tomas, 25 Nov): a classic brass pump oiler, its base centred at (x, y): a squat drum, a dome,
    a long thin spout curving away to screen-left with a black drop at its tip, a thumb lever and a loop handle on the
    right. Office Noir 3's chrome can read as "a bucket, a mug, a bag" (0 of 2 cold viewers) at this size."""
    c = k.c
    BR, BR_D = (0.86, 0.62, 0.20), (0.62, 0.42, 0.12)
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_line_join(1); c.set_line_cap(1)
    c.new_path(); c.arc(24, -16, 11, -1.4, 1.4)                                  # the loop handle
    c.set_source_rgb(*INK); c.set_line_width(7.5); c.stroke_preserve(); c.set_source_rgb(*BR_D); c.set_line_width(3.6); c.stroke()
    c.new_path(); c.move_to(-4, -40); c.curve_to(-22, -70, -52, -72, -70, -52)   # the spout
    c.set_source_rgb(*INK); c.set_line_width(7.0); c.stroke_preserve(); c.set_source_rgb(*BR); c.set_line_width(3.4); c.stroke()
    c.new_path(); c.move_to(-20, 0); c.line_to(20, 0); c.line_to(20, -24); c.curve_to(18, -40, -18, -40, -20, -24); c.close_path()
    c.set_source_rgb(*BR); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    if label:                                                # v2: two cold rounds read the bare can as "a bucket", "a handbag":
        c.set_source_rgb(0.97, 0.95, 0.88); c.rectangle(-17, -24, 34, 19); c.fill_preserve()   # a paper label, OIL
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        c.select_font_face("Lilita One"); c.set_font_size(15)
        e = c.text_extents("OIL"); c.move_to(-e.x_advance / 2, -9.5); c.show_text("OIL")
    else:
        c.set_source_rgb(*BR_D); c.set_line_width(2.0)
        c.move_to(-19, -8); c.line_to(19, -8); c.stroke(); c.move_to(-19, -22); c.line_to(19, -22); c.stroke()
    c.new_path(); c.move_to(2, -38); c.line_to(22, -50)                          # the thumb lever
    c.set_source_rgb(*INK); c.set_line_width(6.0); c.stroke_preserve(); c.set_source_rgb(*BR_D); c.set_line_width(2.6); c.stroke()
    if drop:                                                 # v2: a big drop
        c.new_path(); c.move_to(-71, -52); c.curve_to(-60, -36, -62, -22, -72, -22); c.curve_to(-82, -22, -84, -36, -71, -52)
        c.set_source_rgb(0.07, 0.06, 0.06); c.fill()
    c.set_line_join(0); c.set_line_cap(0)
    c.restore()
    return (x + s * (-71 * math.cos(ang) + 40 * math.sin(ang)), y + s * (-71 * math.sin(ang) - 40 * math.cos(ang)))


def hand_again(k, hx, hy, s):
    """The robot's own hand once more, over what it holds (one hand, two passes: robot_mf does the same for the cuffs).
    The rules page: draw the object, then the fingers over it."""
    w = dq.rm.w
    ellipse(k, hx, hy, 8 * s, 8 * s, w.ARM if hasattr(w, "ARM") else (0.6, 0.62, 0.66), 905, shadow=False, lw=1.6 * s)


CAN_HANDLE = (24, -16)                                       # oil_can's loop handle, in its own units from its base


def visor_icon(k, sx, sy, r, kind):
    """Over the face: the dark visor, then one cyan pictogram. kind: "sun", "barrier", "public"."""
    c = k.c
    c.set_source_rgb(*VISOR); c.arc(sx, sy, 0.86 * r, 0, 2 * math.pi); c.fill()
    g = cairo.RadialGradient(sx, sy, 0.1 * r, sx, sy, 0.86 * r)
    g.add_color_stop_rgba(0, *CYAN, 0.18); g.add_color_stop_rgba(1, *CYAN, 0.0)
    c.set_source(g); c.arc(sx, sy, 0.86 * r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*CYAN); c.set_line_cap(1); c.set_line_join(1)
    if kind == "sun":
        if SUN_UP[0]:
            sx -= 0.16 * r
        c.set_line_width(0.07 * r); c.arc(sx, sy, 0.22 * r, 0, 2 * math.pi); c.stroke()
        for i in range(8):
            a = i * math.pi / 4
            c.move_to(sx + math.cos(a) * 0.34 * r, sy + math.sin(a) * 0.34 * r)
            c.line_to(sx + math.cos(a) * 0.52 * r, sy + math.sin(a) * 0.52 * r); c.stroke()
        if SUN_UP[0]:                                          # the arrow: up
            ax = sx + 0.62 * r
            c.set_line_width(0.08 * r)
            c.move_to(ax, sy + 0.30 * r); c.line_to(ax, sy - 0.32 * r); c.stroke()
            c.move_to(ax - 0.14 * r, sy - 0.16 * r); c.line_to(ax, sy - 0.32 * r); c.line_to(ax + 0.14 * r, sy - 0.16 * r); c.stroke()
    elif kind == "heart":                                    # opt-in (ep 14 gags, 25 Nov): 5.3, the oil can in its hand
        c.new_path(); c.move_to(sx, sy + 0.42 * r)
        c.curve_to(sx - 0.70 * r, sy - 0.05 * r, sx - 0.34 * r, sy - 0.56 * r, sx, sy - 0.18 * r)
        c.curve_to(sx + 0.34 * r, sy - 0.56 * r, sx + 0.70 * r, sy - 0.05 * r, sx, sy + 0.42 * r)
        c.close_path(); c.fill()
    elif kind == "barrier":
        w, h = 0.98 * r, 0.22 * r
        x0, y0 = sx - w / 2, sy - h / 2 + 0.08 * r
        c.set_line_width(0.05 * r); c.rectangle(x0, y0, w, h); c.stroke()
        c.save(); c.rectangle(x0, y0, w, h); c.clip()
        for i in range(-2, 8):                                            # the stripes
            xx = x0 + i * 0.20 * r
            c.move_to(xx, y0 + h); c.line_to(xx + h, y0); c.set_line_width(0.06 * r); c.stroke()
        c.restore()
        for lx in (x0 + 0.12 * r, x0 + w - 0.12 * r):                     # its legs
            c.move_to(lx, y0 + h); c.line_to(lx, y0 + h + 0.24 * r); c.stroke()
        c.set_source_rgba(1.0, 0.25, 0.20, 0.35); c.arc(sx, y0 - 0.16 * r, 0.17 * r, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(1.0, 0.28, 0.22); c.arc(sx, y0 - 0.16 * r, 0.09 * r, 0, 2 * math.pi); c.fill()   # the red light
    elif kind == "ask":                                      # opt-in (ep 14 phone review, 25 Nov): 3.3, one big "?" -- the
        c.select_font_face("Lilita One"); c.set_font_size(0.95 * r)   # bubble already says PUBLIC POST?, the visor
        e = c.text_extents("?"); c.move_to(sx - e.x_advance / 2 - e.x_bearing, sy - e.y_bearing / 2 - e.height / 2 + 0.06 * r)
        c.show_text("?")                                     # must not say it twice
    elif kind == "public":
        c.select_font_face("Lilita One"); c.set_font_size(0.30 * r)
        for i, t in enumerate(("PUBLIC", "POST?")):
            e = c.text_extents(t); c.move_to(sx - e.x_advance / 2, sy - 0.04 * r + i * 0.34 * r); c.show_text(t)


def team_photo(w=184, h=184):
    """v2 (the review: "abstract coloured bars"): the photo as a miniature of 3.1, drawn with the cast's own rigs: the
    glass door with bodyguard 2's silhouette, Don posing, Pam beside him, Mom ON the tape, the robot balancing on it,
    Sofía with her heel behind it. Returns an ARGB surface w x h (in the film: 3.1's own frame instead)."""
    import fs_storyboard as sb
    import mom_fs as mfs
    import sofia_ps as sps
    import pam_bc as pb
    f = cairo.ImageSurface(cairo.FORMAT_ARGB32, w * 2, h * 2); f.set_device_scale(2, 2)
    c = cairo.Context(f); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    fl = h * 0.88
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, fl, w, h - fl); c.fill()
    c.set_source_rgb(0.80, 0.90, 0.95); c.rectangle(4, h * 0.18, w * 0.17, fl - h * 0.18); c.fill()         # the glass door
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(4, h * 0.18, w * 0.17, fl - h * 0.18); c.stroke()
    c.set_source_rgba(0.08, 0.08, 0.10, 0.75); c.arc(4 + w * 0.085, h * 0.30, 9, 0, 2 * math.pi); c.fill()   # the silhouette
    c.rectangle(4 + w * 0.085 - 10, h * 0.36, 20, fl - h * 0.36); c.fill()
    tx = w * 0.70
    cut(k, [(tx - 2.5, fl), (tx + 2.5, fl), (tx + 7, h), (tx - 7, h)], TAPE, shadow=False, lw=1)
    sc = 0.30
    sb.don(k, w * 0.32, fl + 6, 0.60 * sc / 0.60 * 0.95, "vest", "smile", look=(0.2, 0))
    pb.pam(k, w * 0.50, fl + 4, 0.54 * sc / 0.60 * 0.95, "stand", "smile", (-0.6, 0), glasses="low")
    mfs.mom(k, tx - 2, fl, 0.54 * sc / 0.60 * 0.95, "fists", "unimpressed", look=(-0.6, 0.2))
    sps.sofia(k, w * 0.86, fl + 8, 0.47 * sc / 0.60 * 1.0, "stand", "smile", look=(-0.4, 0))
    c.set_source_rgb(*sps.HEEL_GOLD); c.rectangle(tx + 6, fl + 6, 4, 6); c.fill()                      # her heel behind the line
    return f


def phone_screen(k, x, y, s, kind="photo", seed=4700):
    """The selfie phone, screen to us, centred at (x, y). kind "photo": the team shot; "public": PUBLIC POST? and an
    unanswered APPROVE pad; "approved": the pad green under Don's thumb; "posted": #TeamDon."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -60, -104, 120, 208, (0.08, 0.08, 0.09), seed, shadow=False, lw=2.6)
    if UI_KIT[0] and kind in ("public", "approved", "posted", "zoom"):   # opt-in (Pick a Side, 25 Nov): episode 13's UI kit
        import ps_ui
        import of_ui
        fn = (ps_ui.post if kind == "posted" else (lambda c_, H: ps_ui.post(c_, H, False)) if kind == "zoom"
              else (lambda c_, H: ps_ui.public(c_, H, kind == "approved")))
        of_ui.full(c, -52, -94, 104, 188, fn)
        c.restore()
        return
    c.set_source_rgb(0.96, 0.96, 0.98); c.rectangle(-52, -94, 104, 188); c.fill()
    ph = team_photo()
    c.save(); c.translate(-48, -74); c.scale(96 / 184, 96 / 184); c.set_source_surface(ph, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(-48, -74, 96, 96); c.stroke()
    if kind in ("public", "approved"):
        c.set_source_rgba(0.08, 0.10, 0.18, 0.92); c.rectangle(-52, 26, 104, 68); c.fill()
        c.set_source_rgb(*CYAN); c.select_font_face("Lilita One"); c.set_font_size(17)
        e = c.text_extents("PUBLIC POST?"); c.move_to(-e.x_advance / 2, 48); c.show_text("PUBLIC POST?")
        if kind == "public":                                    # unanswered: an outlined pad, the word, no tick
            c.set_source_rgb(0.30, 0.34, 0.42); c.rectangle(-34, 58, 68, 26); c.fill()
            c.set_source_rgb(*CYAN); c.set_line_width(2); c.rectangle(-34, 58, 68, 26); c.stroke()
            c.select_font_face("Inter", 0, 1); c.set_font_size(11); e = c.text_extents("APPROVE")
            c.move_to(-e.x_advance / 2, 75); c.show_text("APPROVE")
        else:                                                   # Don's thumb on it: green, ticked
            rect(k, -34, 58, 68, 26, (0.20, 0.68, 0.36), seed + 1, shadow=False, lw=1.6)
            c.set_source_rgb(1, 1, 1); c.set_line_width(3); c.move_to(-8, 71); c.line_to(-2, 77); c.line_to(10, 63); c.stroke()
            if PAD_THUMB[0]:
                cut(k, [(14, 104), (8, 74), (16, 64), (30, 66), (40, 104)], (0.93, 0.76, 0.62), lw=2)   # his thumb, from below
            ellipse(k, 20, 70, 7, 5, (0.98, 0.90, 0.84), seed + 2, shadow=False, lw=1.2)
    else:
        c.set_source_rgb(0.15, 0.17, 0.25); c.select_font_face("Lilita One"); c.set_font_size(18)
        t = "#TeamDon" if kind == "posted" else ""
        e = c.text_extents(t); c.move_to(-e.x_advance / 2, 52); c.show_text(t)
        if kind == "posted":
            c.set_source_rgb(0.80, 0.30, 0.40); c.select_font_face("Inter", 0, 1); c.set_font_size(11)
            if HEART[0]:                                        # v4 (24 Nov audit): Inter has no ♥, it drew a hex-code box
                c.save(); c.translate(-35, 73); c.new_path(); c.move_to(0, 4)
                c.curve_to(-7, -1, -5, -8, 0, -4); c.curve_to(5, -8, 7, -1, 0, 4); c.close_path(); c.fill(); c.restore()
                c.move_to(-26, 76); c.show_text("1   · just now")
            else:
                c.move_to(-40, 76); c.show_text("♥ 1   · just now")
    c.restore()


def phone_back(k, x, y, s, ang=0.35, seed=4730):
    """The phone from behind, angled down toward the group: a big lens and the flash LED. Returns the lens point."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -60, -104, 120, 208, (0.14, 0.15, 0.18), seed, shadow=False, lw=2.6)
    ellipse(k, -18, -62, 26, 26, (0.22, 0.24, 0.30), seed + 1, shadow=False, lw=2.4)        # the lens housing
    ellipse(k, -18, -62, 15, 15, (0.05, 0.06, 0.10), seed + 2, shadow=False, lw=1.6)        # the lens
    c.set_source_rgba(0.6, 0.8, 1.0, 0.6); c.arc(-23, -67, 4, 0, 2 * math.pi); c.fill()
    ellipse(k, 26, -66, 8, 8, (0.98, 0.95, 0.80), seed + 3, shadow=False, lw=1.4)          # the flash LED
    c.restore()
    lx = x + (math.cos(ang) * 26 - math.sin(ang) * -66) * s
    ly = y + (math.sin(ang) * 26 + math.cos(ang) * -66) * s
    return lx, ly


def telescope(k, bx, by, s, u, angle=0.30, seed=4720):
    """The arm, telescoped out of its hand point (bx, by) by u (0..1), leaning by angle; returns the tip."""
    c = k.c
    L = 230 * u
    c.save(); c.translate(bx, by); c.rotate(angle); c.scale(s, s)
    for i, (w, l0, l1) in enumerate(((16, 0, 0.40), (12, 0.34, 0.72), (9, 0.66, 1.0))):
        if L * l1 <= 0:
            continue
        rect(k, -w / 2, -L * l1, w, L * (l1 - l0), STEEL if i % 2 == 0 else STEEL_D, seed + i, shadow=False, lw=2)
    c.restore()
    return bx + math.sin(angle) * L * s, by - math.cos(angle) * L * s


HEAD_ROT = [None]   # opt-in (28 Nov, ep15): the head's own tilt in radians; None draws as before


def robot(k, x, feet, s=S_OFFICE, arms=None, tilt=0.0, visor=None, selfie=0.0, phone=None, turn=0.0, look=(0, 0), tele=None, phone_s=0.34):
    """arms: ((upper, fore) screen-left, (upper, fore) screen-right) in kit angles (0 down, +90 right); tilt: radians it
    leans about its wheel (balancing); visor: None (its smile) or an icon; selfie: 0..1 the telescope out of its
    screen-right hand; phone: the phone's screen at the tip ("photo", "public", "posted", or None for its back)."""
    c = k.c
    a = arms or ((-8, 0), (8, 0))
    pose = (tilt, 0, 0, a[0], a[1])
    o = dq.rm.robot(k, x, feet, s, pose, "eager", look, 1, head_rot=HEAD_ROT[0])
    r = 50 * s
    if visor:
        visor_icon(k, *o["screen"], r, visor)
    if selfie > 0:
        hx, hy = o["hands"][1]
        tx, ty = telescope(k, hx, hy, s, selfie) if tele is None else telescope(k, hx, hy, s, selfie, angle=tele)   # tele: opt-in lean
        if phone:
            phone_screen(k, tx, ty - 30 * s, s * phone_s, phone)   # phone_s: opt-in size (3.4's gag: it must read at feed size)
            o["phone"] = (tx, ty - 30 * s)
        else:
            o["phone"] = phone_back(k, tx, ty - 30 * s, s * 0.40)           # the lens, angled down at the group
    return o


def tape(k, x, wall, bottom, top_w=10, bot_w=34, lean=0.08):
    """The tape on the floor, from the wall line to the bottom of the frame, widening toward us (it runs at the camera)."""
    dx = (bottom - wall) * lean
    cut(k, [(x - top_w / 2, wall), (x + top_w / 2, wall), (x + dx + bot_w / 2, bottom), (x + dx - bot_w / 2, bottom)], TAPE,
        shadow=False, lw=1.8)


def flash(k, x, y, r):
    """A camera flash (lesson 114: a flash only where something flashes): a white star with rays."""
    c = k.c
    c.set_source_rgba(1, 1, 0.92, 0.85)
    c.move_to(x, y - r)
    for i in range(1, 16):
        a = -math.pi / 2 + i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.38
        c.line_to(x + math.cos(a) * rr, y + math.sin(a) * rr)
    c.close_path(); c.fill()


def _label(c, s, x, y, size=16, col=INK):
    c.select_font_face("Inter", 0, 1); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s); c.move_to(x - e.x_advance / 2, y); c.show_text(s)


def sheet(out):
    import fs_storyboard as sb
    W, H = 2200, 1500
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(*kit.WALL); c.paint()
    F = 760
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, F, W, 180); c.fill()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(30); c.set_source_rgb(*INK); c.move_to(40, 50)
    c.show_text("PICK A SIDE · THE ROBOT · 13's HR robot at the office scale (0.66) · this episode's parts · v2")
    c.select_font_face("Inter", 0, 0); c.set_font_size(18); c.move_to(40, 84)
    c.show_text("the telescopic selfie arm and its phone · balancing on the tape · cyan visor pictograms · it always smiles")
    Z = 1.45
    sb.don(k, 130, F, 0.60 * Z, "stand", "neutral", look=(1, 0))
    robot(k, 330, F, S_OFFICE * Z)
    bx0, by0 = 470, 300                                                                      # 1.1: the blind, its cord, its hand
    c.set_source_rgb(0.86, 0.86, 0.82); c.rectangle(bx0, by0, 170, 120); c.fill()
    c.set_source_rgb(0.55, 0.55, 0.52); c.set_line_width(1.4)
    for yy in range(by0 + 8, by0 + 120, 10):
        c.move_to(bx0, yy); c.line_to(bx0 + 170, yy); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.rectangle(bx0, by0, 170, 120); c.stroke()
    rect(k, bx0 - 6, by0 - 12, 182, 14, (0.70, 0.70, 0.66), 4740, shadow=False, lw=2)          # its rail
    o = robot(k, 560, F, S_OFFICE * Z, arms=((-8, 0), (165, 15)), visor="sun")
    hx, hy = o["hands"][1]
    c.set_source_rgb(0.30, 0.30, 0.30); c.set_line_width(2.4); c.move_to(bx0 + 160, by0 + 120); c.line_to(hx, hy); c.stroke()
    ellipse(k, hx, hy + 10, 4, 6, (0.92, 0.88, 0.70), 4741, shadow=False, lw=1.4)              # the cord's acorn, under the grip
    ellipse(k, hx, hy, 9, 9, (0.60, 0.62, 0.66), 4742, shadow=False, lw=1.8)                  # the grip
    robot(k, 790, F, S_OFFICE * Z, visor="barrier")                                         # 2.9
    tape(k, 940, F, F + 180, top_w=20, bot_w=46, lean=0.85)                                # one stripe, at an angle: behind and in front of the wheel
    robot(k, 1024, F + 98, S_OFFICE * Z, arms=((-150, 25), (55, -25)), tilt=0.18)           # 2.10: the wobble, one arm up
    o = robot(k, 1290, F, S_OFFICE * Z, selfie=1.0, phone=None)                             # 3.1: the arm up, FLASH
    flash(k, o["phone"][0], o["phone"][1], 40)                                              # from the lens
    robot(k, 1540, F, S_OFFICE * Z, visor="public", selfie=0.7, phone="public", arms=((-8, 0), (40, 30)))   # 3.3
    phone_screen(k, 1800, 470, 1.25, "public")
    phone_screen(k, 1960, 470, 1.25, "approved")
    phone_screen(k, 2120, 470, 1.25, "posted")
    for x, n, note in ((130, "DON", "0.60, for scale"), (330, "AT REST", "0.66, the smile"), (560, "1.1", "the cord; the sun"),
                       (790, "2.9", "Border breach"), (1030, "2.10", "on the tape, arms out"), (1290, "3.1", "the arm up; FLASH"),
                       (1540, "3.3", "the phone turned to Don"), (1800, "3.3", "unanswered"), (1960, "3.4", "Don's thumb"), (2120, "3.5", "#TeamDon")):
        _label(c, n, x, F + 230, 20); _label(c, note, x, F + 256, 14, (0.3, 0.3, 0.3))
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    import fs_storyboard as sb
    frames = []
    for name, txt in (("medium", "2.10: wobbling on the tape, Don beside it"), ("close", "2.9: Border breach"), ("insert", "3.2: the photo")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        if name == "medium":
            c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 760, 540, 200); c.fill()
            sb.don(k, 160, 800, 0.60 * 1.9, "stand", "neutral", look=(1, 0))
            tape(k, 300, 760, 960, top_w=24, bot_w=60, lean=0.75)
            robot(k, 392, 880, S_OFFICE * 1.9, arms=((-150, 25), (55, -25)), tilt=-0.16)
        elif name == "close":
            robot(k, 270, 1260, S_OFFICE * 4.0, visor="barrier")
        else:
            phone_screen(k, 270, 470, 3.6, "photo")
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_robot_v2.png"))
    phone(os.path.join(d, "ps_robot_phone_v2.png"))
