"""v4 (pam_xmas3_v3.py = v3 kept), after the review: her neutral is the thin "pressed" mouth (the rose outline
curved up into a smile); "over" drops the glasses lower and lifts the pupils under half lids (judgment, not a
brow); "glance" is a fond side-eye (half lids, pupils hard toward Don, the smallest smile, a light blush) instead
of the wide-eyed stare; the mask pushed up sits flatter and less tilted (its corners read as ears) with the tape
clearer; mask_up() is public so the film's own mask code (shot 10) can draw the same spot.
v3 notes: PAM, Christmas special ("Happy Compliance"), v3: the costume figure of pam_xmas.py (v2, untouched) with her
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

_MASK = px.mask_strip                # the v2 mask as imported
_PX_PAM = px.pam                     # the v2 figure as imported (a film may hook px.pam; never recurse into it)
HERO, POSE_HERO, POSE_FISTS, POSE_THERMOS, POSE_TAKE = px.HERO, px.POSE_HERO, px.POSE_FISTS, px.POSE_THERMOS, px.POSE_TAKE


def _faces(inner_mf, mouth):
    """The Christmas faces on top of the canon (Secret Santa) face function."""
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        if face == "neutral" and not mouth:         # v4: thin pressed lips, not the curved rose smile
            inner_mf(k, x, y, "pressed", look, glasses=glasses, seed=seed)
            return
        if face == "over":                          # v4: judgment over the readers: half lids, pupils up, glasses low
            inner_mf(k, x, y, "pressed", (0.05, -0.9), glasses=glasses, seed=seed)
            ps._lids(c, x, y, low=-1, brows=False, curve=-1.0)
            pm._brows(c, x, y, ((-27, -18), (-9, -17)), ((9, -17), (27, -18)), w=4.2)
            pm.glasses_draw(k, x, y + 7, "low", seed)
            return
        if face == "glance":                        # v4: a fond side-eye at Don, in her deadpan register
            inner_mf(k, x, y, "pressed", (1.0, 0.05), glasses=glasses, seed=seed)
            ps._lids(c, x, y, low=0, brows=False, curve=-1.0)
            pm._brows(c, x, y, ((-27, -21), (-9, -21)), ((9, -24), (27, -22)), w=3.6)   # one brow a touch up
            pm._mouth_erase(k, x, y, seed)
            ps.lips_along(c, x, y, ((-8, 28), (-2, 29), (4, 28), (9, 25)), gloss=False, thin=True)
            c.set_source_rgba(*pt.BLUSH, 0.35)
            for sx in (-26, 26):
                c.save(); c.translate(x + sx, y + 15); c.scale(9, 4.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
                c.fill()
            return
        inner_mf(k, x, y, face, look, glasses=glasses, seed=seed)
    return face_draw


def mask_up(k, x, y, seed=0):
    """v4: the mask pushed up on her head: flatter, a little tilt, clear of the grey streak, the tape bold."""
    c = k.c
    c.save(); c.translate(x + 12, y - 12); c.rotate(0.08); c.scale(1.0, 0.82); c.translate(-x, -y)
    try:
        _MASK(k, x, y, "up", seed)
    finally:
        c.restore()
    c.save(); c.translate(x + 12, y - 12 - 40 * 0.82); c.rotate(0.08 + 0.15)              # the tape, bigger and clear
    c.rectangle(-7, -11, 14, 18); c.set_source_rgb(*px.TAPE); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    c.restore()


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), mask="up", thermos_in_hand=False, orn=False,
        seed=40, badge=True, cape=True, stance=1.0, cape_flare=1.0, chin=0.0, glasses="low", lips="rose", mouth=None):
    old = kit.face_draw
    tg = pt._faces(old, mouth)                                   # streak, smile lines, light lid
    g = "off" if face == "over" and glasses == "low" else glasses   # v4: "over" draws its own, lower glasses
    mf = ps._wrapped_faces(pm._mf_faces, lips, g)(tg, g, mouth)   # glasses on the chain, rose lips
    kit.face_draw = _faces(mf, mouth)
    orig_mask = px.mask_strip

    def mask_up_hook(k, x, y, mode, seed=0):                    # up on her head: the v4 spot
        if mode != "up":
            return orig_mask(k, x, y, mode, seed)
        mask_up(k, x, y, seed)
    px.mask_strip = mask_up_hook
    try:
        return _PX_PAM(k, x, feet, s, pose, face, look, mask=mask, thermos_in_hand=thermos_in_hand, orn=orn,
                      seed=seed, badge=badge, cape=cape, stance=stance, cape_flare=cape_flare, chin=chin)
    finally:
        kit.face_draw = old
        px.mask_strip = orig_mask
