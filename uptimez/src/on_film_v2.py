"""The animation of "Office Noir: The Secret of a Stolen Heart" (grill, 16 Nov): storyboard v4 in motion, on the measured timing
(on_timing.json) and the mix with the jazz-noir cue (on_mix.wav).
- Lips: word-timed mouth shapes from each spoken take itself (closed between words; M / C / E / O / A from the
  loudness and the brightness of every 1/15 s); Don's narration is voice-over, his mouth stays still.
- Acting: limited paper-cutout animation drawn at 15 fps (each drawing held 2 frames at 30 fps): a breath on every
  character, blinks in the close-ups, and the story moves animated: the rain, the flask's cap flips, the lens rises
  to his eye, the POV lens drifts onto her lips, Sofia files, the CCTV lean, the partner's arm comes up, the eyes
  drop and snap, the eye-line in 7B, the shadow grows over the whole of shot 9, the glance at the bunny, the toy
  magnifier slides under the blanket, the baby monitor's light.
- Effects: the old-film look on the noir part only (grain, flicker, a gentle gate weave, the odd scratch); rain and
  the one lightning flash; a jolt on DONNIE! and on the snap, a zoom punch on the SNAG; smoke curling in the lamp
  light (no cigarette) and steam off Mom's mug at the frame's edge.
  python3 on_film.py preview   -> on_film_preview.mp4 (540x960)
  python3 on_film.py release   -> on_film_1080.mp4 (1080x1920)"""
import sys
import json
import math
import subprocess
import numpy as np
import cairo
import soundfile as sf
import kit
from kit import Ctx
import don_on as d
import pam_on as pn
import sofia_on as so
import mom_on as mo
import robot_on as ro
import props_on as pr
import on_set as st
import engine_on as eng
import on_set_sheet as setsh
import props_sheet_on as psh
import sofia_sheet_on as ssh
import pam_sheet_on as pms
import on_sb as sb

FPS, DRAW = 30, 15
FLASH_T = 2 / 15                     # v6: the lightning strikes on the third drawing; frame 0 is the thumbnail
SR = 48000
ANIM = {"don": {}, "sofia": {}, "pam": {}, "mom": {}}
PHASE = {"don": 0.0, "sofia": 1.9, "pam": 3.1, "mom": 4.4}             # breaths out of step


# ---- the characters: a breath, mouth/look overrides, blinks (patched in for the film only) ----------------------

def _wrap(mod, name, key, blink=False):
    import inspect
    orig = getattr(mod, name)
    sig = inspect.signature(orig)

    def f(k, x, feet, s=1.0, *a, **kw):
        A = ANIM[key]
        ba = sig.bind(k, x, feet, s, *a, **kw)                        # overrides win, however the call passed them
        for name_, v in A.get("kw", {}).items():
            if name_ in sig.parameters:
                ba.arguments[name_] = v
        b = A.get("breath", 0.0)
        c = k.c
        c.save(); c.translate(x, feet); c.scale(1, 1 + b); c.translate(-x, -feet)
        prev, REC["cur"] = REC["cur"], key
        try:
            out = orig(*ba.args, **ba.kwargs)
        finally:
            c.restore(); REC["cur"] = prev
        if out and "head" in out:                                    # v7: where the head is, in device space
            REC["heads"][key] = c.user_to_device(*out["head"])
        if blink and A.get("blink") and out and "head" in out:
            hx, hy = out["head"]
            for sx in (-17, 17):
                ex, ey = hx + sx * s, hy + (hy - feet) * b + 7 * s
                kit.ellipse(k, ex, ey, 12.5 * s, 12.5 * s, d.SKIN, 777, shadow=False, outline=False)
                c.set_source_rgb(*kit.INK); c.set_line_width(3 * s / 2.5); c.move_to(ex - 11 * s, ey)
                c.curve_to(ex - 4 * s, ey + 3 * s, ex + 4 * s, ey + 3 * s, ex + 11 * s, ey); c.stroke()
        return out
    setattr(mod, name, f)
    return orig


HEAD_R = {"don": 4.1, "sofia": 2.6, "pam": 4.3, "mom": 4.9}   # v7: face half-width in mouth half-widths
ORIG = {}
REC = {"cur": None, "mouths": [], "heads": {}, "screen": None}     # v7: what was drawn this frame, device space
LAST = {}                                                          # mouth relative to head, for mouthless frames
import iwry_mouths as im


def _rec_mouth(k, x, my, code, *a, **kw):
    c = k.c
    REC["mouths"].append((REC["cur"], c.user_to_device(x, my), c.user_to_device(x + 14, my)))
    return ORIG["im_mouth"](k, x, my, code, *a, **kw)


def _rec_mom_mouth(c, face, mouth, turn=0.0):
    my = mo.HY + 32
    REC["mouths"].append(("mom", c.user_to_device(turn, my), c.user_to_device(turn + 16, my)))
    return ORIG["mom_mouth"](c, face, mouth, turn)


def _rec_screen(c, out, s, text, size=26):
    x, y = out["screen"]
    REC["screen"] = (c.user_to_device(x, y), c.user_to_device(x + 40 * s, y), c.user_to_device(x, y + 34 * s))
    return ORIG["screen_text"](c, out, s, text, size)


def _rec_robot(k, x, feet, s=1.0, *a, **kw):
    out = ORIG["robot_noir"](k, x, feet, s, *a, **kw)
    if out and "screen" in out:
        c = k.c; sx, sy = out["screen"]
        REC["screen"] = (c.user_to_device(sx, sy), c.user_to_device(sx + 40 * s, sy), c.user_to_device(sx, sy + 34 * s))
    return out


def patch():
    ORIG["robot_noir"], ro.robot_noir = ro.robot_noir, _rec_robot
    ORIG["im_mouth"], im.mouth = im.mouth, _rec_mouth
    ORIG["mom_mouth"], mo._mouth = mo._mouth, _rec_mom_mouth
    ORIG["screen_text"], ro.screen_text = ro.screen_text, _rec_screen
    ORIG["don"] = _wrap(d, "don_noir", "don", blink=True)
    ORIG["don_pj"] = _wrap(d, "don_pj", "don", blink=True)
    ORIG["sofia"] = _wrap(so, "sofia_noir", "sofia")
    ORIG["pam"] = _wrap(pn, "pam_noir", "pam")
    ORIG["mom"] = _wrap(mo, "mom", "mom")


def unpatch():
    im.mouth, mo._mouth, ro.screen_text = ORIG["im_mouth"], ORIG["mom_mouth"], ORIG["screen_text"]
    ro.robot_noir = ORIG["robot_noir"]
    d.don_noir, d.don_pj = ORIG["don"], ORIG["don_pj"]
    so.sofia_noir, pn.pam_noir, mo.mom = ORIG["sofia"], ORIG["pam"], ORIG["mom"]


# ---- lips: mouth codes from the takes ------------------------------------------------------------------------------

def visemes(path):
    """One mouth code per drawn frame (1/15 s) of a take: M when quiet (between words), then C / E / O / A by
    loudness, O for the darker (lower) sounds."""
    a, sr = sf.read(path)
    n = int(sr / DRAW)
    frames = [a[i:i + n] for i in range(0, len(a), n)]
    rms = np.array([np.sqrt(np.mean(f ** 2)) if len(f) else 0 for f in frames])
    ref = np.percentile(rms[rms > 0], 90) if np.any(rms > 0) else 1
    out = []
    for f, r in zip(frames, rms):
        L = r / ref
        if L < 0.18 or len(f) < 64:
            out.append("M"); continue
        S = np.abs(np.fft.rfft(f)); fr = np.fft.rfftfreq(len(f), 1 / sr)
        cen = (S * fr).sum() / (S.sum() + 1e-9)
        if L < 0.45:
            out.append("C")
        elif L < 0.75:
            out.append("O" if cen < 1100 else "E")
        else:
            out.append("O" if cen < 900 else "A")
    return out


class Lips:
    def __init__(self, T):
        self.lines = []                                            # (who, t0, codes)
        who = {"sofia": "sofia", "pam": "pam", "don_object": "don", "don_framed": "don", f"mom_{T['mom']}_up": "mom",
               "robot_you": "robot"}
        for name, t0, g in T["cues"]:
            if name in who:
                self.lines.append((who[name], t0, visemes(f"on_voices/{name}.wav")))

    def at(self, who, t):
        for w, t0, codes in self.lines:
            i = int((t - t0) * DRAW)
            if w == who and 0 <= i < len(codes):
                return codes[i]
        return None

    def level(self, who, t):
        m = self.at(who, t)
        return {"M": 0.0, "C": 0.4, "E": 0.6, "O": 0.75, "A": 1.0}.get(m, 0.0)


# ---- effects ---------------------------------------------------------------------------------------------------------

def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def smoke(c, t, x0, y0, h=520, alpha=0.16):
    """A curl of smoke rising through the lamp light: three soft strands, drifting."""
    for j in range(3):
        c.new_path()
        for i in range(40):
            v = i / 39
            y = y0 - v * h
            x = x0 + math.sin(v * 5.0 + t * 1.3 + j * 1.7) * (14 + 40 * v) + j * 10 + v * 30
            (c.move_to if i == 0 else c.line_to)(x, y)
        c.set_source_rgba(0.92, 0.92, 0.92, alpha * (1 - 0.25 * j)); c.set_line_width(7 - 2 * j); c.stroke()


def steam(c, t, x0, y0):
    for j in range(3):
        c.new_path()
        ph = (t * 0.6 + j / 3) % 1.0
        for i in range(24):
            v = i / 23
            y = y0 - (v + ph) * 120
            x = x0 - v * 50 + math.sin(v * 6 + t * 2 + j) * 10
            (c.move_to if i == 0 else c.line_to)(x, y)
        c.set_source_rgba(1, 1, 1, 0.35 * (1 - ph)); c.set_line_width(5); c.stroke()


RNG = np.random.default_rng(1947)
GRAIN = [RNG.normal(0, 9, (960, 540)).astype(np.int16) for _ in range(6)]


def old_film(surf, n, scale=1):
    """Grain, a little flicker, and the odd scratch: on the noir part only."""
    surf.flush()
    H, W = surf.get_height(), surf.get_width()
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data())
    g = GRAIN[n % len(GRAIN)]
    if scale > 1:
        g = np.repeat(np.repeat(g, scale, 0), scale, 1)
    fl = 1.0 + 0.025 * math.sin(n * 2.1) + 0.015 * math.sin(n * 5.3)
    for ch in range(3):
        a[..., ch] = np.clip(a[..., ch].astype(np.int16) * fl + g, 0, 255).astype(np.uint8)
    r = np.random.default_rng(n)
    if r.random() < 0.10:                                            # a scratch for one drawing
        x = int(r.uniform(40, W - 40)); w = max(1, scale)
        a[:, x:x + w, :3] = np.clip(a[:, x:x + w, :3].astype(np.int16) + 70, 0, 255).astype(np.uint8)
    surf.mark_dirty()


# ---- the beats ---------------------------------------------------------------------------------------------------

def surf():
    return cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)


class Film:
    def __init__(self, T):
        self.T = T
        self.st, self.d = T["starts"], T["durations"]
        self.lips = Lips(T)
        self.cache = {}
        self.qa = []                                                  # v7: (t, who, tip, mouth) for the tail check
        d.MOUTH_SCALED = True                                         # v7: Don's talking mouth at his close-up size
        sb.SUSPECT_TIP = (509, 929)                                   # v7: into the CCTV corner bracket
        self.P = sb.build()                                        # the static panels (captions on)
        d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
        base = surf(); sb.k2b_base(Ctx(cairo.Context(base), 0)); eng.accent_pass(base, sb.ACC)
        self.base2b = base
        pov = surf(); ssh.shot2_pov(Ctx(cairo.Context(pov), 0)); eng.accent_pass(pov, ssh.ACC)
        self.pov = pov
        dummy = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)            # where Mom's head is in 10A
        self.mom_head = ORIG["mom"](Ctx(cairo.Context(dummy), 0), 575, 1010, 2.4, pose="loom", face="shout",
                                    lean=-12, look=(-0.9, 0.8), thrust=1.0)["head"]

    def cue(self, name):
        for n, t0, g in self.T["cues"]:
            if n == name:
                return t0
        return None

    def talk(self, out, text, x, y, who, size=36, mono=False):
        """v7: the bubble's curved tail ends beside the mouth drawn in this very frame (the robot: the rim of his
        face screen), coming round the outside of the head."""
        c = cairo.Context(out)
        c.select_font_face("DejaVu Sans Mono" if mono else psh.TYPE, 0, 0); c.set_font_size(size)
        bw = max(c.text_extents(q).x_advance for q in text.split("\n")) + 40
        bxc = x + bw / 2
        U = lambda p: c.device_to_user(*p)
        if who == "robot":
            (cx, cy), (rx_, _), (_, ry_) = [U(p) for p in REC["screen"]]
            rx, ry = abs(rx_ - cx), abs(ry_ - cy)
            side = 1 if bxc >= cx else -1
            mouth = (cx, cy); tip = (cx + side * (rx + 7), cy - 0.25 * ry); head = (cx, cy, rx + 22)
        else:
            ms = [m for m in REC["mouths"] if m[0] == who]
            hd = REC["heads"].get(who)
            if ms:
                (mx, my), (mx2, _) = U(ms[-1][1]), U(ms[-1][2])
                mw = abs(mx2 - mx)
                if hd:
                    hx, hy = U(hd); LAST[(who, self.cur_beat)] = (mx - hx, my - hy, mw)
            else:                                                  # no talking mouth this drawing: this shot's last one
                ox, oy, mw = LAST[(who, self.cur_beat)]; hx, hy = U(hd); mx, my = hx + ox, hy + oy
            hx, hy = U(hd) if hd else (mx, my - 2.2 * mw)
            side = 1 if bxc >= hx else -1
            mouth = (mx, my); tip = (mx + side * (mw * 0.95 + 5), my)
            head = (hx, hy, HEAD_R.get(who, 3.4) * mw)
        self.qa.append((self.now, who, tip, mouth))
        return sb.say_curve(out, text, x, y, tip, head, size, mono)

    def beat(self, i, t):
        """The drawing of beat i at film time t (captions and bubbles included)."""
        REC["mouths"].clear(); REC["heads"].clear(); REC["screen"] = None; self.now, self.cur_beat = t, i
        st_, d_ = self.st, self.d
        tl = t - st_[i]; u = tl / d_[i]
        for k in ANIM:
            ANIM[k] = {"breath": 0.006 * math.sin(2 * math.pi * t / 3.2 + PHASE[k])}
        for who in ("sofia", "pam", "don", "mom"):
            m = self.lips.at(who, t)
            if m:
                ANIM[who]["kw"] = {"mouth": m}
        noir, say, two = sb.noir, sb.say, sb.two_cards
        if i == 0 and t < FLASH_T:                                   # v6: frame 0 is the readable office, not the flash
            return two(noir(lambda kk: sb.k1(kk, t), sb.l1), "Monday. Somebody", "left Pam a heart.")
        if i == 0:
            return noir(lambda kk: sb.k1(kk, t), lambda c: (sb.l1(c), st.flash(c, 0.5),
                                                          st.blinds(c, 0, 120, 540, 700, -0.30, 22, 10, 0.5)))
        if i == 1:
            return two(noir(lambda kk: sb.k1(kk, t), sb.l1), "Monday. Somebody", "left Pam a heart.")
        if i == 2:
            op = u > 0.22
            return noir(lambda kk: sb.k_drink(kk, open_=op, lift=10 * math.sin(math.pi * min(1, u / 0.3))))
        if i == 5:
            sf_ = self.P[i][5]; out = surf(); c = cairo.Context(out); c.set_source_surface(sf_, 0, 0); c.paint()
            smoke(c, t, 120, 980); return out
        if i == 6:                                                  # the lens rises to his eye
            b = surf(); cb = cairo.Context(b); cb.set_source_surface(self.base2b, 0, 0); cb.paint()
            ex, ey = 270 + 17 * 3.6, 1420 + d.HY * 3.6
            y = ey + (1 - ease(u / 0.45)) * 620
            pr.lens_view(cb, self.base2b, ex, y, 92, zoom=1.9, rot=1.1)
            st.hard_side(cb, 360, 0.1, 0.35); smoke(cb, t, 110, 990); return b
        if i == 7:                                                  # POV: the lens drifts onto heart and lips
            L = surf(); cl = cairo.Context(L); cl.set_source_surface(self.pov, 0, 0); cl.paint()
            cl.set_source_rgba(0, 0, 0, 0.45); cl.rectangle(0, 0, 540, 960); cl.fill()
            x = 280 - 60 * (1 - ease(u / 0.5)); y = 405 + 40 * (1 - ease(u / 0.5))
            pr.lens_view(cl, self.pov, x, y, 165, zoom=1.12, rot=1.25)
            if t >= self.cue("don_sofia") - 0.05:
                sb.say_curve(L, "Sofía… did you\nsteal my heart?", 120, 690, (165, 972), None, 36)   # v7: Don off screen, below
            return L
        if i == 8:
            s3 = sb.b_shot3(stroke=0.5 + 0.5 * math.sin(t * 7.0))
            c3 = cairo.Context(s3); smoke(c3, t, 70, 990, 700, 0.12)
            if t >= self.cue("sofia") - 0.05:
                self.talk(s3, "I sign my work\u2026\ndarling.", 150, 40, "sofia", 34)
            return s3
        if i == 9:                                                  # v5: the partner tips his fedora (antenna)
            foot = psh.cctv(psh.frame5(0.0, lean=4 + 8 * ease(u)), "MON 08:59:14")
            lift = math.sin(math.pi * min(1.0, max(0.0, (tl - 0.25) / 0.75)))
            out = surf(); sb.k4(Ctx(cairo.Context(out), 0), foot, hat_lift=max(lift, 1e-6))
            eng.accent_pass(out, sb.ACC)
            return two(out, "My partner.", "Never blinks.")
        if i == 10:
            f = psh.frame5(0.0, lean=4 + 8 * ease(u))
            return psh.cctv(f, "MON 08:59:14")
        if i == 16:                                                 # the partner turns and points
            arm = ease(tl / 0.3)
            out = noir(lambda kk: sb.k_you(kk, arm, screen=arm >= 0.999), lambda c: st.hard_side(c, 330, 0.1, 0.4))
            if t >= self.cue("robot_you") - 0.03:
                self.talk(out, "You.", 330, 60, "robot", 40, mono=True)
            return out
        if i == 17:
            ANIM["don"].setdefault("kw", {})["look"] = (0.3, 0.95 * ease(u / 0.5))
            return sb.b_shot6("eyes")
        if i == 19:
            return sb.b_shot6("snap")
        if i == 20:
            ANIM["don"]["blink"] = 0.35 < u < 0.5
            return sb.b_shot6("mask")
        if i == 21:                                                  # Pam says the line
            out = surf(); pms.shot7a(Ctx(cairo.Context(out), 0)); eng.accent_pass(out, sb.ACC)
            ca = cairo.Context(out)
            pms.soft_light(ca, 165, 1010 + pn.HY * 2.0, 230, 0.30)
            eng.side_light(ca, 300, 0, 240, 960, from_left=True, amount=0.45)
            if t >= self.cue("pam") - 0.05:
                self.talk(out, "You left me\nyour heart.", 40, 60, "pam", 36)
            return out
        if i in (23, 24):
            a0, a1 = ((0.0, 0.0), (-0.1, 0.95)) if i == 23 else ((-0.1, 0.95), (-0.5, -0.6))
            e = ease(u / 0.6)
            ANIM["don"].setdefault("kw", {})["look"] = (a0[0] + (a1[0] - a0[0]) * e, a0[1] + (a1[1] - a0[1]) * e)
            return sb.b_shot6("down" if i == 23 else "up")
        if i == 26:
            out = noir(sb.k8, sb.l8)
            if t >= self.cue("don_framed") - 0.05:
                self.talk(out, "I was framed!", 40, 60, "don", 36)
            return out
        if i in (27, 28, 29):                                        # the shadow grows over the whole of shot 9
            g = ease((t - st_[27]) / (st_[29] + 0.3 - st_[27]))
            out = noir(lambda kk: sb.k9(kk, g, rain_t=t), setsh.l9)
            if i == 27:
                two(out, "Nobody tells me", "what to do.")
            elif i == 28:
                two(out, "Whiskey. Money.", "Women.")
            else:
                sb.shout(out, "DONNIE!")
            return out
        if i == 30:
            out = sb.colour(setsh.k10a)
            c = cairo.Context(out); steam(c, t, 545, 600)
            if tl < 2.0 / DRAW:                                       # v5: the boss shadow flashes over Mom
                hx, hy = self.mom_head
                c.save(); c.rectangle(hx - 170, 0, 540, 960); c.clip()          # on Mom only, not on Don's face
                st.mom_shadow(Ctx(c, 0), hx, hy - mo.HY * 2.4, 2.4, skew=0.0, alpha=0.82, head=1.0, big=True)
                c.restore()
            if t >= self.cue(f"mom_{self.T['mom']}_up") - 0.05:
                self.talk(out, "Up.\nTime for work.", 30, 50, "mom", 36)
            return out
        if i in (31, 32, 33):
            beat = i - 30
            hand = None
            if beat == 2:                                            # v5: the bunny... then the milk
                if u < 0.5:
                    e = ease(u / 0.35); look = (-0.6 * e, 0.3 + 0.65 * e)
                else:
                    e = ease((u - 0.55) / 0.3); look = (-0.6 + 1.6 * e, 0.95 - 0.1 * e)
                ANIM["don"].setdefault("kw", {}).update(look=look, face="neutral")   # pupils that can travel
                ANIM["don"]["blink"] = 0.48 < u < 0.56
            sweat = True
            if beat == 3:                                            # v6: slide under, then the brim comes down (C)
                e3 = ease((u - 0.5) / 0.3)
                drop = 8.5 * e3
                d.PJ_BRIM_DROP, d.PJ_HAT_SCALE, d.PJ_BRIM_FLAP = drop, 1.0 + 0.12 * e3, 0.42 * e3
                ANIM["don"].setdefault("kw", {}).update(look=(0.2, 0.6) if e3 < 0.5 else (0.15, 0.2),
                                                        **({"face": "squint"} if e3 >= 0.5 else {}))
                sweat = u < 0.5                                      # dignity restored: no more sweat
                if 0.42 < u < 0.9:
                    s_ = sb.HEART0[2] / 13.0
                    x = sb.HEART0[0] - 25 * s_; feet = sb.HEART0[1] - (d.BT + 48) * s_
                    hand = (x + 46 * s_, feet + (d.HY - 26 - 6 + drop) * s_ + (2 + 18 * e3) * s_, s_,
                            feet + d.HY * s_ + 74 * s_)                      # on the brim's bent front; the shoulder
            try:
                out = sb.colour(lambda kk: sb.k10b(kk, beat, slide=ease(u / 0.4) if beat == 3 else 1.0, sweat=sweat))
            finally:
                d.PJ_BRIM_DROP, d.PJ_HAT_SCALE, d.PJ_BRIM_FLAP = 0.0, 1.0, 0.0
            if hand:                                                 # one finger on the brim, the sleeve from below
                hx, hy, s_, sy = hand
                c = cairo.Context(out); kk = Ctx(c, 0)
                kit.cut(kk, [(hx + 4 * s_, sy), (hx + 20 * s_, sy), (hx + 7 * s_, hy + 12 * s_), (hx - 7 * s_, hy + 12 * s_)],
                        (0.66, 0.80, 0.93), shadow=False, lw=2.2)
                kit.ellipse(kk, hx, hy + 9 * s_, 8 * s_, 7 * s_, d.SKIN, 871, shadow=False, lw=2.2)
                kit.cut(kk, [(hx - 2.2 * s_, hy + 5 * s_), (hx + 2.2 * s_, hy + 5 * s_), (hx + 2.2 * s_, hy - 1 * s_),
                             (hx - 2.2 * s_, hy - 1 * s_)], d.SKIN, shadow=False, lw=2.0)
            if int(t * 1.5) % 2:                                     # the baby monitor's light blinks
                c = cairo.Context(out); c.set_source_rgb(0.10, 0.35, 0.16)
                c.arc(455 + 15 * 1.5, 62 - 18 * 1.5, 3.2 * 1.5, 0, 2 * math.pi); c.fill()
            return out
        return self.P[i][5]                                          # a held panel

    def camera(self, i, t):
        """zoom, dx, dy for beat i at t: a slow push, the zoom punch on the SNAG, the jolts."""
        st_, d_ = self.st, self.d
        tl = t - st_[i]; u = tl / d_[i]
        z = 1.0 + 0.035 * u if i not in (0, 1) else 1.0 + 0.05 * (t / (st_[1] + d_[1]))
        dx = dy = 0.0
        if i == 12:
            z *= 1 + 0.07 * math.exp(-tl / 0.14)
        jolts = [(st_[19], 9, 0.22), (st_[29], 16, 0.45), (st_[30], 8, 0.25)]
        for t0, amp, dur in jolts:
            if 0 <= t - t0 < dur:
                k = (1 - (t - t0) / dur) * amp
                r = np.random.default_rng(int(t * DRAW))
                dx += r.uniform(-k, k); dy += r.uniform(-k, k)
        return z, dx, dy


class _HiSurfaces:
    """Release mode: every 540x960 surface the drawing code asks for is made at 1080x1920 with a device scale of
    2, so all drawing (lines, text, the accent pass) is native 1080, not an enlarged 540 picture."""
    def __init__(self, orig):
        self._orig = orig

    def __call__(self, fmt, w, h):
        if (w, h) == (540, 960):
            s = self._orig(fmt, 1080, 1920); s.set_device_scale(2, 2); return s
        return self._orig(fmt, w, h)

    def __getattr__(self, n):
        return getattr(self._orig, n)


def hi_on():
    ORIG["surface"] = cairo.ImageSurface
    cairo.ImageSurface = _HiSurfaces(ORIG["surface"])
    ro.LOGICAL_FOOTAGE, pr.ENHANCE_LOGICAL = (540, 960), (540, 960)


def hi_off():
    cairo.ImageSurface = ORIG["surface"]
    ro.LOGICAL_FOOTAGE, pr.ENHANCE_LOGICAL = None, None


def master(src="on_mix.wav", out="on_mix_master.wav", target=-15.0, limit=0.60):   # 0.80 overshot to +0.3 dBTP after AAC
    """The release audio: stereo first (panning adds loudness), one flat gain to the target, then a limiter
    (loudnorm's dynamic mode would flatten the DONNIE! hit)."""
    import re
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ac", "2", "/tmp/on_st.wav"], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", "/tmp/on_st.wav", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
    g = target - I
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/on_st.wav", "-af",
                    f"volume={g:.2f}dB,alimiter=limit={limit}:attack=2:release=60:level=disabled", out], check=True)
    return out, I, g


def render(mode="preview"):
    T = json.load(open("on_timing.json"))
    scale = 1 if mode == "preview" else 2
    W, H = 540 * scale, 960 * scale
    out_path = "on_film_preview.mp4" if mode == "preview" else "on_film_1080.mp4"
    patch()
    audio = "on_mix.wav"
    if mode != "preview":
        hi_on()
        audio, I0, g = master()
        print(f"  master: {I0:.1f} LUFS stereo, gain {g:+.1f} dB")
    try:
        F = Film(T)
        n_draw = int(round(T["total"] * DRAW))
        cmd = (["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
               "-r", str(FPS), "-i", "-", "-i", audio] +
               (["-af", "loudnorm=I=-15:TP=-1.5:LRA=11"] if mode == "preview" else []) +
               ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-c:v", "libx264",
               "-preset", "veryfast" if mode == "preview" else "slow", "-crf", "20" if mode == "preview" else "23",
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest", out_path])
        if mode != "preview":                                          # BT.709 tags on the release
            cmd[-1:-1] = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        frame = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for n in range(n_draw):
            t = n / DRAW
            i = max(k for k in range(len(F.st)) if F.st[k] <= t + 1e-9)
            src = F.beat(i, t)
            z, dx, dy = F.camera(i, t)
            noirpart = t < F.st[30]
            if noirpart:                                               # the gate weave
                r = np.random.default_rng(n + 7)
                dx += r.uniform(-0.8, 0.8); dy += r.uniform(-0.8, 0.8)
            c = cairo.Context(frame)
            c.set_source_rgb(0, 0, 0); c.paint()
            c.scale(scale, scale)
            c.translate(270 + dx, 480 + dy); c.scale(z, z); c.translate(-270, -480)
            c.set_source_surface(src, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
            if i == 0 and t >= FLASH_T:                                # the flash: bright, then it decays (v6: from 0.13 s)
                c2 = cairo.Context(frame)
                a = 0.85 if t < FLASH_T + 1 / DRAW else 0.85 * math.exp(-(t - FLASH_T - 1 / DRAW) / 0.12)
                c2.set_source_rgba(1, 1, 1, a); c2.paint()
            if noirpart:
                old_film(frame, n, scale)
            frame.flush()
            buf = bytes(frame.get_data())
            p.stdin.write(buf); p.stdin.write(buf)                     # each drawing held for 2 frames
            if n % 60 == 0:
                print(f"  {t:5.1f} s", flush=True)
        p.stdin.close(); p.wait()
    finally:
        unpatch()
        if mode != "preview":
            hi_off()
        d.FEDORA_BAND, d.FEDORA_RIM = None, False
    print("wrote", out_path)


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "preview")
