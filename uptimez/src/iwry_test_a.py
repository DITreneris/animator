"""Motion test A for "I Will Replace You": the reveal -> proud robot -> Don's reaction (5.2 s, silent).
Insert: the dome lifts up and away, a clean 0.6 s hold, then one bolt slips off a bun. Robot close-up:
proud, one motivated move (it puffs up). Don close-up: lifts the greasy wrench, an oil drop lands next to
the ketchup stain, "WHAT IS THIS?!"."""
import iwry_common as ic
import day1_sb_v3 as sb
from iwry_common import u, state, shot, head_top
from anim import ease, lerp

DURATION = 5.2
RAW_T = 0.0


def insert_state(t, tl):
    return state(stage=6, robot=None, burgers=True, dome=u(t, 0.15, 0.35), slip=u(t, 1.1, 0.4))


def proud_state(t, tl):
    puff = ease(u(t, 2.55, 0.25))                     # the one motivated move: it puffs itself up
    t0, cr, dr, back, front = ic.w.POSES["serve"]
    pose = (t0 - 0.06 * puff, cr - 10 * puff, dr - 8 * puff, back, front)   # chest out, head up; arms unchanged
    return state(stage=8, r_pose=pose, r_locked=False, r_face="proud", r_look=(0.3, 0), r_tray="empty",
                 r_head_dx=lerp(0, -2, puff))


def don_state(t, tl):
    lift = u(t, 3.2, 0.25)
    pose = tuple(lerp(a, b, ease(lift)) for a, b in zip((-8, 0, 20, 0), (-8, 0, 128, 28)))
    return state(stage=7, don_pose=pose, don_face="shock" if t >= 3.3 else "neutral", don_look=(0, -0.3),
                 don_wrench=lift >= 1, oil_drop=u(t, 3.85, 0.3) if t >= 3.85 else None)


def don_bubble(k, t, out, cam):
    if 3.45 <= t < 5.2:
        sb.bubble(k, "WHAT IS THIS?!", head_top(out, "don", cam), "up", size=34, t=t, t0=3.45)


PANELS = [(0.0, 2.4, shot(6, insert_state)), (2.4, 3.2, shot(8, proud_state)),
          (3.2, 5.2, shot(7, don_state, bubbles=(don_bubble,)))]
