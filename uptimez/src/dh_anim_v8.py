"""Daddy's Home v8: run a v7 scene (dh_anim.Scene) with the v8 bubbles and checks, without rewriting it.

v7's Scene.frame draws its own bubble from box["say"] (the old dh_anim1.bubble). Here the same drawing is made with the
bubble left out, and the line goes through dh_anim3_v8.say (speech.draw + speech_gate) at the speaker's tip. A scene's
v8 module patches only the shots that fail (sc.DRAW[...] = ...), then calls run(sc, ...) or gate(sc, ...).
The gate is the same as scenes 3 and 4: speech_gate per line, the apps' dead zones, set_gate. Exit 1 on any."""
import collections
import math
import os
import subprocess
import sys
import cairo
import kit
import hands_ps as hp
import dh_props as dp
import dh_layout as dl
import dh_scenes as ds
import dh_animatic as da
import dh_anim3_v8 as A3
from kit import Ctx

DPS = A3.DPS
NOBUB = A3.NOBUB
OUT = "../daddys-home"


def frame(sc, tt, n, hi=1):
    rows = sc.rows
    sid = [s for s, _ in rows if sc.T0[s] <= tt + 1e-6][-1]
    t = tt - sc.T0[sid]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
    k = Ctx(c, 0); box = {}
    dp.TAG_ANG[0] = 0.0
    kit.HAND[0] = hp.hand
    A3.AVOID_EXTRA[:] = []
    try:
        if sc.PRE:
            sc.PRE(sid, t, tt, n)
        fr = sc.shot[sid]
        if sid in sc.INS or isinstance(fr, str) or (isinstance(fr, dict) and "insert" in fr):
            if sid in sc.INS:
                say = sc.INS[sid](sc, k, c, t, tt, n)
            else:
                (da.INSERTS[fr] if isinstance(fr, str) else fr["insert"])(k, c); say = None
            c.identity_matrix(); c.scale(hi, hi)
            if say and not NOBUB[0]:
                A3.say(k, say[0], None, n, name=getattr(sc, "CARD", {}).get(say[0], "DON"))
            return surf, sid
        sh = dict(fr)

        def fn(k_, o_):
            box.update(o_)
            sc.DRAW[sid](sc, k_, box, t, tt, n)
        sh["draw"] = fn
        cam = None
        if sid in getattr(sc, "CAM8", {}):
            cam = sc.CAM8[sid]
        elif sid in sc.SHIFT:
            if sid not in sc._cam0:
                scr = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 54, 96)), 0)
                c0 = dl.draw(dict(fr, draw=lambda k_, o_: None), scr)
                sh_ = sc.SHIFT[sid]
                sc._cam0[sid] = (c0[0] + sh_[0], c0[1] + sh_[1], c0[2] * (sh_[2] if len(sh_) > 2 else 1.0))
            cam = sc._cam0[sid]
        if cam:
            sh["cam"] = cam
        cam = dl.draw(sh, k)
        c.identity_matrix(); c.scale(hi, hi)
        for fg in getattr(sc, "FG8", {}).get(sid, ()):
            fg(sc, k, cam, t, tt, n, box)
        if "say" in box and not NOBUB[0]:
            txt, w = box["say"][0], box["say"][1]
            tip = (270 + (w[0] - cam[0]) * cam[2], 480 + (w[1] - cam[1]) * cam[2])
            A3.say(k, txt, tip, n)
    finally:
        kit.HAND[0] = None
    return surf, sid


def install_speech(me):
    import dh_speech as SP
    SY = A3.install_speech()
    SP._fresh(me, "frame8")
    return SY


def gate(sc, me, moves=None, air=None, behind=None, walks=None, entrances=None, foreground=None, flying=()):
    """flying: shots where a logged prop leaves the frame on purpose (the filter's flight): not a sign in a dead zone."""
    import dh_speech as SP
    import set_gate
    SY = install_speech(me); ds.ARM_PHONE[0] = sc.phone
    A3.HELD.clear(); A3.R_HELD.clear(); del A3.CHECKS[:]
    set_gate.install(); del set_gate.SEQ[:]
    zc = collections.Counter(); sc_ = collections.Counter()
    for n in range(int(round(sc.total * DPS))):
        set_gate.begin(None)
        surf, sid = me.frame8(n / float(DPS), n, 1)
        set_gate.SEQ[-1] = (sid, list(set_gate.LOG))
        for f_ in set_gate.faults(sid, moves=moves or {}, air=air or set(), behind=behind or set()):
            sc_[(sid, f_)] += 1
        if sid in sc.INS or isinstance(sc.shot[sid], str):
            continue
        seen = []
        for rec in SP.REG:
            try:
                ms = SY.measure(rec); hx, hy = SP._frame_matrix(rec).transform_point(*rec["head_u"])
            except Exception:
                continue
            if any(math.hypot(hx - a, hy - b) < 0.5 * ms["r"] for a, b in seen):
                continue
            seen.append((hx, hy)); r = ms["r"] * 0.8
            if -r < hx < 540 + r and -r < hy < 960 + r:
                for f_ in A3.zone_faults((hx - r, hy - r, hx + r, hy + r), "face"):
                    if (sid, rec.get("name")) in (foreground or set()):
                        continue
                    if f_ == "at the frame's edge" and (sid, rec.get("name")) in (entrances or set()) and n - int(sc.T0[sid] * DPS) < 2:
                        continue
                    zc[("face %s" % rec.get("name"), sid, f_)] += 1
        for a in (A3._avoid(solid=True) if sid not in flying else ()):
            for f_ in A3.zone_faults(a, "sign"):
                zc[("sign", sid, f_)] += 1
    by = collections.OrderedDict()
    for n, text, faults in A3.CHECKS:
        b = by.setdefault(text, [0, 0, collections.Counter()]); b[0] += 1
        if faults:
            b[1] += 1; b[2].update(faults)
    bad = 0
    for text, (nn, nf, cnt) in by.items():
        print("%-36s %3d drawings %3d with faults  %s" % (text, nn, nf, dict(cnt)))
        bad += nf
    print("speech_gate: %d bubble drawings, %d with faults" % (len(A3.CHECKS), bad))
    for (what, sid, f_), v in sorted(zc.items()):
        print("ZONE %-14s %-6s %-22s %d drawings" % (what, sid, f_, v))
    print("dead zones: %d drawings with a face or sign in them" % sum(zc.values()))
    for (sid, f_), v in sorted(sc_.items()):
        print("SET %-6s %s  %d drawings" % (sid, f_, v))
    cuts = set_gate.cut_faults(walks=walks or set())
    for f_ in cuts:
        print(f_)
    print("set: %d drawings off the set, %d cuts that move someone" % (sum(sc_.values()), len(cuts)))
    return bad + sum(zc.values()) + sum(sc_.values()) + len(cuts)


def run(sc, me, n_scene):
    """Render: bubbles (or none, NOBUB), v7's sound. -> ../daddys-home/dh_s{n}_anim_v8.mp4 (mute: /tmp/dh_s{n}_v8_mute.mp4)."""
    if not NOBUB[0]:
        install_speech(me)
        A3.HELD.clear(); A3.R_HELD.clear(); del A3.CHECKS[:]
    tmp = "/tmp/dh_s%d_v8%s" % (n_scene, "_mute" if NOBUB[0] else ""); os.makedirs(tmp, exist_ok=True)
    ds.ARM_PHONE[0] = sc.phone
    N = int(round(sc.total * DPS)); lst = []
    for n in range(N):
        surf, sid = me.frame8(n / float(DPS), n, 1)
        p = "%s/d_%04d.png" % (tmp, n); surf.write_to_png(p)
        lst.append("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
    lst.append("file '%s'\n" % p)
    open(tmp + "/list.txt", "w").write("".join(lst))
    if NOBUB[0]:
        out = "/tmp/dh_s%d_v8_mute.mp4" % n_scene
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                               "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-t", "%.3f" % sc.total, out])
        print("wrote", out); return
    sc.sound(tmp + "/a.wav")
    out = "%s/dh_s%d_anim_v8.mp4" % (OUT, n_scene)
    part = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-i", tmp + "/a.wav",
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "19",
                           "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % sc.total, part])
    os.rename(part, out)
    bad = [c_ for c_ in A3.CHECKS if c_[2]]
    print("wrote", out, "%.2f s, %d drawings; speech_gate %d bubble drawings, %d with faults" % (sc.total, N, len(A3.CHECKS), len(bad)))
