"""Silent motion test A for "Happy Compliance": the censoring (shot 8), about 5 s.
Tight on the tree, the robot and Sofía. Three slaps (0.4 s apart, a hop along the tree before each), a
cascade of flung bars onto the five ornaments it can't reach, a pause, the robot rolls to Sofía and slaps
the two ornaments in her hands (she freezes, horrified), rolls back, blinks to smug, holds on the tree."""
import math
import kit
from kit import clamp, ease, lerp, INK
import xmas_set as xs
import sofia_xmas as sx
import santa_robot as sr

DURATION = 5.0
RAW_T = 0.0
CAM = (334, 555, 1.25)
SHOULDER = (46, -150)          # robot front shoulder, local units (side=+1)
REACH = 88

ORN = []                        # tree ornament world positions (same as xs.tree returns)
for dx_, dy_, r_, ci in xs.ORNAMENTS:
    ORN.append((xs.TREE_X + dx_ * xs.TREE_S, xs.TREE_BASE + dy_ * xs.TREE_S))
SLAPS = [(7, 0.5), (1, 0.9), (3, 1.3)]                  # (ornament index, slot start): three slaps
CASCADE = [(2, 1.70), (4, 1.80), (0, 1.90), (5, 2.00), (6, 2.10)]   # flung bars: (index, launch time)
FLY = 0.17
SOF_SLAPS = [(0, 2.50), (1, 2.80)]                      # Sofía's two, slots of 0.3 s
ROBOT_HOME = 495
SOF_X = xs.POS["sofia"]


def robot_x_for(ox):
    return max(452, ox + 92)


def arm_to(rx, feet, target, s=1.0, side=-1, up=0.0):
    """Front-arm angles (a1, 0) aiming the straight arm at target (world); up = extra degrees upward."""
    tx, ty = target
    lx = (tx - rx) * side / s - SHOULDER[0]
    ly = (ty - feet) / s - SHOULDER[1]
    a1 = math.degrees(math.atan2(lx, ly)) + up
    return a1


def robot_state(t):
    """Returns robot x, lift, wobble, front arm angle, phase info."""
    x, lift, wob, arm, bar_hold, impact = ROBOT_HOME + 20, 0.0, 0.0, 20.0, False, None
    prev_x = ROBOT_HOME + 20
    for idx, t0 in SLAPS:
        ox, oy = ORN[idx]
        rx = robot_x_for(ox)
        u = t - t0
        if u < 0:
            break
        if u < 0.12:                                   # hop along the tree
            e = ease(u / 0.12)
            x, lift, wob = lerp(prev_x, rx, e), -14 * math.sin(math.pi * u / 0.12), 0.10 * math.sin(math.pi * u / 0.12)
            arm, bar_hold = 20.0, True
        elif u < 0.20:                                 # bar raised above the target
            x, arm, bar_hold = rx, arm_to(rx, xs.FEET, (ox, oy), up=35), True
        elif u < 0.32:                                 # contact
            x, arm, impact = rx, arm_to(rx, xs.FEET, (ox, oy)), (ox, oy, u - 0.20)
        else:                                          # hand away, bar stays
            x, arm = rx, lerp(arm_to(rx, xs.FEET, (ox, oy)), 30, ease((u - 0.32) / 0.08))
        prev_x = rx
    if t >= 1.70 and t < 2.30:                         # cascade: flicking bars up from where it stands
        x = robot_x_for(ORN[3][0])
        ph = int((t - 1.70) / 0.1)
        arm, bar_hold = (150 if ph % 2 == 0 else 120), False
        wob = 0.03 * (1 if ph % 2 else -1)
    if t >= 2.30:                                      # roll to Sofía
        u = clamp((t - 2.30) / 0.2)
        x = lerp(robot_x_for(ORN[3][0]), SOF_X + 108, ease(u))
        wob = -0.08 * math.sin(math.pi * u)
        arm = 20
    for i, t0 in SOF_SLAPS:
        u = t - t0
        if 0 <= u < 0.3:
            x = SOF_X + 108
            target = SOF_ORNS[i]
            if u < 0.08:
                arm, bar_hold = arm_to(x, xs.FEET, target, up=40), True
            elif u < 0.20:
                arm, impact = arm_to(x, xs.FEET, target), (target[0], target[1], u - 0.08)
            else:
                arm = lerp(arm_to(x, xs.FEET, target), 30, ease((u - 0.20) / 0.1))
    if t >= 3.10:                                      # roll home
        u = clamp((t - 3.10) / 0.35)
        x = lerp(SOF_X + 108, ROBOT_HOME, ease(u))
        wob = 0.07 * math.sin(math.pi * u)
        arm = lerp(30, 20, u)
    return x, lift, wob, arm, bar_hold, impact


SOF_ORNS = []


def sofia_orns():
    """World positions of the two ornaments in Sofía's hands (pose hold2, scale 1)."""
    import cairo
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)
    k = kit.Ctx(cairo.Context(surf), 0)
    out = sx.sofia(k, SOF_X, xs.FEET, 1.0, "hold2", "neutral")
    return out["orns"]


SOF_ORNS.extend(sofia_orns())


def impact_ticks(c, x, y, r, big=False):
    c.set_source_rgb(*INK); c.set_line_width(3 if big else 2.2); c.set_line_cap(1)
    n = 7 if big else 5
    for i in range(n):
        a = -math.pi * 0.9 + i * math.pi * 0.8 / (n - 1)
        c.move_to(x + math.cos(a) * r, y + math.sin(a) * r)
        c.line_to(x + math.cos(a) * (r + (16 if big else 11)), y + math.sin(a) * (r + (16 if big else 11)))
        c.stroke()


def frame(k, t, tl):
    c = k.c
    xs.with_cam(c, CAM)
    xs.set_dressing(k, boil=int(t * 4))
    censored = set(i for i, t0 in SLAPS if t >= t0 + 0.20)
    censored |= set(i for i, t0 in CASCADE if t >= t0 + FLY)
    xs.tree(k, censored=censored)
    # Sofía: watches the robot, freezes horrified when it comes for hers
    if t < 2.30:
        sface, slook = ("unimpressed", (0.9, 0)) if t < 1.0 else ("horrified" if t > 1.6 else "unimpressed", (0.9, -0.2))
    else:
        sface, slook = "horrified", (0.9, 0.3)
    if t > 3.6:
        sface = "furious"
    sx.sofia(k, SOF_X, xs.FEET, 1.0, "hold2", sface, look=slook, seed=73)
    for i, t0 in SOF_SLAPS:                            # bars on her ornaments: the biggest
        if t >= t0 + 0.08:
            ox, oy = SOF_ORNS[i]
            sr.censor_bar(k, ox, oy, 58, 19, rot=(0.06 if i else -0.06), seed=980 + i)
    # the robot
    x, lift, wob, arm, bar_hold, impact = robot_state(t)
    if t < 3.5:
        face, alarm = "stern", True
    elif t < 3.6:
        face, alarm = "blink", False
    else:
        face, alarm = "smug", False
    if 2.2 <= t < 2.3:
        face = "blink"
    pose = (0.04, 0, 0, (-20, 0), (arm, 0))
    out = sr.robot(k, x, xs.FEET + lift, 1.0, pose, face, side=-1, wobble=wob, alarm=alarm)
    hx, hy = out["hands"][1]
    if bar_hold:
        sr.censor_bar(k, hx - 10, hy - 8, 56, 18, rot=0.2, seed=990)
    if impact:
        ox, oy, u = impact
        big = t >= SOF_SLAPS[0][1]
        if u < 0.17:
            impact_ticks(c, ox, oy, 26 if big else 20, big)
    for i, t0 in CASCADE:                              # flung bars in flight
        u = (t - t0) / FLY
        if 0 <= u < 1:
            ox, oy = ORN[i]
            bx = lerp(hx, ox, ease(u)); by = lerp(hy, oy, ease(u)) - 40 * math.sin(math.pi * u)
            sr.censor_bar(k, bx, by, lerp(20, 40, u), lerp(7, 13, u), rot=u * 6.0, label=False, seed=995 + i)


PANELS = [(0.0, DURATION, frame)]
