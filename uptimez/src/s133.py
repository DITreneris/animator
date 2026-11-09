"""Saved to Cloud S1v3.3 - S1v3.2 plus a killer opening:
0-0.8 s  cold open on the climax: ACHOO, files burst at the camera, PAM's private page slaps the lens
0.8-1.2 s rewind, caption "15 SECONDS EARLIER..."
then the S1v3.2 film with three freeze-frame name cards (DON, PAM, CLOUD), 1.3 s each.
New module only: drives s132's shots through a time map; s132.py and everything earlier are unchanged.
Render with engine_v.py: s133 (with the sniff tag) or s133n (ends on DON)."""
import math
import cairo
import kit
import s131
import s132
import anim
from kit import W, H, INK, rect, text, ease, clamp, lerp

COLD, REW = 0.8, 0.4
FREEZE = 1.3
CARDS = [  # (s132 time to freeze at, name, role, line)
    (1.1, "DON", "CEO", ["Has never opened a file."]),
    (3.75, "PAM", "PROJECT MANAGER", ["Backs up everything.", "Restores nothing."]),
    (4.85, "CLOUD", "STORAGE", ["Allergic to files."]),
]
END = 21.5                     # s132 end time (20.5 drops the sniff tag)
NAVY = (0x1F / 255, 0x2A / 255, 0x44 / 255)
GREEN = (0x2B / 255, 0xB6 / 255, 0x73 / 255)
RAW_T = 0.0


def duration(end=END):
    return COLD + REW + end + FREEZE * len(CARDS)


DURATION = duration()


def tmap(T):
    """New time -> ('cold'|'rew'|'play'|'freeze', s132 time, card index or None, time inside segment)."""
    if T < COLD:
        return "cold", 11.1 + T, None, T
    if T < COLD + REW:
        u = (T - COLD) / REW
        return "rew", 11.6 * (1 - u), None, T - COLD
    t = T - COLD - REW
    for i, (ft, *_rest) in enumerate(CARDS):
        if t < ft:
            return "play", t, None, 0
        if t < ft + FREEZE:
            return "freeze", ft, i, t - ft
        t -= FREEZE
    return "play", t, None, 0


def draw132(k, t, raw):
    """Draw s132 at its own time t, with its per-panel push and overlay (as engine would)."""
    s132.RAW_T = raw
    c = k.c
    for (t0, t1, fn) in s132.PANELS:
        if t0 <= t < t1:
            tq = math.floor(t * 12) / 12.0
            tl = tq - t0
            c.save()
            push = 1 + 0.03 * (tl / (t1 - t0))
            c.translate(W / 2, H / 2 + s132.shake(t))
            c.scale(push, push)
            c.translate(-W / 2, -H / 2)
            fn(k, tq, tl)
            c.restore()
            return fn.__name__, tq, tl
    return None, t, 0


def card(k, i, u):
    _, name, role, lines = CARDS[i]
    c = k.c
    slide = 1 - ease(clamp(u / 0.18))
    c.save()
    c.translate(-560 * slide, 0)
    rect(k, 20, 112, 500, 120 + 40 * len(lines), NAVY, 960)
    rect(k, 20, 112, 14, 120 + 40 * len(lines), GREEN, 961, shadow=False, outline=False)
    c.select_font_face(kit.FONT)
    c.set_font_size(58)
    c.set_source_rgb(1, 1, 1)
    c.move_to(52, 180)
    c.show_text(name)
    w = c.text_extents(name).x_advance
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(18)
    c.set_source_rgb(*GREEN)
    c.move_to(52 + w + 16, 178)
    c.show_text(role)
    c.select_font_face(kit.FONT)
    c.set_font_size(32)
    c.set_source_rgb(1, 1, 1)
    for j, ln in enumerate(lines):
        c.move_to(52, 228 + j * 40)
        c.show_text(ln)
    c.restore()


def rewind_fx(k, u):
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.12)
    c.rectangle(0, 0, W, H)
    c.fill()
    c.set_source_rgba(1, 1, 1, 0.35)
    for y in range(0, H, 9):
        c.rectangle(0, y + (int(u * 40) % 9), W, 2)
        c.fill()
    kit.sfx(k, "<<", 270, 470, 120, rot=0, fill=(1, 1, 1))


def scene(k, T, tl_unused):
    kind, t, ci, inner = tmap(T)
    raw = tmap(RAW_T)[1]
    c = k.c
    if kind == "cold":
        draw132(k, t, 11.1 + RAW_T)
        u = clamp(T / COLD)                       # PAM's page flies at the lens and slaps it
        sc = lerp(0.6, 9.0, ease(u) ** 1.6)
        c.save()
        c.translate(270, lerp(700, 480, u))
        c.scale(sc, sc)
        s131.private_file(k, 0, 0, 104, 990, rot=lerp(0.9, 0.08, u))
        c.restore()
        return
    if kind == "rew":
        draw132(k, t, t)
        rewind_fx(k, inner / REW)
        return
    name, tq, tl = draw132(k, t, raw if kind == "play" else t)
    if kind == "freeze":
        if inner < 0.07:
            c.set_source_rgba(1, 1, 1, 0.75)
            c.rectangle(0, 0, W, H)
            c.fill()
        card(k, ci, inner)
    else:
        s132.overlay(k, tq, tl, name)


def caption(k, T):
    if COLD + REW - 0.05 <= T < COLD + REW + 0.9:
        a = 1 - clamp((T - COLD - REW - 0.6) / 0.3)
        c = k.c
        c.save()
        rect(k, 95, 700, 350, 54, (1, 1, 1), 970)
        c.restore()
        text(k, "15 SECONDS EARLIER...", 270, 727, 28, INK)


def frame(k, t, tl):
    scene(k, t, tl)
    caption(k, t)


def shake(T):
    return 0      # s132's shake is applied inside draw132


PANELS = [(0.0, DURATION, frame)]


def overlay(k, t, tl, name):
    pass
