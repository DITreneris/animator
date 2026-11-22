"""THE OFFER (episode 13), stage 7: the animation, scene by scene (decided 22 Nov: scene 1 first, reviewed with sound
and cold viewers, then the rest). Drawn from the scene file (of_scenes.py) at 15 drawings a second on the 30 fps
camera; every drawing goes through the scene file's checks (signs, scale, dead zones, tails); bubbles live as long as
their line (lesson 362), lips follow the take's loudness.

  python3 of_film.py 1        ->  ../the-offer/of_scene1_v1_540.mp4 (with the scene's stretch of of_sound_v1.wav)
                                  /tmp/of_film/s1_sheet4.png (4 fps) for the cold viewers
1080 masters are rendered in /tmp only (series rule: 540 copies are committed)."""
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf
import of_scenes as sc
import of_cast as oc
import of_motion as om

TMP = "/tmp/of_film"
VER = {1: 3, 2: 6, 3: 3, 4: 3}                                   # each scene's current version (new versions, new files)
DPS, FPS = 15, 30
LEAD = 0.15
TAKES = os.path.join(sc.HERE, "of_voices", "takes")


def ease(u):
    return om.ease(u)


# --- what moves in each shot: id -> f(t, L) -> (state overrides, pose overrides) ----------------------------------------
def still(t, L):
    return {}, {}


def s02(t, L):                                             # the headlights cross the wall; his hand finds the wrench
    return dict(sweep_x=-260 + 420 * ease(t / 0.6), reach=ease((t - 0.35) / 0.45)), {}       # v2: a longer reach


def s03(t, L):                                             # two pairs of black shoes, together; they step apart
    u = ease((t - 0.30) / 0.35)
    return dict(moved=dict(g1=(150 - 46 * u, 856), g2=(172 + 46 * u, 856))), {}


def s11(t, L):                                             # the finger goes to 7; then he looks round at the real bay
    turn = 0.9 * ease((t - 0.70) / 0.30)
    return {}, dict(g2=dict(targets=["bay7_point"], point=ease(t / 0.40) > 0.5, turn=turn))


def s12(t, L):                                             # the lighter comes up; CLICK; the flame; the paper browns
    up = ease(t / 0.30)
    lit = t > 0.35
    import of_set as gs
    bx, by = gs.bay7()
    hand = (bx + 2, by + 92 + 60 * (1 - up))
    return dict(burn=0.4 * ease((t - 0.45) / 0.80)), dict(g2=dict(targets_xy=[hand], lighter=1.0 if lit else 0.0,
                                                                   lid=1.0 if t > 0.25 else 0.0))


def s13(t, L):                                             # the creeper rolls out; he sits up; the rag; the flame; the watch
    import of_set as gs
    if t < 0.45:
        return dict(_cast=("father", "g1", "g2"), sit=False, legs_out_v=gs.LEGS_OUT * ease(t / 0.40), burn=0.5), {}
    look = (1, -0.6) if t < 0.95 else (0.9, 2.0)              # to the flame, then down at the watch
    return dict(burn=0.6), dict(client=dict(kind="sit", look=look, face="glance" if t >= 0.95 else "bored"))


def s14(t, L):                                             # "Burn them...": he wipes his hands on the rag as he talks
    return {}, dict(client=dict(kind="sit", look=(-1, -0.2), wipe=math.sin(t * 2 * math.pi * 0.9)))


# --- scene 3, The Offer ----------------------------------------------------------------------------------------------
def _work(t):
    return math.sin(t * 2 * math.pi * 1.3)


def s21(t, L):                                             # Father speaks to him; he keeps working
    return {}, dict(client=dict(kind="bent", work=_work(t)))


def s22(t, L):
    return {}, dict(client=dict(kind="bent", work=_work(t + 0.4)))


def s23b(t, L):                                            # his eyes go from the lamp, up there, to the Client: he decides
    u = ease((t - 0.25) / 0.45)
    return {}, dict(father=dict(look=(1, -0.9 + 1.1 * u)))


def s25(t, L):                                             # he straightens, the wrist comes up; the glance
    u = ease(t / 0.35)
    return {}, dict(client=dict(kind="watch", watch_u=u, look=(-1, 0) if u < 0.8 else (1.9, 2.0),
                                face="bored" if u < 0.8 else "glance"))


def s27(t, L):                                             # the phone out of the top pocket, turned round
    return {}, dict(client=dict(kind="pocket", pocket_u=ease((t - 0.1) / 0.4)))


def s28c(t, L):                                            # one nod: down and back up
    return {}, dict(father=dict(face="low" if 0.25 < t < 0.7 else "hard"))


def s28d(t, L):                                            # SLAM
    u = ease(t / 0.18)
    return dict(anim=True, bonnet=1.0 - u, shake=0 if t < 0.18 else 5 * math.exp(-(t - 0.18) * 9) * math.sin(t * 90)), \
        dict(client=dict(kind="slam", slam_y=110 * (1 - u)))


def s28e(t, L):                                            # the key turns; a cough; it runs
    ku = ease(t / 0.3)
    run = 0.0 if t < 0.45 else (4 if t < 0.65 else 1.6) * math.sin(t * 2 * math.pi * 11)
    return dict(key_u=ku, run=run), {}


def s29(t, L):                                             # on his way to the door
    u = t / L
    x = 280 - 52 * u
    return dict(_cam=WALK_CAM, moved=dict(father=(x, 880 - 4 * abs(math.sin(t * math.pi * 2.2))), g2=(120, 872))), {}


WALK_CAM = (290, 780, 1.3)                                 # locked: he walks through the frame (a following camera jumped)


VETO_AT = (345, 880)                                       # v9 (22 Nov, decided): Father shuts the lighter himself
VETO_L = (406, 732)                                        # the flame's foot, held out to him over the roof


def _veto(t16, t17):
    """one continuous two-shot over 1.6 + 1.7: the lighter comes down to him; the brow; his hand; two fingers; SNAP."""
    st = dict(_cast=("father", "g2"), _cam=["father", "g2"], moved=dict(father=VETO_AT), burn=0.8 if t17 is None else 1.0)
    rest = (VETO_AT[0] + 30, 800)
    lid_pt = (VETO_L[0] - 2, VETO_L[1] - 38)
    if t17 is None:
        t = t16
        d = ease(t / 0.30)
        lx, ly = VETO_L[0] + 30 * (1 - d), VETO_L[1] - 50 * (1 - d)
        u = ease((t - 0.40) / 0.35)
        hand = [om.lerp(rest, (lid_pt[0] + 30 * (1 - d), lid_pt[1] - 50 * (1 - d)), u)] if u > 0 else []
        return st, dict(father=dict(face="brow2" if t > 0.15 else "hard", look=(1, -0.4), targets_xy=hand,
                                    two_fingers=u > 0.9, front_lighter=(lx, ly, 1.0, 1.0)),
                        g2=dict(targets_xy=[(VETO_L[0] + 40, VETO_L[1] - 20)], turn=-1.0))
    t = t17
    lid = 1.0 - ease((t - 0.05) / 0.10)                      # SNAP, under his two fingers
    off = ease((t - 0.64) / 0.06)                             # v10: the two fingers HELD on the shut lid, 0.5 s
    hand = [om.lerp(lid_pt, rest, off)] if off < 0.95 else []
    return st, dict(father=dict(face="brow2" if t < 0.4 else "hard", look=(1, -0.4), targets_xy=hand,
                                two_fingers=off < 0.5, front_lighter=(VETO_L[0], VETO_L[1], 1.0 if lid > 0.6 else 0.0, lid)),
                    g2=dict(targets_xy=[(VETO_L[0] + 40, VETO_L[1] - 20)], turn=-1.0))


# --- scene 4, The Calendar ---------------------------------------------------------------------------------------------
def _loud(sid, t):
    m = mouth_at(sid, t)
    return {None: 0.0, "M": 0.15, "C": 0.45, "E": 0.7, "O": 0.85, "A": 1.0}[m]


def s32(t, L):                                             # the visor: the line pops on, and glows as it talks
    k_ = 0.02 + 0.98 * min(1.0, max(0.0, (t / 0.15))) if t < 0.15 else 1.0 + 0.08 * math.sin(min(1.0, (t - 0.15) / 0.12) * math.pi)
    return dict(visor_k=k_, visor_glow=_loud("3.2", t)), {}


def s33(t, L):                                             # he sits up for good news
    return dict(don_over=dict(forward=0.6 * ease(t / 0.3))), {}


def s35(t, L):                                             # he follows the look down, to himself; the smile goes in ONE drawing
    if t < 0.40:
        u = ease(t / 0.35)
        return dict(don="happy", don_over=dict(look=(1 - 0.8 * u, u))), {}
    return {}, {}


def s36(t, L):                                             # buzz; the phone, filling the frame; she looks at Don; face down
    if t < 0.22:                                           # v3: shorter buzz and insert, so face down HOLDS 0.6 s
        return dict(buzz=4 * math.sin(t * 2 * math.pi * 18) if t > 0.03 else 0.0), {}
    if t < 0.67:
        return dict(_cam="insert", insert="invite"), {}
    if t < 0.80:
        return dict(pam_look=(-1, 0.2)), {}                    # she looks at Don, the phone still up
    return dict(pam_look=(1, 0.3) if t > 1.10 else (-1, 0.2), phone_down=True, pam_pose=(-8, 0, 40, 40)), {}    # then away


def s37(t, L):                                             # the smile is gone; he grabs the phone; DAD; the sweat comes back
    if t < 0.2:
        return dict(don="stiff"), {}
    u = ease((t - 0.2) / 0.3)
    return dict(don_over=dict(sweat=1 + int(2 * u), forward=u)), {}


MOTION = {"0.2": s02, "0.3": s03, "1.1": s11, "1.2": s12, "1.3": s13, "1.4": s14,
          "2.1": s21, "2.2": s22, "2.3b": s23b, "2.5": s25, "2.7": s27, "2.8c": s28c, "2.8d": s28d, "2.8e": s28e,
          "2.9": s29,
          "3.2": s32, "3.3": s33, "3.5": s35, "3.6": s36, "3.7": s37}
HANDS_CAM = (500, 742, 3.0)                                # v9: the cut-in: his hands, working in the light


LAMP_IN_BAY = (540, 716)                                   # below his chin, the cage down in the bay: the light on the engine


def s23(t, L):
    """lamp v4 (22 Nov, decided after the cold test read 'interrogation'): the handover as v3, but the bodyguard holds
    it LOW, BESIDE the bay, aimed at the hands; then a cut-in on the hands working in the light."""
    bx, bf = sc.BENT_AT
    start, out_ = (bx - 30, 718), (bx + 60, 724)
    x, f = sc.BLOCK[3]["g1"]
    rest = (x - 44, f - 120)
    u1 = om.hold(t / 0.30)
    u2 = om.hold((t - 0.30) / 0.22)
    u3 = om.hold((t - 0.55) / 0.30)
    st = {}
    if u3 > 0:
        gh = om.lerp(out_, LAMP_IN_BAY, u3)
        return st, dict(client=dict(kind="bent", hand_back=False, work=math.sin(t * 2 * math.pi * 1.3) if t > 0.9 else 0.0),
                        g1=dict(targets_xy=[gh], lamp=True, lamp_xy=gh, cone_side=u3), father=dict(look=(1, -0.2)))
    gh = om.lerp(rest, out_, u2)
    return st, dict(client=dict(kind="bent", hand_back=True, hand_back_at=om.lerp(start, out_, u1), lamp_lit=False),
                    g1=dict(targets_xy=[gh]), father=dict(look=(1, -0.2)))


def s28e2(t, L):                                           # v9: the key turns; at the cough, CUT to the car: it runs
    if t < 0.55:
        return dict(key_u=ease(t / 0.3), run=0.0 if t < 0.45 else 4 * math.sin(t * 2 * math.pi * 11)), {}
    j = 1.4 * math.sin(t * 2 * math.pi * 13) * (1.6 if t < 0.75 else 1.0)
    return dict(_cam=RUN_CAM, _cast=(), insert=None, bonnet=0.0, burn=1.0,
                running=ease((t - 0.55) / 0.08), puff=t - 0.55, tilt=0.004 * j), {}


RUN_CAM = (378, 790, 1.25)                                 # the whole car, nose right: the lights, the puff, the shudder


MOTION["2.3"] = s23
MOTION["2.8e"] = s28e2
for _sid, _fn in om.veto():
    MOTION[_sid] = _fn
MOTION["1.6"] = lambda t, L: _veto(t, None)
MOTION["1.7"] = lambda t, L: _veto(None, t)
for _sid, _fn in om.turn():
    MOTION[_sid] = _fn
for _sid, _fn in om.rock():
    MOTION[_sid] = _fn


# --- the lips: the take's loudness per drawing -> a mouth code ---------------------------------------------------------
_TAKE = {}


def mouth_at(sid, t):
    """the mouth for the speaker of shot sid, t seconds into the shot (None: not speaking)."""
    if sid not in sc.SAY:
        return None
    if sid not in _TAKE:
        a, sr = sf.read(os.path.join(TAKES, "%s.wav" % sid))
        _TAKE[sid] = (a, sr)
    a, sr = _TAKE[sid]
    tt = t - LEAD
    if tt < 0 or tt > len(a) / sr:
        return None
    i0, i1 = int(tt * sr), int((tt + 1.0 / DPS) * sr)
    seg = a[i0:max(i1, i0 + 1)]
    v = float(np.sqrt(np.mean(seg ** 2))) / (np.abs(a).max() + 1e-9)
    return "M" if v < 0.05 else ("C" if v < 0.12 else ("E" if v < 0.2 else ("O" if v < 0.3 else "A")))


def bubble_on(sid, t):
    if sid not in sc.SAY:
        return False
    if sid not in _TAKE:
        mouth_at(sid, 0.0)
    a, sr = _TAKE[sid]
    return LEAD - 0.02 <= t <= LEAD + len(a) / sr + 1.0 / DPS


HOLD_D = 5                                                 # drawings (0.33 s): a prop passing through a zone in a move is fine


def held_only(probs):
    """dead-zone faults count only when they last HOLD_D drawings in a row (a lighter rising into frame through the
    caption zone is a move, not a prop left there); every other fault counts at once."""
    out, runs = [], {}
    for sid, i, t, q in probs:
        if not q.startswith("ZONE"):
            out.append("%s t=%.2f: %s" % (sid, t, q)); continue
        key = (sid, q.split(" (")[0])
        r = runs.get(key)
        if r and r[1] == i - 1:
            r[1] = i; r[2] += 1
        else:
            runs[key] = r = [i, i, 1, t, q]
            runs.setdefault("_all", []).append(r)
    for r in runs.get("_all", []):
        if r[2] >= HOLD_D:
            out.append("%s t=%.2f: %s (for %d drawings)" % ([k for k, v in runs.items() if v is r][0][0], r[3], r[4], r[2]))
    return out


def render_scene(n):
    title, where, scene, shots = sc.SCENES[n - 1]
    tm = sc._timing()
    d = os.path.join(TMP, "s%d" % n)
    os.makedirs(d, exist_ok=True)
    for f_ in os.listdir(d):
        os.remove(os.path.join(d, f_))
    k = 0
    probs, sheet = [], []
    t0 = tm[shots[0]["id"]]["start"]
    for sh0 in shots:
        sid = sh0["id"]
        L = tm[sid]["len"]
        fn = MOTION.get(sid, still)
        nd = max(1, int(round(L * DPS)))
        for i in range(nd):
            t = i / DPS
            st_over, pose_over = fn(t, L)
            st_over = dict(st_over)
            cast = st_over.pop("_cast", None)
            cam_ = st_over.pop("_cam", None)
            sh = dict(sh0, state=dict(sh0["state"], **st_over))
            if cam_ is not None:
                sh["cam"] = cam_
            if cast is not None:
                sh["cast"] = cast
            saved = sc.POSES.get(sid)
            if pose_over:
                base = dict(saved or {})
                for who, ps in pose_over.items():
                    base[who] = dict(base.get(who, {}), **ps)
                sc.POSES[sid] = base
            who = sc.SAY.get(sid, (None,))[0]
            oc.MOUTH[0] = mouth_at(sid, t) if who == "client" else None
            try:
                surf, p = sc.board_frame(sh, scene, bubble=bubble_on(sid, t))
            finally:
                oc.MOUTH[0] = None
                if saved is None:
                    sc.POSES.pop(sid, None)
                else:
                    sc.POSES[sid] = saved
            probs += [(sid, i, t, q) for q in p]
            for _ in range(FPS // DPS):
                surf.write_to_png(os.path.join(d, "f%04d.png" % k)); k += 1
            if (k // 2) % 4 == 1 or i == 0:                       # about 4 fps for the sheet, and every shot's first drawing
                sheet.append((sid, tm[sid]["start"] + t - t0, surf))
    probs = held_only(probs)
    dur = k / FPS
    a, sr = sf.read(os.path.join(sc.OUT, "of_sound_v2.wav"))
    seg = a[int(t0 * sr):int((t0 + dur) * sr)]
    wav = os.path.join(TMP, "s%d.wav" % n)
    sf.write(wav, seg, sr)
    m1080 = os.path.join(TMP, "of_scene%d_v%d_1080.mp4" % (n, VER.get(n, 1)))
    m540 = os.path.join(sc.OUT, "of_scene%d_v%d_540.mp4" % (n, VER.get(n, 1)))
    tags = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(d, "f%04d.png"), "-i", wav,
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast"] + tags +
                   ["-c:a", "aac", "-b:a", "192k", "-shortest", m1080], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", m1080, "-vf", "scale=540:960:flags=lanczos,format=yuv420p", "-c:v",
                    "libx264", "-crf", "20", "-preset", "veryfast"] + tags + ["-c:a", "copy", m540], check=True)
    # the 4 fps sheet
    cols, tw, th = 8, 216, 384
    rows = (len(sheet) + cols - 1) // cols
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, (cols * (tw + 8) + 8) * 2, (rows * (th + 30) + 10) * 2); S.set_device_scale(2, 2)
    c = cairo.Context(S); c.set_source_rgb(1, 1, 1); c.paint()
    for j, (sid, tt, img) in enumerate(sheet):
        x = 8 + (j % cols) * (tw + 8); y = 6 + (j // cols) * (th + 30)
        c.save(); c.translate(x, y); c.scale(tw / 540.0, th / 960.0); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + th + 18); c.show_text("%d   %.1f s" % (j + 1, tt))
    S.write_to_png(os.path.join(TMP, "s%d_sheet4.png" % n))
    return k, dur, probs, m540, m1080


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    k, dur, probs, m540, m1080 = render_scene(n)
    print("scene %d: %d frames, %.2f s -> %s" % (n, k, dur, m540))
    for q in probs[:20]:
        print("FAIL", q)
    sys.exit(1 if probs else 0)
