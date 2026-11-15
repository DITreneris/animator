"""Silent motion test B v2 for "Happy Compliance": Pam's mask (shot 10), 4.5 s. (xmas_test_b_v1.py = v1, kept.)
v2: the handoff is a moment, not a detail. Sofía lifts one of her censored ornaments up between their faces,
the camera pushes in on it, they lock eyes over it, Pam takes it at chest height; the ornament is bigger.
Then the camera pulls back for the mask: one hand pulls it up from her neck, snap, in two drawings; the stance
opens (feet apart, elbows out, chin up) and the towel lifts once and settles; her face stays flat; a blink."""
import math
import kit
from kit import clamp, ease, lerp
import anim
import xmas_set as xs
import sofia_xmas as sx
import pam_xmas as px
import santa_robot as sr
import xmas_test_b_v1 as v1

DURATION = 4.5
RAW_T = 0.0
CAM_WIDE = (415, 565, 1.5)
CAM_HAND = (430, 470, 2.0)                                # pushed in on the ornament between their faces
PAM_X, SOF_X = 490, 340
FISTS = px.POSE_FISTS
GIVE = (-8, 0, 30, 97)                                    # Sofía: ornament raised between their faces
TAKE = (0, -160, 14, -8)                                  # Pam: left hand up at chest height to take it
PULL = (0, -160, 150, 95)                                 # right hand up at her face pulling the mask
HERO = px.POSE_HERO
ORN_R = 24                                                # bigger than the tree balls (17 in v1)
T_RAISE, T_TAKE, T_SWAP, T_BACK = 0.7, 1.1, 1.35, 1.5
T_PULL, T_SNAP = 1.6, 1.78


def tw(a, b, u, over=False):
    e = anim.back_out(u) if over else ease(clamp(u))
    return tuple(lerp(p, q, e) for p, q in zip(a, b))


def cam(t):
    if t < T_RAISE:
        return CAM_WIDE
    if t < T_BACK:
        u = ease(clamp((t - T_RAISE) / 0.3))
    else:
        u = 1 - ease(clamp((t - T_BACK) / 0.25))
    return tuple(lerp(a, b, u) for a, b in zip(CAM_WIDE, CAM_HAND))


def censored_ornament(k, x, y, seed):
    sx.ornament(k, x, y, ORN_R, seed)
    sr.censor_bar(k, x, y, ORN_R * 3.0, ORN_R * 0.95, rot=0.05, seed=seed + 10)


def frame(k, t, tl):
    c = k.c
    xs.with_cam(c, cam(RAW_T if abs(RAW_T - t) < 0.2 else t))
    xs.set_dressing(k, boil=int(t * 4))
    xs.tree(k, censored=tuple(range(8)))
    # Sofía
    if t < T_RAISE:
        spose, sface, slook = "hold2", "furious", (0.9, 0)
    elif t < T_SWAP:
        spose = anim.key(tw((-8, 0, 22, -82) if False else sx.POSES["hold2"], GIVE, (t - T_RAISE) / 0.25))
        sface, slook = "knowing", (0.9, -0.2)
    else:
        spose = anim.key(tw(GIVE, (-8, 0, 8, 0), (t - T_SWAP) / 0.3))
        sface, slook = "knowing", (0.9, 0)
    out_s = sx.sofia(k, SOF_X, xs.FEET + 6, 1.0, spose, sface, look=slook, seed=73, orn="none")
    hl, hr = out_s["hands"]
    censored_ornament(k, hl[0] - 9, hl[1] + 30, 300)                    # the one she keeps
    if t < T_RAISE:
        censored_ornament(k, hr[0] + 9, hr[1] + 30, 301)
    # Pam
    stance, flare, chin, dx = 1.0, 1.0, 0.0, 0.0
    face, look = "neutral", (-0.9, 0)
    if t < T_TAKE:
        pose = FISTS
        look = (-0.9, 0) if t < T_RAISE else (-0.9, -0.3)
    elif t < T_PULL:
        pose = tw(FISTS, TAKE, (t - T_TAKE) / 0.2)
        look = (-0.9, -0.3)
    elif t < T_PULL + 0.1:
        pose = tw(TAKE, PULL, (t - T_PULL) / 0.1)
    else:
        u = (t - T_SNAP) / 0.35
        pose = tw(PULL, HERO, u, over=True) if t >= T_SNAP else PULL
        stance = lerp(1.0, px.HERO["stance"], ease(clamp(u)))
        chin = lerp(0, px.HERO["chin"], ease(clamp(u)))
        dx = 10 * ease(clamp(u))
        lift = math.sin(math.pi * clamp((t - T_SNAP) / 0.6))
        flare = lerp(1.0, px.HERO["cape_flare"], ease(clamp(u))) + 0.35 * lift
        look = (0, 0)
    if 3.4 <= t < 3.57:
        face = "squint"
    out = px.pam(k, PAM_X + dx, xs.FEET, 1.0, pose, face, look=look, mask=None, orn=False,
                 stance=stance, cape_flare=flare, chin=chin, seed=40)
    if T_RAISE <= t < T_SWAP:                                            # held up between them, in front of Pam
        censored_ornament(k, hr[0] + 4, hr[1] + 32, 301)
        kit.ellipse(k, hr[0], hr[1], 9.5, 9.5, sx.SKIN, 302, shadow=False, lw=2)
        if t >= T_TAKE + 0.1:                                            # Pam's fingers reach under it
            hx_, hy_ = out["hands"][0]
            kit.ellipse(k, hx_, hy_, 9.5, 9.5, kit.PEOPLE["PAM"]["skin"], 313, shadow=False, lw=2)
    if t >= T_SWAP:                                                      # now hers
        hx_, hy_ = out["hands"][0]
        censored_ornament(k, hx_ - 4, hy_ + 30, 301)
        kit.ellipse(k, hx_, hy_, 9.5, 9.5, kit.PEOPLE["PAM"]["skin"], 312, shadow=False, lw=2)
    # the mask
    hx, hy = out["head"]
    fy = hy + 4
    if t < T_PULL + 0.1:
        px.mask_strip(k, hx, fy, "neck")
    elif t < T_SNAP:
        c.save(); c.translate(hx, fy + 30); c.rotate(0.06); c.scale(0.95, 0.95)
        px.mask_strip(k, 0, -30, "down"); c.restore()
    else:
        bounce = -5 * math.sin(math.pi * clamp((t - T_SNAP) / 0.17))
        px.mask_strip(k, hx, fy - 7 * chin + bounce, "down")
    if T_SNAP <= t < T_SNAP + 0.12:
        c.set_source_rgb(*kit.INK); c.set_line_width(2.4); c.set_line_cap(1)
        for sx_ in (-1, 1):
            c.move_to(hx + sx_ * 58, fy - 6); c.line_to(hx + sx_ * 72, fy - 10); c.stroke()
            c.move_to(hx + sx_ * 58, fy + 4); c.line_to(hx + sx_ * 72, fy + 6); c.stroke()


PANELS = [(0.0, DURATION, frame)]
