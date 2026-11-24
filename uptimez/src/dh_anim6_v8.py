"""DADDY'S HOME v8, scene 6 "Stand Like One": v7's scene (dh_anim6.sc: clock, takes, mix) through dh_anim_v8 (v8 bubbles,
dead zones, set_gate), with the shots that failed redrawn:
  - the throne on its set mark (452; v7 418): Don in front of it, Mom beside him, the line-up and the cameras with them
  - 8.3 (the zip): Mom is in the shot and zips him with her own arm (v7: a teal sleeve from the bottom-left corner,
    "a tube" in the hands audit; rules: mid-frame, the owner is in the shot)
  - 8.4a, 8.4c: Sofía's CV in her hand (v7: beside it, "the CV floats")
  python3 dh_anim6_v8.py [gate|nobub]  ->  ../daddys-home/dh_s6_anim_v8.mp4"""
import sys
import kit
import hands_ps as hp
import fs_storyboard as sb
import dh_props as dp
import dh_layout as dl
import dh_scenes as ds
import dh_poses as dq
import mom_on as mo
import dh_anim6 as V7
import dh_anim_v8 as E
from kit import INK

sc = V7.sc
F, CH, DS_ = V7.F, V7.CH, V7.DS_
D = 34                                                      # the throne's mark (452) minus v7's 418

# ---- the set: everyone round the throne moves with it; the cameras on them too
ds.THR5 = V7.THR5 = dl.CH[0]
ds.DON6 = V7.DON6 = (ds.DON6[0] + D, ds.DON6[1]) if ds.DON6[0] < 450 else ds.DON6
ds.MOM6 = V7.MOM6 = (ds.DON6[0] - 84, F + 8)
ds.HD6 = dl.hd(ds.DON6[0], ds.DON6[1], 0.60)
ds.HM6 = dl.hm(ds.MOM6[0], ds.MOM6[1], ds.MS)
ds.LINE6 = V7.LINE6 = ((ds.DON6[0], F + 26), (ds.DON6[0] + 72, F + 6), (ds.DON6[0] + 162, F + 8))
ds.CAM6B = (ds.DON6[0] + 92, 762, 1.95)
V7.HEAD = (ds.DON6[0], ds.DON6[1] - 302 * DS_)
sc.CAM8 = {sid: (sc.shot[sid]["cam"][0] + D,) + tuple(sc.shot[sid]["cam"][1:]) for sid in ("8.2", "8.2'", "8.2''", "8.2'''")}
for sid_ in [r for r, _ in sc.rows if r.startswith("8.2")]:   # a step back and right: Don out of the app buttons, room above him
    sc.CAM8[sid_] = (ds.DON6[0] - (10 if sid_ == "8.2" else 14), 640, 2.0)   # 8.2 (no line): Mom whole; then her filter whole at the left edge
sc.CAM8["8.3"] = (ds.DON6[0] - 70, 640, 1.7)                # the zip: the two-shot, Mom whole (v7: Don's close shot, her arm a bar)
sc.CAM8["8.4b"] = (520, 752, 1.85)                         # a step back: the tag whole; Sofía's sleeve and CV at the right edge


# ---- 8.2', 8.2'': the filter she holds low at her side, 22 nearer her (whole in the frame, not cut by its left edge)
_wf = dp.wet_filter


def _wet_filter(k, x, y, *a, **kw):
    if abs(x - (ds.MOM6[0] - 34)) < 0.5 and abs(y - (F - 86)) < 0.5:
        x += 22
    return _wf(k, x, y, *a, **kw)


dp.wet_filter = _wet_filter


# ---- 8.3: Mom zips him, her own arm
def r_zip(s, k, o, t, tt, n):
    end = s.AT["8.3"] + len(s.WAV["8.3"]) / 48000.0 - 0.50
    u = min(1.0, max(0.0, (tt - (end - 0.95)) / 0.85))      # round 2 (cold test: "whose hand? it snaps shut"): a slow pull, 0.85 s
    u = (0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0)[min(7, int(u * 7 + 1e-6))]
    done = u >= 1.0
    c = k.c
    dx_, dfeet = ds.DON6
    mx = dx_ - 66                                           # she has stepped right up to him to reach his zip
    dp.ceo_chair(k, ds.THR5, CH[1], CH[2])
    if not done:
        d = sb.don(k, dx_, dfeet, DS_, (-22, 6, 22, -6), "neutral", look=(-0.5, 0.6))
    else:
        after = int((tt - end + 0.05) * E.DPS); a_ = min(3, max(0, after))
        with V7.A.About(c, dx_, dfeet, (0.95, 0.98, 1.0, 1.0)[a_], (1.08, 0.99, 1.01, 1.0)[a_], (-6, 0, 0, 0)[a_]):
            d = dq.don_zipped(k, dx_, dfeet, 0.60, pose=(-22, 6, 22, -6), face="neutral", look=(-0.5, 0.3))
            hx, hy = d["head"]
            for sg in (-1, 1):
                kit.cut(k, [(hx + sg * 14, hy + 30), (hx + sg * 40, hy + 24), (hx + sg * 47, hy + 46), (hx + sg * 16, hy + 48)], dq.dv.VEST, shadow=False, lw=2.2)
            kit.cut(k, [(hx - 21, hy + 42), (hx - 18, hy + 25), (hx + 18, hy + 25), (hx + 21, hy + 42)], dq.dv.VEST, shadow=False, lw=2.2)
            c.set_source_rgb(*ds.SKIN_M); c.rectangle(hx - 11, hy + 8, 22, 10); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(3.2); c.set_line_cap(1); c.move_to(hx - 8, hy + 14); c.line_to(hx + 8, hy + 14); c.stroke()
        kit.text(k, "eek!", hx + 36, hy - 58, 11, INK)
    hx, hy = d["head"]
    zx, zb = hx + 1, hy + 132
    sy_ = hy + 34 + (1 - u) * 78 if not done else hy + 34
    if not done and zb - sy_ > 4:                           # the zip: closed teeth from the hem up to the slider
        kit.cut(k, [(zx - 13, zb), (zx - 9, sy_ + 6), (zx + 9, sy_ + 6), (zx + 13, zb)], dq.dv.VEST, shadow=False, lw=1.8)
        c.set_source_rgb(0.80, 0.82, 0.86); c.set_line_width(6); c.move_to(zx, zb); c.line_to(zx, sy_ + 6); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.4)
        yy = zb - 2
        while yy > sy_ + 8:
            c.move_to(zx - 3.5, yy); c.line_to(zx + 3.5, yy); c.stroke(); yy -= 4
        kit.rect(k, zx - 7, sy_ - 2, 14, 12, (0.84, 0.86, 0.90), 3610, shadow=False, lw=1.8)
    # her screen-right hand on the pull, by IK in her body units; her left at her side
    s_ = ds.MS
    tx, ty = (zx - 12 - mx) / s_, (sy_ + 6 - (F + 8)) / s_
    pose = (-10, 4) + mo.ik(1, tx, ty)
    hp.reset("quiet", "fist")
    m = sb.mfs.mom(k, mx, F + 8, s_, pose, "sweet", look=(0.8, -0.4), bag=False, mouth=s.code("8.3", tt))
    o["mom_head"] = m["head"]
    if 0 < u < 1:
        ds._lines(k, [(hx + 14, sy_ + 44, hx + 14, sy_ + 22), (hx + 21, sy_ + 40, hx + 21, sy_ + 26)])
    if s.speaking("8.3", tt):
        o["say"] = ("Then stand like one, Donnie.", (m["head"][0] + 20, m["head"][1] + 20), 1, False, 0, 150)


# ---- 8.4a, 8.4c: the CV in her hand (the sheet first, then her fingers over it)
def sofia_with_cv(k, x, feet, pose, face, look, ang):
    """The sheet first, at her screen-left hand (measured on a scratch surface), then she is drawn over it: her fingers
    on its edge. sofia_dh draws its own hands (not kit.HAND), so the one-hand-two-passes trick does not apply."""
    import cairo
    scratch = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    real = getattr(V7.sdh.sofia, "_real", V7.sdh.sofia)
    hx, hy = real(scratch, x, feet, V7.SS, pose, face, look=look, tablet_kind="none")["hands"][0]
    q = V7.sdh.sofia(k, x, feet, V7.SS, pose, face, look=look, tablet_kind="none")
    V7.sdh.cv(k, hx - 22, hy - 16, 0.62, ang)               # held out at her side by its edge: in front of her (behind, it hid)
    kit.ellipse(k, hx - 4, hy - 4, 6, 7, (0.84, 0.66, 0.52), 3120, shadow=False, lw=1.6)   # her fingers on its edge, over it
    return q


def r_sofia(s, k, o, t, tt, n):
    dx = V7.seq(t, [44, 22, 6, 0])
    bob = V7.seq(t, [0, -5, 0, 0])
    with V7.A.About(k.c, V7.SOF6[0], V7.SOF6[1], 1.0, 1.0, bob):
        sofia_with_cv(k, V7.SOF6[0] + dx, V7.SOF6[1], "hold", "interested", (-1, 0.15), -0.12)
    if dx:
        ds._lines(k, [(V7.SOF6[0] + dx + 36, F - 4, V7.SOF6[0] + dx + 52, F - 4), (V7.SOF6[0] + dx + 38, F + 8, V7.SOF6[0] + dx + 56, F + 8)])


def r_left(s, k, o, t, tt, n):
    i = V7.idx(t); j = max(0, i - 3)
    sofia_with_cv(k, V7.SOF6[0], V7.SOF6[1], "hold", "interested" if i < 3 else "tight", (-1, 0.15) if i < 3 else (-1, 0),
                  0.1 + 0.05 * min(3, j))


sc.DRAW.update({"8.3": r_zip, "8.4a": r_sofia, "8.4c": r_left})
SET_MOVES, SET_AIR, SET_BEHIND = {}, set(), set()
SET_WALKS = {("8.2'''", "8.3", "mom")}                     # she steps up to him for the zip
ENTRANCES = {("8.4a", "sofia")}


def frame8(tt, n, hi=1):
    return E.frame(sc, tt, n, hi)


if __name__ == "__main__":
    me = sys.modules[__name__]
    if "gate" in sys.argv[1:]:
        sys.exit(1 if E.gate(sc, me, SET_MOVES, SET_AIR, SET_BEHIND, SET_WALKS, entrances=ENTRANCES) else 0)
    if "nobub" in sys.argv[1:]:
        E.NOBUB[0] = True
    E.run(sc, me, 6)
