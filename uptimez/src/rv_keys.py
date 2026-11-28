"""Approved. (episode 16): the two key stills, stage 3b (plan rule 2; Tomas /grill-me 28 Nov).

K1, the loop seam (frame 0 = the last frame, script v4 1.1 / 7.2): a LOW CLOSE AT THE CASTER (Tomas's pick): the gold
throne's base, REVIEW · TOMORROW folded under its front caster, Don's dangling legs and his hanging right hand (he is
asleep in it, tilted back), the robot's gripper reaching in for the card, UPTIME 100% glowing from out of frame. No full
seated Don is needed (new poses go through the pose sandbox, Tomas's pick).
K2, the silence (6.2-6.7): the robot SET ON THE SEAT (Tomas's pick: no new robot pose, its wheel off the cushion's
edge), its face APPROVER: CEO with Don's face; Don in front, his fingertip raised toward it and stopped (`point`,
clearly apart from the screen: rules "a finger near a sign reads as holding it"); Father beside, turned to Don.
v1 has no Father finger: dh_cast.father has no arm control (to the pose sandbox, with Don's seated pose).

Both in the night lock (rv_night_cast v6: the grade, the shade 0.30 on people, glows only at their sources), the props
from rv_props (one screen function, the tag). Runs on a checkout with episode 15's modules, as rv_night_cast.
  python3 rv_keys.py all  -> ../the-review/rv_K1_v1.png, rv_K2_v1.png (+ _270)
"""
import math
import sys
import cairo
import kit
import bp_frame as bp
import ps_set as pss
import don_ps as dp
import robot_ps as rp
import dh_cast as dc
import hand_lib_v4 as hl
import rv_night_cast as nc
import rv_props as pr

EP = "../the-review/"
F = pss.F
TX, TF, TS = pss.THRONE                                      # (452, 808, 0.6)
SEAT = (452, 742)
KHAKI, SHOE, SHIRT, SKIN = (0.80, 0.74, 0.62), (0.24, 0.18, 0.13), (0.97, 0.97, 0.96), (0.98, 0.84, 0.72)
STEEL, STEEL_D = rp.STEEL, rp.STEEL_D


def _card_under_caster(k, x, y, s=1.0):
    """REVIEW · TOMORROW folded twice into a wedge, its red letters on the visible fold."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    kit.cut(k, [(-22, 0), (24, 0), (20, -9), (-18, -11)], pr.PAPER, lw=1.8, shadow=False)
    c.select_font_face(kit.FONT); c.set_font_size(6.5); c.set_source_rgb(*pr.RED)
    c.move_to(-14, -3); c.show_text("TOMORROW")
    c.restore()


def _lap(k):
    """v1c: what of a sleeping Don shows at the top of the low close: his lap on the seat, the vest's hem, the shirt."""
    c = k.c
    kit.cut(k, [(410, SEAT[1] + 4), (496, SEAT[1] + 4), (500, SEAT[1] - 30), (406, SEAT[1] - 30)], KHAKI, lw=2.0, shadow=False)
    kit.cut(k, [(414, SEAT[1] - 28), (492, SEAT[1] - 28), (488, SEAT[1] - 120), (418, SEAT[1] - 120)], SHIRT, lw=2.0,
            shadow=False)
    for side in (-1, 1):                                     # the vest's two fronts, open over the shirt
        x0 = 452 + side * 40
        kit.cut(k, [(x0, SEAT[1] - 26), (452 + side * 12, SEAT[1] - 24), (452 + side * 10, SEAT[1] - 120), (x0, SEAT[1] - 120)],
                (0.16, 0.22, 0.36), lw=2.0, shadow=False)
    c.set_source_rgb(0.35, 0.25, 0.16); c.rectangle(412, SEAT[1] - 34, 82, 7); c.fill()          # the belt


def _legs(k):
    """Don's lower legs hanging from the seat's front edge, his shoes on the floor (asleep, tilted back)."""
    c = k.c
    for x0, x1, f in ((436, 428, F - 2), (468, 480, F)):
        c.set_source_rgb(*KHAKI)
        c.move_to(x0 - 9, SEAT[1] + 2); c.line_to(x0 + 9, SEAT[1] + 2); c.line_to(x1 + 8, f - 12); c.line_to(x1 - 8, f - 12)
        c.close_path(); c.fill_preserve(); c.set_source_rgb(*kit.INK); c.set_line_width(2.0); c.stroke()
        kit.ellipse(k, x1 + 3, f - 7, 13, 6.5, SHOE, 11, shadow=False, lw=1.8)


def _hanging_hand(k):
    """his right arm off the armrest, hanging (RELAXED, the hand library): sleeve then hand, forearm straight down."""
    ax, ay = 392, 702
    wx, wy = 384, 760                                        # v1c: his LEFT arm, off the far armrest (the right one
                                                             # sat on the throne's red lever: read as holding it)
    c = k.c
    c.set_source_rgb(*SHIRT); c.set_line_width(13); c.set_line_cap(1); c.move_to(ax, ay); c.line_to(wx, wy); c.stroke()
    c.set_source_rgb(*kit.INK); c.set_line_width(1.8)
    for dx in (-7, 7):
        c.move_to(ax + dx, ay); c.line_to(wx + dx, wy); c.stroke()
    hl.draw(k, "RELAXED", wx, wy + 2, math.pi / 2 + 0.12, 15, SKIN, side=-1)


def _gripper(k, tx, ty, reach=1.0):
    """v2 (cold round, 2 of 2: "a claw at the edge, hard to tell it is a robot", "covers the W"): more of the robot:
    its round elbow and a second segment in from the frame's right, its jaws on the card's far corner, the glow of its
    face out of frame on them."""
    c = k.c
    ex, ey = tx + 70, ty - 46                                # the elbow
    sx, sy = tx + 150, ty - 120                              # the shoulder, out of frame
    for (ax, ay), (bx, by) in (((sx, sy), (ex, ey)), ((ex, ey), (tx + 14, ty - 4))):
        c.set_source_rgb(*STEEL); c.set_line_width(13); c.set_line_cap(1); c.move_to(ax, ay); c.line_to(bx, by); c.stroke()
        c.set_source_rgb(*kit.INK); c.set_line_width(2.0)
        nx, ny = -(by - ay), (bx - ax); L = math.hypot(nx, ny); nx, ny = nx / L * 6.5, ny / L * 6.5
        for sgn in (-1, 1):
            c.move_to(ax + sgn * nx, ay + sgn * ny); c.line_to(bx + sgn * nx, by + sgn * ny); c.stroke()
    kit.ellipse(k, ex, ey, 11, 11, STEEL_D, 3, shadow=False, lw=2.0)                       # the elbow joint
    c.set_source_rgb(*kit.INK); c.arc(ex, ey, 3, 0, 2 * math.pi); c.fill()
    kit.cut(k, [(tx + 4, ty - 12), (tx + 20, ty - 12), (tx + 20, ty + 4), (tx + 4, ty + 4)], STEEL_D, lw=1.8, shadow=False)
    for dy in (-11, 2):                                      # the two jaws, closed on the card's corner
        kit.cut(k, [(tx - 8, ty + dy), (tx + 6, ty + dy), (tx + 6, ty + dy + 4), (tx - 8, ty + dy + 4)], STEEL, lw=1.6,
                shadow=False)


def k1(out=EP + "rv_K1_v2.png"):
    cam = (478, 756, 4.0)                                    # v1c: the caster low in frame, his lap at the top edge

    def draw(k):
        nc._room(k, pam_behind=False)
        if nc._PASS[0] == "mask":                            # the people (the cast-light mask): his legs, hand
            _lap(k); _legs(k); _hanging_hand(k); return
        nc._shadow(k, TX, TF, 70)
        pss.throne(k)                                        # G3 (v2): the frame sits between the $49,999 tag above and
        _lap(k)                                              # the floor's DON mark below, both out
        _legs(k)
        _hanging_hand(k)
        _card_under_caster(k, TX - 12, F + 4)
        _gripper(k, TX + 20, F + 2)                          # v2: the jaws past the card's last letter
    glows = [(600, F - 40, 70, 60, bp.NIGHT_MONITOR, 0.45)]  # UPTIME 100%, the robot's face out of frame right
    lights = [(600, F - 40, 160, 1.0), (nc.DOOR[0], nc.DOOR[1], 260, 0.4)]
    nc._frame(cam, draw, glows, lights, out, cast=nc.LOCK_CAST)


def k2(out=EP + "rv_K2_v2.png"):
    cam = (470, 800, 1.62)                                   # v1c: the portrait's plaque out (G3: whole or out)
    st = {}

    def draw(k):
        nc._room(k, pam_behind=False)
        if nc._PASS[0] != "mask":
            nc._shadow(k, TX, TF, 70)
            pss.throne(k)
        r = rp.robot(k, SEAT[0], SEAT[1] + 4, nc.L.SC["robot"], look=(1, 0))      # set on the cushion, wheel at its edge
        if nc._PASS[0] != "mask":
            sx, sy = r["screen"][:2]
            pr.screen(k, sx, sy, 50 * nc.L.SC["robot"] * 1.16, "APPROVER: CEO")   # v2: larger (2 of 2 "small")
            st["screen"] = (sx, sy)
        nc._shadow(k, 590, F + 40, 30)
        dc.father(k, 590, F + 38, nc.L.SC["father"], look=(-1, 0))   # v2: on the tape (Father's side)
        nc._shadow(k, 352, F + 60, 34)
        dp.don(k, 352, F + 58, nc.L.SC["don"], (-6, -8, 62, 84), "neutral", look=(1, -0.3), hands=("relax", "point"))   # v2: Don on HIS side
                                                             # of the tape, by the arrow (2 of 2: "the arrow points away from Don")
    probe = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    probe.c.save(); import fs_storyboard_v17 as sbv; sbv.view(probe.c, *cam); draw(probe); probe.c.restore()
    sx, sy = st["screen"]
    glows = [(sx, sy, 44, 40, bp.NIGHT_MONITOR, 0.50)]
    lights = [(sx, sy, 180, 1.0), (nc.DOOR[0], nc.DOOR[1], 260, 0.5)]
    nc._frame(cam, draw, glows, lights, out, cast=nc.LOCK_CAST)


if __name__ == "__main__":
    {"all": lambda: (k1(), k2()), "k1": k1, "k2": k2}[sys.argv[1]]()
