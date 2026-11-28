"""THE DOUBLE AGENT (episode 15): stage 7, scene 4 (4.1-4.3, 0:27.84-0:34.44), the 540 preview. No lines in this
scene: the sound is the steps, the cup on its saucer, the needles.

  4.1  S6 M: Pam crosses the tape to Don, the cup on its saucer on her palm (the cups canon: SAUCER_SUPPORT); he
       reaches with an open palm, short of it; on the drawing her hand leaves it his palm is under it (one owner a
       drawing). Behind the glass, small and still: the Client and Father seated, her mug between them. Mom at her desk.
  4.2  S1 M: Don at the street door preening in its glass, his back to his office, the cup on its saucer on his palm,
       his other hand smoothing his hair twice; his reflection faint in the glass; the robot working behind.
  4.2b S1 C: he rehearses Father's face in the glass: the smug grin drops, the chin up, lips flat, the hard stare;
       his reflection does it too.
  4.3  S5 M: Pam slips past Mom's desk, hunched, to the office door; Mom knits on (the needles tick), doesn't look up;
       Pam's hand on the handle, the door gives a crack, she leans in.

Hands (rules-hands section 0, the episode's rows): SAUCER_SUPPORT for the cup on a palm (the cups canon); PALM for
a reach that doesn't touch; GRAB for the door handle; RELAXED for the rest. One owner per drawing at the hand-over.

  python3 da_anim_s4.py   ->  ../the-double-agent/da_anim_s4_v1.mp4, da_anim_s4_v1_8fps.png
"""
import math
import os
import sys

import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_cups as cu                                               # noqa: E402
import da_anim_s1 as A                                             # noqa: E402
import da_anim_s3 as C                                             # noqa: E402
import da_layouts as L                                             # noqa: E402
from da_layouts import F, MARKS, SC, dp, ds, kit, rig_hands, shadow, _head  # noqa: E402
from da_motion import ease, ease_out, seg, frame, camera_of, FPS, DRAW  # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
VER = 4
T0 = 27.84
SHOTS = [("4.1", 1.6), ("4.2", 3.0), ("4.2b", 0.8), ("4.3", 1.2)]
drawn = A.drawn
CAMS = {}
CS = cu.CUP_FLOOR                                                  # one cup size in the floor's space (the canon)
declare = C.declare
pam_held = C.pam_held
_MEM = {}                                                          # the drawings render in order


def _probe(draw_rig, scale, jobs, sex="m", skin=L.MALE):
    """run a rig_hands drawing on a throwaway surface with the gate paused; returns what the jobs' got dicts got."""
    import da_hand_gate as g_
    from kit import Ctx
    with g_.paused():
        kk = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
        return rig_hands(kk, draw_rig, scale, jobs, sex=sex, skin=skin)


def don_rig(x, f, face, look, chin=0):
    return lambda kk, a4: dp.don(kk, x, f, SC["don"], a4, face, look, chin=chin, hands=False)


def _mom_folded(k_, look):
    """Mom at her desk, arms folded (Mom v2 sheet): each hand a CLUTCH on the other arm. The gate's CROSS and AIR rules
    read a fold as a fault (crossed forearms, a clutch on no declared prop): she is drawn past the gate, as the people
    behind the glass are (da_set.INSIDE_QUIET); the fold itself was checked on the sheet, up close."""
    import da_hand_gate as g_
    with g_.paused():
        return L.mom(k_, "mom_desk_s", "folded", "unimpressed", look=look)


# ---- 4.1 -------------------------------------------------------------------------------------------------------------------
def s41_parts(t):
    td = drawn(t)
    x1, f = MARKS["pam_cross"]
    dx, df = MARKS["don_take"]
    dx -= 8                                                            # (his body over the throne's red knob, x 519-530:
    sp, sd = SC["pam"], SC["don"]                                      # beside his hand it read as "a stick he holds", 2/2)

    def mom_back(k_):
        return {"mom": _mom_folded(k_, (-1, 0.2))}

    def cast(k_):
        h = {}
        walk = seg(td, 0.0, 0.67)                                      # she steps in over the tape (x 574 here): two steps,
        x = (x1 - 36) + 110 * (1 - ease_out(walk))                     # mid-step over the tape (x 574): her lead foot across                     # ending just over it, on his side (the layout's mark
        back = ease(seg(td, 1.13, 1.6))                                # stopped her short of it); then a step back to it
        x += 30 * back
        step = math.sin(math.pi * 2 * walk) if walk < 1 else 0
        bob = -4 * abs(step)
        T = (x - 40, f - 112)                                          # her wrist: the cup held out at chest height, between them
        if "off" not in _MEM:                                          # his palm's wrist -> the saucer's base, measured
            got = {}
            o_ = _probe(don_rig(dx, df, "pleased", (1, 0.2)), sd, {1: cu.on_palm((dx + 50, df - 130), CS, out=1, got=got)})
            W_ = o_["wrists"][1]                                       # where the wrist really went (the reach clamp)
            _MEM["off"] = (got["base"][0] - W_[0], got["base"][1] - W_[1])
        give = 0.87                                                    # his palm takes it: her hand leaves on this drawing
        mine = td >= give
        rows = [("pam", "L", "saucer_hold" if not mine else "palm", "SAUCER_SUPPORT: the cup on her palm -> palm: let go"),
                ("pam", "R", "quiet", "quiet"),
                ("don", "R", "palm" if not mine else "saucer_hold",
                 "palm: reaching under it, short -> SAUCER_SUPPORT: the cup on his palm"),
                ("don", "L", "quiet", "quiet")]
        declare(tuple(rows), k_)
        # Pam
        shadow(k_, x, f + 2, 32)
        hold = {}
        if not mine:
            pj = {-1: cu.on_palm(T, CS, kind="cup", out=-1, got=hold)}
        else:                                                          # her hand back and down; she turns to go
            back = ease(seg(td, give, give + 0.33))
            pj = {-1: dict(T=(T[0] + 26 * back, T[1] + 40 * back), pose="PALM", out=-1, reach=True)}
        face = "neutral" if td < 1.07 else "doubt"
        look = (-1, 0.3) if td < 1.13 else (1, -0.1)                   # then her eyes go to the office door
        k_.c.save(); k_.c.translate(0, bob)
        op = rig_hands(k_, lambda kk, a4: pam_held(kk, x, f, sp, a4, face, look, mug=False), sp, pj,
                       sex="f", skin=L.FEMALE)
        k_.c.restore()
        h["pam"] = _head(op, "pam")
        if "base" in hold:
            _MEM["base41"] = (hold["base"][0], hold["base"][1] + bob)
        B0 = _MEM.get("base41", (T[0] + 20, T[1]))
        # Don: his palm comes up under it, short; then it is on his palm and he draws it in
        DON_FEET = (dx, df); L.DON_FEET[0] = DON_FEET
        shadow(k_, dx, df + 2, 40)
        off = _MEM["off"]
        if not mine:
            r = ease(seg(td, 0.27, give))
            tgt = (B0[0] - off[0] - 6, B0[1] - off[1] + 12)            # under it, a finger short
            rest = (dx + 30, df - 100)
            DT = (rest[0] + (tgt[0] - rest[0]) * r, rest[1] + (tgt[1] - rest[1]) * r)
            dj = {1: dict(T=DT, pose="PALM", out=-1, reach=True)}         # (the elbow low: the forearm rises to it)
        else:
            home = ease(seg(td, give + 0.13, give + 0.6))              # it comes in to his chest
            base = (B0[0] + (dx + 46 - B0[0]) * home, B0[1] + (df - 150 * sd / 0.6 - B0[1]) * home)
            dj = {1: cu.on_palm((base[0] - off[0], base[1] - off[1]), CS, kind="cup", out=1)}
        dface = "grin" if td < give else "pleased"
        od = rig_hands(k_, don_rig(dx, df, dface, (1, 0.2)), sd, dj)
        h["don"] = _head(od, "don")
        h["cup"] = (B0[0], B0[1] - 14, 16)
        return h
    return cast, mom_back


# ---- 4.2 / 4.2b ------------------------------------------------------------------------------------------------------------
REFLECT = [0.22]
DXS = -14                                                          # 4.2: a step nearer the glass than the layout's mark
CROWN = [(-18, 0), (-18, -16), (-9, -6), (0, -20), (9, -6), (18, -16), (18, 0), (-18, 0)]


def _crown_pt(u, cx, by):
    """the point u (0..1) along the crown's outline, and the outline up to it."""
    pts = [(cx + px, by + py) for px, py in CROWN]
    lens = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    d = u * sum(lens); done = [pts[0]]
    for i, ln in enumerate(lens):
        if d <= ln:
            w = d / ln if ln else 0
            done.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * w, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * w))
            return done[-1], done
        d -= ln; done.append(pts[i + 1])
    return pts[-1], done


def _don_street(k_, td, face, look, chin, hair, cup_up, rows_extra=(), cup_in=0, fog=0.0, crown=0.0, drawing=False,
                mouth=None):
    """Don at the street door, his back to the room: the cup on his screen-right palm; his screen-left hand at his
    hair (hair: 0..1 along the stroke), or drawing on the glass (drawing: its fingertips follow the crown's line);
    his reflection faint in the door's glass (the same drawing, mirrored about the glass at x 92, the gate paused).
    fog: his breath on the glass over the reflection's head; crown: 0..1 of a crown drawn in it with his finger
    (Tomas 28 Nov /grill-me: a gag for 4.2)."""
    import da_hand_gate as g_
    import da_anim_s6 as S6
    x, f = MARKS["don_street"]; x += DXS; L.DON_FEET[0] = (x, f); s_ = SC["don"]
    rows = [("don", "R", "saucer_hold", "SAUCER_SUPPORT: the cup on his palm"),
            ("don", "L", "pinch" if drawing else ("palm" if hair is not None else "quiet"),
             "palm: smoothing his hair -> PINCH: his fingertip drawing on the glass -> quiet")]
    declare(tuple(rows) + tuple(rows_extra), k_)
    shadow(k_, x, f + 2, 40)
    rig = don_rig(x, f, face, look, chin)
    with g_.paused():                                                  # his head, for the reflection's
        kk = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
        hx0, hy0, r0 = _head(rig_hands(kk, rig, s_, {}), "don")
    cx, by = max(2 * 92 - hx0 + 14, 66), hy0 - r0 - 4                 # the crown: on the reflection's head, a little askew
    base = {1: cu.on_palm((x + (40 - 26 * cup_up - cup_in) * s_ / 0.6, f - (150 - 6 * cup_up) * s_ / 0.6), CS, kind="cup", out=1)}
    tip, done = _crown_pt(crown, cx, by)
    if drawing:
        base[-1] = S6.pinch_at(tip, rig, s_, -1, -1)
        m_ = base[-1]["miss"]                                          # (where his arm can't quite take it)
        g_.prop(k_, "glass", tip[0] + m_[0] - 14, tip[1] + m_[1] - 14, 28, 28)
    elif hair is not None:                                             # the stroke: from his brow back over his crown
        hx = x - 20 * s_ / 0.6 + 34 * s_ / 0.6 * hair
        base[-1] = dict(T=(hx, f - (330 - 14 * math.sin(math.pi * hair)) * s_ / 0.6), pose="PALM", out=-1, reach=True)

    def jobs():
        j = dict(base)
        j[1] = cu.on_palm(base[1]["T"], CS, kind="cup", out=1)
        return j
    c = k_.c
    c.save(); c.rectangle(40, F - 360, 100, 360); c.clip()             # his reflection in the door's glass, faint
    c.push_group()
    c.translate(2 * 92, 0); c.scale(-1, 1)
    with g_.paused():
        rig_hands(k_, rig, s_, jobs())
    c.pop_group_to_source(); c.paint_with_alpha(REFLECT[0])
    if fog > 0:                                                        # his breath on the glass
        c.set_source_rgba(1, 1, 1, 0.62 * fog)
        c.save(); c.translate(cx, by - 8); c.scale(36 * (0.6 + 0.4 * fog), 27 * (0.6 + 0.4 * fog))
        c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    if crown > 0 and len(done) > 1:                                    # the crown, wiped clear in it by his fingertip
        c.set_line_cap(1); c.set_line_join(1)
        for col, lw in (((0.30, 0.44, 0.55), 4.6), ((0.93, 0.76, 0.28), 2.6)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.move_to(*done[0])
            for q in done[1:]:
                c.line_to(*q)
            c.stroke()
        c.set_line_cap(0); c.set_line_join(0)
    c.restore()
    kit.MOUTH[0] = mouth
    try:
        o = rig_hands(k_, rig, s_, jobs())                             # Don, over the glass
    finally:
        kit.MOUTH[0] = None
    return {"don": _head(o, "don")}


def s42_cast(t):
    """v3 (Tomas 28 Nov /grill-me: "add a gag to 4.2"): he smooths his hair once, breathes on the glass over his
    reflection's head, and with a fingertip draws a crown on it; steps back to admire: his reflection, crowned."""
    td = drawn(t)

    def cast(k_):
        h = {}
        pick = 0.5 + 0.5 * math.sin(2 * math.pi * 0.9 * td)            # the robot working behind him
        h["robot"] = L.robot(k_, (480, F + 64), tilt=0.20 + 0.08 * pick, look=(0, 1))
        u = seg(td, 0.13, 0.6)
        hair = u if 0 < u < 1 else None
        fog = ease(seg(td, 0.67, 1.0))
        crown = seg(td, 1.07, 2.07)
        drawing = 1.07 <= td < 2.13
        breath = 0.67 <= td < 1.0
        face = "smug" if td < 2.13 else "pleased"
        look = (-1, -0.2) if td < 0.67 else (-1, -0.7)                 # up at the crown's place
        h.update(_don_street(k_, td, face, look, 0, hair, 0.0, fog=fog, crown=crown, drawing=drawing,
                             mouth=0.7 if breath else None))
        return h
    return cast


def s42b_cast(t):
    td = drawn(t)

    def cast(k_):
        # a rehearsal under his crown: Father's hard face, back to his grin, the hard face again, held
        hard = 0.2 <= td < 0.47 or td >= 0.6
        face = "hard" if hard else "smug"
        REFLECT[0] = 0.40
        try:
            return _don_street(k_, td, face, (-1, 0.0), 1 if hard else 0, None, 0.0, cup_in=22, fog=1.0, crown=1.0)
        finally:
            REFLECT[0] = 0.22
    return cast


# ---- 4.3 -------------------------------------------------------------------------------------------------------------------
def s43_parts(t):
    td = drawn(t)
    mx, mf_ = MARKS["mom_desk_s"]

    def mom_back(k_):
        return {"mom": _mom_folded(k_, (0.2, 1.0))}

    def cast(k_):
        h = {}
        c = k_.c
        tick = int(td * DRAW) % 2                                      # the needles tick on her counter
        k_.c.save(); k_.c.translate(mx - 66, F - 190); k_.c.rotate(0.05 * (1 if tick else -1))
        L.dpr.knitting_v2(k_, 0, 0, 0.85)
        k_.c.restore()
        h["knit"] = (mx - 66, F - 180, 28)
        sneak = seg(td, 0.0, 0.6)                                      # small quick steps to the door
        px0, pf_ = mx + 84, F + 24                                     # (left of the knob: at the layout's mark her body hid it)
        slip = ease(seg(td, 0.93, 1.2))                                # (cold test: the end read as a knock) she slips into
        px_ = px0 - 70 * (1 - ease_out(sneak)) + 72 * slip             # the gap, behind the open door's leaf
        step = math.sin(math.pi * 4 * sneak) if sneak < 1 else 0
        bob = -3 * abs(step)
        on = 0.6 <= td < 0.93
        o_door = 0.15 + 0.60 * ease(seg(td, 0.67, 0.93))                # ajar since the Client's crack (3.3); she pulls it wide
        # the office door (layouts' office_door_open, the knob at her waist: its knob_y opt-in, the motion test's
        # precedent); she pulls it open
        handle = L.office_door_open(k_, o_door, knob_y=F - 72)
        lean = 0.12 + 0.10 * slip
        rows = [("pam", "R", "grab" if on else "quiet", "quiet -> GRAB: the office door's handle -> quiet: in"),
                ("pam", "L", "quiet", "quiet")]
        declare(tuple(rows), k_, [("door handle", (handle[0] - 14, handle[1] - 14, 28, 28))] if on else [])
        shadow(k_, px_, pf_ + 2, 32)
        hx_, hy_ = handle[0] - px_, handle[1] - bob - pf_                # her hand's target in her own (leaning) frame:
        ca, sa = math.cos(-lean), math.sin(-lean)                      # the lean turns her after the arm is solved
        Tl = (px_ + hx_ * ca - hy_ * sa, pf_ + hx_ * sa + hy_ * ca)
        jobs = {1: dict(T=Tl, pose="GRAB", out=1, reach=True)} if on else {}
        c.save(); c.translate(0, bob)
        o = L.tilted(k_, px_, pf_, lean, lambda: rig_hands(
            k_, lambda kk, a4: pam_held(kk, px_, pf_, SC["pam"], a4, "neutral", (1, -0.1), mug=False, lean=-10),
            SC["pam"], jobs, sex="f", skin=L.FEMALE))
        c.restore()
        if slip > 0:                                                   # the leaf again, over her: she is past it
            x0, top = 896, 470
            ex = x0 - 44 * o_door
            kit.cut(k_, [(x0, top), (ex, top + 10 * o_door), (ex, F + 14 * o_door), (x0, F)], (0.42, 0.27, 0.16), lw=2.2)
            kit.ellipse(k_, ex + 6, F - 72 + 4 * o_door, 3.5, 3.5, (0.85, 0.72, 0.30), 7201, shadow=False, lw=1)
        h["pam"] = _head(o, "pam")
        return h
    return cast, mom_back


# ---- render, gate, sound ---------------------------------------------------------------------------------------------------
def render_shot(sid, t):
    if sid == "4.1":
        cast, back = s41_parts(t)
        return frame(cast, CAMS[sid][0], tag=True, clips=18, office=dict(client="seated", sofia=True, mug=True), back=[back])
    if sid == "4.2":
        return frame(s42_cast(t), CAMS[sid][0], tag=True, clips=16)
    if sid == "4.2b":
        return frame(s42b_cast(t), CAMS[sid][0], tag=True, clips=16)
    if sid == "4.3":
        cast, back = s43_parts(t)
        return frame(cast, CAMS[sid][0], tag=True, clips=15, back=[back])
    raise KeyError(sid)


STARTS = {}
_acc = 0.0
for _s, _d in SHOTS:
    STARTS[_s] = _acc; _acc += _d

CUES = [
    (STARTS["4.1"] + 0.05, "quiet steps", 0.5),
    (STARTS["4.1"] + 0.87, "cup on saucer", 0.7),                   # it changes palms
    (STARTS["4.2"] + 0.30, "tik", 0.3), (STARTS["4.2"] + 1.40, "tik", 0.3),   # the robot's picks, behind
    (STARTS["4.3"] + 0.0, "needles", 0.5),
    (STARTS["4.3"] + 0.05, "quiet steps", 0.45),
    (STARTS["4.3"] + 0.80, "door", 0.35),
]


def mix(sec, path):
    import numpy as np
    import da_animatic as AN
    sr = AN.SR
    n = int(sec * sr)
    m = 0.004 * AN._lp(AN._noise(sec + 0.1), 200)[:n]
    for t0, word, gain in CUES:
        w = dict(AN.FX)[word]()
        i = int(t0 * sr)
        g = 0.18 * gain / (np.max(np.abs(w)) + 1e-9)
        m[i:i + len(w)] += g * w[:max(0, n - i)]
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)
    return path


GATED = ("4.1", "4.2", "4.2b", "4.3")


def build():
    import subprocess
    from PIL import Image, ImageDraw
    import da_hand_gate as g
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); cu.install(); A._SETUP.append(1)
    for sid, _ in SHOTS:
        CAMS[sid] = camera_of(sid)
    tmp = "/tmp/da_anim_s4"; os.makedirs(tmp, exist_ok=True)
    for f_ in os.listdir(tmp):
        os.remove(os.path.join(tmp, f_))
    n = 0; marks = []; faults = []
    with ds.no_badges(), L.don_legs(), L.sofia_lib_hands(), L.face_guard():
        for sid, dur in SHOTS:
            marks.append((n, sid))
            for i in range(int(round(dur * FPS))):
                g.reset()
                surf = render_shot(sid, i / FPS)
                if i % 2 == 0 and sid in GATED:
                    faults += ["%s %.2fs  %s" % (sid, i / FPS, f) for f in g.check()]
                surf.write_to_png(os.path.join(tmp, "%04d.png" % n)); n += 1
    if faults:
        print("HAND GATE FAIL: %d" % len(faults))
        seen = set()
        for f in faults:
            key = f.split("  ")[1][:50]
            if key not in seen:
                seen.add(key); print("  " + f)
        raise SystemExit(1)
    print("hand gate: PASS on %d drawings" % (n // 2))
    out = os.path.join(EP, "da_anim_s4_v%d.mp4" % VER)
    wav = mix(n / FPS, os.path.join(tmp, "mix.f32"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%04d.png"),
                    "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
    picks = list(range(0, n, FPS // 8))
    tw, th, per = 200, 356, 18
    rows = (len(picks) + per - 1) // per
    S = Image.new("RGB", (per * (tw + 6) + 6, rows * (th + 30) + 6), (245, 244, 240)); d = ImageDraw.Draw(S)
    for j, i in enumerate(picks):
        im = Image.open(os.path.join(tmp, "%04d.png" % i)).convert("RGB").resize((tw, th), Image.LANCZOS)
        X, Y = 6 + (j % per) * (tw + 6), 6 + (j // per) * (th + 30)
        sid = [s for a, s in marks if a <= i][-1]
        S.paste(im, (X, Y + 22)); d.text((X + 2, Y + 4), "%d  %s  %.2fs" % (j + 1, sid, T0 + i / FPS), fill=(20, 20, 20))
    png = os.path.join(EP, "da_anim_s4_v%d_8fps.png" % VER)
    S.save(png)
    print("wrote", out, png, n, "frames")


if __name__ == "__main__":
    build()
