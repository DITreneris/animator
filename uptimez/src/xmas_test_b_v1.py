"""Silent motion test B for "Happy Compliance": Pam's mask (shot 10), about 4 s.
Pam with stiff fists, the mask at her neck; Sofía presses an ornament into her hand (eye contact); Pam pulls
the mask up with one hand, snap, in two drawings; the stance opens (feet apart, elbows out, chin up) and the
towel lifts once and settles; her face stays flat; hold with a blink."""
import math
import kit
from kit import clamp, ease, lerp
import anim
import xmas_set as xs
import sofia_xmas as sx
import pam_xmas as px
import santa_robot as sr

DURATION = 4.0
RAW_T = 0.0
CAM = (418, 565, 1.5)
PAM_X, SOF_X = 490, 340
FISTS = px.POSE_FISTS
TAKE = (0, -30, 14, -8)                                   # left hand out toward Sofía, palm up
PULL = (0, -30, 150, 95)                                  # right hand up at her face, pulling the mask; left keeps the ornament
HERO = px.POSE_HERO


def tw(a, b, u, over=False):
    e = anim.back_out(u) if over else ease(clamp(u))
    return tuple(lerp(p, q, e) for p, q in zip(a, b))


def frame(k, t, tl):
    c = k.c
    xs.with_cam(c, CAM)
    xs.set_dressing(k, boil=int(t * 4))
    xs.tree(k, censored=tuple(range(8)))
    # Sofía: hands her an ornament, deliberately
    GIVE = (-8, 0, 25, 15)                                    # short reach: her hand meets Pam's
    if t < 0.8:
        spose = "hold2"
    elif t < 1.25:
        spose = anim.key(tw(sx.POSES["hold2"], GIVE, (t - 0.8) / 0.25))
    else:
        spose = anim.key(tw(GIVE, sx.POSES["stand"], (t - 1.25) / 0.3))
    sface = "furious" if t < 0.8 else "knowing"
    out_s = sx.sofia(k, SOF_X, xs.FEET + 6, 1.0, spose, sface, look=(0.9, 0), seed=73, orn="none")
    hl, hr = out_s["hands"]
    if t < 0.8:                                              # her two censored ornaments
        for i, (hx_, hy_) in enumerate((hl, hr)):
            ox, oy = hx_ + (-9 if i == 0 else 9), hy_ + 25
            sx.ornament(k, ox, oy, 17, 300 + i); sr.censor_bar(k, ox, oy, 54, 17, rot=0.05, seed=310 + i)
    elif t < 1.15:                                           # the one she presses into Pam's hand
        ox, oy = hr[0] + 6, hr[1] + 24
        sx.ornament(k, ox, oy, 17, 301); sr.censor_bar(k, ox, oy, 54, 17, rot=0.05, seed=311)
    # Pam
    mask_y_mode = "neck"
    stance, flare, chin, dx = 1.0, 1.0, 0.0, 0.0
    face, look = "neutral", (-0.9, 0)
    if t < 0.8:
        pose = FISTS
    elif t < 1.25:
        pose = tw(FISTS, TAKE, (t - 0.8) / 0.2)
    elif t < 1.4:
        pose = TAKE
    elif t < 1.6:
        pose = tw(TAKE, PULL, (t - 1.4) / 0.1)
    else:
        u = (t - 1.6) / 0.35
        pose = tw(PULL, HERO, u, over=True)
        stance = lerp(1.0, px.HERO["stance"], ease(clamp(u)))
        chin = lerp(0, px.HERO["chin"], ease(clamp(u)))
        dx = 10 * ease(clamp(u))
        lift = math.sin(math.pi * clamp((t - 1.6) / 0.6))           # the towel lifts once, settles
        flare = lerp(1.0, px.HERO["cape_flare"], ease(clamp(u))) + 0.35 * lift
        look = (0, 0)
    if 3.0 <= t < 3.17:
        face = "squint"                                               # blink
    out = px.pam(k, PAM_X + dx, xs.FEET, 1.0, pose, face, look=look, mask=None, orn=False,
                 stance=stance, cape_flare=flare, chin=chin, seed=40)
    if t >= 1.15:                                            # the censored ornament, now in Pam's left hand
        hx_, hy_ = out["hands"][0]
        sx.ornament(k, hx_ - 4, hy_ + 22, 17, 301); sr.censor_bar(k, hx_ - 4, hy_ + 22, 54, 17, rot=-0.05, seed=311)
        kit.ellipse(k, hx_, hy_, 9.5, 9.5, kit.PEOPLE["PAM"]["skin"], 312, shadow=False, lw=2)
    # the mask: at her neck, then pulled up in two drawings with a snap
    hx, hy = out["head"]
    fy = hy + 4
    if t < 1.5:
        px.mask_strip(k, hx, fy, "neck")
    elif t < 1.6:
        c.save(); c.translate(hx, fy + 30); c.rotate(0.06); c.scale(0.95, 0.95)
        px.mask_strip(k, 0, -30, "down"); c.restore()                # halfway: over her mouth
    else:
        bounce = -5 * math.sin(math.pi * clamp((t - 1.6) / 0.17))    # snap: overshoots up, settles
        px.mask_strip(k, hx, fy - 7 * chin + bounce, "down")
    if 1.6 <= t < 1.72:                                               # snap lines
        c.set_source_rgb(*kit.INK); c.set_line_width(2.4); c.set_line_cap(1)
        for sx_ in (-1, 1):
            c.move_to(hx + sx_ * 58, fy - 6); c.line_to(hx + sx_ * 72, fy - 10); c.stroke()
            c.move_to(hx + sx_ * 58, fy + 4); c.line_to(hx + sx_ * 72, fy + 6); c.stroke()


PANELS = [(0.0, DURATION, frame)]
