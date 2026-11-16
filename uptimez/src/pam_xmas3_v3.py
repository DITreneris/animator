"""PAM, Christmas special ("Happy Compliance"), v3: the costume figure of pam_xmas.py (v2, untouched) with her
canon office head from the later films, so she matches what viewers saw in Thanksgiving, Mandatory Fun and Secret
Santa (the special releases after them):
- the grey streak in the bob and the smile lines (pam_tg), reading glasses worn low on the gold bead chain
  (pam_mf), the dusty-rose lips (pam_ss);
- the cardboard mask sits pushed up on her head before shot 10 (mask="up", it reads as a mask she hasn't put on
  yet; the neck spot read as goggles and crowded her chest), and goes DOWN OVER HER GLASSES in shot 10: the
  half-moon lenses poke out under it (a superhero who still needs her readers);
- face "over": the deadpan look over the top of her glasses (her Mandatory Fun signature), for "Human in the loop.";
- face "glance": one sideways look at Don with the smallest smile and a faint blush (canon: a soft spot for him),
  during "Nice balls...", before her "Eww.";
- everything else (towel cape, cardigan one button off, paper "P", thermos, hero stance, the flat face) unchanged.
Usage: o = pam(k, x, feet, s, pose, face, look, mask="up", glasses="low", lips="rose", mouth=None, ...px kwargs)"""
import math
import kit
import pam_xmas as px
import pam_tg as pt
import pam_mf as pm
import pam_ss as ps
from kit import INK, ellipse

_PX_PAM = px.pam                     # the v2 figure as imported (a film may hook px.pam; never recurse into it)
HERO, POSE_HERO, POSE_FISTS, POSE_THERMOS, POSE_TAKE = px.HERO, px.POSE_HERO, px.POSE_FISTS, px.POSE_THERMOS, px.POSE_TAKE


def _faces(inner_mf, mouth):
    """The new faces on top of the canon (Secret Santa) face function."""
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        if face == "over":                          # deadpan, eyes up over the half-moons, brows flat and low
            inner_mf(k, x, y, "neutral", (0.15, -0.55), glasses=glasses, seed=seed)
            pm._brows(c, x, y, ((-27, -19), (-9, -19)), ((9, -19), (27, -19)), w=4.0)
            return
        if face == "glance":                        # the soft spot: eyes to Don, the smallest smile, a faint blush
            inner_mf(k, x, y, "hopeful", look, glasses=glasses, seed=seed)
            c.set_source_rgba(*pt.BLUSH, 0.85)
            for sx in (-26, 26):
                c.save(); c.translate(x + sx, y + 15); c.scale(10, 5.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
                c.fill()
            return
        inner_mf(k, x, y, face, look, glasses=glasses, seed=seed)
    return face_draw


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), mask="up", thermos_in_hand=False, orn=False,
        seed=40, badge=True, cape=True, stance=1.0, cape_flare=1.0, chin=0.0, glasses="low", lips="rose", mouth=None):
    old = kit.face_draw
    tg = pt._faces(old, mouth)                                   # streak, smile lines, light lid
    mf = ps._wrapped_faces(pm._mf_faces, lips, glasses)(tg, glasses, mouth)   # glasses on the chain, rose lips
    kit.face_draw = _faces(mf, mouth)
    orig_mask = px.mask_strip

    def mask_up_tilted(k, x, y, mode, seed=0):                  # up on her head, tilted off the grey streak
        if mode != "up":
            return orig_mask(k, x, y, mode, seed)
        c = k.c
        c.save(); c.translate(x + 14, y - 10); c.rotate(0.20); c.translate(-x, -y)
        try:
            orig_mask(k, x, y, mode, seed)
        finally:
            c.restore()
    px.mask_strip = mask_up_tilted
    try:
        return _PX_PAM(k, x, feet, s, pose, face, look, mask=mask, thermos_in_hand=thermos_in_hand, orn=orn,
                      seed=seed, badge=badge, cape=cape, stance=stance, cape_flare=cape_flare, chin=chin)
    finally:
        kit.face_draw = old
        px.mask_strip = orig_mask
