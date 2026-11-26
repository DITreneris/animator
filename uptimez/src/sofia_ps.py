"""SOFÍA in "Pick a Side" (episode 14): episode 12's power suit, war-ready. Tomas, 23 Nov, /grill-me:
the same evening as 12, so the same cream suit (continuity), "armed":
- her hair in a sleek low bun (in place of 12's high ponytail), both ears clear;
- gold SHIELD drop earrings (in place of the triangles): armour for a war day, big enough at phone size;
- black patent stilettos with a GOLD heel (sofia_ss.STILETTO, opt-in): the heel is a story prop (2.8, 3.2, 4.2) and the
  gold reads against the yellow tape. (A red sole was dropped: a real designer's trademark; the series has no brands.)
Built like sofia_dh: the same rig, colours and parts swapped in and put back, so nothing older changes.
  o = sofia(k, x, feet, s, pose, face_kind, look, ...)      the same signature as sofia_dh.sofia
  heel(k, x, y, s, tape=True)                                the insert of 2.8: her shoe, the heel behind the tape
  python3 sofia_ps.py [out_dir]  ->  ps_sofia_v2.png (sheet), ps_sofia_phone_v2.png (phone check); v1 is sofia_ps_v1.py"""
import math
import os
import sys
import cairo
import kit
import sofia_v4 as sf
import sofia_ss as ss
import sofia_bc as sbc
import sofia_ob as so
import sofia_cs as scs
import sofia_dh as sdh
import sofia_fs
import fs_storyboard as sb
from kit import Ctx, INK, cut, ellipse, rect
from sofia_v4 import GOLD, GOLD_LIGHT

HEEL_GOLD = (0.93, 0.72, 0.18)
PATENT = (0.07, 0.07, 0.08)
TAPE = (0.95, 0.78, 0.15)
SHIELD_H = scs.TRI * 1.05


def shield(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """A gold stud at the lobe (x, y) and a solid gold shield under it, point down, with a raised chevron; it swings
    with lgx, about the stud. Both ears (her hair is up)."""
    c = k.c
    h = SHIELD_H
    w = h * 0.78
    c.save(); c.translate(x, y + 3); c.rotate(max(-0.16, min(0.16, -lgx * 0.05)))
    pts = [(-w / 2, 4), (w / 2, 4), (w / 2, 4 + h * 0.42), (0, 4 + h), (-w / 2, 4 + h * 0.42)]
    cut(k, pts, GOLD, shadow=False, lw=2.6)
    c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(2.0); c.set_line_join(0)       # the raised chevron
    c.move_to(-w * 0.30, 4 + h * 0.30); c.line_to(0, 4 + h * 0.58); c.line_to(w * 0.30, 4 + h * 0.30); c.stroke()
    c.set_source_rgba(*INK, 0.55); c.set_line_width(1.2)
    c.move_to(-w * 0.30, 4 + h * 0.36); c.line_to(0, 4 + h * 0.64); c.line_to(w * 0.30, 4 + h * 0.36); c.stroke()
    c.restore()
    ellipse(k, x, y, 4.6, 4.6, GOLD, seed, shadow=False, lw=1.7)


def bun(k, hy, seed):
    """The sleek low bun at the nape, behind her head, peeking out at screen right; a gold pin through it."""
    c = k.c
    bx, by = 58, hy + 6
    ellipse(k, bx, by, 27, 22, sofia_fs.HAIR, seed, shadow=False, lw=2.2)
    c.set_source_rgb(*sofia_fs.HAIR_SHADE); c.set_line_width(2.2); c.set_line_cap(1)
    c.new_path(); c.arc(bx, by, 13, 0.4, 3.6); c.stroke()
    c.set_source_rgb(*sofia_fs.HAIR_SHINE); c.set_line_width(3.2)
    c.new_path(); c.arc(bx, by - 2, 20, 3.8, 5.0); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4.4); c.move_to(bx - 10, by - 24); c.line_to(bx + 22, by - 4); c.stroke()
    c.set_source_rgb(*GOLD); c.set_line_width(2.6); c.move_to(bx - 10, by - 24); c.line_to(bx + 22, by - 4); c.stroke()
    ellipse(k, bx - 11, by - 25, 3.8, 3.8, GOLD, seed + 1, shadow=False, lw=1.4)


def sofia(k, x, feet, s=1.0, pose="hold", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          mouth=None, sparkle=0.0, tablet_kind="auto"):
    """Episode 12's suit (sofia_dh's swaps), the bun, the shields, the stilettos."""
    old = (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, so.drop, so.strand, so.pearl,
           ss.SWEPT[0], sbc._blazer, ss.PULLED[0], ss.PENCIL[0], ss.STILETTO[0])
    ss.PULLED[0] = True; ss.PENCIL[0] = True; ss.STILETTO[0] = HEEL_GOLD
    ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE = sdh.CREAM, sdh.CREAM_SHADE, sdh.CREAM, sdh.CREAM
    sbc.BLAZER, sbc.BLAZER_EDGE = sdh.CREAM, sdh.CREAM_SHADE
    so.drop, so.strand, so.pearl = shield, (lambda k_, seed_: None), scs._gold_bead
    ss.SWEPT[0] = False
    sbc._blazer = sdh._suit(sbc._blazer)
    ss.SLEEK[0] = True
    if "hip_out" not in sbc.POSES:
        sbc.POSES["hip_out"] = (-58, 118, 8, 0)                  # v2: the upper arm well out from the body, the elbow a clear point
    own = face_kind if face_kind in scs.OWN else None
    orig_face = so._face
    if own:
        so._face = lambda o, sp: scs._mine(orig_face(o, sp), own)
    if face_kind == "tight":
        so._face = lambda o, sp: sdh._tight(orig_face(o, sp))
        face_kind = "smile"
    c = k.c
    c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.scale(s, s)   # the bun, behind everything (v2: leans with her)
    bun(k, sofia_fs.HY, seed + 1)
    c.restore()
    try:
        return so.sofia(k, x, feet, s, pose, scs.OWN.get(face_kind, face_kind), look, lag, seed, badge, lean, mouth,
                        sparkle, tablet_kind)
    finally:
        so._face = orig_face
        (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, so.drop, so.strand, so.pearl,
         ss.SWEPT[0], sbc._blazer, ss.PULLED[0], ss.PENCIL[0], ss.STILETTO[0]) = old
        ss.SLEEK[0] = False


def heel(k, x, y, s=1.0, tape=True, seed=3300):
    """v2 (the sheet review): the insert of 2.8, drawn from the foot outward. A low side view, toe to screen left: the
    lower leg leans forward over the shoe, the instep curves into a short pointed pump, the gold stiletto grows out of
    the heel cup. The ball of the foot is on Don's side; the gold tip is planted on the floor just past the tape.
    (x, y): the heel's tip on the floor."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    if tape:                                                 # the tape on the floor plane, running away from us, under the arch
        cut(k, [(-60, 120), (0, 120), (-90, -112), (-128, -112)], TAPE, shadow=False, lw=2.2)   # receding left, away from the heel
        c.set_source_rgba(1, 1, 1, 0.40); c.set_line_width(3); c.move_to(-44, 112); c.line_to(-112, -106); c.stroke()
    for cx, rx in ((-140, 46), (5, 12)):                     # two contacts: the ball and the heel tip
        c.set_source_rgba(0, 0, 0, 0.22); c.save(); c.translate(cx, 2); c.scale(1, 0.22); c.arc(0, 0, rx, 0, 2 * math.pi)
        c.restore(); c.fill()
    leg = [(-104, -40), (-60, -72), (-28, -118), (-36, -156), (-58, -250), (-118, -620), (-50, -630), (-6, -260),
           (14, -190), (30, -140), (28, -122), (8, -112)]
    cut(k, leg, (0.17, 0.16, 0.19), lw=2.4)                                                    # the leg in dark tights, leaning forward
    c.set_source_rgba(1, 1, 1, 0.16); c.set_line_width(5); c.set_line_cap(1)
    c.move_to(-48, -320); c.curve_to(-40, -250, -30, -190, -40, -150); c.stroke()             # the sheen down the shin
    cut(k, [(2, -104), (24, -104), (10, 0), (1, 0)], HEEL_GOLD, lw=2.4)                       # the gold stiletto, from the heel cup
    c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(2.4); c.move_to(18, -96); c.line_to(8, -10); c.stroke()
    rect(k, -2, -6, 14, 7, (0.30, 0.22, 0.08), seed + 1, shadow=False, lw=1.6)                # the tip
    shoe = [(-182, -2), (-178, -18), (-160, -32), (-130, -42), (-100, -44), (-60, -64), (-22, -94), (6, -120),
            (24, -132), (32, -114), (28, -98), (6, -94), (-30, -64), (-80, -24), (-120, -6), (-160, -2)]
    cut(k, shoe, PATENT, lw=2.8)                                                                # the pump
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(4); c.set_line_cap(1)                   # the patent shine
    c.move_to(-170, -20); c.curve_to(-156, -32, -136, -38, -114, -40); c.stroke()
    c.set_line_width(2.6); c.move_to(14, -122); c.curve_to(22, -116, 24, -108, 22, -100); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.0)                                              # the sole line, arching
    c.move_to(-178, 0); c.curve_to(-120, 0, -60, -30, 22, -98); c.stroke()
    c.restore()


def don(k, x, feet, s):
    sb.DON_STATE[0] = ("up", "up")
    try:
        return sb.don(k, x, feet, s, "stand", "neutral", (1, 0))
    finally:
        sb.DON_STATE[0] = None


CV_WORD = ["COO?"]                                          # opt-in (Tomas, 25 Nov: "COO not works for our audience"): "HR?",
                                                            # the robot's own badge: Father's side offers her its job


CV_N = [None]                                              # opt-in (film 5.2): only the first n letters written so far, in the word's place
CV_FONT, CV_AT = [None], ["top"]                            # opt-in (25 Nov, 5.5: HR? over her mouth): a size, "top" / "bottom"


def cv_coo(k, x, y, s=1.0, ang=-0.06):
    """Her CV from 12 with COO? in gold across the top (5.2, 6.1); CV_WORD changes the word (a short one is drawn bigger)."""
    sdh.cv(k, x, y, s, ang)
    c = k.c
    w_ = CV_WORD[0]
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    fs_ = CV_FONT[0] or (17 if len(w_) > 3 else 22)
    c.select_font_face("Lilita One"); c.set_font_size(fs_)
    e = c.text_extents(w_)
    ty = (-40 if len(w_) > 3 else -37) if CV_AT[0] == "top" else 27      # "bottom": across the sheet's foot, clear of its edge (opt-in, 25 Nov)
    c.set_source_rgb(*INK); c.set_line_width(3.2); c.move_to(-e.x_advance / 2, ty); c.text_path(w_ if CV_N[0] is None else w_[:CV_N[0]]); c.stroke_preserve()
    c.set_source_rgb(*HEEL_GOLD); c.fill()
    c.restore()


def sheet(out):
    Wd, Hd, Z = 1800, 1120, 2.2
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL); c.paint()
    F = 960
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, F - 20, Wd, Hd - F + 20); c.fill()
    k = Ctx(c, 0)
    kit.text(k, "PICK A SIDE · SOFÍA · 12's power suit, war-ready · v2", Wd / 2, 46, 34, INK)
    kit.text(k, "the same evening as 12: the cream suit; the hair in a low bun, gold shield earrings, black patent stilettos with gold heels",
             Wd / 2, 82, 17, INK, font=kit.MONO)
    S = 0.47 * Z                                               # the set's home scales: Sofía 0.47, Don 0.60
    don(k, 150, F, 0.60 * Z)
    sofia(k, 400, F, S, "stand", "smile", look=(-0.5, 0))
    sofia(k, 690, F, S, "stand", "interested", look=(1.0, -0.1))
    sofia(k, 980, F, S, "hip_out", "tight", look=(-0.9, 0.1))
    o = sofia(k, 1270, F, S, "stand", "smile", look=(0.4, 0))
    if isinstance(o, dict) and o.get("hands"):
        hx, hy = o["hands"][1]
        cv_coo(k, hx + 30, hy + 30, 1.6)
    c.save(); c.set_source_rgb(0.97, 0.95, 0.90); c.rectangle(1440, 600, 330, 330); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(1440, 600, 330, 330); c.stroke(); c.restore()
    c.save(); c.rectangle(1440, 600, 330, 330); c.clip()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(1440, 760, 330, 170); c.fill()
    heel(k, 1680, 880, 0.85)
    c.restore()
    for name, note, x in (("DON, for scale", "0.60 · the series' proportions", 150), ("THE LOOK", "the suit, the bun, the shields", 400),
                          ("2.7", "eyes to the door (the step: motion test)", 690), ("2.12", "hands to hips, one flat look at Don", 980),
                          ("6.1", "Father's side, COO? in hand", 1270), ("2.8 · INSERT", "the gold heel behind the tape", 1605)):
        kit.text(k, name, x, 1010, 22, INK); kit.text(k, note, x, 1040, 14, INK, font=kit.MONO)
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    """The figure alone at three sizes, as the film will frame her, each shown at 270 px wide (a phone in the feed)."""
    frames = []
    for name, txt in (("wide", "2.4/6.1: across the room, COO? in hand"), ("medium", "2.7: stopped mid-step"),
                      ("insert", "2.8: the heel behind the tape")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        if name == "wide":
            c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 680, 540, 280); c.fill()
            o = sofia(k, 270, 700, 0.47 * 1.6, "stand", "smile", look=(0.4, 0))
            hx, hy = o["hands"][1]; cv_coo(k, hx + 20, hy - 8, 1.1)
        elif name == "medium":
            S2 = 0.47 * 4.4
            tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
            hy0 = sofia(Ctx(cairo.Context(tmp), 0), 270, 0, S2, "stand", "interested")["head"][1]
            sofia(k, 270, 400 - hy0, S2, "stand", "interested", look=(1.0, -0.1))
        else:
            c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 420, 540, 540); c.fill()
            heel(k, 380, 700, 1.25)
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_sofia_v2.png"))
    phone(os.path.join(d, "ps_sofia_phone_v2.png"))
