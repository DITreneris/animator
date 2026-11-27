"""The Blueprint, the picture pass. Budget: bp_pic_v1 to bp_pic_v5.

A new picture. It does not rewrite bp_rough_v1 to v5, bp_sound_v1, or the locked stills, and it does not edit
bp_set._poster. The green disc stays in the set. This cut paints a dull disc over it until Don's "Approved."
on shot 07, then lets the poster green show.

v1: one bubble on the hold (and on an insert, when a line falls there) while that person talks. Shot 10 is PUSH
in this cut only. SHOTS stays COUNTER, so a rebuild of rough v5 is unchanged. Inserts stay in v5's order.

v2: the same picture, except shot 03 and shot 11. The promise is said, then Don's hand puts the page in the
shredder, then the deal. The joke is said, then the card leaves the pocket while Pam says to check it, then
her hand is on the card. The finger insert stays undrawn. Line times for this cut are bp_pic_v2_timing.json.
bp_sound_v1_timing.json is not rewritten.

v3: the same times as v2. Shot 01 hides the wall portrait and drops fs.portrait to the floor. Shot 04's
cannon runs its fuse and throws confetti at the bin. On "I'm matching them." the taped plan and Pam's hand
are on the desk. The stamp is not redrawn. write_timing() is not called.

v4: the same times as v3. SHEET and MOM_ARMS are on for this version only, so the signed sheet look is in
the frames. Shot 12's star insert is the phone grip from the signed still, on that still's crop. The
rectangle phone stays on v3. Shred, the card and the tape stay point. write_timing() is not called.

  python3 bp_picture.py plant     -> the bubble, the gap and the zero, each on a known wrong frame; exit 1 unless all three fail
  python3 bp_picture.py bubbles   -> speech_gate on one frame of every line; exit 1 on a fault
  python3 bp_picture.py beats     -> the fall, the firing and the matching; exit 1 on a fault
  python3 bp_picture.py beats --plant -> an olive board, a cold cannon, a sheet with no hand, a hand with no arm; exit 1 when each is caught
  python3 bp_picture.py grips     -> the hand stills; exit 1 on a stroke, a second point, or a phone rectangle
  python3 bp_picture.py grips --plant -> those three on today's picture; exit 1 when each is caught
  python3 bp_picture.py handstills -> the four stills only, full size and 270 px
  python3 bp_picture.py use       -> the sheet look and phone v4b, new files only; exit 1 if a lock moves
  python3 bp_picture.py look      -> the v4 checks; exit 1 on a fault. Does not render.
  python3 bp_picture.py render 1  -> bp_pic_v1.mp4 and bp_pic_v1_nonight.mp4
"""
import hashlib
import json
import math
import os
import subprocess
import sys

import cairo
import numpy as np

import bp_frame as fr
import bp_scenes as bs

PIC_BUDGET = 5
FPS = bs.FPS
# Shot 10 only. PUSH holds the Client (132), the robot (248) and Don (476). COUNTER does not.
PUSH_SHOTS = {"10": "PUSH"}
# The disc inside bp_set._poster(k, 300, 78): arc at (350, 146), radius 16. Sampled beside the digit.
DISC = (350, 146, 17)
SAMPLE = (362, 146)
DULL = (0.55, 0.56, 0.58)
LOCKED = {
    "bp_still_s0.png": "25111ff33a2338b32e7bdea584204c28",
    "bp_still_shred.png": "da34775d2ac9821b42f149abb8261149",
    "bp_still_counter.png": "0a25fcc6b5831f360f24eb79c312fb5f",
    "bp_still_night.png": "31e044d813fe94ead453458d7b71d5fe",
}
MOTION = {"arrive", "back", "shred", "finger", "pocket", "stamp", "frame"}
BANNED = ("bp_rough_", "bp_sound_v1")


def _refuse(path, allow_create=False):
    """Refuse banned prefixes. Refuse overwriting an existing file unless allow_create is for a missing path only."""
    name = os.path.basename(path)
    if name.startswith(BANNED):
        raise SystemExit("refusing to write %s" % name)
    if os.path.isfile(path) and not allow_create:
        raise SystemExit("refusing to overwrite %s" % name)


def out_path(version, cut):
    if not 1 <= version <= PIC_BUDGET:
        raise SystemExit("the picture pass has a budget of %d versions; refused %d" % (PIC_BUDGET, version))
    path = os.path.join(bs.EP, "bp_pic_v%d%s.mp4" % (version, "_nonight" if cut == "nonight" else ""))
    _refuse(path)
    return path


def timing_path(version):
    name = "bp_sound_v1_timing.json" if version <= 1 else "bp_pic_v%d_timing.json" % version
    return os.path.join(bs.EP, name)


def rows(cut="full", version=1):
    path = timing_path(version)
    if not os.path.isfile(path):
        raise SystemExit("no timing %s; run write_v%d_timing once" % (os.path.basename(path), version))
    data = json.load(open(path, encoding="utf-8"))["lines"]
    if cut == "nonight":
        data = [r for r in data if r["nonight"] is not None]
    return data


def switch_frame():
    """The first frame after Don's Approved on shot 07. The disc is dull up to here."""
    row = next(r for r in rows() if r["key"] == "fs_4.3")
    return int(round(row["t1"] * FPS))


def drawn(shot):
    """The shot the picture cut paints. SHOTS itself is not changed."""
    shot = dict(shot)
    if shot["id"] in PUSH_SHOTS:
        shot["cam"] = PUSH_SHOTS[shot["id"]]
    return shot


def dull_at(shot_id, frame, switch):
    if shot_id < "07":
        return True
    if shot_id > "07":
        return False
    return frame < switch


def zero_disc(c):
    x, y, r = DISC
    c.set_source_rgb(*DULL)
    c.arc(x, y, r, 0, 2 * np.pi)
    c.fill()
    c.set_source_rgb(1, 1, 1)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(18)
    e = c.text_extents("0")
    c.move_to(x - e.x_advance / 2, y + 6)
    c.show_text("0")


# v2 only. Shot length stays. The finger's 45 empty frames go into the holds: it is not drawn.
# 8s of the promise, then the 2s shred, then the deal. 3.5s of the joke, then the 2s pocket, then the hold.
V2_SPANS = {
    "03": (("promise", 240), ("shred", 60), ("rest", None)),
    "11": (("joke", 105), ("pocket", 60), ("found", None)),
}
# Line lengths are the shipped takes. The starts move so the shred and the pocket come after the lines
# that name them. "Check your pocket." is the one line that plays while the card is moving.
V2_START = {
    "ob_4.1": 1.500,
    "ob_4.3": 5.200,
    "ob_5.4": 11.500,
    "ob_5.5": 14.500,
    "cs_3.5": 1.500,
    "cs_4.2p": 3.500,
    "cs_4.4": 7.000,
}
HOLDS = {"hold", "promise", "rest", "joke", "found", "match"}
# point, from the hands_ps sheet (the index out along the arm). grab, the hand already used on an object.
DON_HAND = "point"
PAM_HAND = "point"
# The fists the room already draws (stand pose). The sleeve starts there, so it is the same arm reached out.
DON_FIST = (508.0, 410.6)
PAM_FIST = (705.0, 341.0)
DON_SLEEVE = (0.93, 0.93, 0.90)   # his shirt
PAM_SLEEVE = (0.45, 0.27, 0.62)   # her top


def _unit(d):
    import math
    n = math.hypot(d[0], d[1]) or 1.0
    return d[0] / n, d[1] / n


def _box(a, b, pad):
    return (min(a[0], b[0]) - pad, min(a[1], b[1]) - pad, max(a[0], b[0]) + pad, max(a[1], b[1]) + pad)


def _overlap(a, b):
    if a is None or b is None:
        return False
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def shred_pose(t, hand=True, arm=True):
    """Don's point, the hands-sheet gesture. The index lands on the page. The sleeve leaves his right fist."""
    x, y0 = bs.SHEET_FROM
    y = y0 + (bs.SHEET_TO[1] - y0) * t
    sheet = (x - 14, y - 18, x + 14, y + 18)
    if not hand:
        return sheet, None, None, None
    w = 20
    d = (1.0, -0.08)
    ux, uy = _unit(d)
    hx, hy = x - ux * 0.85 * w, y - uy * 0.85 * w
    tip = (hx + ux * 1.35 * w, hy + uy * 1.35 * w)
    hand_r = _box((hx, hy), tip, 0.30 * w)
    if not arm:
        return sheet, hand_r, None, (hx, hy, w, d, None)
    return sheet, hand_r, _box(DON_FIST, (hx, hy), 9), (hx, hy, w, d, DON_FIST)


def pocket_pose(t, hand=True, arm=True):
    """Pam's point. The index ends on the card. The sleeve leaves her right fist, below her face."""
    x, y = bs._arc(t, bs.POCKET_FROM, bs.POCKET_TO, bs.POCKET_BEND)
    card = (x - 11, y - 7, x + 11, y + 7)
    if not hand:
        return card, None, None, None
    w = 16
    # From her fist toward the card, stopped on the card so the finger does not run on into Mom.
    d = (x - PAM_FIST[0], y - PAM_FIST[1])
    ux, uy = _unit(d)
    tip = (x - 4, y + 2)
    hx, hy = tip[0] - ux * 1.20 * w, tip[1] - uy * 1.20 * w
    hand_r = _box((hx, hy), tip, 0.28 * w)
    if not arm:
        return card, hand_r, None, (hx, hy, w, d, None)
    return card, hand_r, _box(PAM_FIST, (hx, hy), 8), (hx, hy, w, d, PAM_FIST)


def touch(which, hand=True, arm=True):
    """The frame the hand check measures. Middle of the shred, last frame of the pocket."""
    if which == "shred":
        return shred_pose(30 / 59.0, hand, arm)[:3]
    return pocket_pose(1.0, hand, arm)[:3]


def _near_body(arm_r, body):
    """The sleeve's box comes up to the torso. A hand floating on the prop does not."""
    if arm_r is None:
        return False
    chest = (body[0], body[1] - 90)
    dx = 0 if arm_r[0] <= chest[0] <= arm_r[2] else min(abs(chest[0] - arm_r[0]), abs(chest[0] - arm_r[2]))
    dy = 0 if arm_r[1] <= chest[1] <= arm_r[3] else min(abs(chest[1] - arm_r[1]), abs(chest[1] - arm_r[3]))
    return dx * dx + dy * dy <= 48 * 48


def _in_cam(rect, cam_name):
    import bp_draw_audit as ad
    if rect is None:
        return False
    return ad.inside(ad.span(bs.CAM[cam_name]), (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2)


def hand_faults(hand=True, arm=True):
    """Empty when the middle shred frame and the last pocket frame both show a hand on an arm."""
    import bp_set as room
    faults = []
    sheet, hand_r, arm_r = touch("shred", hand, arm)
    if not _overlap(sheet, hand_r):
        faults.append("shred: the sheet does not meet the hand")
    elif not _overlap(hand_r, arm_r):
        faults.append("shred: the hand has no arm")
    elif not _near_body(arm_r, room.DON):
        faults.append("shred: the arm does not reach Don")
    elif not _in_cam(hand_r, "SHRED"):
        faults.append("shred: the hand is outside SHRED")
    card, ph, pa = touch("pocket", hand, arm)
    if not _overlap(card, ph):
        faults.append("pocket: the card does not meet the hand")
    elif not _overlap(ph, pa):
        faults.append("pocket: the hand has no arm")
    elif not _near_body(pa, room.PAM):
        faults.append("pocket: the arm does not reach Pam")
    elif not _in_cam(ph, "PUSH"):
        faults.append("pocket: the hand is outside PUSH")
    return faults


def _sleeve(c, shoulder, wrist, color):
    bs.grip_mark("stroke")
    c.save()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(*shoulder)
    c.line_to(*wrist)
    c.set_source_rgb(0.15, 0.12, 0.10)
    c.set_line_width(18)
    c.stroke()
    c.move_to(*shoulder)
    c.line_to(*wrist)
    c.set_source_rgb(*color)
    c.set_line_width(12)
    c.stroke()
    c.restore()


def _limb(c, pose, gesture, skin, sleeve, arm_side):
    if pose is None:
        return
    hx, hy, w, d, shoulder = pose
    if shoulder is not None:
        _sleeve(c, shoulder, (hx, hy), sleeve)
    if gesture == "point":
        bs.grip_mark("point")
    import kit
    import hands_ps
    hands_ps.draw(kit.Ctx(c, 0), gesture, hx, hy, w, skin, d, arm_side)


def don_hand(c, t):
    import kit
    _limb(c, shred_pose(t)[3], DON_HAND, kit.PEOPLE["DON"]["skin"], DON_SLEEVE, -1)


def pam_hand(c, t):
    import kit
    _limb(c, pocket_pose(t)[3], PAM_HAND, kit.PEOPLE["PAM"]["skin"], PAM_SLEEVE, -1)


def _after_hand(kind):
    """World space, after the prop. Don's hand rides the page. Pam's hand meets the card as it arrives."""
    def draw(c, i, n, kind=kind):
        t = i / max(1, n - 1)
        if kind == "shred":
            don_hand(c, t)
        elif kind == "pocket" and t >= 0.90:
            pam_hand(c, t)
    return draw


def _hold_overlay(shot, kind):
    if kind == "promise":
        return lambda c: bs.shred_sheet(c, 0.0)
    if kind == "found":
        def both(c):
            bs.pocket(c, 1.0)
            pam_hand(c, 1.0)
        return both
    if kind in ("rest", "joke"):
        return None
    return bs.overlay_still(shot["motion"]) if shot["motion"] else None


def _write_timing_once(path, data):
    """Create a timing JSON only when it is absent. Existing files stay byte-stable."""
    if os.path.isfile(path):
        raise SystemExit("refusing to overwrite %s" % os.path.basename(path))
    _refuse(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    return path


def write_v2_timing():
    """Shot 03 and shot 11 only. Every other line keeps the v1 time. The v1 file is only read."""
    path = timing_path(2)
    if os.path.isfile(path):
        return path
    src = json.load(open(timing_path(1), encoding="utf-8"))
    starts = {}
    full, night = 0.0, 0.0
    for shot in bs.SHOTS:
        starts[shot["id"]] = (full, night)
        full += shot["dur"]
        if shot["id"] != "05":
            night += shot["dur"]
    lines = []
    for row in src["lines"]:
        row = dict(row)
        if row["key"] in V2_START:
            length = row["t1"] - row["t0"]
            row["t0"] = round(V2_START[row["key"]], 3)
            row["t1"] = round(row["t0"] + length, 3)
            base_full, base_night = starts[row["shot"]]
            row["full"] = round(base_full + row["t0"], 3)
            row["nonight"] = round(base_night + row["t0"], 3)
        lines.append(row)
    return _write_timing_once(path, {"picture": "bp_pic_v2", "fps": FPS, "lines": lines})


def write_v3_timing():
    """The v2 times, under the v3 name. v1 and v2 are only read. write_timing() is not called."""
    path = timing_path(3)
    if os.path.isfile(path):
        return path
    src_path = timing_path(2)
    if not os.path.isfile(src_path):
        write_v2_timing()
    data = json.load(open(src_path, encoding="utf-8"))
    data["picture"] = "bp_pic_v3"
    return _write_timing_once(path, data)


def write_v4_timing():
    """The v3 times, under the v4 name. v1, v2 and v3 are only read. write_timing() is not called."""
    path = timing_path(4)
    if os.path.isfile(path):
        return path
    src_path = timing_path(3)
    if not os.path.isfile(src_path):
        write_v3_timing()
    data = json.load(open(src_path, encoding="utf-8"))
    data["picture"] = "bp_pic_v4"
    return _write_timing_once(path, data)


def write_v5_timing():
    """The v4 times, under the v5 name. Earlier timing files are only read."""
    path = timing_path(5)
    if os.path.isfile(path):
        return path
    src_path = timing_path(4)
    if not os.path.isfile(src_path):
        raise SystemExit("no timing %s" % os.path.basename(src_path))
    data = json.load(open(src_path, encoding="utf-8"))
    data["picture"] = "bp_pic_v5"
    return _write_timing_once(path, data)


# Shot 01. The wall peg is fs.portrait. It lands beside Don's feet, clear of his face and of the Client.
FALL_FROM = (508.0, 128.0)
FALL_TO = (400.0, 478.0)
# Shot 04. Confetti is in the air once the fuse has caught, and on the floor after.
FIRE_FROM = 0.34
# "I'm matching them." The desk sheet on shots 06-13 stays at 0.15. This one is the night beat only.
MATCH_AT = (732.0, 392.0)
MATCH_S = 0.58
# plan_patched seam: edges[1], the tape row at local y -14.
MATCH_SEAM = (-31.9, -14.0)


def _fall_xy(t):
    """Left first, then down, so the frame is not on Don's face on the way to the floor."""
    ux = 1.0 - (1.0 - t) ** 2
    uy = t * t
    return (FALL_FROM[0] + (FALL_TO[0] - FALL_FROM[0]) * ux,
            FALL_FROM[1] + (FALL_TO[1] - FALL_FROM[1]) * uy)


def _falling_portrait(c, t):
    import fs_set
    import kit
    fs_set.portrait(kit.Ctx(c, 0), *_fall_xy(t), 0.72)


def _olive_board(c, t):
    """The blank board v2 dropped. A face check on this frame has to fail."""
    x, y = _fall_xy(t)
    c.save()
    c.translate(x, y)
    c.set_source_rgb(0.25, 0.18, 0.12)
    c.rectangle(-46, -62, 92, 118)
    c.fill()
    c.set_source_rgb(0.72, 0.78, 0.55)
    c.rectangle(-36, -48, 72, 88)
    c.fill()
    c.restore()


def _muzzle(x, floor, s):
    import math
    px, py = x, floor - 52.0 * s
    ang = -0.55
    ly = -44.0 * s
    return px - ly * math.sin(ang), py + ly * math.cos(ang)


def _fire(c, fuse, air=False, floor=False):
    """The same cannon. fuse runs, then confetti leaves the muzzle toward the ARCHIVE bin."""
    import kit
    import set_ob
    x, fl, s = bs.CANNON_AT
    k = kit.Ctx(c, 0)
    prev = set_ob.CANNON_LABEL[0]
    set_ob.CANNON_LABEL[0] = True
    try:
        set_ob.cannon(k, x, fl, s, fuse=fuse)
        if air:
            mx, my = _muzzle(x, fl, s)
            sx, sy = bs.SHRED_SLOT
            set_ob.confetti(k, mx, my, sx, sy, n=8 + int(24 * fuse), seed=7, s=0.50)
        if floor:
            sx, _sy = bs.SHRED_SLOT
            set_ob.confetti(k, sx - 16, fl - 8, sx + 40, fl + 2, n=6, seed=3, s=0.35)
    finally:
        set_ob.CANNON_LABEL[0] = prev


def _seam():
    return (MATCH_AT[0] + MATCH_SEAM[0] * MATCH_S, MATCH_AT[1] + MATCH_SEAM[1] * MATCH_S)


def match_pose(hand=True, arm=True):
    """Pam's point on a tape seam. The sleeve leaves the fist the room already draws."""
    x, y = MATCH_AT
    s = MATCH_S
    sheet = (x - 62 * s, y - 61 * s, x + 62 * s, y + 43 * s)
    if not hand:
        return sheet, None, None, None
    w = 16
    tip = _seam()
    d = (tip[0] - PAM_FIST[0], tip[1] - PAM_FIST[1])
    ux, uy = _unit(d)
    hx, hy = tip[0] - ux * 1.15 * w, tip[1] - uy * 1.15 * w
    hand_r = _box((hx, hy), tip, 0.28 * w)
    if not arm:
        return sheet, hand_r, None, (hx, hy, w, d, None)
    return sheet, hand_r, _box(PAM_FIST, (hx, hy), 8), (hx, hy, w, d, PAM_FIST)


def _match_world(c, hand=True, arm=True):
    import fs_set
    import kit
    fs_set.plan_patched(kit.Ctx(c, 0), MATCH_AT[0], MATCH_AT[1], MATCH_S)
    if hand:
        _limb(c, match_pose(True, arm)[3], PAM_HAND, kit.PEOPLE["PAM"]["skin"], PAM_SLEEVE, -1)


def match_faults(hand=True, arm=True):
    """Empty when the taped sheet meets Pam's hand and that hand meets her arm."""
    import bp_set as room
    sheet, hand_r, arm_r = match_pose(hand, arm)[:3]
    if not _overlap(sheet, hand_r):
        return ["match: the sheet does not meet the hand"]
    if not _overlap(hand_r, arm_r):
        return ["match: the hand has no arm"]
    if not _near_body(arm_r, room.PAM):
        return ["match: the arm does not reach Pam"]
    if not _in_cam(hand_r, "NIGHT"):
        return ["match: the hand is outside NIGHT"]
    return []


def _base(shot, extra, skip_client=False, skip_portrait=False):
    import bp_set
    bp_set.SKIP_CLIENT[0] = skip_client
    bp_set.SKIP_PORTRAIT[0] = skip_portrait
    try:
        cam = bs.CAM[shot["cam"]]
        return fr.paint(cam, overlay=extra, hide_plan=shot["hide"], grade=shot["grade"]), cam
    finally:
        bp_set.SKIP_CLIENT[0] = False
        bp_set.SKIP_PORTRAIT[0] = False


def _compose(base, cam, world):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, fr.OUT_W, fr.OUT_H)
    surf.set_device_scale(fr.SCALE, fr.SCALE)
    c = cairo.Context(surf)
    c.set_source_surface(base, 0, 0)
    c.paint()
    c.save()
    c.rectangle(0, 0, fr.W, fr.H)
    c.clip()
    fr.view(c, *cam)
    world(c)
    c.restore()
    return surf


def _v3(shot, kind):
    if shot["id"] == "01" and kind in ("arrive", "hold"):
        return True
    if shot["id"] == "04" and kind in ("cannon", "hold"):
        return True
    return kind == "match"


def _v3_maker(shot, kind, extra):
    """draw(i, n) for the three beats. v1 and v2 never call this."""
    if shot["id"] == "01" and kind == "arrive":
        base, cam = _base(shot, extra, skip_client=True, skip_portrait=True)

        def draw(i, n, base=base, cam=cam):
            t = i / float(max(1, n - 1))

            def world(c, t=t, i=i, n=n):
                bs._place_client(c, bs._walk_x(bs.ARRIVE, i, n))
                _falling_portrait(c, t)
            return _compose(base, cam, world)
        return draw
    if shot["id"] == "01" and kind == "hold":
        base, cam = _base(shot, extra, skip_portrait=True)
        landed = _compose(base, cam, lambda c: _falling_portrait(c, 1.0))

        def draw(i, n, landed=landed):
            return landed
        return draw
    if shot["id"] == "04" and kind == "cannon":
        base, cam = _base(shot, extra)

        def draw(i, n, base=base, cam=cam):
            t = i / float(max(1, n - 1))

            def world(c, t=t):
                _fire(c, t, air=t >= FIRE_FROM)
            return _compose(base, cam, world)
        return draw
    if shot["id"] == "04" and kind == "hold":
        base, cam = _base(shot, extra)
        spent = _compose(base, cam, lambda c: _fire(c, 1.0, floor=True))

        def draw(i, n, spent=spent):
            return spent
        return draw
    if kind == "match":
        base, cam = _base(shot, extra)
        sheet = _compose(base, cam, lambda c: _match_world(c))

        def draw(i, n, sheet=sheet):
            return sheet
        return draw
    raise RuntimeError("v3 has no %s on shot %s" % (kind, shot["id"]))


def _piece_kind(shot, kind, line, version):
    """n6 is the only night piece that shows the taped plan. Earlier night lines keep it hidden."""
    if version >= 3 and shot["id"] == "05" and kind == "hold" and line and line.get("key") == "n6":
        return "match"
    return kind


def _moving(kind, version):
    return kind in MOTION or (version >= 3 and kind == "cannon")


def spans(shot, version):
    """(start, end, kind) across the shot. v1 is v5's order. v2 moves two shots and drops the undrawn finger."""
    total = shot["dur"] * FPS
    if version >= 2 and shot["id"] in V2_SPANS:
        cursor = 0
        out = []
        for kind, n in V2_SPANS[shot["id"]]:
            n = total - cursor if n is None else n
            out.append((cursor, cursor + n, kind))
            cursor += n
        return out
    cursor = 0
    out = []
    for kind, n in bs._motions(5).get(shot["id"], []):
        out.append((cursor, cursor + n, kind))
        cursor += n
    out.append((cursor, total, "hold"))
    return out


def cam_of(shot, kind):
    name = bs.CROPS[kind] if kind in bs.CROPS else shot["cam"]
    return bs.CAM[name], name


def maker(shot, kind, dull, version=1):
    """A draw(i, n) for this insert. The zero sits in the base, so a moving sheet does not wipe it."""
    shot = drawn(shot)
    extra = zero_disc if dull else None
    if version >= 4 and kind == "star":
        return _star_v4()
    if version >= 3 and _v3(shot, kind):
        return _v3_maker(shot, kind, extra), cam_of(shot, kind)
    if kind in HOLDS:
        return bs._static(shot, _hold_overlay(shot, kind), extra), cam_of(shot, kind)
    after = _after_hand(kind) if version >= 2 and kind in ("shred", "pocket") else None
    return bs._motion_draw(kind, shot, extra, after), cam_of(shot, kind)


def clone(surf):
    surf.flush()
    out = cairo.ImageSurface(cairo.FORMAT_RGB24, surf.get_width(), surf.get_height())
    out.set_device_scale(*surf.get_device_scale())
    a = np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data())
    b = np.ndarray((out.get_height(), out.get_stride() // 4, 4), np.uint8, out.get_data())
    b[:] = a
    out.mark_dirty()
    return out


def heads(shot, cam, t):
    """(who, frame head) for every person inside this camera. The Client follows his walk."""
    import bp_draw_audit as ad
    rect = ad.span(cam)
    found = []
    for who, name in ad.WHO.items():
        x, y = ad.head(name, ad.homes()[name])
        if name == "client":
            x = bs.client_x(shot, t)
        if ad.inside(rect, x, y):
            found.append((who, bs._head((x, y), cam)))
    return found


def _nearer(tip, speaker, others):
    import math
    d = math.hypot(tip[0] - speaker[0], tip[1] - speaker[1])
    return all(d < math.hypot(tip[0] - o[0], tip[1] - o[1]) for o in others)


def _copy(src, dst):
    src.flush()
    a = np.ndarray((src.get_height(), src.get_stride() // 4, 4), np.uint8, src.get_data())
    b = np.ndarray((dst.get_height(), dst.get_stride() // 4, 4), np.uint8, dst.get_data())
    b[:] = a
    dst.mark_dirty()


def _on_someone_else(box, others):
    return any(box[0] < h[0] < box[2] for h in others)


def _paint_at(surf, text, box, tip):
    import kit
    import speech
    k = kit.Ctx(cairo.Context(surf), 0)
    rows, size, font, _bw, _bh = speech._metrics(k, text, False, max(48, box[2] - box[0] - 28))
    speech._paint(k, box, tip, rows, size, font)


def _lift(box, tip, others):
    """The side box was sitting on the next person's face. Raise it above every other head.
    The tail stays a short one, pointing at this speaker."""
    import math
    from speech_gate import SAFE_16X9, TAIL_MIN, TAIL_MAX
    x0, y0, x1, y1 = box
    h = y1 - y0
    # Only the person standing against the box. The woman on the speaker's other side is not a reason to climb.
    blocking = [hy - r for hx, hy, r in others
                if y1 > hy - r and ((hx < x0 and x0 - hx < 80) or (hx > x1 and hx - x1 < 80))]
    if not blocking:
        return box
    hair = min(blocking)
    y1 = hair - 4
    y0 = y1 - h
    if y0 < SAFE_16X9[1] or not (y0 + 8 <= tip[1] <= y1 - 8):
        return None
    dx = max(x0 - tip[0], 0, tip[0] - x1)
    dy = max(y0 - tip[1], 0, tip[1] - y1)
    if not (TAIL_MIN <= math.hypot(dx, dy) <= TAIL_MAX):
        return None
    return (x0, y0, x1, y1)


def place_bubble(surf, text, speaker, others, intend=None):
    """Draw one bubble that clears every face. Over the head when that clears; beside the mouth when it does not.
    intend is who the tail must be nearest. The plant points it at someone else."""
    import kit
    import speech
    import speech_gate as sg
    from speech_gate import SAFE_16X9
    intend = speaker if intend is None else intend
    crowd = [h for h in [speaker] + list(others) if h != intend]
    above = (speaker[0], speaker[1] - speaker[2] - 6)

    def attempt(kw):
        trial = clone(surf)
        before = sg.snapshot(trial)
        box, tip = speech.draw(kit.Ctx(cairo.Context(trial), 0), text, speaker, safe=SAFE_16X9,
                              others=list(others), **kw)
        if tip is None:
            return ["no tail"], trial, None
        faults = sg.check(trial, box, tip, [speaker] + list(others), before=before, safe=SAFE_16X9,
                          above=kw.get("above"))
        if not _nearer(tip, intend, crowd):
            faults.append("TAIL nearer another head than the speaker")
        return faults, trial, box, tip

    # Two women on one desk. A bubble over the left one also reads as the right one's.
    # Put it beside her, clear of the man on her other side, so the tail is hers and her face shows.
    close = [h for h in others if abs(h[0] - speaker[0]) < 100 and abs(h[1] - speaker[1]) < 40]
    if close:
        speech.MAX_W[0] = 120
        try:
            faults, trial, box, tip = attempt({})
            if not faults and box is not None and tip is not None:
                lifted = _lift(box, tip, others)
                if lifted is None:
                    faults = ["box sits on the next person"]
                elif lifted != box:
                    trial = clone(surf)
                    before = sg.snapshot(trial)
                    _paint_at(trial, text, lifted, tip)
                    faults = sg.check(trial, lifted, tip, [speaker] + list(others), before=before,
                                     safe=SAFE_16X9)
                    if not _nearer(tip, intend, crowd):
                        faults.append("TAIL nearer another head than the speaker")
        finally:
            speech.MAX_W[0] = 220
        if not faults:
            _copy(trial, surf)
            return []
    # A wide box over Pam also hangs over Mom. Narrow it until it sits on this head only.
    # If the only box that clears the gate still reaches a neighbour, keep that one: the tail is on this head.
    speech.TOP_FIRST[0] = True
    wide = speech.MAX_W[0]
    chosen = None
    fallback = None
    try:
        for width in (wide, 160, 140, 120, 100):
            speech.MAX_W[0] = width
            faults, trial, box, _tip = attempt({"above": above})
            if faults or box is None:
                if width == wide:
                    break
                continue
            if fallback is None:
                fallback = trial
            if not _on_someone_else(box, others):
                chosen = trial
                break
    finally:
        speech.TOP_FIRST[0] = False
        speech.MAX_W[0] = wide
    chosen = chosen if chosen is not None else fallback
    if chosen is not None:
        _copy(chosen, surf)
        return []
    faults, trial, _box, _tip = attempt({})
    if not faults:
        _copy(trial, surf)
        return []
    return faults


def line_at(frame, shot_rows):
    for r in shot_rows:
        f0, f1 = int(round(r["t0"] * FPS)), int(round(r["t1"] * FPS))
        if f0 <= frame < f1:
            return r
    return None


def pieces(shot, shot_rows, switch, version=1):
    """(f0, f1, kind, line or None) covering the shot. A line and the zero each get their own piece."""
    total = shot["dur"] * FPS
    out = []
    for a, b, kind in spans(shot, version):
        marks = {a, b}
        for r in shot_rows:
            f0, f1 = int(round(r["t0"] * FPS)), int(round(r["t1"] * FPS))
            if f1 > a and f0 < b:
                marks.add(max(a, f0))
                marks.add(min(b, f1))
        if shot["id"] == "07" and a < switch < b:
            marks.add(switch)
        marks = sorted(marks)
        for c, d in zip(marks, marks[1:]):
            if d > c:
                out.append((c, d, kind, line_at(c, shot_rows)))
    got = sum(d - c for c, d, _, _ in out)
    if got != total:
        raise RuntimeError("shot %s covers %d frames, wants %d" % (shot["id"], got, total))
    return out


def paint_piece(shot, kind, dull, line, t, version=1):
    """One frame of a static piece, slate on the hold, bubble while a line plays."""
    kind = _piece_kind(shot, kind, line, version)
    with _look(version):
        draw, (cam, _name) = maker(shot, kind, dull, version)
        surf = clone(draw(0, 1))
    if kind in HOLDS:
        c = cairo.Context(surf)
        label = "%s  %s" % (shot["id"], shot["title"])
        if shot["line"]:
            label += "  —  " + shot["line"]
        bs._slate(c, label)
    faults = []
    if line is not None:
        found = dict(heads(drawn(shot), cam, t))
        if line["who"] not in found:
            faults.append("%s outside the camera" % line["who"])
        else:
            speaker = found.pop(line["who"])
            faults += place_bubble(surf, line["text"], speaker, list(found.values()))
    # "Your number." falls in the star insert. The phone crop holds his head and cannot hold the bubble.
    # The same pose on S0 can. The rectangle stays off.
    if version >= 4 and kind == "star" and line is not None and faults:
        print("star %s: phone crop cannot hold the bubble; S0, no rectangle" % line["key"], flush=True)
        with _look(version):
            draw, (cam, _name) = _star_room(shot)
            surf = clone(draw(0, 1))
        faults = []
        found = dict(heads(drawn(shot), cam, t))
        if line["who"] not in found:
            faults.append("%s outside the camera" % line["who"])
        else:
            speaker = found.pop(line["who"])
            faults += place_bubble(surf, line["text"], speaker, list(found.values()))
    return surf, faults, cam


def disc_rgb(surf, cam):
    x, y = _px(cam, *SAMPLE)
    surf.flush()
    buf = np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data())
    b, g, r = (int(v) for v in buf[y, x, :3])
    return r, g, b


def _px(cam, x, y):
    cx, cy, z = cam
    return (int(round(((x - cx) * z + fr.W / 2.0) * fr.SCALE)),
            int(round(((y - cy) * z + fr.H / 2.0) * fr.SCALE)))


def is_green(rgb):
    r, g, b = rgb
    return g > 120 and r < 90 and g > b


def is_dull(rgb):
    r, g, b = rgb
    return max(rgb) - min(rgb) < 24 and 110 < r < 180


_MOM_JOINED = [None]


def _mom_joined():
    if _MOM_JOINED[0] is None:
        _MOM_JOINED[0] = _mom_differs()
    return _MOM_JOINED[0]


class _Look:
    """v4 paints the signed sheet. v1 to v3 leave SHEET and MOM_ARMS as they were."""

    def __init__(self, version):
        self.version = version
        self.saved = None

    def __enter__(self):
        import bp_set
        self.bp = bp_set
        self.saved = (bp_set.SHEET[0], bp_set.MOM_ARMS[0])
        if self.version >= 4:
            bp_set.SHEET[0] = True
            bp_set.MOM_ARMS[0] = _mom_joined()
        return self

    def __exit__(self, *exc):
        self.bp.SHEET[0], self.bp.MOM_ARMS[0] = self.saved
        return False


def _look(version):
    return _Look(version)


def bubbles(cut="full", version=1):
    """speech_gate on one frame of every line. This is the check the render refuses to skip."""
    with _look(version):
        return _bubbles(cut, version)


def _bubbles(cut, version):
    switch = switch_frame()
    bad = []
    by = {s["id"]: s for s in bs.SHOTS}
    seen = []
    for shot in (bs.without_night() if cut == "nonight" else bs.SHOTS):
        mine = [r for r in rows(cut, version) if r["shot"] == shot["id"]]
        for f0, f1, kind, line in pieces(shot, mine, switch, version):
            if line is None or line["key"] in seen:
                continue
            seen.append(line["key"])
            _surf, faults, _cam = paint_piece(by[shot["id"]], kind, dull_at(shot["id"], f0, switch), line,
                                              (f0 + 0.5) / FPS, version)
            if faults:
                bad.append(line["key"])
            print("%s %-8s %s  %s" % (shot["id"], line["key"], "FAIL" if faults else "ok",
                                     "; ".join(faults) or line["text"]), flush=True)
    want = [r["key"] for r in rows(cut, version)]
    missed = [k for k in want if k not in seen]
    if missed:
        bad += missed
        print("lines with no frame: %s" % missed)
    print("FAIL" if bad else "PASS", "(%d of %d lines)" % (len(bad), len(want)))
    return bad


def _md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def plant():
    """Three checks, each shown failing on a frame that is wrong on purpose."""
    caught = 0
    shot = next(s for s in bs.SHOTS if s["id"] == "05")
    line = next(r for r in rows() if r["key"] == "n5")
    surf, faults, cam = paint_piece(shot, "hold", True, line, line["t0"])
    ok = not faults
    print("bubble on Sofía: %s  %s" % ("ok" if ok else "FAIL", "; ".join(faults)), flush=True)
    found = dict(heads(drawn(shot), cam, line["t0"]))
    wrong = clone(maker(shot, "hold", True)[0](0, 1))
    swapped = place_bubble(wrong, line["text"], found["PAM"], [found["SOFIA"]], intend=found["SOFIA"])
    hit = any("nearer" in f for f in swapped)
    caught += hit
    print("plant: her line on Pam  %s" % ("caught" if hit else "MISSED"), flush=True)
    bare, _, _ = paint_piece(shot, "hold", True, None, 1.0)
    bubbled = clone(bare)
    place_bubble(bubbled, line["text"], found["SOFIA"], [found["PAM"]])
    differ = not np.array_equal(_buf(bare), _buf(bubbled))
    caught += differ
    print("plant: a bubble on a silent frame  %s" % ("caught" if differ else "MISSED"), flush=True)
    crop = next(s for s in bs.SHOTS if s["id"] == "07")
    dull, _, zcam = paint_piece(crop, "zero", True, None, 1.0)
    green_shot = drawn(crop)
    green = bs._motion_draw("zero", green_shot, None)(0, 1)
    dull_ok = is_dull(disc_rgb(dull, zcam)) and not is_green(disc_rgb(dull, zcam))
    hit = is_green(disc_rgb(green, zcam)) and not is_dull(disc_rgb(green, zcam))
    caught += hit
    print("zero crop dull %s; plant green with no overlay  %s  %s / %s" % (
        "ok" if dull_ok else "FAIL", "caught" if hit else "MISSED", disc_rgb(dull, zcam), disc_rgb(green, zcam)),
        flush=True)
    stills = all(_md5(os.path.join(bs.EP, "stills", name)) == want for name, want in LOCKED.items())
    print("locked stills %s" % ("unchanged" if stills else "CHANGED"), flush=True)
    print("plants caught %d of 3" % caught)
    return caught == 3 and ok and dull_ok and stills


def _buf(surf):
    surf.flush()
    return np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data()).copy()


def _loop(surf, frames, path):
    png = path + ".png"
    surf.write_to_png(png)
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", png,
        "-frames:v", str(frames), "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "20",
        "-preset", "veryfast", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709"] + bs._BSF + [path])
    os.remove(png)


def _bed(parts, out, seconds):
    """The picture file needs a bed the loudness check can measure. It is pink noise, as on the silent roughs,
    and it is not the mix. bp_sound lays the takes on a later copy of these packets."""
    lst = out + ".txt"
    with open(lst, "w", encoding="utf-8") as f:
        for p in parts:
            f.write("file '%s'\n" % p.replace("\\", "/"))
    silent = out + ".silent.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-i", silent,
        "-f", "lavfi", "-t", str(seconds), "-i", "anoisesrc=d=%d:c=pink:r=48000:a=0.4" % seconds,
        "-filter:a", "loudnorm=I=-15:TP=-1.5:LRA=11,alimiter=limit=0.80:level=disabled",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"] + bs._BSF + [
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", out])
    os.remove(silent)
    os.remove(lst)


def render(version=1, cut="full"):
    with _look(version):
        return _render(version, cut)


def _render(version, cut):
    if bubbles(cut, version):
        raise SystemExit("bubbles failed; not rendering")
    out = out_path(version, cut)
    work = os.path.join(bs.EP, "rough_work", "pic_v%d" % version, cut)
    os.makedirs(work, exist_ok=True)
    switch = switch_frame()
    shots = bs.without_night() if cut == "nonight" else bs.SHOTS
    parts = []
    n = 0
    for shot in shots:
        mine = [r for r in rows(cut, version) if r["shot"] == shot["id"]]
        for f0, f1, kind, line in pieces(shot, mine, switch, version):
            frames = f1 - f0
            path = os.path.join(work, "s%s_%05d.mp4" % (shot["id"], f0))
            dull = dull_at(shot["id"], f0, switch)
            kind = _piece_kind(shot, kind, line, version)
            if _moving(kind, version):
                draw, (cam, _) = maker(shot, kind, dull, version)
                motion_n = f1 - f0
                # Frame index inside the whole insert, not inside this piece.
                origin = f0 - _span_start(shot, kind, version)

                def one(i, _n, draw=draw, origin=origin, motion_n=motion_n, line=line, shot=shot, cam=cam, f0=f0):
                    surf = clone(draw(origin + i, _insert_n(shot, kind, version)))
                    if line is not None:
                        found = dict(heads(drawn(shot), cam, (f0 + 0.5) / FPS))
                        speaker = found.pop(line["who"])
                        place_bubble(surf, line["text"], speaker, list(found.values()))
                    return surf

                bs._encode(path, one, frames)
            else:
                surf, faults, _cam = paint_piece(shot, kind, dull, line, (f0 + 0.5) / FPS, version)
                if faults:
                    raise SystemExit("shot %s %s: %s" % (shot["id"], line["key"] if line else kind, faults))
                _loop(surf, frames, path)
            parts.append(path)
            n += frames
            print("  %s %5.1f  %-8s %s" % (shot["id"], f0 / float(FPS), kind, line["key"] if line else ""), flush=True)
    want = sum(s["dur"] for s in shots) * FPS
    if n != want:
        raise SystemExit("%s has %d frames, wants %d" % (cut, n, want))
    _bed(parts, out, want // FPS)
    print(out)
    return out


def _span_start(shot, kind, version=1):
    for a, _b, name in spans(shot, version):
        if name == kind:
            return a
    return 0


def _insert_n(shot, kind, version=1):
    for a, b, name in spans(shot, version):
        if name == kind:
            return b - a
    return shot["dur"] * FPS


def _shot(sid):
    return next(s for s in bs.SHOTS if s["id"] == sid)


def _region(surf, cam, x, y, hw, hh):
    x0, y0 = _px(cam, x - hw, y - hh)
    x1, y1 = _px(cam, x + hw, y + hh)
    surf.flush()
    buf = np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data())
    ya, yb = sorted((int(y0), int(y1)))
    xa, xb = sorted((int(x0), int(x1)))
    ya, xa = max(0, ya), max(0, xa)
    yb, xb = min(buf.shape[0], yb), min(buf.shape[1], xb)
    if yb <= ya or xb <= xa:
        return buf[0:0, 0:0, :3]
    return buf[ya:yb, xa:xb, :3]


def _face_olive(pix):
    if pix.size == 0:
        return 0, 0, 0
    b = pix[:, :, 0].astype(int)
    g = pix[:, :, 1].astype(int)
    r = pix[:, :, 2].astype(int)
    olive = (g > r + 8) & (g > b + 30) & (g > 150) & (r > 140)
    # The wall is (230, 216, 188). Skin is redder than that, so the empty peg does not count as a face.
    skin = (r > 180) & (g > 120) & (b > 90) & (r > g + 28) & (r > b + 55)
    photo = (b > 185) & (g > 165) & (r > 130) & (b > r + 12)
    n = int(pix.shape[0] * pix.shape[1])
    return int((skin | photo).sum()), int(olive.sum()), n


def _confetti_count(surf, cam):
    """Blue strips between the muzzle and the ARCHIVE slot. The cannon body is yellow."""
    x, fl, s = bs.CANNON_AT
    mx, my = _muzzle(x, fl, s)
    sx, sy = bs.SHRED_SLOT
    pix = _region(surf, cam, (mx + sx) / 2.0, (my + sy) / 2.0, abs(mx - sx) / 2.0 + 18, abs(my - sy) / 2.0 + 18)
    if pix.size == 0:
        return 0
    b = pix[:, :, 0].astype(int)
    g = pix[:, :, 1].astype(int)
    r = pix[:, :, 2].astype(int)
    return int(((b > r + 40) & (b > g) & (b > 80)).sum())


def _covers_face(t):
    """The falling frame's box against Don's face and the Client's mark."""
    x, y = _fall_xy(t)
    box = (x - 36, y - 42, x + 36, y + 42)
    for px, py in ((476, 420), (132, 390)):
        if box[0] <= px <= box[2] and box[1] <= py <= box[3]:
            return True
    return False


def beat_frames():
    """Mid-fall, the firing frame, and Pam's hand on the tape. Full size."""
    fall_draw, (fall_cam, _) = maker(_shot("01"), "arrive", True, 3)
    n = bs.WALK_N
    fall = fall_draw(n // 2, n)
    fire_draw, (fire_cam, _) = maker(_shot("04"), "cannon", True, 3)
    fire = fire_draw(int(0.80 * (n - 1)), n)
    match, _cam = maker(_shot("05"), "match", True, 3)
    return (fall, fall_cam), (fire, fire_cam), match(0, 1)


def _olive_frame():
    shot = drawn(_shot("01"))
    base, cam = _base(shot, zero_disc, skip_client=True, skip_portrait=True)
    n = bs.WALK_N
    i = n // 2
    t = i / float(n - 1)

    def world(c, t=t, i=i, n=n):
        bs._place_client(c, bs._walk_x(bs.ARRIVE, i, n))
        _olive_board(c, t)
    return _compose(base, cam, world), cam


def _cold_frame():
    shot = drawn(_shot("04"))
    base, cam = _base(shot, zero_disc)
    return _compose(base, cam, lambda c: _fire(c, 0.0)), cam


def beats(plant=False):
    """The three beats. --plant exits 1 when the olive board, the cold cannon and the bare hand are caught."""
    n = bs.WALK_N
    t = (n // 2) / float(n - 1)
    (fall, fall_cam), (fire, fire_cam), matched = beat_frames()
    directory = os.path.join(bs.EP, "rough_work", "pic_v3")
    os.makedirs(directory, exist_ok=True)
    fall.write_to_png(os.path.join(directory, "bp_beat_fall.png"))
    fire.write_to_png(os.path.join(directory, "bp_beat_cannon.png"))
    matched.write_to_png(os.path.join(directory, "bp_beat_match.png"))
    spent_draw, _spent_cam = maker(_shot("04"), "hold", True, 3)
    spent_draw(0, 1).write_to_png(os.path.join(directory, "bp_beat_spent.png"))
    face, olive, total = _face_olive(_region(fall, fall_cam, *_fall_xy(t), 22, 30))
    peg, _peg_olive, _peg_n = _face_olive(_region(fall, fall_cam, *FALL_FROM, 22, 30))
    live_blue = _confetti_count(fire, fire_cam)
    cold, cold_cam = _cold_frame()
    cold_blue = _confetti_count(cold, cold_cam)
    matching = match_faults()
    stills = all(_md5(os.path.join(bs.EP, "stills", name)) == want for name, want in LOCKED.items())
    faults = []
    if face < 30:
        faults.append("fall: the frame has no face (%d)" % face)
    if olive > total * 0.45:
        faults.append("fall: the frame is the olive board")
    if peg >= 30:
        faults.append("fall: the wall still has the portrait")
    if _covers_face(1.0) or _covers_face(t):
        faults.append("fall: the portrait covers a face")
    if live_blue < cold_blue + 25:
        faults.append("cannon: fuse 0 and no confetti on the last third (%d vs %d)" % (live_blue, cold_blue))
    faults += matching
    if not stills:
        faults.append("locked stills changed")
    print("fall face %d olive %d/%d peg %d" % (face, olive, total, peg), flush=True)
    print("cannon confetti %d  cold %d" % (live_blue, cold_blue), flush=True)
    print("match %s" % ("; ".join(matching) or "clean"), flush=True)
    print("locked stills %s" % ("unchanged" if stills else "CHANGED"), flush=True)
    print("stills %s" % directory, flush=True)
    if not plant:
        print("FAIL" if faults else "PASS", flush=True)
        for row in faults:
            print("FAIL " + row, flush=True)
        return 1 if faults else 0
    board, board_cam = _olive_frame()
    bf, bo, bt = _face_olive(_region(board, board_cam, *_fall_xy(t), 22, 30))
    olive_caught = bf < 8 and bo > bt * 0.40
    cold_caught = cold_blue + 25 <= live_blue and cold_blue < live_blue
    no_hand = any("sheet" in row for row in match_faults(hand=False))
    no_arm = any("no arm" in row for row in match_faults(hand=True, arm=False))
    print("mode     beats plant", flush=True)
    print("live     %s" % ("clean" if not faults else "FAIL " + "; ".join(faults)), flush=True)
    print("plant: olive board  %s  face %d olive %d/%d" % ("caught" if olive_caught else "MISSED", bf, bo, bt), flush=True)
    print("plant: fuse 0, no confetti  %s" % ("caught" if cold_caught else "MISSED"), flush=True)
    print("plant: sheet with no hand  %s" % ("caught" if no_hand else "MISSED"), flush=True)
    print("plant: a hand with no arm  %s" % ("caught" if no_arm else "MISSED"), flush=True)
    caught = olive_caught and cold_caught and no_hand and no_arm and not faults
    return 1 if caught else 0


# --- hand stills. Opt-in. The picture render does not call these. --------------
HAND_DIR = os.path.join(bs.EP, "rough_work", "pic_hands")
BONE = 48.0


def _hands_dir():
    os.makedirs(HAND_DIR, exist_ok=True)
    return HAND_DIR


def _write_both(surf, name, directory=None):
    directory = directory or _hands_dir()
    full = os.path.join(directory, name + ".png")
    surf.write_to_png(full)
    loaded = cairo.ImageSurface.create_from_png(full)
    w = 270
    h = max(1, int(round(w * loaded.get_height() / float(loaded.get_width()))))
    small = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    c = cairo.Context(small)
    c.scale(w / float(loaded.get_width()), h / float(loaded.get_height()))
    c.set_source_surface(loaded, 0, 0)
    c.paint()
    tile = os.path.join(directory, name + "_270.png")
    small.write_to_png(tile)
    return full, tile


def _shoulder(name, home, which):
    import kit
    x, feet, s = home
    h = kit.PEOPLE[name]["h"]
    sy = -300.0 * h + 78.0 + 14.0
    side = 1 if which == "R" else -1
    return (x + side * 40.0 * s, feet + sy * s), s, side


def _bend(shoulder, elbow, hand):
    v1 = (elbow[0] - shoulder[0], elbow[1] - shoulder[1])
    v2 = (hand[0] - elbow[0], hand[1] - elbow[1])
    n1 = math.hypot(*v1) or 1.0
    n2 = math.hypot(*v2) or 1.0
    dot = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
    return math.degrees(math.acos(dot))


def _reach(shoulder, preferred, scale, side):
    """Hand on the ray toward preferred, inside two bones of length 48. Returns hand, elbow, gap, bend."""
    import of_scenes
    length = BONE * scale
    reach = length + length - 0.5
    dx, dy = preferred[0] - shoulder[0], preferred[1] - shoulder[1]
    dist = math.hypot(dx, dy) or 1.0
    use = dist
    if dist > reach * 0.82:
        use = reach * 0.72
    gap = max(0.0, dist - use)
    hand = (shoulder[0] + dx / dist * use, shoulder[1] + dy / dist * use)
    best = None
    for sg in (side, -side):
        elbow = of_scenes.ik2(hand, shoulder, length, length, sg)
        bend = _bend(shoulder, elbow, hand)
        ok = 20.0 <= bend <= 140.0
        if best is None:
            best = (elbow, hand, bend, ok)
        elif ok and not best[3]:
            best = (elbow, hand, bend, ok)
        elif ok == best[3] and elbow[1] > best[0][1]:
            best = (elbow, hand, bend, ok)
    return best[1], best[0], gap, best[2]


def _angles(home, shoulder, elbow, hand):
    """kit arm degrees. 0 is down, because the arm steps by (sin, cos)."""
    x, feet, s = home
    def local(p):
        return ((p[0] - x) / s, (p[1] - feet) / s)
    sh, el, hd = local(shoulder), local(elbow), local(hand)
    a1 = math.degrees(math.atan2(el[0] - sh[0], el[1] - sh[1]))
    fore = math.degrees(math.atan2(hd[0] - el[0], hd[1] - el[1]))
    a2 = fore - a1
    while a2 > 180.0:
        a2 -= 360.0
    while a2 < -180.0:
        a2 += 360.0
    return a1, a2


def _fits(cam, points, margin=12):
    cx, cy, z = cam
    for x, y in points:
        fx = (x - cx) * z + fr.W / 2.0
        fy = (y - cy) * z + fr.H / 2.0
        if fx < margin or fx > fr.W - margin or fy < margin or fy > fr.H - margin:
            return False
    return True


def _widen(cam, points):
    cx, cy, z = cam
    while z > 0.9 and not _fits((cx, cy, z), points):
        z = round(z - 0.05, 2)
    return (cx, cy, z)


def _tight(points, margin=20):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0
    zw = (fr.W - 2.0 * margin) / max(8.0, max(xs) - min(xs))
    zh = (fr.H - 2.0 * margin) / max(8.0, max(ys) - min(ys))
    return (cx, cy, round(min(zw, zh), 2))


def _paper(c, hand, toward, w=16, h=28):
    dx, dy = toward[0] - hand[0], toward[1] - hand[1]
    ang = math.atan2(dy, dx)
    c.save()
    c.translate(hand[0] + math.cos(ang) * (h * 0.45), hand[1] + math.sin(ang) * (h * 0.45))
    c.rotate(ang)
    c.set_source_rgb(0.12, 0.10, 0.08)
    c.rectangle(-w / 2 - 1, -4, w + 2, h + 2)
    c.fill()
    c.set_source_rgb(0.95, 0.86, 0.55)
    c.rectangle(-w / 2, -3, w, h)
    c.fill()
    c.restore()


def _card(c, hand):
    c.save()
    c.translate(hand[0], hand[1] - 6)
    c.rotate(-0.4)
    c.set_source_rgb(0.15, 0.12, 0.08)
    c.rectangle(-8, -6, 18, 16)
    c.fill()
    c.set_source_rgb(0.96, 0.78, 0.22)
    c.rectangle(-7, -5, 16, 14)
    c.fill()
    c.restore()


def _oval(k, hx, hy, w, skin, seed):
    import kit
    rw = (w / 1.15) * 0.6
    kit.ellipse(k, hx, hy, rw, rw, skin, seed, shadow=False, lw=2)


# Pam's other hand is an oval about 10 px across in the room. The clutch at width 18 was twice that.
PAM_CLUTCH = 0.70
# Her forearm is the rig's 17 px at scale 0.50. The wrist that crosses the desk lip stays that wide.
PAM_WRIST = 8.0


def _wrist_bridge(c, hx, hy, d, width, skin):
    """Skin along the cuff, the same width as the sleeve, so the end line is covered."""
    ux, uy = d
    n = math.hypot(ux, uy) or 1.0
    ux, uy = ux / n, uy / n
    c.save()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.set_source_rgb(*skin)
    c.set_line_width(width + 2.0)
    c.move_to(hx - ux * width * 0.45, hy - uy * width * 0.45)
    c.line_to(hx + ux * width * 0.20, hy + uy * width * 0.20)
    c.stroke()
    c.restore()


def _lip_wrist(c, hand, color):
    """A short sleeve on the desk slab, into the palm. The forearm stays behind the desk."""
    import bp_set
    x, y = hand
    top = bp_set.TOP_FRONT
    c.save()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.set_source_rgb(*color)
    c.set_line_width(PAM_WRIST)
    c.move_to(x, top - 22)
    c.line_to(x, y + 4)
    c.stroke()
    c.restore()


def _clutch_world(c, x, y, w, skin, scale):
    import kit
    import of_cast as oc
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    oc.clutch(kit.Ctx(c, 0), 0, 0, w, skin)
    c.restore()


def _clutch_hand(aim, over=False):
    """kit.HAND. The aimed wrist is a clutch, or left bare when the clutch is drawn after the desk. Other wrists stay ovals."""
    import kit
    import of_cast as oc

    def hand(k, hx, hy, w, skin, seed, d, side, aim=aim, over=over):
        dx, dy = k.c.user_to_device(hx, hy)
        if any(math.hypot(dx - ax, dy - ay) < 40 for ax, ay in aim):
            if over:
                return
            _wrist_bridge(k.c, hx, hy, d, w / 1.15, skin)
            oc.clutch(k, hx, hy, w * 0.72, skin)
        else:
            _oval(k, hx, hy, w, skin, seed)
    kit.HAND[0] = hand


def _star_screen(c):
    c.set_source_rgb(0.86, 0.64, 0.10)
    c.save()
    c.translate(0, -14)
    c.new_path()
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 8 if i % 2 == 0 else 3.2
        c.line_to(math.cos(ang) * rad, math.sin(ang) * rad)
    c.close_path()
    c.fill()
    c.restore()
    c.set_source_rgb(0.10, 0.10, 0.12)
    c.select_font_face("Inter", 0, 1)
    c.set_font_size(16)
    word = "1/5"
    ext = c.text_extents(word)
    x, y = -ext.x_advance / 2.0, 20
    c.move_to(x, y)
    c.show_text(word)
    x0, y0 = c.user_to_device(x, y - 14)
    x1, y1 = c.user_to_device(x + ext.x_advance, y + 2)
    bs.DRAW_LOG.append(("word", x0, y0, x1, y1))


def _phone_v4b(k, hx, hy, w, seed):
    """The accepted sheet grip, with this film's star. of_cast.phone_grip stays for the old still."""
    import bp_hand_sheet_v4 as v4
    import sofia_v4 as sv
    c = k.c
    c.save()
    c.translate(hx, hy)
    c.rotate(-0.05)
    v4._phone_b(k, 0, 0, 1.05 * 26.0, sv.SKIN, 1, screen=_star_screen)
    c.restore()


def _phone_at(k, hx, hy, w, seed):
    import of_cast as oc
    import sofia_v4 as sv
    s = 1.05
    ang = -0.05
    thumb = oc.inner_thumb(hx, 0.0, False)
    tip = (22 * thumb, 18)
    c = k.c
    c.save()
    c.translate(hx, hy)
    c.rotate(ang)
    c.scale(s, s)
    td = c.user_to_device(*tip)
    c.restore()
    bs.DRAW_LOG.append(("thumb", td[0], td[1]))
    oc.phone_grip(k, hx, hy, s, screen=_star_screen, ang=ang, skin=sv.SKIN, body_x=0.0, thumb_tip=tip)


def _job_paint(cam, job, aim_world, over=False, overlay=None):
    import kit
    import bp_set
    aim = []
    saved = kit.HAND[0]
    hooked = job.get("before_pam")
    try:
        if aim_world is not None:
            _clutch_hand(aim, over)
        bp_set.HAND_JOB[0] = job

        def remember(c, aim=aim, aim_world=aim_world, hooked=hooked):
            if aim_world is not None:
                aim[:] = [c.user_to_device(*aim_world)]
            if hooked:
                hooked(c)

        def top(c, overlay=overlay):
            if overlay:
                overlay(c)
        job["before_pam"] = remember
        return fr.paint(cam, overlay=top if overlay else None, hide_plan=job.get("hide_plan", False))
    finally:
        kit.HAND[0] = saved
        bp_set.HAND_JOB[0] = None


def _don_job(cam):
    import bp_set
    home = bp_set.DON
    shoulder, scale, side = _shoulder("DON", home, "R")
    preferred = bs.SHRED_SLOT
    hand, elbow, gap, bend = _reach(shoulder, preferred, scale, side)
    a1, a2 = _angles(home, shoulder, elbow, hand)
    cam = _widen(cam, (shoulder, elbow, hand))

    def sheet(c, hand=hand):
        _paper(c, hand, bs.SHRED_SLOT)
    job = {"don": (-8.0, 0.0, a1, a2), "before_don": sheet}
    _clear_logs()
    surf = _job_paint(cam, job, hand)
    dist = math.hypot(bs.SHRED_SLOT[0] - hand[0], bs.SHRED_SLOT[1] - hand[1])
    slot_gap = max(0.0, dist - (28 * 0.45 + 14))
    return _snap({"name": "shred", "surf": surf, "cam": cam, "hand": hand, "want": "clutch", "ink": "paper",
                  "bend": bend, "gap": gap, "note": "slot gap %.0f px, arm shortened %.0f px" % (slot_gap, gap),
                  "elbow": elbow, "shoulder": shoulder})


def _pam_hand_world():
    import kit
    import bp_set
    x, feet, s = bp_set.PAM
    h = kit.PEOPLE["PAM"]["h"]
    sy = -300.0 * h + 92.0
    return (x + 22.0 * s, feet + (sy + 60.0) * s), (x, feet, s)


def _pam_hands(right):
    import kit
    import bp_set
    x, feet, s = bp_set.PAM
    h = kit.PEOPLE["PAM"]["h"]
    sy = -300.0 * h + 92.0
    left = (-22.0, sy + 60.0)
    return (left, ((right[0] - x) / s, (right[1] - feet) / s))


def _card_job(cam):
    import bp_set
    import kit
    home = bp_set.PAM
    shoulder, scale, side = _shoulder("PAM", home, "R")
    hand, _home = _pam_hand_world()
    _held, elbow, gap, bend = _reach(shoulder, hand, scale, side)
    cam = _widen(cam, (shoulder, elbow, hand))

    def on_counter(c, hand=hand):
        _card(c, hand)
        _lip_wrist(c, hand, kit.PEOPLE["PAM"]["body"])
        _clutch_world(c, hand[0], hand[1], 18, kit.PEOPLE["PAM"]["skin"], PAM_CLUTCH)
    job = {"pam_hands": _pam_hands(hand), "pam_strip": False, "hide_plan": False}
    _clear_logs()
    surf = _job_paint(cam, job, hand, over=True, overlay=on_counter)
    miss = math.hypot(hand[0] - bs.POCKET_TO[0], hand[1] - bs.POCKET_TO[1])
    return _snap({"name": "card", "surf": surf, "cam": cam, "hand": hand, "want": "clutch", "ink": "paper",
                  "bend": bend, "gap": gap,
                  "note": "card is %.0f px from the pocket mark, on the hand the bones hold" % miss,
                  "elbow": elbow, "shoulder": shoulder})


def _tape_job(cam):
    import bp_set
    import fs_set
    import kit
    shoulder, scale, side = _shoulder("PAM", bp_set.PAM, "R")
    natural, _home = _pam_hand_world()
    seam = (MATCH_AT[0] + MATCH_SEAM[0] * MATCH_S, MATCH_AT[1] + MATCH_SEAM[1] * MATCH_S)
    dist = math.hypot(seam[0] - shoulder[0], seam[1] - shoulder[1])
    reach = BONE * scale * 2.0 - 0.5
    if dist <= reach:
        hand, elbow, gap, bend = _reach(shoulder, seam, scale, side)
        origin = MATCH_AT
        moved = 0.0
    else:
        hand = natural
        _h, elbow, gap, bend = _reach(shoulder, natural, scale, side)
        origin = (hand[0] - MATCH_SEAM[0] * MATCH_S, hand[1] - MATCH_SEAM[1] * MATCH_S)
        moved = math.hypot(origin[0] - MATCH_AT[0], origin[1] - MATCH_AT[1])
        gap = dist - reach
    cam = _widen(cam, (shoulder, elbow, hand))

    def plan(c, origin=origin):
        fs_set.plan_patched(kit.Ctx(c, 0), origin[0], origin[1], MATCH_S)

    def on_counter(c, hand=hand):
        skin = kit.PEOPLE["PAM"]["skin"]
        _lip_wrist(c, hand, kit.PEOPLE["PAM"]["body"])
        _clutch_world(c, hand[0], hand[1], 18, skin, PAM_CLUTCH)
    job = {"pam_hands": _pam_hands(hand), "pam_strip": False, "before_pam": plan, "hide_plan": True}
    _clear_logs()
    surf = _job_paint(cam, job, hand, over=True, overlay=on_counter)
    return _snap({"name": "tape", "surf": surf, "cam": cam, "hand": hand, "want": "clutch", "ink": "tape",
                  "bend": bend, "gap": 0.0,
                  "note": "seam on the hand, sheet moved %.0f px, bone shortfall %.0f px closed" % (moved, gap),
                  "elbow": elbow, "shoulder": shoulder})


def _sofia_local():
    import of_scenes
    import sofia_fs as sfs
    sx, sy = sfs.SH[0]
    pref = (sx + 30.0, sy + 46.0)
    length = BONE
    reach = length * 2.0 - 0.5
    dx, dy = pref[0] - sx, pref[1] - sy
    dist = math.hypot(dx, dy) or 1.0
    use = min(dist, reach * 0.7)
    hand = (sx + dx / dist * use, sy + dy / dist * use)
    elbow = of_scenes.ik2(hand, (sx, sy), length, length, -1)
    a1 = math.degrees(math.atan2(elbow[0] - sx, elbow[1] - sy))
    fore = math.degrees(math.atan2(hand[0] - elbow[0], hand[1] - elbow[1]))
    a2 = fore - a1
    bend = _bend((sx, sy), elbow, hand)
    return (a1, a2, 8.0, 0.0), hand, bend


def _phone_job(drawer=None):
    import bp_set
    import sofia_fs as sfs
    pose, local, bend = _sofia_local()
    x, feet, s = bp_set.SOFIA
    hand = (x + local[0] * s, feet + local[1] * s)
    poster = (350.0, 146.0)
    head = (x, feet + sfs.HY * s)
    cam = _tight((poster, (poster[0] - 18, poster[1] - 18), (poster[0] + 18, poster[1] + 18), hand, head))
    _clear_logs()
    sfs.WRIST[0] = (local[0], local[1], _phone_at if drawer is None else drawer)
    try:
        surf = _job_paint(cam, {"sofia_pose": pose, "tablet": None}, None)
        return _snap({"name": "phone", "surf": surf, "cam": cam, "hand": hand, "want": "phone", "ink": "phone",
                      "bend": bend, "gap": 0.0,
                      "note": "crop (%.0f, %.0f, %.2f), not written into the set" % cam,
                      "elbow": None, "shoulder": None})
    finally:
        sfs.WRIST[0] = None


def _star_v4():
    """The signed phone still. star_overlay is the v3 rectangle and is not drawn."""
    row = _phone_job(_phone_v4b)
    surf, cam = row["surf"], row["cam"]

    def draw(i, n, surf=surf):
        return surf
    return draw, (cam, "phone")


def _star_room(shot):
    """The same wrist and pose, on this shot's camera, so a speaker outside the crop still has a head.
    The rectangle is not drawn."""
    import sofia_fs as sfs
    shot = drawn(shot)
    pose, local, _bend = _sofia_local()
    cam = bs.CAM[shot["cam"]]
    sfs.WRIST[0] = (local[0], local[1], _phone_v4b)
    try:
        surf = _job_paint(cam, {"sofia_pose": pose, "tablet": None}, None)
    finally:
        sfs.WRIST[0] = None

    def draw(i, n, surf=surf):
        return surf
    return draw, (cam, shot["cam"])


def _flight():
    _clear_logs()
    shot = drawn(_shot("11"))
    draw = bs._motion_draw("pocket", shot)
    surf = draw(30, 60)
    return _snap({"name": "flight", "surf": surf, "cam": bs.CAM["PUSH"], "hand": None, "want": "none", "ink": "paper",
                  "bend": None, "gap": 0.0, "note": "the card in the air, no hand",
                  "elbow": None, "shoulder": None})


def handstills():
    """Four stills plus the flight control. Full size and 270 px. Does not render v4."""
    rows = [
        _flight(),
        _don_job(fr.SHRED),
        _card_job(bs.CAM["PUSH"]),
        _tape_job(bs.CAM["NIGHT"]),
        _phone_job(),
    ]
    lines = []
    for row in rows:
        full, tile = _write_both(row["surf"], "bp_hand_" + row["name"])
        row["path"] = full
        row["tile"] = tile
        lines.append("%s  bend %s  gap %.0f  %s" % (
            row["name"], ("%.0f" % row["bend"]) if row["bend"] is not None else "-", row["gap"], row["note"]))
    note = os.path.join(_hands_dir(), "bp_hand_reach.txt")
    with open(note, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    print("note %s" % note, flush=True)
    return rows


def _skin_prop(surf, cam, x, y, ink="paper", radius=70):
    px, py = _px(cam, x, y)
    surf.flush()
    buf = np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data())
    skin = prop = 0
    y0, y1 = max(0, py - radius), min(buf.shape[0], py + radius)
    x0, x1 = max(0, px - radius), min(buf.shape[1], px + radius)
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            b, g, r = (int(v) for v in buf[yy, xx, :3])
            if r > 175 and r > g + 18 and r > b + 35:
                skin += 1
            elif ink == "paper" and r > 175 and g > 140 and b < 190 and r > b + 20:
                prop += 1
            elif ink == "tape" and b > 120 and b > r + 30 and g > 60:
                prop += 1
            elif ink == "phone" and r > 200 and g > 200 and b > 200:
                prop += 1
    return skin, prop


def _thumb_on_word(log):
    words = [item for item in log if isinstance(item, tuple) and item[0] == "word"]
    thumbs = [item for item in log if isinstance(item, tuple) and item[0] == "thumb"]
    if not words or not thumbs:
        return True
    _k, x0, y0, x1, y1 = words[-1]
    _t, tx, ty = thumbs[-1]
    left, right = min(x0, x1), max(x0, x1)
    top, bot = min(y0, y1), max(y0, y1)
    return left <= tx <= right and top <= ty <= bot


def _glyph_270(log):
    words = [item for item in log if isinstance(item, tuple) and item[0] == "word"]
    if not words:
        return 0.0
    _k, x0, y0, x1, y1 = words[-1]
    return abs(x1 - x0) * 270.0 / (fr.W * fr.SCALE)


def _frame_faults(row, log, grips):
    faults = []
    if "stroke" in log:
        faults.append("%s: a sleeve stroke" % row["name"])
    if "point" in log:
        faults.append("%s: a second point" % row["name"])
    if "slide" in log:
        faults.append("%s: a phone rectangle" % row["name"])
    want = row["want"]
    if want != "none" and not any(g.get("kind") == want for g in grips):
        faults.append("%s: no %s" % (row["name"], want))
    if row["bend"] is not None and not (20.0 <= row["bend"] <= 140.0):
        edge = row["elbow"] is not None and not _fits(row["cam"], (row["elbow"],))
        if not edge:
            faults.append("%s: elbow %.0f" % (row["name"], row["bend"]))
    if row["hand"] is not None and want != "none":
        skin, prop = _skin_prop(row["surf"], row["cam"], row["hand"][0], row["hand"][1], row.get("ink", "paper"))
        if skin < 8 or prop < 8:
            faults.append("%s: prop does not meet the hand (%d skin, %d prop)" % (row["name"], skin, prop))
    if want == "phone" and _thumb_on_word(log):
        faults.append("%s: thumb on 1/5" % row["name"])
    if want == "phone":
        size = _glyph_270(log)
        print("phone 1/5 at 270 px: %.1f" % size, flush=True)
        poster = (350.0, 146.0)
        if not _fits(row["cam"], (poster, row["hand"])):
            faults.append("phone: the poster 0 or the hand is outside the crop")
    return faults


def _snap(row):
    import of_cast as oc
    row["log"] = list(bs.DRAW_LOG)
    row["grips"] = [dict(g) for g in oc.GRIP_LOG]
    return row


def _clear_logs():
    import of_cast as oc
    bs.DRAW_LOG[:] = []
    oc.GRIP_LOG[:] = []
    oc.HAND_LOG[:] = []


def _old_frames():
    bs.GRIP_WATCH[0] = True
    _clear_logs()
    try:
        frames = {
            "shred": maker(_shot("03"), "shred", False, 2)[0](30, 60),
            "pocket": maker(_shot("11"), "pocket", False, 2)[0](59, 60),
            "tape": maker(_shot("05"), "match", False, 3)[0](0, 1),
            "phone": fr.paint(bs.CAM["S0"], overlay=bs.star_overlay),
        }
        log = list(bs.DRAW_LOG)
    finally:
        bs.GRIP_WATCH[0] = False
    for name, surf in frames.items():
        _write_both(surf, "bp_hand_plant_" + name)
    return log


def _locked_ok():
    return all(_md5(os.path.join(bs.EP, "stills", name)) == want for name, want in LOCKED.items())


def _mom_differs():
    """The sheet sleeve against the room's two segments. Same pixels means Mom is not a new drawing."""
    import acts_ob as ac
    import kit
    import mom_fs as mfs

    def once(joined):
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 420, 520)
        c = cairo.Context(surf)
        c.set_source_rgb(0.93, 0.89, 0.82)
        c.paint()
        k = kit.Ctx(c, 0)
        if joined:
            with ac.arms():
                mfs.mom(k, 210, 500, 0.8, "fists", "unimpressed", look=(-0.9, 0.3), chin=True)
        else:
            mfs.mom(k, 210, 500, 0.8, "fists", "unimpressed", look=(-0.9, 0.3), chin=True)
        surf.flush()
        buf = np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data())
        return np.array(buf[:, :surf.get_width(), :3])

    return not np.array_equal(once(False), once(True))


def use():
    """Sheet look and the v4b phone, as new PNGs. The clutch stills and v4 stay unwritten."""
    import bp_set
    import bp_hand_sheet_v4 as sheet
    if not _locked_ok():
        print("locked stills CHANGED", flush=True)
        return 1
    before = {name: _md5(path) for name, path in sheet.SHEETS.items()}
    held = sheet.OUT + ".held.png"
    import shutil
    from PIL import Image, ImageChops
    shutil.copyfile(sheet.OUT, held)
    try:
        try:
            sheet.write()
        except RuntimeError as err:
            print(err, flush=True)
            return 1
        fresh = Image.open(sheet.OUT).convert("RGB")
        old = Image.open(held).convert("RGB")
        if fresh.size != old.size or ImageChops.difference(fresh, old).getbbox() is not None:
            shutil.copyfile(held, sheet.OUT)
            print("class sheet pixels changed", flush=True)
            return 1
    finally:
        if os.path.exists(held):
            os.remove(held)
    for name, path in sheet.SHEETS.items():
        if _md5(path) != before[name]:
            print("%s class sheet changed" % name, flush=True)
            return 1
    differs = _mom_differs()
    saved_mom = bp_set.MOM_ARMS[0]
    bp_set.SHEET[0] = True
    bp_set.MOM_ARMS[0] = differs
    try:
        room = fr.paint(fr.S0)
        night = fr.paint(fr.S0, grade=0.55)
        phone = _phone_job(_phone_v4b)["surf"]
        mom = fr.paint(fr.COUNTER) if differs else None
    finally:
        bp_set.SHEET[0] = False
        bp_set.MOM_ARMS[0] = saved_mom
    if not _locked_ok():
        print("locked stills CHANGED", flush=True)
        return 1
    directory = os.path.join(bs.EP, "rough_work", "pic_use")
    os.makedirs(directory, exist_ok=True)
    _write_both(room, "bp_use_room", directory)
    _write_both(night, "bp_use_night", directory)
    _write_both(phone, "bp_use_phone", directory)
    if mom is not None:
        _write_both(mom, "bp_use_mom", directory)
        print("mom elbow differs", flush=True)
    else:
        print("mom elbow is the same", flush=True)
    print("locked stills unchanged", flush=True)
    return 0


def grips(plant=False):
    """Live: the new stills. --plant: today's stroke, second point and phone rectangle. Exit 1 when the plant is caught."""
    if not _locked_ok():
        print("locked stills CHANGED", flush=True)
        return 0 if plant else 1
    if plant:
        log = _old_frames()
        stroke = "stroke" in log
        point = "point" in log
        slide = "slide" in log
        print("mode     grips plant", flush=True)
        print("plant: sleeve stroke   %s" % ("caught" if stroke else "MISSED"), flush=True)
        print("plant: second point    %s" % ("caught" if point else "MISSED"), flush=True)
        print("plant: phone rectangle %s" % ("caught" if slide else "MISSED"), flush=True)
        print("locked stills unchanged", flush=True)
        return 1 if stroke and point and slide else 0
    bs.GRIP_WATCH[0] = True
    try:
        rows = handstills()
    finally:
        bs.GRIP_WATCH[0] = False
    faults = []
    for row in rows:
        faults.extend(_frame_faults(row, row.get("log") or [], row.get("grips") or []))
    print("mode     grips", flush=True)
    if faults:
        for row in faults:
            print("FAIL " + row, flush=True)
        return 1
    print("clean", flush=True)
    print("locked stills unchanged", flush=True)
    return 0


def _tree_md5(directory):
    found = {}
    if not os.path.isdir(directory):
        return found
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            found[name] = _md5(path)
    return found


def _has(log, kind):
    return any(item == kind or (isinstance(item, tuple) and item and item[0] == kind) for item in log)


def look_gate():
    """The checks the v4 encode waits for. Returns 0 when they pass. Does not render."""
    import of_cast as oc
    faults = []
    use_dir = os.path.join(bs.EP, "rough_work", "pic_use")
    timing = {v: _md5(timing_path(v)) for v in (1, 2, 3) if os.path.isfile(timing_path(v))}
    use_before = _tree_md5(use_dir)
    if not _locked_ok():
        faults.append("locked stills changed before the gate")
    if use():
        faults.append("use() failed")
    if _tree_md5(use_dir) != use_before:
        faults.append("pic_use pixels changed")
    if not _locked_ok():
        faults.append("locked stills changed after use()")
    if not os.path.isfile(timing_path(4)):
        faults.append("missing bp_pic_v4_timing.json")
    for version, digest in timing.items():
        if _md5(timing_path(version)) != digest:
            faults.append("timing v%d was rewritten" % version)
    if os.path.isfile(timing_path(4)) and os.path.isfile(timing_path(3)):
        fresh = json.load(open(timing_path(4), encoding="utf-8"))
        src = json.load(open(timing_path(3), encoding="utf-8"))
        if fresh.get("picture") != "bp_pic_v4" or fresh.get("lines") != src.get("lines"):
            faults.append("v4 times are not the v3 times")
    poster = (350.0, 146.0)
    bs.GRIP_WATCH[0] = True
    try:
        _clear_logs()
        with _look(4):
            _draw, (cam, name) = maker(_shot("12"), "star", False, 4)
            _draw(0, 1)
            star_log = list(bs.DRAW_LOG)
        if name != "phone":
            faults.append("v4 star is on %s" % name)
        if _has(star_log, "slide"):
            faults.append("v4 star drew the rectangle")
        if not _has(star_log, "word"):
            faults.append("v4 star has no 1/5")
        if not _fits(cam, (poster,)):
            faults.append("v4 star crop misses the poster 0")
        _clear_logs()
        _draw, (_cam, name3) = maker(_shot("12"), "star", False, 3)
        _draw(0, 1)
        if not _has(bs.DRAW_LOG, "slide") or name3 != "S0":
            faults.append("v3 star is no longer the rectangle on S0")
        old = maker(_shot("01"), "hold", True, 3)[0](0, 1)
        with _look(4):
            new = maker(_shot("01"), "hold", True, 4)[0](0, 1)
        if np.array_equal(_buf(old), _buf(new)):
            faults.append("v4 S0 matches v3; the sheet look is off")
        if DON_HAND != "point" or PAM_HAND != "point":
            faults.append("hands are %s and %s" % (DON_HAND, PAM_HAND))
        for label, sid, kind, i, n in (
            ("shred", "03", "shred", 30, 60),
            ("pocket", "11", "pocket", 59, 60),
            ("match", "05", "match", 0, 1),
        ):
            _clear_logs()
            with _look(4):
                maker(_shot(sid), kind, False, 4)[0](i, n)
            if not _has(bs.DRAW_LOG, "point"):
                faults.append("%s did not draw point" % label)
            if any(g.get("kind") == "clutch" for g in oc.GRIP_LOG):
                faults.append("%s drew a clutch" % label)
    finally:
        bs.GRIP_WATCH[0] = False
    if not _locked_ok():
        faults.append("locked stills changed after the frames")
    if beats():
        faults.append("beats failed")
    if beats(True) != 1:
        faults.append("beats --plant missed a plant")
    if bubbles("full", 4):
        faults.append("bubbles full 4 failed")
    if bubbles("nonight", 4):
        faults.append("bubbles nonight 4 failed")
    if not _locked_ok():
        faults.append("locked stills changed after bubbles")
    print("LOOK " + ("FAIL " + "; ".join(faults) if faults else "PASS"), flush=True)
    return 1 if faults else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plant"
    if cmd == "plant":
        sys.exit(0 if plant() else 1)
    elif cmd == "bubbles":
        cut = sys.argv[2] if len(sys.argv) > 2 else "full"
        version = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        sys.exit(1 if bubbles(cut, version) else 0)
    elif cmd == "beats":
        sys.exit(beats("--plant" in sys.argv))
    elif cmd == "look":
        sys.exit(look_gate())
    elif cmd == "render":
        version = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        render(version, "full")
        render(version, "nonight")
    elif cmd == "grips":
        sys.exit(grips("--plant" in sys.argv))
    elif cmd == "use":
        sys.exit(use())
    elif cmd == "handstills":
        handstills()
    else:
        raise SystemExit("plant | bubbles [full|nonight] [version] | beats | look | render <version> | grips | handstills | use")
