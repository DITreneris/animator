"""PAM, "First Search" (episode 10): her look for this episode, picked by Tomas (19 Nov):
- the reading glasses stay, the gold bead chain goes (Mom has the pearl chain: one chain in the room);
- the lilac flower brooch goes (Mom has the order: one brooch in the room);
- NEW: from the moment Mom holds the candy out to her (3.1b), her cardigan sleeves are shoved up to the elbows: she
  feels supported for the first time, and she gets to work (the tape, the comment, the plan held up, the plan saved).
  At the end, as the robot retries, they come down again (the loop).
Every Pam in this episode goes through pam_bc.pam (acts_ob's poses too), so this file changes her by patching
pam_bc.pam, pam_mf.glasses_draw and kit.arm for the length of one call: pam_bc, pam_mf, acts_ob and kit are untouched.
Usage: with pam_fs.look(sleeves=False|True): ...draw...      (every Pam drawn inside wears this episode's look)"""
import math
import kit
import pam_bc as pb
import pam_mf as pm
from kit import INK, cut, ellipse

SKIN = pm.SKIN


def _draw_no_chain(k, x, y, state, seed):
    """pam_mf.glasses_draw without the bead chain (the same lenses, temples, bridge and flash)."""
    c = k.c
    top = y - 4 if state == "up" else y + 9
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
    for sx in (-1, 1):
        c.move_to(x + sx * 29, top + 1); c.line_to(x + sx * 42, top + 2); c.stroke()
    for sx in (-17, 17):
        pm.half_moon(c, x + sx, top, 25, 10)
        c.set_source_rgba(*pm.LENS, 0.55); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    c.move_to(x - 5, top + 1); c.curve_to(x - 2, top - 3, x + 2, top - 3, x + 5, top + 1); c.stroke()
    if state == "flash":
        c.set_source_rgb(1, 1, 1); c.set_line_width(3.2)
        for sx in (-17, 17):
            c.move_to(x + sx - 6, top + 9); c.line_to(x + sx + 2, top + 1); c.stroke()


def _arm_pushed(inner):
    """kit.arm for her purple sleeves, shoved up: the upper arm in the sleeve, a bunched cuff at the elbow, the bare
    forearm. Any other arm goes straight through."""
    def arm(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
        if col != pm.PURPLE:
            return inner(k, sx, sy, a1, a2, col, skin, seed, ln, w)
        d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
        ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
        hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
        for (ax, ay, bx, by, cc, ww) in ((sx, sy, ex, ey, col, w), (ex, ey, hx, hy, skin, w * 0.72)):
            ang = math.atan2(by - ay, bx - ax)
            nx, ny = -math.sin(ang) * ww / 2, math.cos(ang) * ww / 2
            cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], cc, shadow=False, lw=2)
        ang = math.atan2(ey - sy, ex - sx)
        c = k.c
        c.save(); c.translate(ex, ey); c.rotate(ang)                       # the bunched cuff
        for i, dx in enumerate((-5, 2)):
            ellipse(k, dx, 0, 6, w * 0.66, col, seed + 20 + i, shadow=False, lw=1.8)
        c.restore()
        if kit.HAND[0]:                                    # an episode's own hand (opt-in)
            kit.HAND[0](k, hx, hy, w * 1.15, skin, seed, (math.sin(math.radians(a1 + a2)), math.cos(math.radians(a1 + a2))), 1 if a2 >= 0 else -1)
        else:
            ellipse(k, hx, hy, w * 0.6, w * 0.6, skin, seed, shadow=False, lw=2)
        return hx, hy
    return arm


class look:
    """Inside: every Pam is this episode's Pam (no chain, no brooch; sleeves up if sleeves=True)."""
    def __init__(self, sleeves=False):
        self.sleeves = sleeves

    def __enter__(self):
        self.old = (pb.pam, pm.glasses_draw, kit.arm)
        inner_pam, inner_arm = pb.pam, kit.arm
        sleeves = self.sleeves

        def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=40, glasses="low", lips="berry",
                mouth=None, lean=0.0, paddle=None, note=None, pen=False, brooch=True, badge=True):
            if sleeves:
                kit.arm = _arm_pushed(inner_arm)
            try:
                return inner_pam(k, x, feet, s, pose, face, look, seed, glasses, lips, mouth, lean, paddle, note, pen,
                                 False, badge)
            finally:
                kit.arm = inner_arm
        pb.pam = pam
        pm.glasses_draw = lambda k, x, y, state, seed=0: _draw_no_chain(k, x, y, state, seed) \
            if state not in (None, "off") else None
        return self

    def __exit__(self, *e):
        pb.pam, pm.glasses_draw, kit.arm = self.old
