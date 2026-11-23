"""DADDY'S HOME (episode 12): the shared part of the animation pass, from scene 4 on (scenes 1 to 3 carry their own copy
of this in dh_anim1/2/3.py). A Scene takes a scene sheet's rows (dh_scenes.S4 ...), plays them on the sheet's own clock
and in the sheet's own camera frames at 12 drawings a second, lays the takes under them and puts each line in a speech
bubble while it is spoken.
  sc = Scene(4, "v1", ds.S4, takes=[(take, row, offset)], cut={take: next_take})
  sc.DRAW[row] = fn(sc, k, o, t, tt, n)      a staged shot; o["say"] = (text, world_point, side, dark, shift, maxw)
  sc.INS[row]  = fn(sc, k, c, t, tt, n)      an insert, drawn straight on the 540x960 frame; may return a say tuple in frame units
  sc.CLOSER[row] = (factor, head)            the sheet's camera, that much closer on that head
  sc.SHIFT[row] = (dx, dy)                   the sheet's camera moved, in world units
  sc.sfx = [(samples, at, gain)]; sc.main(hi)"""
import math
import os
import subprocess
import cairo
import numpy as np
import soundfile as sf
import kit
import fs_storyboard as sb
import iwry_mouths as im
import dh_props as dp
import dh_layout as dl
import dh_animatic as da
import dh_voices as dv
import dh_scenes as ds
import dh_anim1 as A
from kit import Ctx

DPS, SR, F, CH = 12, 48000, sb.F, dp.CHAIR
DS_ = 0.60
OUT = "../daddys-home"
_M = sorted(im.SIZES, key=lambda q: im.SIZES[q][0] * im.SIZES[q][1])
M_SMALL, M_BIG = _M[len(_M) // 3], _M[-1]


def seq(t, vals):                                          # one value per drawing, the last one held
    return vals[min(len(vals) - 1, int(t * DPS + 1e-6))]


def idx(t):
    return int(t * DPS + 1e-6)


def lerp4(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(4))


def don_at(k, x, feet, pose, face, look, tt, still=False, fn=None):
    with A.About(k.c, x, feet, 1.0, 1.0 if still else A.breath(tt, 0.2)):
        return (fn or sb.don)(k, x, feet, DS_, pose, face, look=look)


def cheek(d, side=-1, s=DS_):
    return (d["head"][0] + side * 27, d["head"][1] + 27 * s)


class Scene:
    def __init__(self, n, V, rows, takes, cut=None, phone=True):
        self.n, self.V, self.phone = n, V, phone
        self.rows = [(r[0], r[1]) for r in rows]
        self.shot = {r[0]: r[2] for r in rows}
        self.T0 = {}; t = 0.0
        for sid, d in self.rows:
            self.T0[sid] = t; t += d
        self.total = t
        self.takes = [(key, self.T0[row] + off) for key, row, off in takes]
        self.AT = dict(self.takes)
        self.WAV = {}
        for key, _ in self.takes:
            a, _sr = sf.read("%s/%s.wav" % (dv.FILM_OUT, key)); self.WAV[key] = np.asarray(a, dtype=np.float64).copy()
        for key, nxt in (cut or {}).items():               # a line talked over on purpose: cut where the next one starts
            m = int((self.AT[nxt] - 0.02 - self.AT[key]) * SR)
            if 0 < m < len(self.WAV[key]):
                self.WAV[key] = self.WAV[key][:m]; f = int(0.04 * SR); self.WAV[key][-f:] *= np.linspace(1, 0, f)
        self.DRAW, self.INS, self.CLOSER, self._cam0, self.sfx = {}, {}, {}, {}, []
        self.PRE = None                                     # PRE(sid, t, tt, n): called before a drawing is made (to set a prop's clock)
        self.SHIFT = {}                                     # row -> (dx, dy): the sheet's camera moved that far (world units), to keep a sign whole

    def loud(self, key, t):
        a = self.WAV[key]; i0 = int((t - self.AT[key]) * SR); m = SR // DPS
        if i0 < 0 or i0 >= len(a):
            return 0.0
        r = float(np.sqrt(np.mean(a[i0:i0 + m] ** 2))) / (float(np.sqrt(np.mean(a ** 2))) + 1e-9)
        return 0.0 if r < 0.35 else min(1.0, 0.35 + 0.5 * r)

    def code(self, key, t):                                # a mouth shape for the rigs that take one (Sofía, Pam, Mom)
        op = self.loud(key, t)
        return None if op <= 0 else (M_SMALL if op < 0.75 else M_BIG)

    def speaking(self, key, t):
        return self.AT[key] <= t < self.AT[key] + len(self.WAV[key]) / float(SR)

    def since(self, key, t):                               # seconds since the take began
        return t - self.AT[key]

    def frame(self, tt, n, hi=1):
        sid = [s for s, _ in self.rows if self.T0[s] <= tt + 1e-6][-1]
        t = tt - self.T0[sid]
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
        k = Ctx(c, 0); box = {}
        dp.TAG_ANG[0] = 0.0
        if self.PRE:
            self.PRE(sid, t, tt, n)
        fr = self.shot[sid]
        if sid in self.INS or isinstance(fr, str) or (isinstance(fr, dict) and "insert" in fr):
            if sid in self.INS:
                say = self.INS[sid](self, k, c, t, tt, n)
            else:
                (da.INSERTS[fr] if isinstance(fr, str) else fr["insert"])(k, c); say = None
            c.identity_matrix(); c.scale(hi, hi)
            if say:
                A.bubble(c, say[0], say[1], y=say[5] if len(say) > 5 else 150, side=say[2], maxw=220, dark=say[3] if len(say) > 3 else False,
                         up=say[4] if len(say) > 4 else False)
            return surf, sid
        sh = dict(fr)

        def fn(k_, o_):
            box.update(o_)
            self.DRAW[sid](self, k_, box, t, tt, n)
        sh["draw"] = fn
        if sid in self.SHIFT:
            if sid not in self._cam0:
                sc = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 54, 96)), 0)
                c0 = dl.draw(dict(fr, draw=lambda k_, o_: None), sc)
                self._cam0[sid] = (c0[0] + self.SHIFT[sid][0], c0[1] + self.SHIFT[sid][1], c0[2])
            sh["cam"] = self._cam0[sid]
        if sid in self.CLOSER:
            if sid not in self._cam0:                       # the sheet's own camera, found once on a scratch surface
                sc = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 54, 96)), 0)
                c0 = dl.draw(dict(fr, draw=lambda k_, o_: None), sc)
                f_, hd = self.CLOSER[sid]
                self._cam0[sid] = (hd[0] - (hd[0] - c0[0]) / f_, hd[1] - (hd[1] - c0[1]) / f_, c0[2] * f_)
            sh["cam"] = self._cam0[sid]; sh["ymin"] = 100
        cam = dl.draw(sh, k)
        c.identity_matrix(); c.scale(hi, hi)
        if "say" in box:
            sy = box["say"]
            txt, w, side = sy[0], sy[1], sy[2]
            dark = sy[3] if len(sy) > 3 else False
            shift = sy[4] if len(sy) > 4 else 0
            mw = sy[5] if len(sy) > 5 else 200
            tip = (270 + (w[0] - cam[0]) * cam[2], 480 + (w[1] - cam[1]) * cam[2])
            y = max(110, min(150, tip[1] - 190))
            A.bubble(c, txt, tip, y=y, side=side, maxw=mw, dark=dark, shift=shift)
        return surf, sid

    def sound(self, out):
        mix = np.zeros(int((self.total + 0.3) * SR))

        def put(a, at_, g=1.0):
            i0 = int(at_ * SR)
            if i0 < len(mix):
                a = a[:len(mix) - i0]; mix[i0:i0 + len(a)] += a * g
        for key, at_ in self.takes:
            put(self.WAV[key], at_)
        for a, at_, g in self.sfx:
            put(a, at_, g)
        sf.write(out, mix, SR)

    def main(self, hi=1):
        tmp = "/tmp/dh_s%d_%s" % (self.n, self.V); os.makedirs(tmp, exist_ok=True)
        ds.ARM_PHONE[0] = self.phone
        N = int(round(self.total * DPS)); lst = []; tiles = []
        for n in range(N):
            surf, sid = self.frame(n / float(DPS), n, hi)
            p = "%s/d_%04d.png" % (tmp, n); surf.write_to_png(p)
            lst.append("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
            if n % 3 == 0:
                tiles.append((p, sid, n / float(DPS)))
        lst.append("file '%s'\n" % p)
        open(tmp + "/list.txt", "w").write("".join(lst))
        self.sound(tmp + "/a.wav")
        out = "%s/dh_s%d_anim_%s%s.mp4" % (OUT, self.n, self.V, "" if hi == 1 else "_1080")
        part = out[:-4] + ".tmp.mp4"
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-i", tmp + "/a.wav",
                               "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "19",
                               "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % self.total, part])
        os.rename(part, out)
        cols = 12; tw, th = 180, 320; rows_ = (len(tiles) + cols - 1) // cols
        sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, rows_ * (th + 18)); c = cairo.Context(sheet)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, (p, sid, tt) in enumerate(tiles):
            im_ = cairo.ImageSurface.create_from_png(p)
            x, y = (i % cols) * tw, (i // cols) * (th + 18)
            c.save(); c.translate(x, y + 18); c.scale(tw / float(im_.get_width()), th / float(im_.get_height())); c.set_source_surface(im_, 0, 0); c.paint(); c.restore()
            c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.move_to(x + 4, y + 13); c.show_text("%s  %.2f" % (sid, tt))
        sheet.write_to_png("%s/dh_s%d_anim_%s_strip.png" % (OUT, self.n, self.V))
        print("wrote", out, "%.2f s, %d drawings" % (self.total, N))
