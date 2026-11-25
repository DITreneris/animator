import sys, math, cairo, os, subprocess
sys.path.insert(0, "/home/claude/animator/uptimez/src")
import ps_scenes as ps, ps_motion as m, ps_checks as pc
from kit import INK, Ctx
ps.FIX_V4[0] = True; ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
F = ps.F
DX, FD = ps.tape_x(140) - 190, F + 140
c0 = m._board_cam("3.4"); ps.NO_SHIFT[0] = True
Z = 2.3
CAM = (DX + 85 / Z, c0[1] - 10, Z)
WAIT = dict(arms=((-95, 0), (-20, -40)), tele=-1.25, sel=0.6)
FIX = dict(arms=((-95, 0), (-80, 0)), tele=-1.57, sel=0.6)
PH = 0.58
TH = ps.dp.POSES["thumbs"]
KK = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
o_, _ = ps.don(KK, (DX, FD), TH, "grin", (0, -0.3), chin=1, hands=("thumb", "thumb")); UP = o_["hands"][1]
ps.rp.PAD_THUMB[0] = False                                   # the hand sheet: the screen's own drawn thumb was a second hand
o_, _ = ps.robot(KK, "rob_tape", selfie=FIX["sel"], phone="approved", arms=FIX["arms"], tele=FIX["tele"], phone_s=PH)
ik_ = m.don_arms(DX, FD, right=(o_["phone"][0], o_["phone"][1] + 24))
o2_, _ = ps.don(KK, (DX, FD), (TH[0], TH[1], ik_[2], ik_[3]), "grin", (0, -0.3), chin=1, hands=("thumb", "thumb"))
PAD = o2_["hands"][1]                                        # where his arm really puts the hand (fixed bones): the pad comes to it
PAD_DY = 84 * ps.SC["robot"] * PH                            # the green pad below the phone's centre
best = None
for up in range(-170, 171, 6):
    for fo in (-80, -60, -40, -20, 0, 20, 40):
        for tele in (-1.75, -1.6, -1.45, -1.3, -1.15):
            for sel in (0.5, 0.6, 0.7, 0.8):
                oo, _ = ps.robot(KK, "rob_tape", selfie=sel, phone="approved", arms=((-95, 0), (up, fo)), tele=tele, phone_s=PH)
                d_ = math.hypot(oo["phone"][0] - (PAD[0] + 4), oo["phone"][1] + PAD_DY - (PAD[1] - 12))
                if best is None or d_ < best[0]: best = (d_, dict(arms=((-95, 0), (up, fo)), tele=tele, sel=sel))
FIX = best[1]; print("thumb tip to the pad's centre: %.1f world px" % best[0])
lerp = m.lerp; ease = m.ease
T_HOLD, T_D1, T_UP, T_REST, T_SINK, T_HIT, T_BACK, T_END = 0.45, 0.62, 0.95, 1.15, 1.55, 1.85, 2.15, 2.6
def at_(v):                                                  # the hand v of the way from the thumbs-up down to the pad
    return (lerp(UP[0], PAD[0], v), lerp(UP[1], PAD[1] - 14, v))
def state(t, i):
    """v2 (three rounds read the shaking arm as nerves, lesson 178: a new gesture): the raised arm DROPS, he heaves it
    back up, it drops for good, and the phone slides in under the thumb. No shake marks; he grins throughout."""
    if t < T_HOLD: return dict(hand=None, rob=0.0, kind="public", face="grin", mark=None)
    if t < T_D1:                                             # it gives way
        u = (t - T_HOLD) / (T_D1 - T_HOLD); return dict(hand=at_(0.45 * u * u), rob=0.0, kind="public", face="grin", mark="drop")
    if t < T_UP:                                             # heaved back up, not quite all the way
        u = ease((t - T_D1) / (T_UP - T_D1)); return dict(hand=at_(lerp(0.45, 0.10, u)), rob=0.0, kind="public", face="grin", mark="heave")
    if t < T_REST: return dict(hand=at_(0.10), rob=0.0, kind="public", face="grin", mark=None)
    if t < T_SINK:                                           # and down for good; the phone comes to meet it
        u = (t - T_REST) / (T_SINK - T_REST)
        return dict(hand=at_(lerp(0.10, 1.0, u * u)), rob=ease(u / 0.8), kind="public", face="grin", mark="drop" if u < 0.7 else None)
    if t < T_HIT: return dict(hand=PAD, rob=1.0, kind="approved", face="grin", mark="hit" if t - T_SINK < 0.14 else None)
    if t < T_BACK:
        u = ease((t - T_HIT) / (T_BACK - T_HIT))
        return dict(hand=(lerp(PAD[0], UP[0], u), lerp(PAD[1], UP[1], u)), rob=1.0, kind="approved", face="smug", mark=None)
    return dict(hand=None, rob=1.0, kind="approved", face="smug", mark=None)
def frame(t, i):
    st = state(t, i); r = st["rob"]
    rob = dict(arms=((-95, 0), (lerp(WAIT["arms"][1][0], FIX["arms"][1][0], r), lerp(WAIT["arms"][1][1], FIX["arms"][1][1], r))),
               tele=lerp(WAIT["tele"], FIX["tele"], r), sel=lerp(WAIT["sel"], FIX["sel"], r))
    def cast(k):
        heads = {}; c = k.c
        if st["hand"] is None: pose = TH
        else:
            ik = m.don_arms(DX, FD, right=st["hand"]); pose = (TH[0], TH[1], ik[2], ik[3])
        front = st["kind"] == "approved"
        if front: _, heads["robot"] = ps.robot(k, "rob_tape", selfie=rob["sel"], phone=st["kind"], arms=rob["arms"], tele=rob["tele"], phone_s=PH)
        od, heads["don"] = ps.don(k, (DX, FD), pose, st["face"], (0, -0.3), chin=1, hands=("thumb", "thumb"))
        if not front: o, heads["robot"] = ps.robot(k, "rob_tape", selfie=rob["sel"], phone=st["kind"], arms=rob["arms"], tele=rob["tele"], phone_s=PH)
        hd_ = od["hands"][1]
        c.set_source_rgb(*INK); c.set_line_cap(1); c.set_line_width(2.8)
        mk = st["mark"]
        if mk == "drop":                                     # two lines above the falling hand
            for dx_ in (-9, 9):
                c.move_to(hd_[0] + dx_, hd_[1] - 34); c.line_to(hd_[0] + dx_, hd_[1] - 58); c.stroke()
        elif mk == "heave":                                  # two short arcs under the elbow: the effort
            ex, ey = (hd_[0] + DX + 40) / 2, hd_[1] + 34
            for r_ in (14, 24):
                c.new_path(); c.arc(ex, ey - 10, r_, 0.5, 2.6); c.stroke()
        elif mk == "hit":
            for a_ in (-2.4, -1.57, -0.75):
                c.move_to(PAD[0] + 26 * math.cos(a_), PAD[1] - 8 + 26 * math.sin(a_)); c.line_to(PAD[0] + 40 * math.cos(a_), PAD[1] - 8 + 40 * math.sin(a_)); c.stroke()
        return heads
    sh = ps.S("3.4", CAM, ps.ROOM3, cast)
    pc.install_scene(ps); pc.begin()
    surf, msgs = ps.render(sh); msgs = msgs + pc.frame_checks(ps, ps.LAST[0])
    return surf, msgs
D = "/tmp/gags/L6f"; os.makedirs(D, exist_ok=True)
bad = {}; N = int(T_END * 15)
for i in range(N):
    surf, msgs = frame(i / 15, i); surf.write_to_png("%s/%03d.png" % (D, i))
    for x in msgs: bad.setdefault(x.split(" (")[0][:60], []).append(i)
print("checks:", bad or "pass")
picks = [min(N - 1, round(j * 15 / 10)) for j in range(int(T_END * 10) + 1)]
cols = 9; rows = (len(picks) + cols - 1) // cols; TW = 216; TH_ = 384
out = cairo.ImageSurface(cairo.FORMAT_RGB24, 10 + cols * (TW + 6), 10 + rows * (TH_ + 26)); c = cairo.Context(out); c.set_source_rgb(.13, .13, .14); c.paint()
for j, i in enumerate(picks):
    im = cairo.ImageSurface.create_from_png("%s/%03d.png" % (D, i)); X = 10 + (j % cols) * (TW + 6); Y = 10 + (j // cols) * (TH_ + 26)
    c.save(); c.translate(X, Y); c.scale(TW / 540, TW / 540); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(1, 1, 1); c.set_font_size(13); c.move_to(X, Y + TH_ + 16); c.show_text("%d  %.1f s" % (j + 1, j / 10))
out.write_to_png("/tmp/gags/L6_strip.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "15", "-i", D + "/%03d.png", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", "/tmp/gags/L6.mp4"])
