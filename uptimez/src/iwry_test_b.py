"""Motion test B for "I Will Replace You": the point -> collapse -> whisper, then "Approved." (5.6 s, silent).
Shot 9 (robot and Sofía; the robot slides away from her): the wheel clamps, the body snaps upright, the
arm snaps out at her, stern face aimed at her; it holds completely still; Sofía goes from unimpressed to
horrified. Shot 10 (robot and Don): 0.3 s of stillness, the collapse (head sinks, arms drop, tips toward
Don, looks up at him), it settles, whispers, and only then the nervous wobble returns. Shot 11 (Don):
chin up, hand on chest; eyes open, a glance at Sofía, thumbs-up, "Approved."."""
import math
import iwry_common as ic
import day1_sb_v3 as sb
import cafe_kit as ck
from iwry_common import u, state, shot, head_top, to_screen
from anim import ease, lerp, back_out

DURATION = 5.6
RAW_T = 0.0
W = ic.w


def point_state(t, tl):
    snap = u(t, 0.0, 0.17)                             # 0.17 s snap with a small overshoot
    e = min(1.0, back_out(snap, 1.6)) if snap < 1 else 1.0
    pose = W.blend("tie", "lock", e)
    return state(stage=9, r_pose=pose, r_locked=snap >= 0.6, r_face="stern" if snap >= 0.5 else "pleading",
                 r_look=(-1, 0.1), sof_face="horrified" if t >= 0.35 else "unimpressed", sof_look=(0.8, 0))


def point_bubble(k, t, out, cam):
    if 0.25 <= t < 1.85:
        hx, hy = out["robot"]["head"]
        a = to_screen((hx - 10, hy - 30), cam)
        ck.shout(k, "I WILL\nREPLACE YOU!", a, 300, 210, size=44)


def whisper_state(t, tl):
    col = ease(u(t, 2.3, 0.35))                        # collapse after 0.3 s of stillness
    pose = W.blend("lock", "lean", col)
    wob = 0.0
    if t >= 4.1:                                       # nervous wobble returns only after the line
        wob = 0.05 * math.sin((t - 4.1) * 14) * (1 - u(t, 4.1, 0.6) * 0.4)
    return state(stage=10, r_pose=pose, r_locked=col < 0.3, r_face="stern" if col < 0.3 else "timid",
                 r_look=(lerp(-1, 0.6, col), lerp(0, -0.8, col)), r_wobble=wob,
                 r_head_dx=lerp(0, 8, col), r_head_rot=lerp(0, -0.10, col),
                 r_talk=(0.5 if int(t * 8) % 2 == 0 else 0.15) if 2.8 <= t < 3.9 else 0.0,
                 don_face="neutral", don_look=(-0.8, 0))


def whisper_bubble(k, t, out, cam):
    if 2.8 <= t < 4.15:
        hx, hy = out["robot"]["head"]
        a = to_screen((hx + 20, hy - 40), cam)
        ck.whisper(k, "If that's okay, sir?", a, 250, 230, size=30)


def don_state(t, tl):
    chest = t < 4.75
    if chest:
        return state(stage=11, don_pose=(-8, 0, -30, -125), don_face="smug", don_chin=1, don_look=(0, -0.2))
    if t < 5.0:                                        # the glance at Sofía, hand still on his chest
        return state(stage=11, don_pose=(-8, 0, -30, -125), don_face="grin", don_look=(-1, 0))
    return state(stage=11, don_pose=(-8, 0, 40, 120), don_face="grin", don_look=(-0.4, 0), don_thumb=True)


def don_bubble(k, t, out, cam):
    if 5.0 <= t < 5.6:
        sb.bubble(k, "Approved.", head_top(out, "don", cam), "up", size=34, t=t, t0=5.0)


PANELS = [(0.0, 2.0, shot(9, point_state, bubbles=(point_bubble,))),
          (2.0, 4.3, shot(10, whisper_state, bubbles=(whisper_bubble,))),
          (4.3, 5.6, shot(11, don_state, bubbles=(don_bubble,)))]
