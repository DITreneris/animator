"""ONE STAR v15e (25 Nov, Tomas's notes and /grill-me picks):
  1.4  no tilt down from the portrait: the shot opens on the robot and Don, so the robot's bubble is never there before
       the robot is (0:05, "dragging").
  3.2  the pass-by in depth: Sofía near us (lower, bigger), the Client walking past behind her (0:23).
  3.5  his lean held still while he speaks, so the locked bubble stays off his face (0:31; cs_v14).
  4.2  the taped plan lands on a plain desk: no AI plan peeking out from under it (0:37).
  4.4  the paddle says HUMAN and a tick, big; its arrow points down at Pam's badge, not into her eye; the bubble keeps
       the stammer (0:44)."""
import math
import cs_scene1 as s1
import cs_scene3 as s3
import cs_scene4 as s4
import cs_props as cp
import cs_hands as ch
import kit
from cs_scene1 import S, at, base, sb, ellipse, rect
from kit import INK

DPS = 12


def ease(u):
    return s1.ease(u)


# ---- 3.2 ---------------------------------------------------------------------------------------------------------------

SOF_FG = (1.18, 46.0)                                       # her scale against the set's, and how much nearer (lower) her feet


def s3_2(k, d):
    """24 drawings (2.0 s). The door at 9:00. He is already walking (a bob each step), eyes on Don off right; Sofía,
    near us, smooths her lapel and steps into his line; he walks straight past behind her; her smile at his back."""
    u = d / float(s3.N32 - 1)
    x = s3.WALK[0] + (s3.WALK[1] - s3.WALK[0]) * u
    bob = abs(math.sin(math.pi * d / 3.0)) * 3.0
    sx = s3.SOF[0] + (s3.SOF[1] - s3.SOF[0]) * ease((d - 4) / 5.0)
    past = x > sx + 10
    sface = "knowing" if not past else "caught"
    spose = "lapel" if d < 12 else "hold"
    cam = tuple(a_ + (b_ - a_) * ease(u) for a_, b_ in zip(*s3.CAM32))
    cam = (cam[0], cam[1] + 22, cam[2] * 0.92)                                   # a little wider and lower: her feet in
    with s3.Client(lean=1.5 if d % 3 else 0.5), s1.Breath(s1.sofia_fs, "sofia", s1.br(d, 0.6)):
        S(k, cam, auto=False, portrait="hang", back=lambda k_: None,
          **base(door=0.85, rb=False, dn=False, pm=False, mm=False,
                 sf=at("sofia", x=sx, feet=sb.FOOT["sofia"] + SOF_FG[1], s=sb.SC["sofia"] * SOF_FG[0], pose=spose,
                       face=sface, look=(-1, 0) if not past else (1, 0)),
                 cl=at("client", x=x, feet=sb.FOOT["client"] - bob, face="plain", look=(1, 0))))


# ---- 4.2: a plain desk ---------------------------------------------------------------------------------------------------

def _desk(k):
    """The desk under the taped plan: wood, a grain, no AI plan under it."""
    c = k.c
    c.set_source_rgb(0.62, 0.46, 0.30); c.paint()
    c.set_source_rgba(0.45, 0.31, 0.18, 0.5); c.set_line_width(2)
    for i in range(14):
        y = 40 + i * 68
        c.move_to(0, y); c.curve_to(180, y + 10, 360, y - 12, 540, y + 6); c.stroke()


# ---- 4.4 ----------------------------------------------------------------------------------------------------------------

def s4_4(k, d):
    t = d / float(DPS)
    f = ease((d - s4.FLIP44[0]) / float(s4.FLIP44[1] - s4.FLIP44[0]))
    speaking = s4.LINE44[0] <= t <= s4.LINE44[1]
    look_p = (1, 0.2) if d < 13 else ((1, -0.1) if d < 24 else (-0.4, 0.8))
    face_p = "neutral" if d < 16 else "pleased"
    got = {}

    def pre(k_):
        got["pam"] = s4.pam(k_, s4.PX44, "stand", face_p, look_p, glasses="up", d=d)

    def ex(k_, o):
        c = k_.c
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        dim = 0.6 * (1 - f)
        if speaking and (d // 2) % 3 == 0:
            dim = min(0.75, dim + 0.2)
        if dim > 0:
            c.set_source_rgba(0.02, 0.03, 0.06, dim); c.new_path(); c.arc(sx, sy, 0.78 * r, 0, 6.3); c.fill()
        hx, hy = min(o["robot"]["hands"])
        c.set_source_rgb(*INK); c.set_line_width(4.2); c.set_line_cap(1)
        c.move_to(hx, hy + 3); c.line_to(hx - 6, hy - 26); c.stroke()
        c.set_source_rgb(0.70, 0.55, 0.35); c.set_line_width(2.4); c.move_to(hx, hy + 3); c.line_to(hx - 6, hy - 26); c.stroke()
        ellipse(k_, hx, hy, 4.2, 4.2, (0.62, 0.64, 0.68), 983, shadow=False, lw=1.2)
        turn = math.cos(math.pi * f)
        px, py = hx - 7, hy - 44
        c.save(); c.translate(px, py); c.rotate(-0.04); c.scale(max(0.06, abs(turn)), 1.0)
        rect(k_, -33, -20, 66, 40, (1, 1, 1) if turn < 0 else (0.80, 0.82, 0.86), 982, lw=2)
        if turn < 0:                                                               # v15e: one word, big, and a tick
            cp.T(c, "HUMAN", -5, 7, 14, col=cp.GRN)
            c.set_source_rgb(*cp.GRN); c.set_line_width(3.0); c.set_line_cap(1); c.set_line_join(1)
            c.move_to(18, 1); c.line_to(22, 7); c.line_to(29, -7); c.stroke()
        c.restore()
        if turn < 0 and "pam" in got:                                              # the arrow, from the paddle down to her badge
            bx, by = got["pam"]["head"][0] + 8, got["pam"]["head"][1] + 52 * s4.PAM_S / 0.54 * 0.54 * 1.9
            ax, ay = px - 30, py + 18
            c.set_source_rgb(*cp.GRN); c.set_line_width(4.0); c.set_line_cap(1); c.set_line_join(1)
            ex_, ey_ = bx + 14, by - 10
            c.move_to(ax, ay); c.curve_to(ax - 8, ay + 18, ex_ + 12, ey_ - 14, ex_, ey_); c.stroke()
            an = math.atan2(ey_ - (ey_ - 14), ex_ - (ex_ + 12))
            for s_ in (-0.5, 0.5):
                c.move_to(ex_, ey_); c.line_to(ex_ - 9 * math.cos(an + s_), ey_ - 9 * math.sin(an + s_)); c.stroke()

    with s1.Breath(sb, "robot", s1.br(d, 0.5, 0.006)):
        S(k, s4.CAM44, auto=False, portrait=False, pre=pre, extra=ex,
          **base(cl=False, sf=False, dn=False, mm=False, pm=False, door=0.0, rb=at("robot", arm="paddle")))


def _set(shots, name, entry):
    shots[[x[0] for x in shots].index(name)] = entry


def install():
    """After cs_say.install() (which moves 1.4's camera)."""
    s1.TWO14 = s1.TWO14_IN
    _set(s3.SHOTS, "3.2", ("3.2", s3.N32, s3_2))
    s4._desk = _desk
    _set(s4.SHOTS, "4.4", ("4.4", s4.N44, s4_4))
    ch._BYFN.clear()
