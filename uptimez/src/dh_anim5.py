"""DADDY'S HOME (episode 12): the animation pass, scene 5 "The Filter" (scene sheet v3, 13.95 s). The engine is
dh_anim.Scene. Between and inside the key drawings: the case dropped on the counter, the room's flinch, the latches and
the slow lid, the brush lifted, the hand coming in, the touch and the machine's shake, the POP and the filter leaving,
two heads following it across the room, the SLAP on Don's head and the coffee running, the robot's REC, the invoice
coming out, the smile going, the drop off his jaw, Pam's sip.
  KOKORO_DIR=/tmp/kokoro python3 dh_anim5.py [hi]  ->  ../daddys-home/dh_s5_anim_v1.mp4, dh_s5_anim_v1_strip.png"""
import math
import sys
import kit
import fs_storyboard as sb
import dh_cast as dc
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_animatic as da
import dh_scenes as ds
import dh_anim1 as A
import cs_sfx as fx
from dh_anim import Scene, seq, idx, don_at, cheek, DPS, DS_, F, CH, M_SMALL, M_BIG
from kit import INK

SS, PS, MS, GS = ds.SS, ds.PS, ds.MS, ds.GS
VIS, THR5, DON5, PAM5, SOF5, MOM5 = ds.VIS, ds.THR5, ds.DON5, ds.PAM5, ds.SOF5, ds.MOM5
MX, MY, MZ = dp.MACHINE
scs, pb = ds.scs, ds.pb

sc = Scene(5, "v1", ds.S5,
           takes=[("7.3b", "7.3b", 0.12), ("7.4", "7.4", 0.12), ("7.5", "7.5", 0.12), ("7.6", "7.6", 0.14), ("7.8", "7.8", 0.22)])

# the coffee machine keeps its own clock: it shakes and steams by the film's time, not frozen at 0
NOW = [0.0]
_cm0 = dp.coffee_machine


def _cm(k, x, base, s=1.0, state="broken", t=0.0, **kw):
    return _cm0(k, x, base, s, state, t=NOW[0], **kw)


dp.coffee_machine = _cm
sc.PRE = lambda sid, t, tt, n: NOW.__setitem__(0, tt)


def vtip(x, side=-1):
    h = dl.hc(x, VIS[1], GS)
    return (h[0] + side * h[2] * 0.62, h[1] + h[2] * 0.5)


def don5(k, face, tt, filt="on", look=(1, 0), pose="stand", still=False, mouth_key=None, drop=None, grin=False):
    """Don where he has stood since scene 4: in front of the throne. filt: None, "flat" (the drawing it lands on) or "on"."""
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    d = don_at(k, DON5[0], DON5[1], pose, face, look, tt, still=still)
    if mouth_key:
        A.mouth(k, d["head"], DS_, sc.loud(mouth_key, tt))
    if filt:
        if filt == "on":
            dp.coffee_run(k, d["head"], DS_)
        flat = filt == "flat"
        dp.wet_filter(k, d["head"][0] + (0 if flat else 4), d["head"][1] - (22 if flat else 25), 0.80, 0.0 if flat else -0.16)
    if drop is not None:                                    # one fat drop off his jaw, falling
        c = k.c
        hx, hy = d["head"]
        c.save(); c.translate(hx - 25, hy + 44 + 70 * drop * drop); c.scale(0.8, 0.8)
        c.move_to(0, -9); c.curve_to(7, 0, 6, 7, 0, 7); c.curve_to(-6, 7, -7, 0, 0, -9); c.close_path()
        c.set_source_rgb(*dp.COFFEE); c.fill(); c.restore()
    return d


def r_bang(s, k, o, t, tt, n):                              # 7.1a: the metal case comes down on the counter
    i = idx(t)
    dc.repairman(k, 648, VIS[1], GS, case=False, look=(1, 0.2)); ds._sticker(k, 648, VIS[1])
    dy = seq(t, [-70, -24, 5, -3, 0])
    dc.tool_case(k, 716, F - 216 + dy, 0.62)
    if i in (2, 3):
        ds._lines(k, [(716 + math.cos(a_) * 44, F - 196 + math.sin(a_) * 30, 716 + math.cos(a_) * (66 + 8 * (i == 2)), F - 196 + math.sin(a_) * (48 + 6 * (i == 2)))
                      for a_ in (-2.6, -2.1, -1.0, -0.5)])


def r_flinch(s, k, o, t, tt, n):                            # 7.1a': the room jumps; Don leaves the floor
    i = idx(t)
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    jolt = seq(t, [-9, -3, 0])
    sb.mfs.mom(k, MOM5[0], MOM5[1] + jolt, MS, "stand", "sweet", look=(1, 0))
    scs.sofia(k, SOF5[0], SOF5[1] + jolt, SS, "hold", "horrified", look=(1, 0))
    up = seq(t, [20, 42, 46, 44, 34, 18])
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.20); c.save(); c.translate(DON5[0], F + 30); c.scale(1, 0.22); c.arc(0, 0, 34 - up * 0.2, 0, 6.2832); c.fill(); c.restore()
    d = sb.don(k, DON5[0], DON5[1] - up, DS_, kit.ARM_POSES["shock"], "shock", look=(1, 0))
    A.fear(k, d["head"], DS_, "o")
    if i < 4:
        ds._lines(k, [(DON5[0] - 26, F - 4, DON5[0] - 26, F + 16), (DON5[0], F, DON5[0], F + 20), (DON5[0] + 26, F - 4, DON5[0] + 26, F + 16)])


def i_case(s, k, c, t, tt, n):                              # 7.1b: click, click; the lid comes up slowly; one small brush
    c.set_source_rgb(0.55, 0.38, 0.24); c.paint()
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 540, 420); c.fill()
    lid = 0.0 if t < 0.5 else A.ease((t - 0.5) / 0.7)
    dc.case_open(k, 270, 640, 3.6, lid=max(0.04, lid), brush_in=lid > 0.25)
    for at_, x_ in ((0.10, 130), (0.30, 410)):              # the latches
        if at_ <= t < at_ + 0.17:
            c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(1)
            for a_ in (-2.4, -1.57, -0.74):
                c.move_to(x_ + math.cos(a_) * 26, 500 + math.sin(a_) * 26); c.line_to(x_ + math.cos(a_) * 48, 500 + math.sin(a_) * 48); c.stroke()


def r_brush(s, k, o, t, tt, n):                             # 7.1c: he lifts it out between two fingers and turns to the machine
    dy = seq(t, [16, 6, -3, 0])
    with A.About(k.c, VIS[0] - 30, VIS[1], 1.0, 1.0, 0):
        dq.visitor_brush(k, VIS[0] - 30, VIS[1] + 0, GS, look=(0.6, 0.2 + dy * 0.02))
    ds._sticker(k, VIS[0] - 30, VIS[1])


def brush_hand(k, back, touch):
    hx = MX - 62 * MZ - back
    hy = MY - 92 * MZ
    kit.cut(k, [(hx - 90, hy), (hx - 40, hy - 4), (hx - 38, hy + 22), (hx - 90, hy + 30)], dc.SUIT, shadow=False, lw=2)
    kit.ellipse(k, hx - 30, hy + 9, 13, 11, ds._co.SKIN, 3570, shadow=False, lw=2)
    dc.brush(k, hx - 14, hy + 4, 0.8, 0.0)
    if touch:
        ds._lines(k, [(hx + 14, hy - 10, hx + 24, hy - 20), (hx + 18, hy + 4, hx + 30, hy + 4), (hx + 14, hy + 18, hx + 24, hy + 28)])


def r_reach(s, k, o, t, tt, n):                             # 7.2a: the hand comes in, slowly
    brush_hand(k, seq(t, [64, 50, 38, 28, 22]), False)


def r_touch(s, k, o, t, tt, n):                             # 7.2a': ONE touch; the machine shakes
    brush_hand(k, seq(t, [8, 0, 0, 6, 14]), idx(t) in (1, 2))


def r_pop(s, k, o, t, tt, n):                               # 7.2a'': POP; the filter leaves by the top of the frame
    i = idx(t)
    fx_, fy_ = MX - 6 - 26 * i, MY - 150 * MZ - 80 * i
    if i < 4:
        dp.wet_filter(k, fx_, fy_, 0.8, -0.5 * i, drips=True)
    if i < 2:
        ds._lines(k, [(MX + math.cos(a_) * 50, MY - 130 * MZ + math.sin(a_) * 34, MX + math.cos(a_) * 78, MY - 130 * MZ + math.sin(a_) * 56) for a_ in (-2.7, -2.2, -0.9, -0.4)])


def r_track(s, k, o, t, tt, n):                             # 7.2b: two heads follow it across the room, right to left
    u = min(1.0, t / 0.36)
    lx = 0.7 - 1.5 * u
    scs.sofia(k, SOF5[0], SOF5[1], SS, "hold", "horrified", look=(lx, -0.9))
    sb.mfs.mom(k, MOM5[0], MOM5[1], MS, "stand", "sweet", look=(lx + 0.2, -0.9))
    x = 700 - 220 * u
    y = F - 214 - 16 * math.sin(u * math.pi)                 # just over their heads, inside the frame
    dp.wet_filter(k, x, y, 0.5, 2.6 - 3.0 * u, drips=False)
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_dash([7, 6])
    c.move_to(x + 16, y + 2); c.line_to(x + 60, y + 14 - 20 * u); c.stroke(); c.set_dash([])


def r_land(s, k, o, t, tt, n):                              # 7.3: SLAP. He does not move. Held in silence
    i = idx(t)
    hx, hy = DON5[0], DON5[1] - 302 * DS_
    if i == 0:                                              # still in the air, coming in from the top right
        don5(k, "neutral", tt, filt=None, look=(0, 0), still=True)
        dp.wet_filter(k, hx + 30, hy - 86, 0.8, 0.5, drips=True)
    else:
        don5(k, "neutral", tt, filt="flat" if i == 1 else ("on" if i >= 3 else "tilt"), look=(0, 0), still=True)
    if i in (1, 2):
        ds._lines(k, [(hx - 42, hy - 40, hx - 58, hy - 50), (hx + 42, hy - 40, hx + 58, hy - 50), (hx - 48, hy - 22, hx - 66, hy - 24), (hx + 48, hy - 22, hx + 66, hy - 24)])


def r_robot(s, k, o, t, tt, n):                             # 7.3b: REC, a shutter, cheerful
    i = idx(t)
    dy = -3 if (s.speaking("7.3b", tt) and n % 2) else 0
    c = k.c
    c.save(); c.translate(0, dy); da._rb("rec" if (i < 2 or (n // 3) % 2 == 0) else "idle")(k, o); c.restore()
    if s.speaking("7.3b", tt):
        o["say"] = ("CEO responsible.", (da.RH[0] + 24, da.RH[1] + 4), 1, False, 20, 200)


def r_clear(s, k, o, t, tt, n):                             # 7.4: he wipes his hands and says it across the room
    bob = -2 if (s.speaking("7.4", tt) and n % 2) else 0
    with A.About(k.c, VIS[0], VIS[1], 1.0, 1.0, bob):
        dc.repairman(k, VIS[0], VIS[1], GS, look=(-0.6, 0), case=False)
    ds._sticker(k, VIS[0], VIS[1] + bob)
    if s.speaking("7.4", tt):
        o["say"] = ("All clear.", vtip(VIS[0], -1), -1, False, -20, 190)


def r_hope(s, k, o, t, tt, n):                              # 7.5: he dares to smile: he thinks he has passed
    pose = seq(t, [(-8, 0, 8, 0), (-22, -6, 22, 6), (-30, -10, 30, 10)])
    d = don5(k, "happy", tt, look=(1, 0), pose=pose, mouth_key="7.5")
    if s.speaking("7.5", tt):
        o["say"] = ("The company?", cheek(d, 1), 1, False, 50, 170)


def r_inv(s, k, o, t, tt, n):                               # 7.6: the invoice comes out. $80
    dx = seq(t, [-26, -8, 3, 0])
    bob = -2 if (s.speaking("7.6", tt) and n % 2) else 0
    with A.About(k.c, VIS[0] - 70, VIS[1], 1.0, 1.0, bob):
        dq.visitor_invoice(k, VIS[0] - 70 + dx, VIS[1], GS, big=True)
    ds._sticker(k, VIS[0] - 70 + dx, VIS[1] + bob)
    if s.speaking("7.6", tt):
        o["say"] = ("The coffee machine.", vtip(VIS[0] - 70, -1), -1, False, -30, 150)


def r_dead(s, k, o, t, tt, n):                              # 7.7: the smile is gone in one drawing; a drop falls off his jaw
    i = idx(t)
    don5(k, "happy" if i == 0 else "neutral", tt, look=(1, 0) if i == 0 else (1, 0.2), pose=(-30, -10, 30, 10) if i == 0 else "stand",
         still=i > 0, drop=None if i < 2 else min(1.0, (i - 2) / 4.0))


def r_pam(s, k, o, t, tt, n):                               # 7.8: a sip, eyes down; then, into the mug, to nobody
    sip = t < 0.22                                          # the mug is up at her lips for the sip, then comes down a finger's width
    q = pb.pam(k, PAM5[0], PAM5[1], PS, (-8, 0, 150, 96), "neutral", look=(-0.2, 0.6), glasses="up", mouth=None if sip else s.code("7.8", tt))
    c = k.c
    hx, hy = q["head"][0] + 14, q["head"][1] + (36 if sip else 50)
    c.save(); c.translate(hx, hy); c.rotate(-0.60 if sip else -0.30); c.scale(1.45, 1.45)
    c.set_source_rgb(*INK); c.set_line_width(5); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()
    c.set_source_rgb(0.36, 0.62, 0.80); c.set_line_width(2.4); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()
    kit.cut(k, [(-10, -12), (10, -12), (9, 12), (-9, 12)], (0.36, 0.62, 0.80), shadow=False, lw=2)
    kit.ellipse(k, 0, -12, 10, 3.2, (0.97, 0.96, 0.92), 3580, shadow=False, lw=1.6)
    c.restore()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(3); c.set_line_cap(1)
    w = math.sin(tt * 5) * 4
    for dx in (-10, 4):
        c.move_to(hx + dx, hy - 26); c.curve_to(hx + dx + 6 + w, hy - 36, hx + dx - 6 - w, hy - 44, hx + dx + 2, hy - 54); c.stroke()
    if s.speaking("7.8", tt):
        o["say"] = ("Some inspect." if s.since("7.8", tt) < 0.95 else "Others drink.", (q["head"][0] - 44 * PS, q["head"][1] + 30 * PS), -1, False, -10, 170)


# "tilt": the filter settled crooked but the coffee not yet running (one drawing)
_w0 = dp.wet_filter
sc.DRAW.update({"7.1a": r_bang, "7.1a'": r_flinch, "7.1c": r_brush, "7.2a": r_reach, "7.2a'": r_touch, "7.2a''": r_pop, "7.2b": r_track,
                "7.3": r_land, "7.3b": r_robot, "7.4": r_clear, "7.5": r_hope, "7.6": r_inv, "7.7": r_dead, "7.8": r_pam})
sc.INS["7.1b"] = i_case
T = sc.T0
sc.sfx = [(fx.step(), T["7.1a"] + 0.17, 0.9), (fx.tap(110.0), T["7.1a"] + 0.19, 0.8),          # BANG
          (fx.whoosh(0.2), T["7.1a'"], 0.4),
          (fx.key(), T["7.1b"] + 0.10, 0.9), (fx.key(), T["7.1b"] + 0.30, 0.9),                  # click, click
          (fx.scratch(0.6), T["7.1b"] + 0.5, 0.18),                                              # the lid
          (fx.tap(400.0), T["7.2a'"] + 0.09, 0.5),                                               # the touch
          (fx.whirr(0.4), T["7.2a'"] + 0.10, 0.25),                                              # the shake
          (fx.pop(), T["7.2a''"], 1.0), (fx.whoosh(0.4), T["7.2a''"] + 0.03, 0.6),               # POP
          (fx.whoosh(0.4), T["7.2b"], 0.35),
          (fx.step(), T["7.3"] + 0.09, 0.8), (fx.rustle(0.2), T["7.3"] + 0.09, 0.7),             # SLAP
          (fx.key(), T["7.3b"] + 0.02, 0.7),                                                     # the shutter
          (fx.rustle(0.25), T["7.6"], 0.5),                                                      # the invoice
          (fx.tap(500.0), T["7.7"] + 0.45, 0.35)]                                                # the drop

if __name__ == "__main__":
    sc.main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
