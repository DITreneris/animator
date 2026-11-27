"""16:9 frame for The Blueprint. Opt-in.

kit.W, kit.H and fs_storyboard.view stay 540x960, centre (270, 480).
This module centres a 960x540 logical frame at (480, 270) and can render that
frame at 2x to 1920x1080. Nothing here is imported by a shipped episode.
"""
import os

import cairo
import numpy as np

import kit

W, H = 960, 540
SCALE = 2
OUT_W, OUT_H = W * SCALE, H * SCALE

# Phase-1 stills, logical pixels. These are not the 540-wide gate bands
# (CU r >= 120 at 540). S0 at z=1.0 is a wide of a 960-wide world: a face
# that was a medium shot in 9:16 reads smaller here. Pin after the stills
# are looked at; the render writes the measured note beside the PNG.
FACE_WS_MAX = 70

# Cameras: (cx, cy, z) in fs_set4 world space. Floor is set_ob.FLOOR = 800.
# Character scales stay the home scales. Don stays the tallest.
# S0 is the wide. cy leaves air above the UPTIMEZ FIND screen (its top is world y 286).
# SHRED is the action detail: the robot is inside, the portrait is out, the counter is only a slice.
# COUNTER is centred on the desk. z is high enough that the frame does not run off the
# world into an empty wall (the set ends at x 960).
# The room is already 960x540. S0 shows all of it, so the floor band is the bottom 26%.
S0 = (480, 270, 1.0)
SHRED = (300, 386, 1.45)
COUNTER = (730, 320, 1.58)
PUSH = (420, 360, 1.35)
# Night two-shot. Sofía and Pam both in, Client and both doors out. Not in set-16x9.md until a still is approved.
NIGHT = (560, 360, 1.85)
# Phase 5. The words the wide cameras crop off. Not in set-16x9.md.
# ZERO holds the poster, the screen, the lockup, and OUR FIRST CLIENT, each whole.
ZERO = (357, 108, 2.27)
# STAMP holds the landed page and the robot's head. CUSTOMER SUCCESS is the word.
STAMP = (246, 430, 2.8)
# PLAN is the taped strips on the desk. The monitor and the nameplate stay outside.
PLAN = (715, 329, 19.0)

# Blueprint staging only. Not written back to fs_set4.HOME.
# Sofía steps toward Don and onto the client's floor line. Pam and Mom rise
# behind the counter so the desk does not swallow their faces.
SOFIA_DX = 30
PAM_LIFT = 20
MOM_LIFT = 12
PORTRAIT_DY = 18           # down, so the wide uses the wall under the frame


def view(c, cx, cy, z):
    """Stage point (cx, cy) to the centre of the 960x540 frame, zoom z."""
    c.translate(W / 2.0, H / 2.0)
    c.scale(z, z)
    c.translate(-cx, -cy)


def surface(scale=SCALE):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, int(W * scale), int(H * scale))
    if scale != 1:
        surf.set_device_scale(scale, scale)
    return surf


def rgb_bytes(surf):
    """Cairo RGB24 is B,G,R,X in memory on little-endian. ffmpeg wants packed RGB."""
    surf.flush()
    w, h = surf.get_width(), surf.get_height()
    buf = np.ndarray((h, surf.get_stride() // 4, 4), dtype=np.uint8, buffer=surf.get_data())
    rgb = np.ascontiguousarray(buf[:, :w, 2::-1])
    return rgb.tobytes(), w, h


def _cast(s4):
    """Same drawings as fs_set4's home cast, with the Blueprint places. Scales are the home scales."""
    F = s4.F
    H = s4.HOME
    sb = s4.sb
    sofia = (H["sofia"][0] + SOFIA_DX, F - 14, H["sofia"][2])
    pam = (H["pam"][0], H["pam"][1] - PAM_LIFT, H["pam"][2])
    mom = (H["mom"][0], H["mom"][1] - MOM_LIFT, H["mom"][2])

    def pam_back(k):
        sb.pam_taping(k, *pam)

    def mom_back(k):
        s4.mfs.mom(k, *mom, "fists", "unimpressed", look=(-0.9, 0.3), chin=True)

    def client(k):
        s4.shadow(k, H["client"][0], F - 12, 44)
        sb.client(k, *H["client"], "stand", "confident", (0.9, 0))

    def robot(k):
        s4.shadow(k, H["robot"][0], F + 6, 30)
        s4.fs.robot_finger(k, *H["robot"])

    def sofia_draw(k):
        s4.shadow(k, sofia[0], sofia[1] + 2, 32)
        s4.sfs.sofia(k, *sofia, "hold", "charm", look=(0.6, -0.2))

    def don(k):
        s4.shadow(k, H["don"][0], F + 28, 46)
        sb.DON_STATE[0] = ("up", "up")
        try:
            sb.don(k, *H["don"], "stand", "neutral", (-1, 0))
        finally:
            sb.DON_STATE[0] = None

    return {"pam_back": pam_back, "mom_back": mom_back, "client": client, "robot": robot,
            "sofia": sofia_draw, "don": don}


def _line(c, text, x, y, w, size, col, baseline):
    """Centre text in an existing bar. Shrink until it fits. The bar is not resized."""
    c.set_source_rgb(*col)
    c.select_font_face("Inter", 0, 1)
    while size > 4:
        c.set_font_size(size)
        if c.text_extents(text).x_advance <= w - 6:
            break
        size -= 0.4
    e = c.text_extents(text)
    c.move_to(x + (w - e.x_advance) / 2.0, baseline)
    c.show_text(text)


def _fit_door_label(s4):
    """Repaint the door's two existing labels so the words sit inside them."""
    real = s4.office_door

    def office_door(k):
        real(k)
        x, y, w, h = s4.OFFICE
        c = k.c
        # The old type runs past the bar. Cover it, then put the stile and the wall back.
        c.set_source_rgb(0.62, 0.44, 0.28)
        c.rectangle(x + 4, y + 6, w - 4, 22)
        c.fill()
        c.set_source_rgb(0.30, 0.24, 0.20)
        c.rectangle(x + w, y - 6, 6, h + 12)
        c.fill()
        c.set_source_rgb(*kit.WALL)
        c.rectangle(x + w + 6, y, 40, 32)
        c.fill()
        kit.rect(k, x + 6, y + 8, w - 12, 18, (0.15, 0.17, 0.22), 805, shadow=False, lw=1.2)
        _line(c, "DON · CEO", x + 6, y + 8, w - 12, 9, (1, 1, 1), y + 21)
        kit.rect(k, x - 4, y - 46, w + 8, 34, (0.85, 0.70, 0.30), 806, lw=1.6)
        _line(c, "DON · CEO", x - 4, y - 46, w + 8, 10, (0.25, 0.18, 0.05), y - 31)
        _line(c, "VISIONARY", x - 4, y - 46, w + 8, 9, (0.25, 0.18, 0.05), y - 18)

    return real, office_door


# Night palette. Only grade<1 frames. The locked stills stay on grade 1.
NIGHT_AMBIENT = (0x24 / 255.0, 0x2D / 255.0, 0x40 / 255.0)  # #242D40
NIGHT_SHADOW = (0x13 / 255.0, 0x1C / 255.0, 0x2C / 255.0)   # #131C2C
NIGHT_MONITOR = (0x9E / 255.0, 0xDF / 255.0, 0xFF / 255.0)  # #9EDFFF
NIGHT_WARM = (0xE5 / 255.0, 0xB3 / 255.0, 0x6D / 255.0)     # #E5B36D


def _night_bars(c, room, clip_y, clip_h, slope, pitch, y_shift, n, gain):
    """One plane. Wall and floor do not share a slope. Day ambience is not edited."""
    x0, w = room._span()
    x1 = x0 + w
    # About 40% quieter than the previous night bars (0.07 / 0.13).
    for i in range(n):
        y0 = y_shift + i * pitch
        drop = (x1 - x0) * slope
        for thick, a_l, a_r in ((16, 0.042, 0.015), (8, 0.078, 0.030)):
            pad = (16 - thick) / 2.0
            c.save()
            c.rectangle(x0, clip_y, w, clip_h)
            c.clip()
            g = cairo.LinearGradient(x0, 0, x1, 0)
            g.add_color_stop_rgba(0, *NIGHT_SHADOW, a_l * gain)
            g.add_color_stop_rgba(1, *NIGHT_SHADOW, a_r * gain)
            c.set_source(g)
            yy = y0 + pad
            c.move_to(x0, yy)
            c.line_to(x1, yy + drop)
            c.line_to(x1, yy + thick + drop)
            c.line_to(x0, yy + thick)
            c.close_path()
            c.fill()
            c.restore()


def _pool(c, cx, cy, rx, ry, stops):
    c.save()
    c.translate(cx, cy)
    c.scale(rx, ry)
    g = cairo.RadialGradient(0, 0, 0.08, 0, 0, 1.0)
    for stop, col in stops:
        g.add_color_stop_rgba(stop, *col)
    c.set_source(g)
    c.arc(0, 0, 1.0, 0, 6.2832)
    c.fill()
    c.restore()


def _rim(c, room):
    """A cold edge on the window side of Sofía and Don. The offset is 3 device pixels."""
    target = c.get_target()
    sx, sy = target.get_device_scale()
    mask = cairo.ImageSurface(cairo.FORMAT_A8, target.get_width(), target.get_height())
    mask.set_device_scale(sx, sy)
    mc = cairo.Context(mask)
    mc.set_matrix(c.get_matrix())
    k = kit.Ctx(mc, 0)
    import fs_storyboard_v17 as sb
    import sofia_fs as sfs
    mc.save()
    mc.rectangle(300, 290, 110, 175)
    mc.clip()
    sfs.sofia(k, *room.SOFIA, "hold", "charm", look=(0.6, -0.2))
    mc.restore()
    mc.save()
    mc.rectangle(415, 280, 140, 230)
    mc.clip()
    sb.DON_STATE[0] = ("up", "up")
    try:
        sb.don(k, *room.DON, "stand", "neutral", (-1, 0))
    finally:
        sb.DON_STATE[0] = None
    mc.restore()
    mask.flush()

    edge = cairo.ImageSurface(cairo.FORMAT_A8, target.get_width(), target.get_height())
    edge.set_device_scale(sx, sy)
    ec = cairo.Context(edge)
    ec.set_source_surface(mask, -3.0 / sx, -1.0 / sy)
    ec.paint()
    ec.set_operator(cairo.OPERATOR_DEST_OUT)
    ec.set_source_surface(mask, 0, 0)
    ec.paint()

    c.save()
    c.identity_matrix()
    c.set_operator(cairo.OPERATOR_SCREEN)
    c.set_source_rgba(0.62, 0.78, 1.0, 0.42)
    c.mask_surface(edge, 0, 0)
    c.restore()


def _copy_frame(c):
    target = c.get_target()
    target.flush()
    sx, sy = target.get_device_scale()
    snap = cairo.ImageSurface(cairo.FORMAT_RGB24, target.get_width(), target.get_height())
    snap.set_device_scale(sx, sy)
    sc = cairo.Context(snap)
    sc.set_source_surface(target, 0, 0)
    sc.paint()
    return snap


def _restore_colors(c, snap, clip, draw):
    """Put the day colours back inside one visible body. The night grade stays on the room."""
    target = c.get_target()
    sx, sy = target.get_device_scale()
    mask = cairo.ImageSurface(cairo.FORMAT_A8, target.get_width(), target.get_height())
    mask.set_device_scale(sx, sy)
    mc = cairo.Context(mask)
    mc.set_matrix(c.get_matrix())
    mc.rectangle(*clip)
    mc.clip()
    draw(kit.Ctx(mc, 0))
    c.save()
    c.identity_matrix()
    c.set_source_surface(snap, 0, 0)
    c.mask_surface(mask, 0, 0)
    c.restore()


def _night_layers(room):
    """Back to front, same order as the day room. Each shape is restored from the day frame."""
    import fs_set as fs
    import fs_storyboard_v17 as sb
    import mom_fs as mfs
    import sofia_fs as sfs

    wide = (-200, -40, 1600, 820)

    def chair_l(k):
        room._chair(k, room.PAM[0] - 36, room.BACK)

    def chair_r(k):
        room._chair(k, room.MOM[0] + 30, room.BACK)

    def pam(k):
        room._contact(k, room.PAM[0], room.PAM[1], 28)
        sb.pam_taping(k, *room.PAM)

    def mom(k):
        room._contact(k, room.MOM[0], room.MOM[1], 28)
        mfs.mom(k, *room.MOM, "fists", "unimpressed", look=(-0.9, 0.3), chin=True)

    def desk(k):
        room._counter(k)
        room._desk_things(k, room._people.hide_plan)

    def portrait(k):
        fs.portrait(k, 508, 128, 0.72)

    def cabinet(k):
        room._cabinet(k, 540, room.CAB)

    def sofia(k):
        room._contact(k, room.SOFIA[0], room.SOFIA[1], 26)
        sfs.sofia(k, *room.SOFIA, "hold", "charm", look=(0.6, -0.2))

    def shredder(k):
        room._shredder(k)

    def don(k):
        room._contact(k, room.DON[0], room.DON[1], 34)
        sb.DON_STATE[0] = ("up", "up")
        try:
            sb.don(k, *room.DON, "stand", "neutral", (-1, 0))
        finally:
            sb.DON_STATE[0] = None

    return (
        (wide, chair_l), (wide, chair_r), (wide, pam), (wide, mom), (wide, desk),
        (wide, portrait), (wide, cabinet), (wide, sofia), (wide, shredder), (wide, don),
    )


def _pam_hands(room):
    import fs_storyboard_v17 as sb
    dummy = cairo.ImageSurface(cairo.FORMAT_A8, 8, 8)
    o = sb.pam_taping(kit.Ctx(cairo.Context(dummy), 0), *room.PAM)
    return o["hands"]


def _night(c, room):
    """Flat night wall and floor, then the day shapes put back. Stripes do not cross both planes."""
    day = _copy_frame(c)
    x0, w = room._span()
    c.set_source_rgb(0x59 / 255.0, 0x67 / 255.0, 0x80 / 255.0)
    c.rectangle(x0, -80, w, room.F + 80)
    c.fill()
    c.set_source_rgb(0x3E / 255.0, 0x4B / 255.0, 0x63 / 255.0)
    c.rectangle(x0, room.F, w, 240)
    c.fill()
    room._baseboard(kit.Ctx(c, 0))
    c.set_source_rgba(*NIGHT_SHADOW, 0.22)
    c.set_line_width(1.1)
    c.move_to(x0, room.F - 72)
    c.line_to(x0 + w, room.F - 72)
    c.stroke()

    # Wall keeps the window's slope. The floor is a flatter plane, so the bars do not continue.
    _night_bars(c, room, 0, room.F, 0.36, 52, 18, 5, 1.0)
    _night_bars(c, room, room.F, 210, 0.08, 78, room.F + 18, 3, 0.70)

    for clip, draw in _night_layers(room):
        _restore_colors(c, day, clip, draw)

    c.save()
    c.translate(566, 409)
    c.scale(26, 5)
    c.set_source_rgba(*NIGHT_SHADOW, 0.80)
    c.arc(0, 0, 1, 0, 6.2832)
    c.fill()
    c.restore()
    c.set_source_rgba(*NIGHT_SHADOW, 0.75)
    c.rectangle(536, 404, 62, 5)
    c.fill()

    c.save()
    c.set_source_rgb(*NIGHT_MONITOR)
    c.rectangle(666.1, 313.3, 19.8, 12.2)
    c.fill()
    c.set_operator(cairo.OPERATOR_SCREEN)
    _pool(c, 676, 314, 28, 18, (
        (0.0, NIGHT_MONITOR + (0.28,)),
        (1.0, NIGHT_MONITOR + (0.0,)),
    ))
    _pool(c, room.PAM[0], room.PAM[1] - 88, 16, 11, (
        (0.0, NIGHT_MONITOR + (0.42,)),
        (1.0, NIGHT_MONITOR + (0.0,)),
    ))
    for hx, hy in _pam_hands(room):
        _pool(c, hx, hy, 9, 6, (
            (0.0, NIGHT_MONITOR + (0.48,)),
            (1.0, NIGHT_MONITOR + (0.0,)),
        ))
    c.set_operator(cairo.OPERATOR_OVER)
    _pool(c, 792, 358, 52, 30, (
        (0.0, NIGHT_WARM + (0.34,)),
        (1.0, NIGHT_WARM + (0.0,)),
    ))
    c.restore()
    _rim(c, room)


def paint(cam, overlay=None, hide_plan=False, grade=1.0, bubble=None, scale=SCALE):
    """One frame. hide_plan skips fs.plan_taped for this call only. fs_set4.py is not edited."""
    import fs_set as fs
    import fs_set4

    if kit.W != 540 or kit.H != 960:
        raise RuntimeError("kit frame changed: %s x %s" % (kit.W, kit.H))
    surf = surface(scale)
    c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL)
    c.paint()
    c.save()
    c.rectangle(0, 0, W, H)
    c.clip()
    view(c, *cam)
    import bp_set
    saved_door, door = _fit_door_label(fs_set4)
    fs_set4.office_door = door
    try:
        k = kit.Ctx(c, 0)
        bp_set.draw(k, hide_plan=hide_plan)
        if overlay is not None:
            overlay(c)
        if grade < 1.0:
            _night(c, bp_set)
    finally:
        fs_set4.office_door = saved_door
        c.restore()
    if bubble is not None:
        import speech
        from speech_gate import SAFE_16X9
        text, head = bubble
        speech.draw(kit.Ctx(c, 0), text, head, safe=SAFE_16X9)
    return surf


def write_png(surf, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    surf.write_to_png(path)
    return path
