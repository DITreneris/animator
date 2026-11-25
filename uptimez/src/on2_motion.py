"""v29 (25 Nov): the raven at 0:00 (Tomas: "the opening is bad, the leg is drawn badly; like 4, where the cat leaps, but a
raven"; two outside reviews, his picks): on2_raven.RAVEN. The leg is out and the taxi's door stays shut; 1.1 is five
drawings of the raven diving at us from the lamp; one wing wipes the lens and 1.2 is under it at 0.42 s, holding its first
drawing for four drawings so the first shot is still fired at 1.0 s. The last two drawings of the film (in the window,
8.7) have it back on the lamp, then crouched to spring: the seam. Sound: one caw, its wings, a low thump on the lens,
then nothing but her voice until the first shot (on2_sound.motion_mix16(raven=True)). RAVEN[0] = False draws v28
(pinned by commit 8c25517).
v28 (20 Nov): a joke by 0:01 (the outside review: "no joke at 0:01-0:02, the first is the gang war at about 0:03"; Tomas
chose): OPEN28. 1.1 is 0.75 s (the taxi, the door, her heel); the cab pulls away at once and the gang war starts 0.25 s
into 1.2, so the first shot is fired at 1.0 s and she doesn't blink. "New Year's Eve." runs on over the war and "The
whole city was celebrating." waits for it. Frame 0 and the loop are unchanged. OPEN28[0] = False draws v27.
on2_motion_v27.py is pinned.
v27 (18 Nov): 5.1, smoke lit behind the tables and black arms to the hands (on2_motion_b5 v13). on2_motion_v26.py is pinned.
v26 (18 Nov): Tomas: "0:29 too dark, the money must read; 0:32 too dark, I can't see the glass or the pour; 0:47
too dark, I can't see the office; the UptimeZ logo must be there": lit spots on the money, the pour and the logo; a
lighter side light there; the pour earlier and longer and the coupe clear of her hair; the office lit, its glass door,
no extra blinds on it. on2_motion_v25.py is pinned.
v25 (18 Nov): the first Noir's look (Tomas: "why does Noir 1 still look better"; he chose): the blinds' shadow on
the walls of the bar, the office and the wall (under the people), a side light with her face on the lit side, lighter
faces with true blacks (engine_on TONE v3), the narration in typewriter on cream cards. LOOK3[0] = False draws v24.
on2_motion_v24.py is pinned.
v24 + release (18 Nov): `python3 on2_motion.py A2 release` draws the same film at 1080x1920 (opt-in; the 540 test is
unchanged). on2_motion_v24.py is pinned.
v24 (18 Nov): lip-sync from the takes, one drawing early (b5 v11, b68 v13); 4.1b, 5.1, 5.5 and 5.10 shorter (Tomas
chose). on2_motion_v23.py is pinned.
v23 (18 Nov): Tomas: the banner in the first shot takes the eye from TAXI, and the shooting can't be heard. HAPPY NEW
YEAR is gone from 1.1 and hangs over the alley's mouth in 1.2, above the gang war; the shots are louder and brighter,
with a slap off the walls (motion_mix15). on2_motion_v22.py is pinned.
v22 (18 Nov): the loop: the film ends in the window, on the first drawing of the taxi (Tomas chose: she falls asleep,
into the window; rain and the taxi's brakes over the seam). Beats 06-08: b68 v12; sound: motion_mix14. on2_motion_v21.py
is pinned.
v21 (18 Nov): from the second cold viewer's notes (Tomas chose): three reaction closes, Pam's sweep pays off, the end
is a joke and not a lamp, and the narration is 30 px (two rows at most). Beats 06-08: on2_motion_b68 v11; sound:
on2_sound.motion_mix13. on2_motion_v20.py is pinned.
OFFICE NOIR 2: the motion test, v20. 18 Nov. on2_motion_v19.py to _v1.py are pinned.
v20 is v19 with less New Year in the street (Tomas: "too many lights and HAPPY NEW YEAR"; he chose): the banner only
in the first two shots (the cab, the gang war); lights in one window only, and over the bar's door; the clocks stay.
3.4: her wrap swings from his right hand, the side the sweeper does not hide.
Writes ../office-noir-2/on2_motion_test_v20.mp4 (540 x 960) and on2_motion_timing_v20.json.
  KOKORO_DIR=/tmp/kokoro python3 on2_motion.py [A2|A|B|C]"""
import contextlib
import json
import math
import os
import subprocess
import sys
import cairo
import kit
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import on2_board as b
import on2_sound as snd
import on2_motion_b5 as b5
import on2_motion_b68 as b68
import engine_on as eng
import noir2_cast as n
n.SPARKLE2[0] = True                                     # v11
import client_ob as co
from kit import Ctx, INK, ellipse, rect, cut

V = "v41"
W, H, FPS = 540, 960, 30
SAFE = (18, 96, 522, 820)
LEAD, TAIL = 0.25, 0.42
PLAN = [("1.1", 2.0, "n1"), ("1.2", 2.5, "n6", 0.05), ("1.2b", 0.75, None), ("2.1", 1.5, "n2"), ("2.3a", 10 / 12.0, None), ("2.2", 1.0, None), ("2.3b", 8 / 12.0, None), ("2.4", 1.5, None),
        ("2.5", 1.0, None), ("2.6", 3.0, "n3", -0.7),
        ("3.1", 1.75, None), ("3.2", 2.5, "n7", -0.5), ("3.3", 1.0, None), ("3.4", 1.5, None),
        ("4.1a", 1.5, "n8", -1.2), ("4.1b", 15 / 12.0, None), ("4.2", 1.25, None)]
OPEN28 = [True]                                           # v28: the opening re-timed; False draws v27
PLAN28 = {"1.1": ("1.1", 0.75, "n1", -1.03), "1.2": ("1.2", 2.75, "n6", 0.05)}   # 1.1's line runs on into 1.2
LEADS28 = {"1.2": 0.75}                                   # the city line waits for New Year's Eve. to end
SHOTS_12_28 = ((3, 0), (5, 2), (7, 1), (8, 3), (10, 0), (12, 2), (13, 1))
FALL_28 = 14
import on2_raven as rv
rv.RAVEN[0] = True                                        # v29: the raven at 0:00; False draws v28
RAVEN_HOLD = 4 / 12.0                                     # 1.2 starts this much earlier and holds its first drawing
if rv.RAVEN[0]:
    PLAN28 = {"1.1": ("1.1", 5 / 12.0, "n1", 5 / 12.0 - 0.25 - 1.112), "1.2": ("1.2", 2.75 + RAVEN_HOLD, "n6", 0.05)}
    LEADS28 = {"1.2": 0.75 + RAVEN_HOLD}
V30 = [True]                                              # v30 (25 Nov, cold test v29, Tomas's picks): "I only want my blueprint", the wing's gap, no leg at 0:11, the push to her face, "The usual." hers, the desk from the side, owners for the bar's hands; False draws v29
if V30[0]:
    PLAN28["7.2b"] = ("7.2b", 16 / 12.0, "c1b", -0.55)       # the pop lands on "-print" (7.3 starts 1.37 s into the take; the pop is 2 drawings in)
V31 = [True]                                              # v31 (25 Nov, cold test v30, Tomas's picks): the raven whole in the lamp's light at 0:00 and no red gap; no tube in her hand before the office; the compact open with her in its mirror, her shadow over it; her back; faces for the bar's guests; a glove over her mouth; the seam two drawings early. False draws v30
V32 = [True]                                              # v32 (25 Nov, the review of v31's stills; Tomas: "tobulinam"; polish, no rebuild): the glove's fingers, the compact drawn at its own size (hinge, sheen, powder, her own figure in the mirror), wet stones (on4_weather.glints, Office Noir 4) and contact shadows, the wrap and her hair from behind, three different guests in the dark with the smoke over them, the raven's rim as light. False draws v31
V33 = [True]                                              # v33 (25 Nov, the hands audit; Tomas: "tobulinam"): the series' one hand (hands_ps) on her rig, a shape per pose; her inserts a forearm from the frame's edge with that hand (on2_hands). False draws v32
V34 = [True]                                              # v34 (25 Nov, the hand sheet's review; Tomas: "tvarkom"): hands_ps's glove mode for her hands (one silhouette, slimmer tapered fingers). False draws v33
V35 = [True]                                              # v35 (25 Nov, cold test v34, Tomas's picks; the last round for the hands): the note and the number over her shoulder; the wrap as fur on her shoulders; the Shadow's sleeve; the detective's elbow; her beckon, her hand over her mouth, her back's hands; the bartender's fist. False draws v34
# v36 (25 Nov, Tomas: "undo it"): v35 without the Shadow's sleeve and rim (on2_board.arm_in at 42-45 s and 55 s, noir2_cast.shadow) (noir2_cast.SLEEVE off); nothing else changes
V37 = [True]                                              # v37 (25 Nov, Tomas at 0:27: "the people at the sides, pathetic"): the bar's guests as the film's hat shadows, tables with hats, lamps and glasses at the bottom, the detective's glass at his own eye. False draws v36
V38 = [True]                                              # v38 (25 Nov, the bar's review; Tomas: "tvarkom"; the hiding gag kept): her chin up and a knowing look as the hands come; the guests stand there from the start, the far pair paler; the glass shows the money magnified; she winks over the money as the glass goes past; the blinds 20 % lighter in the bar. False draws v37
V39 = [True]                                              # v39 (25 Nov, the detective's arm's review; Tomas: "tobulinam"): his lens arm in 5.2 drawn again (noir2_cast.ARM3). False draws v38
V40 = [True]                                              # v40 (25 Nov, the arm's second review; Tomas: "tvarkom"; the last round on this arm): his elbow up and near his body, the glass on a short level arc while she winks, and he freezes for it. False draws v39
V41 = [True]                                              # v41 (25 Nov, Tomas: "back to the bar and finalize"): the detective's arm out of the frame (his fist and cuff at the bottom edge, a long-handled glass), the wink 0.33 s sooner (0.83 s), the glass eased over four drawings. False draws v40
END = {}                                                  # v29: set while 8.7 draws the street in its window
TEXT = dict(snd.NARR)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def lerp(a, c, x):
    return a + (c - a) * min(1.0, max(0.0, x))


def rain(k, t, floor=None):
    """Streaks that fall: each one drops the height of the frame in about two thirds of a second."""
    cc = k.c
    cc.set_source_rgba(1, 1, 1, 0.20); cc.set_line_width(1.6); cc.set_line_cap(1)
    for i in range(30):
        x0 = (i * 97) % 580 - 20
        y = ((i * 173) % 1000 + t * 1500) % 1040 - 60
        cc.move_to(x0 - y * 0.26 + 120, y); cc.line_to(x0 - y * 0.26 + 111, y + 34); cc.stroke()


def drops(k, t, floor):
    """v4: rain on the ground. Rings that open and fade in four drawings, most of them in the two puddles."""
    cc = k.c
    d = int(round(t * 12))
    spots = [(120, floor + 150, 92, 16), (430, floor + 230, 120, 20)]
    for i in range(10):
        per = 7 + (i * 5) % 6
        cyc, age = divmod(d + i * 3, per)
        if age > 3:
            continue
        a = age / 4.0
        if i < 6:
            ex, ey, rw, rh = spots[i % 2]
            x = ex + ((i * 37 + cyc * 53) % 100 / 50.0 - 1) * rw * 0.7
            y = ey + ((i * 61 + cyc * 29) % 100 / 50.0 - 1) * rh * 0.5
        else:
            x = (i * 131 + cyc * 197) % 520 + 10
            y = floor + 44 + (i * 71 + cyc * 113) % max(1, int(940 - floor - 44))
        if y > 950:
            continue
        g = 0.6 + 0.8 * (y - floor) / (960.0 - floor)
        cc.set_source_rgba(1, 1, 1, 0.55 * (1 - a)); cc.set_line_width(1.6 * g)
        cc.save(); cc.translate(x, y); cc.scale((5 + 16 * a) * g, (5 + 16 * a) * g * 0.3); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
        cc.restore(); cc.stroke()


NOW = {"min": 55, "sec": None}                           # v12: what the clocks read in the drawing being made; set by frame()


def clock(k, x, y, r, hh=11, mm=None, sec=None, face=(0.93, 0.92, 0.88)):
    """v12: a round wall clock. mm None: what NOW says. sec: a second hand, or None."""
    cc = k.c
    mm = NOW["min"] if mm is None else mm
    if mm >= 60:
        hh, mm = 12, mm - 60
    ellipse(k, x, y, r, r, face, 940, shadow=False, lw=max(2.0, r * 0.12))
    cc.set_source_rgb(*INK); cc.set_line_cap(1)
    for i in range(12):                                                   # the hours
        a = i * math.pi / 6
        cc.set_line_width(max(1.6, r * 0.07) * (1.6 if i % 3 == 0 else 1.0))
        cc.move_to(x + math.sin(a) * r * 0.76, y - math.cos(a) * r * 0.76); cc.line_to(x + math.sin(a) * r * 0.90, y - math.cos(a) * r * 0.90); cc.stroke()
    ah = (hh % 12 + mm / 60.0) * math.pi / 6
    am = mm * math.pi / 30
    cc.set_line_width(max(2.4, r * 0.12)); cc.move_to(x, y); cc.line_to(x + math.sin(ah) * r * 0.48, y - math.cos(ah) * r * 0.48); cc.stroke()
    cc.set_line_width(max(1.8, r * 0.08)); cc.move_to(x, y); cc.line_to(x + math.sin(am) * r * 0.74, y - math.cos(am) * r * 0.74); cc.stroke()
    if sec is not None:
        a_ = sec * math.pi / 30
        cc.set_line_width(max(1.0, r * 0.035)); cc.move_to(x - math.sin(a_) * r * 0.15, y + math.cos(a_) * r * 0.15)
        cc.line_to(x + math.sin(a_) * r * 0.84, y - math.cos(a_) * r * 0.84); cc.stroke()
    ellipse(k, x, y, r * 0.08, r * 0.08, INK, 941, shadow=False, outline=False)


def bulbs(k, x0, y0, x1, y1, sag, n_, t, s=1.0, seed=0):
    """v12: a string of lights: a wire hanging between two points, white bulbs that glow, a few of them twinkling."""
    cc = k.c
    pts = []
    for i in range(n_):
        u = (i + 0.5) / n_
        pts.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + sag * 4 * u * (1 - u)))
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.set_line_width(1.6 * s); cc.move_to(x0, y0)
    cc.curve_to(x0 + (x1 - x0) * 0.33, y0 + sag * 1.33, x0 + (x1 - x0) * 0.67, y1 + sag * 1.33, x1, y1); cc.stroke()
    d = int(round(t * 12))
    for i, (bx, by) in enumerate(pts):
        on = (i * 7 + seed + d // 3) % 5 != 0                            # one in five is off for a moment
        r = 4.2 * s
        if on:
            g = cairo.RadialGradient(bx, by + r, 0, bx, by + r, r * 4.2)
            g.add_color_stop_rgba(0, 1, 1, 1, 0.55); g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
            cc.set_source(g); cc.new_path(); cc.arc(bx, by + r, r * 4.2, 0, 2 * math.pi); cc.fill()
        cc.save(); cc.translate(bx, by + r); cc.scale(r * 0.75, r); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore()
        cc.set_source_rgb(*((1, 1, 1) if on else (0.40, 0.40, 0.42))); cc.fill()


def ny_sign(k, x, y, s=1.0, t=0.0):
    """v12: over the street door, HAPPY NEW YEAR in white light. Two letters are dead, as signs are at night."""
    cc = k.c
    cc.save(); cc.translate(x, y); cc.scale(s, s)
    rect(k, 0, 0, 120, 48, (0.06, 0.06, 0.07), 950, shadow=False, lw=2.2)
    cc.set_source_rgb(0.08, 0.08, 0.09); cc.set_line_width(2.4)
    for bx in (24, 96):                                                   # it hangs from two rods
        cc.move_to(bx, 0); cc.line_to(bx, -16); cc.stroke()
    cc.select_font_face("Inter", 0, 1)
    dead = {(0, 3), (1, 6)}                                               # the second P, and the last A
    for row, (word, size, yy) in enumerate((("HAPPY", 16, 21), ("NEW YEAR", 14, 41))):
        cc.set_font_size(size)
        w = cc.text_extents(word).x_advance
        xx = 60 - w / 2
        for j, ch in enumerate(word):
            if ch != " ":
                lit = (row, j) not in dead
                if lit:
                    cc.set_source_rgba(1, 1, 1, 0.35); cc.move_to(xx - 0.8, yy + 0.8); cc.show_text(ch)
                cc.set_source_rgb(*((1, 1, 1) if lit else (0.30, 0.30, 0.32))); cc.move_to(xx, yy); cc.show_text(ch)
            xx += cc.text_extents(ch).x_advance
    cc.restore()


def banner(k, t, x=12, y=240, w=236, h=50, fs=25):
    """v14: HAPPY NEW YEAR across the facade, between the rows of windows: dark cloth on two cords, white letters, two of
    them dead, and lights along its top and bottom edges."""
    cc = k.c
    cc.set_source_rgb(0.08, 0.08, 0.09); cc.set_line_width(2.4)
    for bx in (x + 16, x + w - 16):
        cc.move_to(bx, y); cc.line_to(bx, y - 14); cc.stroke()
    rect(k, x, y, w, h, (0.07, 0.07, 0.08), 951, shadow=False, lw=2.6)
    cc.select_font_face("Inter", 0, 1); cc.set_font_size(fs)
    word = "HAPPY NEW YEAR"
    dead = {3, 12}                                                        # the second P and the A
    xx = x + w / 2 - cc.text_extents(word).x_advance / 2
    for j, ch in enumerate(word):
        if ch != " ":
            lit = j not in dead
            if lit:
                cc.set_source_rgba(1, 1, 1, 0.30); cc.move_to(xx - 1, y + h / 2 + fs * 0.36 + 1); cc.show_text(ch)
            cc.set_source_rgb(*((1, 1, 1) if lit else (0.28, 0.28, 0.30))); cc.move_to(xx, y + h / 2 + fs * 0.36); cc.show_text(ch)
        xx += cc.text_extents(ch).x_advance
    bulbs(k, x + 4, y - 5, x + w - 4, y - 5, 0, 10, t, 0.9, 7)
    bulbs(k, x + 4, y + h - 4, x + w - 4, y + h - 4, 0, 10, t, 0.9, 11)


def contact(cc, x, y, rx, ry=None, a=0.55):
    """v32: a soft dark pool where something stands on the wet stones"""
    ry = ry or rx * 0.16
    cc.save(); cc.translate(x, y); cc.scale(rx, ry)
    g = cairo.RadialGradient(0, 0, 0.2, 0, 0, 1.0)
    g.add_color_stop_rgba(0, 0, 0, 0, a); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    cc.set_source(g); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.fill(); cc.restore()


def stands(cc, x, y, s=1.0):
    """v34: she stands on it: a narrow dark line under her heels, and the gown's red broken up in the wet below her
    (solid red dashes: a tint would be taken for grey by the noir pass)"""
    contact(cc, x, y + 2, 46 * s, 7 * s, 0.9)
    cc.set_source_rgb(*n.KEY); cc.set_line_cap(1)
    for i in range(6):
        yy = y + (16 + i * 13 + i * i * 1.5) * s
        w = (40 - i * 5.5) * s
        cc.set_line_width(max(1.2, (3.4 - i * 0.4) * s))
        cc.move_to(x - w + (i % 2) * 8 * s, yy); cc.line_to(x + w - ((i + 1) % 2) * 10 * s, yy); cc.stroke()


def glints(c, x0, x1, y0, y1, n_, t, seed=1, a=0.55):
    """on4_weather.glints, copied: importing on4_weather imports a second on2_motion, which takes b5 and b68 over
    (use()) from the film being rendered"""
    import random
    d = int(t * 6)
    c.set_line_cap(1)
    for i in range(n_):
        r = random.Random(seed * 131 + i * 17 + (d + i) // 5)
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); g = 0.5 + (y - y0) / max(1.0, y1 - y0)
        c.set_source_rgba(1, 1, 0.97, a * r.uniform(0.4, 1.0)); c.set_line_width(2.0 * g)
        w = r.uniform(5, 14) * g; c.move_to(x - w, y); c.line_to(x + w, y); c.stroke()
    c.set_line_cap(0)


def wet(k, floor, lamp, t):
    """v32: the road wet. Office Noir 4's glints (on4_weather.glints), the lamp's light smeared down the stones, and
    splashes where the rain lands."""
    cc = k.c
    if lamp:
        lx = lamp[0] - 30
        g = cairo.LinearGradient(0, floor + 34, 0, 950)
        g.add_color_stop_rgba(0, 1, 1, 0.96, 0.30); g.add_color_stop_rgba(1, 1, 1, 0.96, 0.0)
        cc.new_path(); cc.move_to(lx - 26, floor + 34); cc.line_to(lx + 26, floor + 34); cc.line_to(lx + 70, 950); cc.line_to(lx - 70, 950); cc.close_path()
        cc.set_source(g); cc.fill()
        for i in range(7):                                                # broken by the ripples
            yy = floor + 60 + i * i * 6.5
            if yy < 950:
                w = 22 + i * 7 + 6 * math.sin(t * 5 + i)
                cc.set_source_rgba(1, 1, 0.96, 0.34 - i * 0.035); cc.set_line_width(2.4 + i * 0.5); cc.set_line_cap(1)
                cc.move_to(lx - w, yy); cc.line_to(lx + w, yy); cc.stroke()
    glints(cc, 0, 540, floor + 44, 940, 26, t, 11, 0.42)
    d = int(round(t * 12))
    for i in range(6):                                                    # a splash: two short strokes up from where a drop lands
        r = (i * 97 + (d // 2) * 61) % 500 + 20, floor + 50 + (i * 53 + (d // 2) * 89) % max(1, int(880 - floor))
        if (d + i) % 2 == 0 and r[1] < 940:
            cc.set_source_rgba(1, 1, 1, 0.5); cc.set_line_width(1.4); cc.set_line_cap(1)
            for dx in (-5, 5):
                cc.move_to(r[0], r[1]); cc.line_to(r[0] + dx, r[1] - 8); cc.stroke()


def street(k, floor, lamp, t):
    b.street(k, floor, lamp, rain=False)
    if V31[0] and V32[0]:
        wet(k, floor, lamp, t)
    wx, wy = 156, 110                                                     # v20: lights in one window only, the lit one
    bulbs(k, wx + 2, wy + 92, wx + 76, wy + 92, 12, 5, t, 1.8, 3)
    if floor > 330 and NOW.get("shot") == "1.2":                         # v23: not over the taxi; over the alley, above the war
        banner(k, t, x=6, y=356, w=198, h=44, fs=21)
    if lamp:                                                              # v14: a street clock on the lamp post
        px, cy = lamp[0] + 44, lamp[1] + 150
        if cy + 34 < floor:
            cc = k.c
            cc.set_source_rgb(0.04, 0.04, 0.05); cc.set_line_width(7); cc.move_to(px, cy - 40); cc.line_to(px, cy + 40); cc.stroke()
            clock(k, px, cy, 30)
    drops(k, t, floor)


@contextlib.contextmanager
def lids(skin, on, line=False):
    """v4: a blink. While this is open, whoever is drawn has their eyes shut for the drawing."""
    if not on:
        yield
        return
    old = kit.face_draw

    def face_draw(k_, x, y, face, look, glasses=False, seed=0):
        old(k_, x, y, face, look, glasses=glasses, seed=seed)
        c = k_.c
        for sx in (-17, 17):
            c.set_source_rgb(*skin); c.new_path(); c.arc(x + sx, y, 12, 0, 2 * math.pi); c.fill()
            if line:
                c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1); c.move_to(x + sx - 10, y + 3); c.line_to(x + sx + 10, y + 3); c.stroke()
    kit.face_draw = face_draw
    try:
        yield
    finally:
        kit.face_draw = old


def said(row_shot, tl, codes, lead=LEAD):
    """v8: the mouth shape for this drawing of a spoken line, or None when the speaker's mouth is shut.
    codes: one letter a drawing from the start of the line (iwry_mouths: M A E O U F C)."""
    i = int(round((tl - lead) * 12))
    return codes[i] if 0 <= i < len(codes) and codes[i] != "M" else None


@contextlib.contextmanager
def talking(skin, code, lip):
    """v8: for a figure whose drawing has no mouth shapes of its own: this shape over its mouth for the drawing."""
    if not code:
        yield
        return
    import iwry_mouths as im
    old = kit.face_draw

    def face_draw(k_, x, y, face, look, glasses=False, seed=0):
        old(k_, x, y, face, look, glasses=glasses, seed=seed)
        im.mouth(k_, x, y + 28, code, skin, lip_col=lip, erase=(18, 10), seed=seed + 67)
    kit.face_draw = face_draw
    try:
        yield
    finally:
        kit.face_draw = old


@contextlib.contextmanager
def breath(k, x, feet, t, on=True, rate=2.6, amt=0.007):
    """v4: the figure drawn inside grows and sinks by a few pixels, feet where they are."""
    cc = k.c
    cc.save()
    if on:
        cc.translate(x, feet); cc.scale(1.0, 1.0 + amt * math.sin(2 * math.pi * t / rate)); cc.translate(-x, -feet)
    try:
        yield
    finally:
        cc.restore()


TROUSERS, SHOE = (0.60, 0.60, 0.63), (0.11, 0.11, 0.13)


def don_legs(k, x, feet, s, steps):
    """v4: the detective's legs, from under his coat. steps: for each foot (x from his middle, how high it is lifted,
    toe: -1 or 1 for a shoe seen from the side pointing that way, 0 for one seen from the front). Local units."""
    cc = k.c
    hem = n.d.HEM
    cc.save(); cc.translate(x, feet); cc.scale(s, s)
    for hip, (fx, lift, toe) in zip((-13, 13), steps):
        cut(k, [(hip - 11, hem - 8), (hip + 11, hem - 8), (fx + 9, -lift - 8), (fx - 9, -lift - 8)], TROUSERS, shadow=False, lw=2)
        if toe:
            cut(k, [(fx - toe * 11, -lift - 11), (fx + toe * 8, -lift - 11), (fx + toe * 22, -lift - 4), (fx + toe * 22, -lift), (fx - toe * 11, -lift)],
                SHOE, shadow=False, lw=1.8)
        else:
            ellipse(k, fx, -lift - 5, 13, 7, SHOE, 560 + hip, shadow=False, lw=1.8)
    cc.restore()


def stride(u, a=28.0, up=14.0):
    """One foot through a walk cycle, u 0..1: on the ground and travelling back for the first half, lifted and
    swung forward for the second. Returns (how far ahead of his middle, how high)."""
    u = u % 1.0
    if u < 0.5:
        return a * (1 - 4 * u), 0.0
    q = (u - 0.5) / 0.5
    return -a + 2 * a * q, up * math.sin(math.pi * q)


def don(k, x, feet, s, look, steps, lean=0.0, cloth_ang=0.0, shut=False, pose="look", wrap=True, face="squint", pocket=False,
        glass=True):
    """v4: the detective with legs. The block he stands on in the kit is taken out below his coat.
    v5: any of noir2_cast.detective's poses and faces; pocket: the napkin in his breast pocket."""
    cc = k.c
    cc.save(); cc.translate(x, feet); cc.rotate(math.radians(lean)); cc.translate(-x, -feet)
    don_legs(k, x, feet, s, steps)
    cc.push_group()
    with lids(n.d.SKIN, shut):
        o = n.detective(k, x, feet, s, pose, face, look, wrap=wrap, cloth_ang=cloth_ang, napkin_in_band=pocket, glass=glass)
    cc.save(); cc.set_operator(cairo.OPERATOR_CLEAR)
    cc.rectangle(x - 62 * s, feet + (n.d.HEM + 1.5) * s, 124 * s, (-n.d.HEM + 12) * s); cc.fill(); cc.restore()
    cc.pop_group_to_source(); cc.paint()
    dev = {"head": cc.user_to_device(*o["head"]), "hands": [cc.user_to_device(*q) for q in o["hands"]]}
    cc.restore()
    return {"head": cc.device_to_user(*dev["head"]), "hands": [cc.device_to_user(*q) for q in dev["hands"]]}


STAND = ((-14, 0, 0), (14, 0, 0))


def splash(k, x, y, a):
    """Rings where something met the wet stones. a: 0..1 through its life."""
    if a <= 0 or a >= 1:
        return
    cc = k.c
    cc.set_source_rgba(1, 1, 1, 0.7 * (1 - a)); cc.set_line_width(2.4)
    for r in (16 + 40 * a, 8 + 22 * a):
        cc.save(); cc.translate(x, y); cc.scale(r, r * 0.3); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.stroke()


# ---------------------------------------------------------------- the shots
TAXI_DX = [0.0]                                             # v22: where the taxi is short of its place (8.7 brings it in)


def m1_1(k, tl):
    if rv.RAVEN[0]:                                                  # v29: no leg; the door stays shut (the raven is the action)
        return _m1_1(k, tl, 99.0, 0.25, 999)
    if OPEN28[0]:                                                    # v28: the same drawings, faster: door, foot, splash
        return _m1_1(k, tl, 0.08, 0.25, 5)
    return _m1_1(k, tl, 0.25, 0.34, 8)


def _m1_1(k, tl, d0, dd, f0):
    street(k, 668, (440, 150), tl)
    door = ease((tl - d0) / dd)
    if V31[0] and V32[0]:
        contact(k.c, 150 + TAXI_DX[0], 722, 330, 26, 0.6)
        cc_ = k.c                                                        # TAXI, upside down and broken, in the wet under it
        cc_.save(); cc_.translate(150 + TAXI_DX[0] - 104, 770); cc_.scale(1, -0.55)
        cc_.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); cc_.set_font_size(40)
        cc_.set_source_rgba(1, 1, 1, 0.16); cc_.move_to(0, 0); cc_.show_text("TAXI"); cc_.restore()
    n.taxi(k, 150 + TAXI_DX[0], 716, 2.5, door=door)
    d12 = int(round(tl * 12))
    if d12 >= f0:                                                               # her foot comes out of the dark and down, in four drawings
        foot, knee = (((186, 636), (219, 563)), ((192, 664), (218, 566)), ((199, 696), (217, 569)), ((206, 716), (216, 572)))[min(3, d12 - f0)]
        b.step_out(k, foot, knee, hand=0.0)
    splash(k, 176, 722, (tl - (f0 + 3) / 12.0) / 0.5)
    rain(k, tl)


# v13: who fires in which drawing of 1.2: (drawing, gunman). Gunmen 0, 1 on the left, 2, 3 on the right; 3 goes down.
SHOTS_12 = ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1))
GUNMEN = ((-70, 1), (-38, 1), (40, -1), (72, -1))         # x from the alley's middle, which way they face
FALL_AT = 23


def alley(k, tl, cx=118, top=420, floor=690):
    """v13: an alley in the facade, lit at its far end, and a gang war in it: hatted shadows behind both corners."""
    cc = k.c
    d = int(round(tl * 12))
    cut(k, [(cx - 104, floor), (cx - 104, top), (cx + 104, top), (cx + 104, floor)], (0.05, 0.05, 0.06), shadow=False, lw=4)
    fx0, fx1, fy0, fy1 = cx - 82, cx + 82, top + 34, floor - 34              # the far end, in the light of a lamp out of sight
    g = cairo.LinearGradient(0, fy0, 0, fy1)
    g.add_color_stop_rgb(0, 0.42, 0.42, 0.44); g.add_color_stop_rgb(1, 0.78, 0.78, 0.76)
    cc.set_source(g); cc.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0); cc.fill()
    cc.set_source_rgb(0.12, 0.12, 0.13)                                      # its walls, running away from us
    for sx in (-1, 1):
        x0, x1 = cx + sx * 104, cx + sx * 82
        cc.new_path(); cc.move_to(x0, top); cc.line_to(x1, fy0); cc.line_to(x1, fy1); cc.line_to(x0, floor); cc.close_path(); cc.fill()
    cc.set_source_rgb(0.20, 0.20, 0.22); cc.new_path(); cc.move_to(cx - 104, floor); cc.line_to(fx0, fy1); cc.line_to(fx1, fy1)
    cc.line_to(cx + 104, floor); cc.close_path(); cc.fill()
    shots12, fall_at = (SHOTS_12_28, FALL_28) if OPEN28[0] else (SHOTS_12, FALL_AT)
    fired = {who: dd for dd, who in shots12}
    for i, (ox, face) in enumerate(GUNMEN):
        x, feet = cx + ox, fy1 + 2
        aim = co._ik(face, 118, co.BT + 46)                                  # the gun arm, straight out at the other side
        other = co._ik(-face, 34, co.BT + 120)
        pose = (other + aim) if face > 0 else (aim + other)
        cc.save()
        if i == 3 and d >= fall_at:                                          # hit: he goes over backwards
            f = min(1.0, (d - fall_at + 1) / 3.0)
            cc.translate(x, feet); cc.rotate(f * 1.35); cc.translate(-x, -feet)
        o = n.shadow(k, x, feet, 0.25, pose, lit_hand=None, seed=430 + i)
        cc.restore()
        if any(dd == d for dd, who in shots12 if who == i):                 # the flash at the muzzle
            hx, hy = o["hands"][1 if face > 0 else 0]
            cc.save(); cc.translate(hx + face * 9, hy); cc.new_path()
            for j in range(10):
                r = 19 if j % 2 == 0 else 6
                a_ = j * math.pi / 5
                (cc.move_to if j == 0 else cc.line_to)(math.cos(a_) * r, math.sin(a_) * r)
            cc.close_path(); cc.set_source_rgb(1, 1, 1); cc.fill()
            cc.restore()
            gl = cairo.RadialGradient(hx, hy, 0, hx, hy, 110)
            gl.add_color_stop_rgba(0, 1, 1, 1, 0.75); gl.add_color_stop_rgba(1, 1, 1, 1, 0.0)
            cc.set_source(gl); cc.new_path(); cc.arc(hx, hy, 110, 0, 2 * math.pi); cc.fill()


def zoom(cc, cx, cy, z):
    """v17: the camera pushed in on (cx, cy)."""
    cc.translate(cx, cy); cc.scale(z, z); cc.translate(-cx, -cy)


def m1_2b(k, tl):
    """v17: close on her face. Behind her the shots light her hair; she does not blink."""
    cc = k.c
    d = int(round(tl * 12))
    cc.set_source_rgb(0.08, 0.08, 0.09); cc.paint()
    for fd, fx, fy in ((1, 90, 240), (4, 470, 300), (7, 120, 420)):                # flashes, behind her
        if d == fd:
            g = cairo.RadialGradient(fx, fy, 0, fx, fy, 260)
            g.add_color_stop_rgba(0, 1, 1, 1, 0.85); g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
            cc.set_source(g); cc.paint()
    n.star(k, 270, 1700, 4.6, "g_pose", "interested", (0.1, -0.2), sparkle=1.0 if d in (1, 2, 4, 5, 7) else 0.0)
    rain(k, tl + 4)


def m1_2(k, tl):
    if rv.RAVEN[0]:                                                  # v29: it starts under the wing and holds, so the war is where it was
        tl = max(0.0, tl - RAVEN_HOLD)
    cc = k.c
    cc.save()
    if V30[0]:                                                           # v30: after the war, in to her face, ending on 1.2b's framing (no jump)
        zoom(cc, 406, 166, 1.0 + 1.42 * ease((tl - 1.25) / 1.55))
    else:
        z0 = 0.5 if OPEN28[0] else 0.9                                     # v28: the war starts sooner, so does the push
        zoom(cc, 118, 560, 1.0 + 0.45 * ease((tl - z0) / 1.4))          # v17: over her shoulder, into the alley
    _m1_2(k, tl)
    cc.restore()


def _m1_2(k, tl):
    street(k, 690, (430, 150), tl)
    alley(k, tl)                                                             # v13: behind her, as the cab pulls away
    x = 40 - 640 * (ease(tl / 0.4) if OPEN28[0] else ease((tl - 0.3) / 0.9)) ** 1.6    # v28: the cab goes at once
    n.taxi(k, x, 730, 1.5, door=0.0)
    rise = 12 if tl < 1 / 12.0 else 5 if tl < 2 / 12.0 else 0
    look = (0.1, -0.2) if tl < 2.0 else (0.3, -0.3)                         # v13: she never looks round
    if V31[0] and V32[0]:
        contact(k.c, 350, 802, 120, 16, 0.6)
        if V34[0]:
            stands(k.c, 350, 802, 1.0)
    n.star(k, 350, 800 + rise, 1.9, "g_pose", "interested", look, sparkle=1.0 if int(tl * 12) % 6 < 3 else 0.2)
    rain(k, tl + 2)


def m2_1(k, tl, dur=2.75):
    cc = k.c
    street(k, 600, (440, 140), tl)
    p = tl / dur
    dy = 300 * (1 - ease(tl / 1.4))                                      # his shadow slides onto the stones after her
    cc.save(); cc.translate(0, dy)
    cc.set_source_rgb(*n.BLACK)
    cc.new_path(); cc.move_to(-20, 960); cc.line_to(120, 760); cc.line_to(200, 760); cc.line_to(190, 960); cc.close_path(); cc.fill()
    cc.save(); cc.translate(160, 752); cc.scale(84, 15); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()
    cc.new_path(); cc.move_to(118, 752); cc.line_to(128, 700); cc.line_to(152, 712); cc.line_to(170, 696); cc.line_to(196, 708); cc.line_to(204, 752)
    cc.close_path(); cc.fill()
    cc.restore()
    if V31[0] and V32[0]:
        contact(k.c, 340, lerp(808, 774, p), 96, 13, 0.65)
        if V34[0]:
            stands(k.c, 340, lerp(808, 774, p), 0.95)
    n.star_back(k, 340, lerp(806, 772, p), lerp(1.92, 1.76, p), step=tl * 1.6)
    rain(k, tl + 4)


def m2_2(k, tl):
    cc = k.c
    cc.set_source_rgb(0.11, 0.11, 0.13); cc.paint()
    b.pool(cc, 300, 200, 420, 0.22)
    ang = 0.16 if tl < 1 / 12.0 else 0.10 if tl < 2 / 12.0 else 0.06
    if V34[0]:                                                          # v34: her forearm from the edge, the compact, her fingers round its base
        import on2_hands as oh
        oh.insert(k, (370, 1030), (300, 830), "grab", 150, arm=1, under=lambda: n.compact2(k, 270, 470, 9.0, ang, hat=tl >= 4 / 12.0))
        return
    n._seg(k, 330, 1000, 290, 760, 110, 96, n.KEY, 3.4)
    n.compact2(k, 270, 470, 9.0, ang, hat=tl >= 4 / 12.0)
    ellipse(k, 286, 760, 58, 52, n.KEY, 363, shadow=False, lw=3.4)


def m2_3a(k, tl):
    """v6: she smiles at herself in the compact. The hat is not there yet."""
    cc = k.c
    cc.set_source_rgb(0.13, 0.13, 0.15); cc.paint()
    b.pool(cc, 380, 160, 420, 0.30)
    d12 = int(round(tl * 12))
    n.star(k, 240, 1270 - (0 if d12 < 3 else 6), 3.4, "g_mirror", "interested" if d12 < 3 else "real", (0.9, -0.1), wrap=False, mirror=True,
           sparkle=1.0 if d12 >= 5 and d12 % 4 < 2 else 0.0)        # v11: it twinkles


def m2_3b(k, tl):
    """v6: she has seen the hat. The smile is gone at once; then her eyes go to the side, to him."""
    cc = k.c
    cc.set_source_rgb(0.13, 0.13, 0.15); cc.paint()
    b.pool(cc, 380, 160, 420, 0.30)
    d12 = int(round(tl * 12))
    zoom(cc, 200, 380, 1.0 + 0.30 * ease(d12 / 3.0))                     # v17: in on her face as the smile goes
    n.star(k, 240, 1264 + (9 if d12 == 0 else 0), 3.4, "g_mirror", "caught", (0.9, -0.1) if d12 < 3 else (-1.0, 0.0), wrap=False, mirror="hat")


def m2_4(k, tl):
    street(k, 720, None, tl)
    b.pool(k.c, 300, 120, 520, 0.38)
    slide = -40 * (1 - ease(tl / 0.25))
    n.shadow(k, 20 + slide, 1180, 2.5, "open", lit_hand=None, look_down=1.0)
    reach = ease((tl - 0.25) / 0.5)
    face = "caught"                                                      # v6: the smile went in 2.3b
    look = (-1.0, 0.0) if tl < 0.5 else (-0.6, 0.5) if tl < 0.75 else (-1.0, 0.9)
    o = n.star(k, 340, 1060, 2.6, "g_stand", face, look, wrap=False)
    lx, ly = o["hands"][0]
    ex, ey = lerp(-200, lx - 22, reach), lerp(380, ly - 52, reach)
    if tl >= 0.25:
        b.arm_in(k, ex - 320, ey - 110, ex, ey)


def compact3(k, x, y, d, u):
    """v32: her compact, drawn at its own size (not a small drawing enlarged): the lid up with its mirror, a hinge, the
    base lying away from us with its powder. In the mirror, her, from behind (n.star_back), going. u 0..1 how far."""
    cc = k.c
    SIL, SIL_D = (0.86, 0.87, 0.90), (0.42, 0.44, 0.50)

    def disc(cx, cy, rx, ry, g0, g1, lw=3.0):
        cc.save(); cc.translate(cx, cy); cc.scale(rx, ry); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore()
        g = cairo.LinearGradient(cx - rx, cy - ry, cx + rx, cy + ry)
        g.add_color_stop_rgb(0, *g0); g.add_color_stop_rgb(1, *g1)
        cc.set_source(g); cc.fill_preserve(); cc.set_source_rgb(*INK); cc.set_line_width(lw); cc.stroke()
    contact(cc, x + 6, y + 150, 150, 34, 0.55)
    disc(x, y + 128, 96, 40, SIL_D, (0.30, 0.31, 0.36))                    # the base: its side, then its top, lying away from us
    disc(x, y + 116, 96, 40, SIL, SIL_D)
    disc(x, y + 116, 76, 30, (0.93, 0.88, 0.84), (0.78, 0.72, 0.68), 2.0)  # the powder
    import random
    r = random.Random(4)
    for i in range(70):                                                   # pressed powder: its grain, and where she has rubbed it
        a_, rr = r.uniform(0, 2 * math.pi), r.uniform(0, 1) ** 0.5
        cc.set_source_rgba(0.55, 0.48, 0.44, 0.5); cc.new_path(); cc.arc(x + math.cos(a_) * rr * 70, y + 116 + math.sin(a_) * rr * 26, 1.3, 0, 2 * math.pi); cc.fill()
    cc.set_source_rgba(0.60, 0.53, 0.49, 0.8); cc.set_line_width(2); cc.set_line_cap(1)
    cc.save(); cc.translate(x - 14, y + 114); cc.scale(34, 12); cc.new_path(); cc.arc(0, 0, 1, 0.3, 2.6); cc.restore(); cc.stroke()
    cc.set_source_rgb(*SIL_D); cc.rectangle(x - 36, y + 70, 72, 16); cc.fill_preserve(); cc.set_source_rgb(*INK); cc.set_line_width(2.4); cc.stroke()   # the hinge
    if V34[0]:                                                             # a barrel hinge: three knuckles and its pin
        for hx0 in (-36, -12, 12):
            cc.set_source_rgb(*(SIL if hx0 != -12 else SIL_D)); cc.rectangle(x + hx0, y + 70, 24, 16); cc.fill_preserve(); cc.set_source_rgb(*INK); cc.set_line_width(1.8); cc.stroke()
        cc.set_source_rgba(1, 1, 1, 0.8); cc.set_line_width(1.6); cc.move_to(x - 32, y + 74); cc.line_to(x + 32, y + 74); cc.stroke()
    for hx in (-18, 0, 18):
        cc.set_source_rgb(*SIL); cc.new_path(); cc.arc(x + hx, y + 79, 3.2, 0, 2 * math.pi); cc.fill()
    disc(x, y, 100, 88, SIL, SIL_D)                                        # the lid, toward us
    if V34[0]:
        disc(x, y, 82, 71, (0.30, 0.33, 0.38), (0.58, 0.62, 0.68), 2.0)    # v34: the glass darker (the night in it), so she is IN it
    else:
        disc(x, y, 82, 71, (0.62, 0.68, 0.76), (0.86, 0.90, 0.94), 2.0)    # its mirror
    cc.save(); cc.save(); cc.translate(x, y); cc.scale(80, 69); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.clip()
    sc_ = 0.62 - 0.36 * u                                                  # her, from behind, in it: the gown, the wrap, her hair
    if V34[0]:                                                             # seen at the mirror's angle: leaning with the lid, cut by its lower edge
        cc.translate(x, y); cc.transform(cairo.Matrix(1, 0, -0.18, 0.92, 0, 0)); cc.translate(-x, -y)
        cc.set_source_rgba(1, 1, 1, 0.10); cc.new_path(); cc.move_to(x - 90, y + 50 - 30 * u); cc.line_to(x + 90, y + 40 - 30 * u); cc.line_to(x + 90, y + 90); cc.line_to(x - 90, y + 90); cc.close_path(); cc.fill()   # the wet street she runs on
    n.star_back(k, x - 10 + 34 * u, y + 66 - 26 * u, sc_, step=d / 6.0)
    cc.set_source_rgba(1, 1, 1, 0.55); cc.set_line_width(7); cc.set_line_cap(1)                 # the glass: two bars of light across it
    cc.move_to(x - 62, y - 14); cc.line_to(x - 30, y - 52); cc.stroke()
    cc.set_line_width(3); cc.move_to(x - 46, y + 2); cc.line_to(x - 12, y - 40); cc.stroke()
    cc.restore()
    cc.set_source_rgba(1, 1, 1, 0.9); cc.set_line_width(3); cc.set_line_cap(1)                   # the rim, lit
    cc.save(); cc.translate(x, y); cc.scale(94, 82); cc.new_path(); cc.arc(0, 0, 1, math.pi * 1.1, math.pi * 1.45); cc.restore(); cc.stroke()


def compact32(k, tl):
    cc = k.c
    d = int(round(tl * 12))
    if d < 2:                                                             # it falls, turning
        cc.save(); cc.translate(250, 250 + 180 * d); cc.rotate(0.5 - 0.3 * d); cc.scale(0.8, 0.8); compact3(k, 0, 0, d, 0.0); cc.restore()
        return
    if d < (4 if V34[0] else 6):                                          # powder, off the stones (v34: gone in two drawings)
        g = ease((d - 2) / (2.0 if V34[0] else 3.0))
        cc.save(); cc.translate(250, 700); cc.scale(0.5 + 0.6 * g, 0.5 + 0.6 * g); cc.translate(-250, -700)
        cc.push_group(); n.powder_puff(k, 250, 700, 4.0); cc.pop_group_to_source(); cc.paint_with_alpha(0.8 * (1.0 - g))
        cc.restore()
    cc.save(); cc.translate(262, 560); cc.scale(1.35, 1.35); cc.translate(-250, -560)
    compact3(k, 250, 500 - (10 if d == 2 else 0), d, min(1.0, (d - 2) / 6.0))
    cc.restore()
    if 3 <= d < 7:                                                        # her shadow, running, across the stones
        sx_ = -160 + 190 * (d - 3)
        cc.set_source_rgba(0.02, 0.02, 0.03, 0.55)
        cc.new_path(); cc.move_to(sx_, 960); cc.line_to(sx_ + 110, 760); cc.line_to(sx_ + 190, 760); cc.line_to(sx_ + 250, 960); cc.close_path(); cc.fill()
        cc.new_path(); cc.arc(sx_ + 150, 716, 58, 0, 2 * math.pi); cc.fill()
    if d >= 5:
        n.footprints(k, 360, 800, 4.2, n=1, step=30)
    if d >= 7:
        n.footprints(k, 450, 700, 3.6, n=1, step=30)


def m2_5(k, tl):
    cc = k.c
    cc.set_source_rgb(*b.GROUND); cc.paint()
    cc.set_source_rgb(0.20, 0.20, 0.23); cc.set_line_width(3)
    for i in range(7):
        cc.move_to(-20, 140 + i * 140); cc.line_to(560, 110 + i * 140); cc.stroke()
    cc.set_source_rgba(1, 1, 1, 0.16); cc.save(); cc.translate(250, 600); cc.scale(260, 200); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    if V31[0] and V32[0]:
        return compact32(k, tl)
    if V31[0]:                                                          # v31: the compact open on the stones, her in its mirror, going; her shadow over it
        d = int(round(tl * 12))
        if d < 2:
            n.compact2(k, 250, 250 + 190 * d, 4.6, 0.5 - 0.35 * d)
        else:
            if d < 6:
                g = ease((d - 2) / 3.0)
                cc.save(); cc.translate(250, 690); cc.scale(0.3 + 0.5 * g, 0.3 + 0.5 * g); cc.translate(-250, -690)
                cc.push_group(); n.powder_puff(k, 250, 690, 4.0); cc.pop_group_to_source(); cc.paint_with_alpha(1.0 - 0.6 * g)
                cc.restore()
            n.compact2(k, 250, 560 - (10 if d == 2 else 0), 5.4, -0.10)
            mx, my, mr = 250 + 5.4 * 17 * math.sin(-0.10) * -1, 560 - 5.4 * 17, 5.4 * 14     # its mirror
            mx, my = 250 - 9, 560 - 92
            cc.save(); cc.new_path(); cc.arc(mx, my, mr, 0, 2 * math.pi); cc.clip()
            u = min(1.0, (d - 2) / 6.0); sc_ = 1.55 - 0.95 * u                               # her, from behind, in it: smaller and smaller
            fx_, fy_ = mx - 14 + 30 * u, my + 70 - 40 * u
            cc.set_source_rgb(*n.KEY); cc.new_path(); cc.move_to(fx_ - 34 * sc_, fy_); cc.line_to(fx_ - 12 * sc_, fy_ - 52 * sc_); cc.line_to(fx_ - 16 * sc_, fy_ - 74 * sc_)
            cc.line_to(fx_ + 16 * sc_, fy_ - 74 * sc_); cc.line_to(fx_ + 12 * sc_, fy_ - 52 * sc_); cc.line_to(fx_ + 34 * sc_, fy_); cc.close_path(); cc.fill()
            for sx__ in (-1, 1):                                              # her arms, pumping
                cc.set_line_width(7 * sc_); cc.set_line_cap(1); cc.move_to(fx_ + sx__ * 16 * sc_, fy_ - 70 * sc_)
                cc.line_to(fx_ + sx__ * 30 * sc_, fy_ - (48 if (d + (sx__ > 0)) % 2 else 62) * sc_); cc.stroke()
            cc.set_source_rgb(0.86, 0.86, 0.88); cc.new_path(); cc.rectangle(fx_ - 22 * sc_, fy_ - 112 * sc_, 44 * sc_, 44 * sc_); cc.fill()   # her hair
            cc.set_source_rgb(*INK); cc.set_line_width(2); cc.rectangle(fx_ - 22 * sc_, fy_ - 112 * sc_, 44 * sc_, 44 * sc_); cc.stroke()
            cc.move_to(fx_, fy_ - 112 * sc_); cc.line_to(fx_, fy_ - 76 * sc_); cc.stroke()
            cc.restore()
            if 3 <= d < 7:                                                # her shadow, running, across the stones
                sx_ = -160 + 190 * (d - 3)
                cc.set_source_rgba(0.02, 0.02, 0.03, 0.62)
                cc.new_path(); cc.move_to(sx_, 960); cc.line_to(sx_ + 110, 720); cc.line_to(sx_ + 190, 720); cc.line_to(sx_ + 250, 960); cc.close_path(); cc.fill()
                cc.new_path(); cc.arc(sx_ + 150, 676, 58, 0, 2 * math.pi); cc.fill()
            if d >= 5:
                n.footprints(k, 330, 760, 4.2, n=1, step=30)
            if d >= 7:
                n.footprints(k, 440, 640, 3.6, n=1, step=30)
        return
    if tl < 2 / 12.0:                                                   # the compact, falling
        n.compact2(k, 230, 330 + 1500 * tl, 3.6, 0.9 + tl * 6)
    else:
        g = ease((tl - 2 / 12.0) / 0.34)
        cc.save(); cc.translate(220, 640); cc.scale(0.35 + 0.65 * g, 0.35 + 0.65 * g); cc.translate(-220, -640)
        n.powder_puff(k, 220, 640, 5.0)
        cc.restore()
    if 4 / 12.0 <= tl < 6 / 12.0:
        if not V30[0]:                                                  # v30: the leg is out (cold test v29, 3/3 "a leg with no body")
            b.red_shoe(k, 330, 610, 3.6)
    elif 6 / 12.0 <= tl < 8 / 12.0:
        if not V30[0]:
            b.red_shoe(k, 460, 470, 3.2)
        n.footprints(k, 300, 700, 4.2, n=1, step=30)
    elif tl >= 8 / 12.0:
        n.footprints(k, 300, 700, 4.2, n=1, step=30)
        n.footprints(k, 420, 560, 3.6, n=1, step=30)


def cloth(k, x, y, s, ang):
    cc = k.c
    cc.save(); cc.translate(x, y); cc.rotate(ang); cc.scale(s, s)
    n._cloth(cc, [("M", -5, 0), ("C", -2, -3, 2, -3, 5, 0), ("C", 20, 14, 26, 50, 20, 88), ("C", 18, 104, 12, 114, 8, 122),
                  ("C", 4, 110, 0, 100, -4, 104), ("C", -8, 110, -12, 116, -16, 124), ("C", -22, 104, -26, 50, -5, 0)])
    n._curve(cc, (4, 6, 16, 22, 20, 56, 14, 96), n.WRAP_PALE, 1.6)
    cc.restore()


def runner(k, x, y, s, tl, face="caught", look=(-0.9, 0.0)):
    """Her run: a loop of eight drawings, two thirds of a second. She is highest between her steps."""
    u = (tl * 1.5) % 1.0
    up = 6 * (0.5 + 0.5 * math.cos(4 * math.pi * (u + 0.03)))
    w = math.sin(4 * math.pi * u)
    return n.star(k, x, y - up * s, s, "g_run3", face, look, lean=7 + w, lag=(-14 + 3 * w, -4), wrap=False, run=True, phase=float(u))


def m2_6(k, tl, dur=3.5):
    cc = k.c
    street(k, 580, (440, 140), tl)
    cc.set_source_rgba(1, 1, 1, 0.26); cc.save(); cc.translate(150, 690); cc.scale(190, 96); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    p = tl / dur
    x, y, s = lerp(250, 470, p), lerp(720, 640, p), lerp(1.42, 1.0, p)
    for i in range(int(tl * 1.5 + 1e-6) + 1):                           # her prints: one where her near foot lands
        q = (i / 1.5) / dur
        n.footprints(k, lerp(250, 470, q) - 46, lerp(720, 640, q) + 6 + (7 if i % 2 else -7), lerp(2.2, 1.5, q), n=1, step=30)
    runner(k, x, y, s, tl)
    # the wrap: off her shoulders, down to the stones, and it lies there. v9: no hand picks it up; the detective has it later
    if tl < 0.75:                                                       # all of this stays above the narration's line
        f = tl / 0.75
        n.wrap_flying(k, lerp(250, 124, f), lerp(470, 716, f * f), 1.5, lerp(0.5, 0.05, f))
    else:
        n.wrap_flying(k, 124, 722, 1.5, 0.05)
    rain(k, tl + 7)


# ---------------------------------------------------------------- beat 03: the sweeper and the detective
def prints(k, x, y, s, step, which):
    """Her prints, each one separately, so that they can be swept away one at a time."""
    for i in which:
        n.footprints(k, x + i * step * s, y - (14 * s if i % 2 else 0), s, n=1, step=step)


def m3_1(k, tl):
    street(k, 600, (420, 140), tl)
    d12 = int(round(tl * 12))
    xs = -130 + 800 * max(0.0, tl - 2 / 12.0)                            # the red dress, through the frame
    prints(k, 250, 840, 2.6, 30, [i for i in range(3) if xs > 300 + i * 78])
    if xs < 700:
        look = (max(-1.0, min(1.0, (xs - 170) / 260.0)), 0.1)             # her head goes with it
    else:
        look = (1.0, 0.1) if tl < 17 / 12.0 else (0.6, 0.9)               # then down, to what it left
    with breath(k, 170, 930, tl), lids(n.pn.ps.SKIN, d12 in (1, 19), line=True):
        n.sweeper(k, 170, 930, 2.2, "lean", "neutral", look)
    if tl >= 2 / 12.0 and xs < 700:                                      # v4: in front of the sweeper
        runner(k, xs, 940, 2.1, tl)
    rain(k, tl + 11)


# the broom's head and how far she leans, drawing by drawing: lifted, reached out, planted, pulled across, nudged, settled
SWEEP = {10: ((474, 868), 2), 11: ((530, 888), 4), 12: ((522, 904), 4), 13: ((452, 905), 2), 14: ((368, 906), -1), 15: ((300, 908), -3),
         16: ((284, 908), -3), 17: ((294, 907), -1)}


def m3_2(k, tl, dur=2.5):
    cc = k.c
    street(k, 540, (300, 130), tl)
    p = tl / dur
    d12 = int(round(tl * 12))
    u = (d12 / 10.0) % 1.0                                               # he comes on, heavily, a step every five drawings
    sd = lerp(0.90, 1.22, p)
    la, lb = 10 * max(0.0, math.sin(2 * math.pi * u)), 10 * max(0.0, -math.sin(2 * math.pi * u))
    don(k, lerp(486, 412, p) + 2.5 * sd * math.cos(2 * math.pi * u), lerp(670, 712, p) + 3 * sd * max(0.0, math.cos(4 * math.pi * u)), sd,
        (0.6, 0.8), ((-14, la, 0), (14, lb, 0)), lean=1.5 * math.cos(2 * math.pi * u), cloth_ang=0.10 * math.sin(2 * math.pi * u), shut=d12 in (7, 23))
    left = 3 if d12 < 13 else 2 if d12 < 14 else 1 if d12 < 15 else 0
    prints(k, 300, 900, 2.6, 30, range(left))
    n.dustpan(k, 262 - (3 if d12 == 16 else 0), 922, 2.0, full=d12 >= 15)
    if d12 in (15, 16, 17):                                              # her powder, rising out of the pan
        q = (d12 - 15) / 3.0
        for i, (dx, r) in enumerate(((-14, 13), (6, 16), (22, 11))):
            cc.set_source_rgba(1, 1, 1, 0.5 * (1 - q)); cc.new_path(); cc.arc(262 + dx, 896 - 26 * q - i * 5, r * (0.7 + 0.6 * q), 0, 2 * math.pi); cc.fill()
    if d12 in SWEEP:
        head, lean = SWEEP[d12]
        a = math.radians(lean)
        dx, dy = head[0] - 190, head[1] - 930                            # the broom's head, taken back into her leaning space
        hx, hy = 190 + dx * math.cos(a) + dy * math.sin(a), 930 - dx * math.sin(a) + dy * math.cos(a)
        cc.save(); cc.translate(190, 930); cc.rotate(a); cc.translate(-190, -930)
        n.sweeper(k, 190, 930, 2.25, "sweep", "neutral", (0.9, 0.7) if d12 < 13 else (0.6, 0.9), head=(hx, hy))
        cc.restore()
    else:
        look = (0.6, 0.9) if d12 < 5 else (1.0, -0.2) if d12 < 10 else (0.5, 0.9) if d12 < 21 else (1.0, -0.2)
        with breath(k, 190, 930, tl), lids(n.pn.ps.SKIN, d12 in (3, 25), line=True):
            n.sweeper(k, 190, 930, 2.25, "lean", "neutral", look)
    rain(k, tl + 13)


def glass_prints(k, x, y, r, off):
    """What his glass shows, as noir2_cast.glass_view draws it, but the stones slide under the glass: off is how far the
    trail still has to come (in pixels). A print, a print, then the bristles."""
    c = k.c
    g = r / 42.0
    c.save(); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.clip()
    c.set_source_rgb(0.46, 0.46, 0.49); c.paint()
    c.set_source_rgb(0.38, 0.38, 0.41); c.set_line_width(1.2 * g)
    for i in range(-3, 4):
        c.move_to(x - r, y + i * 15 * g); c.line_to(x + r, y + i * 15 * g); c.stroke()
    x0 = x + off
    for i, (px, py) in enumerate(((-30, 9), (-13, -8), (4, 9))):
        c.save(); c.translate(x0 + px * g, y + py * g); c.rotate(-0.12); c.scale(g, g)
        c.set_source_rgb(1, 1, 1)
        c.new_path(); c.move_to(-2, -5.5); c.curve_to(8, -8, 15, -3, 15, 0); c.curve_to(15, 3, 8, 8, -2, 5.5); c.close_path(); c.fill()
        c.new_path(); c.arc(-8.5, 0, 3.0, 0, 2 * math.pi); c.fill()
        c.restore()
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(5 * g); c.set_line_cap(1)
    c.move_to(x0 + 10 * g, y + 4 * g); c.line_to(x0 + 19 * g, y - 3 * g); c.stroke()
    c.save(); c.translate(x0 + 27 * g, y + 2 * g); c.rotate(0.22); c.scale(g, g)
    c.set_source_rgb(*INK); c.set_line_width(8); c.move_to(4, -12); c.line_to(22, -60); c.stroke()
    c.set_source_rgb(0.72, 0.56, 0.36); c.set_line_width(4.6); c.move_to(4, -12); c.line_to(22, -60); c.stroke()
    rect(k, -9, -22, 13, 44, (0.50, 0.36, 0.22), 720, shadow=False, lw=1.8)
    cut(k, [(-9, -22), (-9, 22), (-27, 27), (-27, -27)], (0.86, 0.74, 0.46), shadow=False, lw=1.8)
    c.set_source_rgb(0.50, 0.40, 0.20); c.set_line_width(1.3)
    for i in range(-3, 4):
        c.move_to(-10, i * 6); c.line_to(-26, i * 7.4); c.stroke()
    c.restore()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(max(5.0, r * 0.11)); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*n.SILVER); c.set_line_width(max(2.2, r * 0.045)); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(max(2.0, r * 0.05)); c.set_line_cap(1)
    c.new_path(); c.arc(x, y, r - r * 0.16, math.pi * 1.10, math.pi * 1.36); c.stroke()


def m3_3(k, tl):
    cc = k.c
    cc.set_source_rgb(0.09, 0.09, 0.10); cc.paint()
    f = ease(tl / 0.58)
    gx = lerp(214, 250, f)                                               # the glass itself moves a little along the trail
    n.glass_handle(k, gx, 440, 220, 0.6)
    glass_prints(k, gx, 440, 220, lerp(300, 0, f))


def m3_4(k, tl):
    d12 = int(round(tl * 12))
    if d12 < 9:                                                          # v17: from below: he straightens up over her
        cc = k.c
        street(k, 960, (430, 150), tl)
        cc.set_source_rgba(0, 0, 0, 0.35); cc.paint()
        look = (-0.4, 0.95) if d12 < 6 else (-1.0, 0.3) if d12 < 8 else (1.0, 0.1)
        don(k, 300, 1330 + (30 if d12 < 2 else 0), 3.3, look, STAND, lean=-6 if d12 < 2 else 0, shut=d12 == 4)
        rain(k, tl + 17)
        return
    street(k, 580, (270, 130), tl)
    w = max(0, d12 - 10)                                                 # drawings into his walk (v16: from 10)
    stp = 2 * 28 * 1.75 / 5.0                                            # what a planted foot covers in a drawing: he does not slide
    xd = 410 - stp * w
    if d12 < 2:                                                          # v16: the look after the sweep, shorter
        dlook, dlean = (-0.3, 0.9), -7                                   # bent over the pan
    elif d12 < 6:
        dlook, dlean = (-0.8, -0.3), 0                                   # he straightens up and looks at her
    elif d12 < 8:
        dlook, dlean = (-1.0, 0.3), 0                                    # left
    elif d12 < 10:
        dlook, dlean = (1.0, 0.1), 0                                     # right
    else:
        dlook, dlean = (-1.0, 0.1), -4                                   # and off, the wrong way, leaning into it
    plook = (1.0, 0.0) if d12 < 3 else (0.2, -1.0) if d12 < 12 else (max(-1.0, min(1.0, (xd - 150) / 200.0)), 0.0)

    def him():
        if w > 0:                                                        # v18: his back, walking away up the street
            u = w / 10.0
            (fa, la), (fb, lb) = stride(u, 10.0, 12.0), stride(u + 0.5, 10.0, 12.0)
            sc = 1.75 - 0.11 * w                                        # v19: clearly away, up the street
            n.detective_back(k, 400 - 14 * w, 930 - 26 * w - 4 * max(0.0, math.cos(4 * math.pi * u)), sc,
                             steps=((-14 + fa, la), (14 + fb, lb)), wrap=True, wrap_big=True, wrap_side=1,
                             wrap_swing=0.25 * math.sin(2 * math.pi * u))       # v20: in his right hand, swinging
        else:
            with breath(k, 410, 930, tl, on=d12 >= 5):
                don(k, 410, 930, 1.75, dlook, STAND, lean=dlean, shut=d12 == 4)
    if w > 0:                                                            # he passes behind her
        him()
    with breath(k, 150, 930, tl + 0.9), lids(n.pn.ps.SKIN, d12 in (3, 22, 41), line=True):
        n.sweeper(k, 150, 930, 2.0, "lean", "neutral", plook)
    n.dustpan(k, 280, 900, 2.0, full=True)
    if w <= 0:
        him()
    rain(k, tl + 17)


# ---------------------------------------------------------------- beat 04: the door
def door_set(k, tl, floor=760):
    """on2_board.bar_door, with the rain left to fall."""
    cc = k.c
    street(k, floor, None, tl)
    cc.set_source_rgb(0.72, 0.71, 0.66); cc.rectangle(300, 110, 300, floor - 110); cc.fill()
    cc.set_source_rgb(*INK); cc.set_line_width(5); cc.rectangle(300, 110, 300, floor - 110); cc.stroke()
    bulbs(k, 292, 100, 548, 100, 22, 11, tl, 1.2, 5)                      # v12: lights over the bar's door
    cc.set_source_rgba(1, 1, 1, 0.20); cc.new_path(); cc.move_to(300, floor); cc.line_to(600, floor); cc.line_to(600, 960); cc.line_to(120, 960)
    cc.close_path(); cc.fill()


def tag(k, x, y, s, ang):
    cc = k.c
    cc.save(); cc.translate(x, y); cc.rotate(ang); cc.scale(s, s)
    cut(k, [(-44, 8), (-36, 0), (36, 0), (44, 8), (44, 36), (-44, 36)], (0.98, 0.95, 0.80), shadow=False, lw=1.8 / max(1.0, s / 1.25))
    cc.set_source_rgb(*INK); cc.select_font_face("Inter", 0, 1); cc.set_font_size(11.5)
    for i, t in enumerate(("PENDING", "APPROVAL")):
        e = cc.text_extents(t); cc.move_to(-e.width / 2 - e.x_bearing, 16 + i * 13); cc.show_text(t)
    cc.restore()


def m4_1a(k, tl):
    cc = k.c
    door_set(k, tl)
    d12 = int(round(tl * 12))
    rlook = (-0.8, -0.3) if d12 < 6 else (-0.6, 0.8) if d12 < 13 else (0.9, 0.0)      # the glove, the cup, then after her
    turn = {} if d12 < 6 else dict(head_rot=0.10, head_dx=-4) if d12 < 13 else dict(head_rot=-0.12, head_dx=6)
    if d12 in (1, 2, 15, 16):                                                # v4: its head twitches while it waits
        turn = dict(head_rot=turn.get("head_rot", 0.0) + (0.035 if d12 % 2 else -0.035), head_dx=turn.get("head_dx", 0))
    o = n.rn.robot_noir(k, 340, 1020, 2.2, "stand", "blink" if d12 in (0, 12) else "eager", rlook, cap=False, **turn)
    (lx, ly), (rx, ry) = o["hands"]
    hx, hy = o["head"]
    n.charge_card(k, 336, hy + 150 * 2.2, 2.0, 0.05)                         # v9
    if d12 == 10:                                                            # the coin goes into the cup: drawn behind its rim
        b.coin(k, lx + 4, ly - 100, 34)
    n.cup(k, lx, ly - 34 + (6 if d12 == 11 else 0), 3.6)
    ellipse(k, lx, ly, 18, 18, (0.20, 0.20, 0.22), 23, shadow=False, lw=3)
    if d12 < 2 or d12 >= 13:
        g = None
    elif d12 < 10:
        g = 1 - ease((d12 - 1) / 3.0)                                        # in, from the left
    else:
        g = ease((d12 - 9) / 3.0)                                            # and gone again: she has not slowed
    if g is not None and V33[0]:                                            # v33: a forearm from the edge, the coin in her fingers, then let go
        import on2_hands as oh
        ox, oy = -230 * g, -150 * g
        opened = d12 >= 6
        oh.insert(k, (-80 + ox, 250 + oy), (96 + ox, 388 + oy), "palm" if opened else "grab", 96,
                  under=None if opened else (lambda: b.coin(k, 190 + ox, 470 + oy, 34)))
    elif g is not None:
        ox, oy = -230 * g, -150 * g
        n._seg(k, -60 + ox, 300 + oy, 110 + ox, 420 + oy, 96, 84, n.KEY, 3.2)
        ellipse(k, 118 + ox, 428 + oy, 48, 44, n.KEY, 336, shadow=False, lw=3.2)
        opened = d12 >= 6
        for i, a in enumerate((0.25, 0.65, 1.05, 1.45) if opened else (0.95, 1.12, 1.29, 1.46)):
            ln = 78 if opened else 64
            n._seg(k, 118 + ox + math.cos(a) * 34, 428 + oy + math.sin(a) * 34, 118 + ox + math.cos(a) * ln, 428 + oy + math.sin(a) * ln, 20, 16, n.KEY, 2.6)
        if not opened:                                                       # the coin, still in her fingers
            b.coin(k, 142 + ox, 500 + oy, 34)
    if 6 <= d12 < 10:                                                        # it falls
        f = (d12 - 6) / 4.0
        cx, cy = lerp(142, lx + 4, f), lerp(500, ly - 100, f * f)
        b.coin(k, cx, cy, 34)
        cc.set_source_rgb(1, 1, 1); cc.set_line_width(4); cc.set_line_cap(1)
        for dx in (-22, 0, 22):
            cc.move_to(cx + dx, cy - 50); cc.line_to(cx + dx, cy - (100 if dx else 120)); cc.stroke()
    rain(k, tl + 19)


def m4_1b(k, tl):
    cc = k.c
    door_set(k, tl)
    d12 = int(round(tl * 12))
    e = d12 - 6                                                              # drawings since the arm came out
    if e < 0:                                                                # v4: she comes to the door in two steps
        sw = (1.0, 0.4, -0.4, -1.0, -0.4, 0.4)[d12]
        n.so.POSES["_g_walk"] = n.so._ik(-1, -38 + 13 * sw, n.BT + 112) + n.so._ik(1, 38 + 13 * sw, n.BT + 112)
        n.star(k, 300 + d12 * 28, 1010 + (0, -6, -2, 0, -6, -2)[d12], 2.2, "_g_walk", "interested", (0.6, 0.0), lean=2.0 * sw, lag=(-6, 0),
               wrap=False, bag=False)
        o = n.rn.robot_noir(k, 56, 800, 1.18, "stand", "blink" if d12 == 2 else "eager", (0.9, 0.0), cap=False)
        (lx, ly), _ = o["hands"]
        n.charge_card(k, 56 - 2 * 1.18, o["head"][1] + 150 * 1.18, 1.18 * 0.9, 0.05, 920)
        n.cup(k, lx, ly - 16 * 1.18, 1.18 * 1.5, 921)
        ellipse(k, lx, ly, 8 * 1.18, 8 * 1.18, (0.20, 0.20, 0.22), 923, shadow=False, lw=1.6 * 1.18)
    else:
        n.star(k, 468, 1010, 2.2, "g_down", "appraise", (-1.0, 0.5), lean=-3 if e < 2 else 0, wrap=False, bag=False)
        o = n.coin_steps(k, 56, 800, 1.18, 2, lines=e < 2, sign="charge")                   # the arm is out, across her path
        if e >= 3:                                                           # her coin, back, and the tag swinging under it
            bx, by = o["claw"]
            b.coin(k, bx + 14, by, 30)
            sw = 0.22 * math.cos((e - 3) * 1.6) * math.exp(-(e - 3) / 3.5)
            cc.set_source_rgb(*INK); cc.set_line_width(2.4); cc.move_to(bx + 14, by + 30); cc.line_to(bx + 18 - sw * 22, by + 52); cc.stroke()
            tag(k, bx + 18 - sw * 22, by + 52, 1.25, 0.05 + sw)
    rain(k, tl + 21)


def m4_2(k, tl):
    cc = k.c
    cc.set_source_rgb(0.12, 0.12, 0.14); cc.paint()
    b.pool(cc, 300, 300, 460, 0.26)
    d12 = int(round(tl * 12))
    taken = d12 >= 10
    spread = 86 if not taken else 40                                         # the claw, and it closes on nothing
    for col, w in ((INK, 62), (n.SILVER, 44)):
        cc.set_source_rgb(*col); cc.set_line_width(w); cc.set_line_cap(1); cc.move_to(-40, 330); cc.line_to(110, 330); cc.stroke()
    for sy in (-1, 1):
        cc.set_source_rgb(*INK); cc.set_line_width(26); cc.move_to(110, 330); cc.line_to(180, 330 + sy * spread); cc.stroke()
        cc.set_source_rgb(*n.SILVER); cc.set_line_width(15); cc.move_to(110, 330); cc.line_to(180, 330 + sy * spread); cc.stroke()
    if d12 < 6:
        gx, gy = (240, -150) if d12 < 5 else (110, -70)                      # her glove comes in from the door's side
        show = d12 >= 5
    elif d12 < 10:
        gx, gy, show = 0, 0, True                                            # a finger and thumb on the coin
    else:
        f = (d12 - 9) / 2.0
        gx, gy, show = 330 * f, -210 * f, d12 < 12                           # and it is gone, sharply
    ox, oy = (gx, gy) if taken else (0, 0)
    if not taken or show:
        b.coin(k, 250 + ox, 330 + oy, 92)
        sw = 0.10 * math.cos(d12 * 1.5) * math.exp(-d12 / 4.0) + (0.5 if taken else 0.0)
        cc.set_source_rgb(*INK); cc.set_line_width(4.5); cc.move_to(250 + ox, 424 + oy); cc.line_to(256 + ox - sw * 40, 462 + oy); cc.stroke()
        tag(k, 256 + ox - sw * 40, 462 + oy, 3.2, 0.05 + sw)
    if show and V34[0]:                                                  # v34: a forearm from the edge, her fingers closing on the coin
        import on2_hands as oh
        oh.insert(k, (660 + gx, 120 + gy), (452 + gx, 236 + gy), "grab", 120, arm=1)
    elif show:
        n._seg(k, 600 + gx, 150 + gy, 420 + gx, 250 + gy, 100, 88, n.KEY, 3.4)
        ellipse(k, 410 + gx, 256 + gy, 50, 46, n.KEY, 336, shadow=False, lw=3.2)
        for (fx, fy) in ((346, 262), (352, 312)):
            ellipse(k, fx + gx, fy + gy, 40, 17, n.KEY, 337 + fy, shadow=False, lw=3)
    if taken and d12 < 12:                                                   # how fast
        cc.set_source_rgb(1, 1, 1); cc.set_line_width(5); cc.set_line_cap(1)
        for dy in (-40, 0, 44):
            cc.move_to(250, 330 + dy); cc.line_to(250 + gx * 0.7, 330 + dy + gy * 0.7); cc.stroke()


SHOTS = {"1.1": (m1_1, 0, lambda cc: b.shade(cc, -1, 0.45)), "1.2": (m1_2, 0, lambda cc: b.shade(cc, -1, 0.50)),
         "1.2b": (m1_2b, 0, lambda cc: b.shade(cc, 1, 0.40)), "2.1": (m2_1, 0, None),
         "2.2": (m2_2, 0, None), "2.3a": (m2_3a, 0, lambda cc: b.shade(cc, -1, 0.55)), "2.3b": (m2_3b, 0, lambda cc: b.shade(cc, -1, 0.55)), "2.4": (m2_4, -0.07, None), "2.5": (m2_5, 0, None),
         "2.6": (m2_6, 0, lambda cc: b.shade(cc, -1, 0.35)),
         "3.1": (m3_1, 0, lambda cc: b.shade(cc, 1, 0.40)), "3.2": (m3_2, 0, lambda cc: b.shade(cc, -1, 0.30)), "3.3": (m3_3, 0, None),
         "3.4": (m3_4, 0, None), "4.1a": (m4_1a, 0, lambda cc: b.shade(cc, -1, 0.40)), "4.1b": (m4_1b, 0, lambda cc: b.shade(cc, -1, 0.40)),
         "4.2": (m4_2, 0, None)}


PLAN = PLAN + b5.PLAN + b68.PLAN
SHOTS.update(b5.SHOTS)
SHOTS.update(b68.SHOTS)
b5.use(sys.modules[__name__])
b68.use(sys.modules[__name__])


def timing(kind):
    rows_, total_ = _timing(kind)
    timing.rows = rows_
    return rows_, total_


def _timing(kind):
    meta = json.load(open(snd.TAKES + "/takes.json"))
    rows, t = [], 0.0
    for item in PLAN:
        if OPEN28[0] and item[0] in PLAN28:                              # v28: the opening re-timed
            item = PLAN28[item[0]]
        shot, planned, key, *more = item
        lead = LEADS28.get(shot, LEAD) if OPEN28[0] else LEAD
        tail = more[0] if more else TAIL                                  # a line that is cut off has no air after it
        take = meta["%s_%s" % (key, kind) if key and key[0] == "n" else key] if key else None    # the narration has kinds; the others have one take
        need = (lead + take["len"] + tail) if key else 0.0
        d = math.ceil(max(planned, need) * 12 - 1e-6) / 12.0
        row = {"shot": shot, "start": round(t, 4), "len": round(d, 4)}
        if key:
            row["line"] = {"who": "N" if key[0] == "n" else take["who"], "key": key, "text": take["text"], "t0": round(t + lead, 3),
                           "t1": round(t + lead + take["len"], 3)}
        rows.append(row); t += d
    return rows, t


CAP = (30, 38)                                             # v21: the narration's size and line height (v20: 23, 30)


LOOK3 = [True]                                             # v25 (False: v24's look)
b.OFFICE_LIT[0] = True                                     # v26: the office readable, the UptimeZ mark on its wall: the first Noir's light (blinds, side light), lighter faces, typewriter cards
SIDE = {"1.2": (False, 0.40), "5.2": (True, 0.20), "5.3": (True, 0.22), "5.9": (True, 0.45), "6.1": (True, 0.22), "7.1": (True, 0.35),
        "7.2a": (True, 0.30), "7.2b": (True, 0.30)}
KEY = {"5.2": (170, 640, 300, 0.22), "5.3": (410, 470, 260, 0.20), "6.1": (404, 500, 260, 0.16)}   # v26: lit spots: the money, the pour, the logo
NO_BLINDS = {"6.1", "6.2", "6.2r", "6.4", "6.5", "6.6", "6.7", "6.7a"}    # v26: the office has its own bars of light                                # shot -> (light from the left?, how dark the far side): her face on the lit side


def _blinds(k, a=0.34):
    import on_set as ons
    ons.blinds(k.c, -40, -40, W + 80, H + 80, -0.32, 30, 12, a)


def caption_card(cc, text):
    """v25: the first Noir's narration: typewriter on cream cards with a black edge, at the top, two rows at most."""
    cc.select_font_face("Special Elite", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); cc.set_font_size(CAP[0])
    rows, line = [], ""
    for wd in text.split():
        trial = (line + " " + wd).strip()
        if cc.text_extents(trial).x_advance > SAFE[2] - SAFE[0] - 40 and line:
            rows.append(line); line = wd
        else:
            line = trial
    rows.append(line)
    assert len(rows) <= 2, rows
    y = SAFE[1] + 4
    for ln in rows:
        e = cc.text_extents(ln); w = e.x_advance + 24
        cc.set_source_rgba(0, 0, 0, 0.45); cc.rectangle(SAFE[0] + 4, y + 4, w, 42); cc.fill()
        cc.set_source_rgb(0.93, 0.90, 0.82); cc.rectangle(SAFE[0], y, w, 42); cc.fill()
        cc.set_source_rgb(0.06, 0.06, 0.07); cc.set_line_width(2.6); cc.rectangle(SAFE[0], y, w, 42); cc.stroke()
        cc.move_to(SAFE[0] + 12, y + 30); cc.show_text(ln); y += 48


def caption(cc, text):
    if LOOK3[0]:
        return caption_card(cc, text)
    cc.select_font_face("Inter", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD); cc.set_font_size(CAP[0])   # v21: 30 px
    rows, line = [], ""
    for wd in text.split():
        trial = (line + " " + wd).strip()
        if cc.text_extents(trial).x_advance > SAFE[2] - SAFE[0] - 36 and line:
            rows.append(line); line = wd
        else:
            line = trial
    rows.append(line)
    assert len(rows) <= 2, rows                                          # v21: two rows at most
    lh = CAP[1]
    hh = len(rows) * lh + 22; y0 = SAFE[1]                               # v10: at the top, under the app's bar
    for j, ln in enumerate(rows):                                         # v14: no band; a dark edge and a shadow instead
        e = cc.text_extents(ln); x_, y_ = (W - e.x_advance) / 2, y0 + 33 + 7 * (lh > 30) + j * lh
        cc.move_to(x_ + 2, y_ + 3); cc.text_path(ln); cc.set_source_rgba(0, 0, 0, 0.65); cc.fill()
        cc.move_to(x_, y_); cc.text_path(ln); cc.set_line_join(1); cc.set_line_width(5); cc.set_source_rgb(0.03, 0.03, 0.04); cc.stroke()
        cc.move_to(x_, y_); cc.set_source_rgb(1, 1, 1); cc.show_text(ln)


CLOCK = {"1": 55, "2": 55, "3": 56, "4": 57, "5": 58, "6": 59, "7": 59, "8": 60}


def frame(row, tl, t):
    n.NO_BAG[0] = n.HIDE2[0] = n.BACK2[0] = V31[0]
    n.HIDE3[0] = n.BACK3[0] = rv.RIM2[0] = V31[0] and V32[0]
    n.HAND3[0] = V31[0] and V32[0] and V33[0]
    import hands_ps as _hp
    import on2_hands as _oh
    _hp.GLOVE[0] = _oh.GLOVE_CFG if (n.HAND3[0] and V34[0]) else None
    n.FUR[0] = n.ARMS2[0] = n.HAND3[0] and V34[0] and V35[0]
    del n.ARMS2[1:]
    if rv.RAVEN[0] and not END.get("on") and row["shot"] == "1.1" and int(round(tl * 12)) >= 5:    # v29: 1.2's start is rounded up past
        row, tl = [r for r in timing.rows if r["shot"] == "1.2"][0], 0.0                # its drawing; the wipe is on 1.2 already
    fn, tilt, post = SHOTS[row["shot"]]
    NOW["min"], NOW["sec"] = CLOCK[row["shot"][0]], None                  # v12: the clocks
    NOW["shot"] = row["shot"]                                             # v20: which shot is being drawn
    if row["shot"] in ("7.1", "7.1r", "7.1c", "7.2a", "7.2b", "7.3"):                     # the last seconds, run out to the pop
        tpop = [r for r in timing.rows if r["shot"] == "7.3"][0]["start"] + 2 / 12.0
        left = tpop - t
        NOW["sec"] = 60 - max(0.0, math.ceil(left - 1e-6))
        if left <= 1e-6:
            NOW["min"], NOW["sec"] = 60, 0
    sf_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cc = cairo.Context(sf_); cc.set_source_rgb(*b.NIGHT); cc.paint()
    if tilt:
        cc.translate(W / 2, H / 2); cc.rotate(tilt); cc.scale(1.10, 1.10); cc.translate(-W / 2, -H / 2)
    k = Ctx(cc, int(round(t * 12)) % 3)
    saved = None
    if LOOK3[0] and row["shot"] not in b68.COLOUR:          # v25: the blinds' shadow on the rooms' walls, under the people
        saved = (b5.room, b.office, b.lit_wall)
        r0, o0, w0 = saved
        b5.room = lambda k_, *a, **kw: (r0(k_, *a, **kw), _blinds(k_, 0.27 if (V38[0] and row["shot"] in ("5.1", "5.2")) else 0.34))[0]
        b.office = lambda k_, *a, **kw: (o0(k_, *a, **kw), None if row["shot"] in NO_BLINDS else _blinds(k_))[0]
        b.lit_wall = lambda k_, *a, **kw: (w0(k_, *a, **kw), _blinds(k_))[0]
        eng.TONE = "v3"
    try:
        if row["shot"] in ("2.1", "2.6", "3.2") or row["shot"] in b5.SHOTS or row["shot"] in b68.SHOTS:
            fn(k, tl, row["len"])
        else:
            fn(k, tl)
    finally:
        if saved:
            b5.room, b.office, b.lit_wall = saved
    if row["shot"] in b68.COLOUR:                                        # awake: colour, and no shade
        cc = cairo.Context(sf_)
    else:
        eng.accent_pass(sf_, n.ACCENTS2)
        cc = cairo.Context(sf_)
        if post:
            post(cc)
        b.vignette(cc)
        if LOOK3[0]:                                          # v25: a side light, and true black at the edges
            fl, am = SIDE.get(row["shot"], (True, 0.38))
            eng.side_light(cc, 0, 0, W, H, from_left=fl, amount=am)
            if row["shot"] in KEY:                                        # v26: what the shot is about, in its own light
                import on_set as ons
                ons.key_light(cc, *KEY[row["shot"]])
            g = cairo.RadialGradient(W / 2, H * 0.42, H * 0.30, W / 2, H * 0.42, H * 0.80)
            g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, 0.40); cc.set_source(g); cc.paint()
        eng.TONE = "v2"
    if rv.RAVEN[0] and not END.get("plain"):                              # v29: the raven, after the grade (on2_raven.draw3)
        dd = int(round(tl * 12))
        key = None
        if END.get("on"):
            key = "coil" if END.get("last") else "perch"
        elif row["shot"] == "1.1" and dd < 5:
            key = (rv.KEYS4 if V31[0] else rv.KEYS3)[dd]
        elif row["shot"] == "1.2" and dd < 2:
            key = rv.KEYS3[5 + dd]
        if key:
            behind = None
            if V30[0] and not V31[0] and key in ("strike", "wipe"):                     # v30: her red through the wing's gap
                END["plain"] = True
                try:
                    behind = frame([r for r in timing.rows if r["shot"] == "1.2"][0], 0.0, 0.0)
                finally:
                    END.pop("plain", None)
            sf_ = rv.draw3(sf_, key, behind)
            cc = cairo.Context(sf_)
    ln = row.get("line")
    if not (ln and ln["t0"] - 0.05 <= t <= ln["t1"] + 0.30):             # v15: her line may run on from the set-up before
        for r_ in timing.rows:
            l_ = r_.get("line")
            if l_ and l_["who"] == "N" and l_["t0"] - 0.05 <= t <= l_["t1"] + 0.30:
                ln = l_
    if ln and ln["t0"] - 0.05 <= t <= ln["t1"] + 0.30:
        if ln["who"] == "N":
            caption(cc, ln["text"])
        else:                                                            # spoken: a bubble, its tail beside the mouth
            if row["shot"] in b68.SHOTS:
                tip, box = b68.TIP[row["shot"]]
                b68.say(cc, ln["text"] + ("\u2014" if ln["key"] in ("c1", "c1b") else ""), box, tip)
            else:
                tip, box = b5.TIP[row["shot"]]
                b5.bubble(cc, ln["text"], box, tip)
    return sf_


class _Hi:
    """Release: every 540x960 surface is made at 1080x1920 with a device scale of 2 (as on_film.py does), so lines,
    text and the noir pass are native 1080, not an enlarged 540 picture."""
    def __init__(self, orig):
        self._orig = orig

    def __call__(self, fmt, w, h):
        if (w, h) == (W, H):
            s = self._orig(fmt, 2 * W, 2 * H); s.set_device_scale(2, 2); return s
        return self._orig(fmt, w, h)

    def __getattr__(self, a):
        return getattr(self._orig, a)


def main(kind="A2", folder="../office-noir-2", hi=False):
    """hi: the 1080 release, on2_film_<V>_1080.mp4 (not committed); otherwise the 540 motion test."""
    if hi and not isinstance(cairo.ImageSurface, _Hi):
        cairo.ImageSurface = _Hi(cairo.ImageSurface)
    SW, SH = (2 * W, 2 * H) if hi else (W, H)
    rows, total = timing(kind)
    json.dump({"kind": kind, "total": total, "shots": rows}, open("on2_motion_timing_%s.json" % V, "w"), indent=1)
    tmp = "/tmp/on2/motion"; os.makedirs(tmp, exist_ok=True)
    nfr = int(round(total * FPS))
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "%dx%d" % (SW, SH), "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                            "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/video.part.mp4"], stdin=subprocess.PIPE)
    last, buf = None, None
    for f in range(nfr):
        t = f / float(FPS)
        d12 = math.floor(t * 12 + 1e-6)                                  # which drawing: twelve a second, held
        row = [r for r in rows if r["start"] <= d12 / 12.0 + 1e-6][-1]
        if d12 != last:
            tl = d12 / 12.0 - row["start"]
            buf = bytes(frame(row, max(0.0, tl), d12 / 12.0).get_data()); last = d12
        enc.stdin.write(buf)
    enc.stdin.close(); enc.wait()
    os.replace(tmp + "/video.part.mp4", tmp + "/video.mp4")
    rr = [(r["shot"], r["start"], r["len"]) for r in rows]
    if OPEN28[0]:                                                        # v28: the opening's sound follows its new timing
        if rv.RAVEN[0]:
            sh = tuple((dr + int(round(RAVEN_HOLD * 12)), who) for dr, who in SHOTS_12_28)
            wav, spans = snd.motion_mix16(rr, total, kind, tmp + "/mix.wav", leads=LEADS28, heel_at=None, shots12=sh, raven=True, swap={"7.2b": "c1b"} if V30[0] else None)
        else:
            wav, spans = snd.motion_mix16(rr, total, kind, tmp + "/mix.wav", leads=LEADS28, heel_at=8 / 12.0, shots12=SHOTS_12_28)
    else:
        wav, spans = snd.motion_mix15(rr, total, kind, tmp + "/mix.wav")
    out = ("%s/on2_film_%s_1080.mp4" if hi else "%s/on2_motion_test_%s.mp4") % (folder, V)
    # one constant gain to about -14.5 LUFS, then the final file is measured
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    cur = float([x for x in r.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    gain = -13.5 - cur
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/video.mp4", "-i", wav, "-map", "0:v", "-map", "1:a", "-af",
                    "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % gain, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", tmp + "/out.part.mp4"], check=True)
    os.replace(tmp + "/out.part.mp4", out)
    return out, rows, total, nfr


if __name__ == "__main__":
    hi = "release" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != "release"]
    out, rows, total, nfr = main(args[0] if args else "A2", hi=hi)
    print("wrote", out, "%.2f s" % total, nfr, "frames")
