"""OFFICE NOIR 4: the words on the approved motion (24 Nov). Narration (Pam-Cat, off screen) as typewriter cards at the
top (on3_animatic._card, Office Noir 2 and 3); Father's off-screen line as a named card (speech.draw, head None);
the speakers seen on screen get a bubble (speech.draw) and every bubble is checked on its pixels (speech_gate.check).
Heads are measured where the rigs drew them: each rig's own head point through the drawing's matrix, never typed.

  python3 on4_text.py   ->  ../office-noir-4/on4_text_stills_v1.png  (one drawing per line, under the app's dead zones)"""
import math
import cairo
import on4_film as F
import on4_scenes as sc
import on4_motion as m
import on4_anim as an
import on4_rough as r
import on4_cast as oc
import on4_street as st
import client_ob as co
import sofia_dh as sd
import on3_animatic as a3
import speech
import speech_gate as gate

HEADS = {}                                                   # who -> (x, y, r) on the screen, in the drawing being made
BY = {}                                                      # id(surface) -> its heads
R_HEAD = {"pam": 47.0, "sofia": 47.0, "client": 52.0, "don": 47.0, "pam_awake": 47.0}
CARD_Y = {"n6": 276}
SPLIT = {"n2": ("I know where to see", "what others do not see."),      # a two-row card is shown one row at a time, each while it is spoken:
         "n3": ("I am like a cat.", "I have seven lives.")}              # one row is clear of her head in 2.1 (two rows covered it for a second) and reads faster                                         # 2.4: she stands on the platform at the top of the frame: the card under her feet, over the bills
SPEAKER = {"PAM": "pam", "DON": "don", "CLIENT": "client", "SOFIA": "sofia"}
_done = [False]
_FR = {}                                                     # a motion test's drawings, made once
LINGER = 0.20
CARD_HALO = [True]                                                # a bubble stays this long after its last word (never over a cut)


CLOCK = {"say": {}, "blink": set(), "live": False}           # set per drawing by the film: who is saying which mouth shape, whose eyes are shut
SHUT_FACES = ("squint", "happy", "pleased", "smug", "fade")
LIP = (0.62, 0.20, 0.26)


def _skin(who):
    import kit
    if who == "client":
        return co.SKIN
    if who == "sofia":
        import sofia_v4 as s4
        return s4.SKIN
    return kit.PEOPLE["DON" if who == "don" else "PAM"]["skin"]


def _wrap(mod, name, who):
    import iwry_mouths as im
    f = getattr(mod, name)
    def w(k, x, feet, s=1.0, *a, **kw):
        code = CLOCK["say"].get(who) if CLOCK["live"] else None
        shut = CLOCK["live"] and who in CLOCK["blink"]
        if code and who in ("client", "sofia"):
            kw = dict(kw); kw["mouth"] = code                # these two rigs draw the spoken mouth themselves
        if code and who == "don" and kw.get("whistle_in"):
            kw = dict(kw); kw["whistle_in"] = False          # he lets the whistle hang on its cord while he speaks
        if who == "pam":
            oc.BLINK[0] = bool(shut)
        try:
            o = f(k, x, feet, s, *a, **kw)
        finally:
            if who == "pam":
                oc.BLINK[0] = False
        try:
            hx, hy = o["head"]
            c = k.c
            face = a[1] if len(a) > 1 else kw.get("face", "")
            if code and who == "don":
                c.save(); c.translate(hx, hy); c.scale(s, s); im.don_mouth(sc.Ctx(c, 0), (0, 0), code, kw.get("chin", 0)); c.restore()
            if code and who == "pam":
                c.save(); c.translate(hx, hy); c.scale(s, s); im.mouth(sc.Ctx(c, 0), 0, 31, code, _skin(who), lip_col=LIP, erase=(19, 11), seed=67); c.restore()
            if shut and who in ("client", "don", "sofia") and face not in SHUT_FACES:
                c.save(); c.translate(hx, hy); c.scale(s, s)
                for sx in (-17, 17):
                    c.new_path(); c.arc(sx, 4, 12.5, 0, 2 * math.pi); c.set_source_rgb(*_skin(who)); c.fill()
                    c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(3.0); c.set_line_cap(1); c.move_to(sx - 9, 6); c.curve_to(sx - 3, 9, sx + 3, 9, sx + 9, 6); c.stroke(); c.set_line_cap(0)
                c.restore()
            dx, dy = c.user_to_device(hx, hy)
            rx, ry = c.user_to_device_distance(R_HEAD[who] * s, 0)
            if -60 < dx < 600 and -60 < dy < 1020:               # a figure drawn off the frame has no head on it
                h_ = (dx, dy, math.hypot(rx, ry))
                if who in HEADS and math.hypot(HEADS[who][0] - dx, HEADS[who][1] - dy) > 4:
                    HEADS["%s#%d" % (who, len(HEADS))] = HEADS[who]   # a second figure from the same rig (the card players): kept as a face to keep clear of
                HEADS[who] = h_
        except Exception:
            pass
        return o
    setattr(mod, name, w)


def install():
    if _done[0]:
        return
    _done[0] = True
    _wrap(oc, "pam_cat", "pam"); _wrap(oc, "don_cop2", "don"); _wrap(co, "client", "client"); _wrap(sd, "sofia", "sofia"); _wrap(oc, "pam_awake", "pam_awake")
    g0 = m.Lazy.get
    def get(self):
        if hasattr(self, "_s"):
            return self._s
        HEADS.clear()
        s = g0(self)
        BY[id(s)] = dict(HEADS)
        return s
    m.Lazy.get = get


def _split_at(key, a_, b_):
    """seconds into the take where its second half starts: the longest quiet stretch in the middle half of the take
    (a sentence stop), else the halves' share of the letters"""
    import numpy as np
    import os
    L = r.LENS[key]
    try:
        if key in r.NARR:
            w = r.load(os.path.join(r.narr_takes(sc._timing()[1].get("narration", "A")), key + ".wav"))
        else:
            w = r.stops(r.load(os.path.join(r.vo.OUT, "takes_v1", key + ".wav")), " ".join(p_[0] for p_ in r.vo.LINES[key][2]))
        hop = int(r.SR * 0.02); e = np.array([np.abs(w[i:i + hop]).mean() for i in range(0, len(w) - hop, hop)])
        q = e < 0.06 * e.max(); best = (0, 0); i = 0
        while i < len(q):
            if q[i]:
                j = i
                while j < len(q) and q[j]:
                    j += 1
                mid = (i + j) / 2.0 * 0.02
                if 0.25 * L < mid < 0.75 * L and j - i > best[0]:
                    best = (j - i, mid)
                i = j
            else:
                i += 1
        if best[0] * 0.02 >= 0.12:
            return best[1]
    except Exception:
        pass
    return L * len(a_) / float(len(a_) + len(b_))


def lines():
    """every line: (key, start, end, kind, who, text). kind: "card" (the narrator), "named" (off screen), "bubble"."""
    tm, d = sc._timing()
    total = sum(v["dur"] for v in tm.values())
    _mix, marks, _ev = r.sound(tm, d, total)
    out = []
    for key, t0 in marks:
        if key in r.NEW:
            _shot, _lead, who, txt = r.NEW[key]
            kind = "named" if who == "FATHER" else "bubble"
        elif key in r.NARR:
            who, txt = "PAM_N", r.NARR[key][2]
        else:
            ln = d["lines"][key]
            who = ln.get("who", "PAM_N"); txt = " ".join(p_[0] for p_ in r.vo.LINES[key][2])
        if key not in r.NEW:
            kind = "card" if who == "PAM_N" else "bubble"
        if key in SPLIT and kind == "card":
            a_, b_ = SPLIT[key]; cut_ = t0 + _split_at(key, a_, b_)
            out.append((key + "a", t0, cut_, kind, who, a_)); out.append((key + "b", cut_, t0 + r.LENS[key], kind, who, b_))
            continue
        out.append((key, t0, t0 + r.LENS[key], kind, who, txt))
    return sorted(out, key=lambda x: x[1]), tm


def frame_at(T, tm):
    """the film's drawing at time T and the heads measured in it"""
    N = int(T * F.DPS)
    ids = [x["id"] for _, ss in sc.SCENES for x in ss]
    n = 0; i = 0
    while i < len(ids):
        grp = next((g for g in F.MOT if g[0] == ids[i]), None)
        span = grp if grp else (ids[i],)
        end = tm[span[-1]]["start"] + tm[span[-1]]["dur"]
        count = int(round(end * F.DPS)) - n
        if n <= N < n + count:
            j = N - n
            if grp:
                t_, a, b = F.MOT[grp]
                if t_ not in _FR:
                    _FR[t_] = m.TESTS[t_](sub=2)
                fr = _FR[t_][a:b]
                s = fr[j] if len(fr) >= count else fr[min(len(fr) - 1, int(j * len(fr) / count))]
                return s, BY.get(id(s), {}), span[0]
            f, _dur = an.SHOTS[ids[i]]
            HEADS.clear()
            s = f(j / float(F.DPS))
            return s, dict(HEADS), span[0]
        n += count; i += len(span)
    raise ValueError(T)


def put(s, line, heads, pin=None):
    """the line's card or bubble on a copy of the drawing; returns (surface, faults)"""
    key, t0, t1, kind, who, txt = line
    o = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); c = cairo.Context(o); c.set_source_surface(s, 0, 0); c.paint()
    if kind == "named":                                      # (the cards' audit, 24 Nov) the off-screen voice in the narrator's cream card, his name in front: two styles on screen, not three
        txt = '%s: "%s"' % (who, txt); kind = "card"
    if kind == "card":
        y0 = CARD_Y.get(key.rstrip('ab') if key[:-1] in SPLIT else key, 100)
        if CARD_HALO[0]:                                     # (the cards' audit) a soft dark edge all round the card, so cream on a white wall still has a shape
            c.push_group(); a3._card(c, txt, y0); pat = c.pop_group()
            for r_, al in ((7, 0.10), (4, 0.14), (2, 0.18)):
                for q in range(8):
                    c.save(); c.translate(r_ * math.cos(q * math.pi / 4), r_ * math.sin(q * math.pi / 4) + 1); c.set_source_rgba(0, 0, 0, al); c.mask(pat); c.restore()
        y1 = a3._card(c, txt, y0)
        c.select_font_face("Special Elite", 0, 0); c.set_font_size(30)
        wmax = c.text_extents(txt).x_advance + 24
        box = (18, y0, min(522, 18 + wmax), y1 - 6)
        return o, ["CARD over %s's face" % who_ for who_, f_ in heads.items() if gate._over_face(box, f_)], box
    me = SPEAKER[who]
    if me not in heads:
        return o, ["NO HEAD measured for %s" % who], None
    before = gate.snapshot(o)
    others = [v for k_, v in heads.items() if k_ != me]
    box, tip = speech.draw(c, txt, heads[me], others=others, pin=pin)
    return o, gate.check(o, box, tip, [heads[me]] + others, before=before), box


def stills(out="../office-noir-4/on4_text_stills_v1.png", debug=False):
    install()
    ls, tm = lines()
    tiles = []; rep = []
    for ln in ls:
        T = ln[1] + min(0.45, (ln[2] - ln[1]) / 2)
        s, heads, shot = frame_at(T, tm)
        o, faults, _box = put(s, ln, heads)
        c = cairo.Context(o)
        if debug:
            for who, (hx, hy, hr) in heads.items():
                c.set_source_rgba(0, 1, 0, 0.8); c.set_line_width(2); c.new_path(); c.arc(hx, hy, hr, 0, 2 * math.pi); c.stroke()
        st.overlay(c)
        c.set_source_rgba(0, 0, 0, 0.35); c.rectangle(0, 0, 540, 96); c.fill()                      # the app's bar
        tiles.append(o); rep.append((ln[0], shot, round(ln[1], 2), round(ln[2], 2), ln[3], ln[4], ln[5], faults))
        print(rep[-1], flush=True)
    cols = 8; w = 270; h = 480; rows = (len(tiles) + cols - 1) // cols
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * w, rows * (h + 26)); c = cairo.Context(S); c.set_source_rgb(0.12, 0.12, 0.13); c.paint()
    for i, o in enumerate(tiles):
        x, y = (i % cols) * w, (i // cols) * (h + 26)
        c.save(); c.translate(x, y + 26); c.scale(0.5, 0.5); c.set_source_surface(o, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 0.6); c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.move_to(x + 6, y + 18)
        c.show_text("%s  %s  %.1f s%s" % (rep[i][0], rep[i][1], rep[i][2], "  FAULT" if rep[i][7] else ""))
    S.write_to_png(out)
    return tiles, rep


def follow(pin, ph, head):
    """the pinned box goes with the cheek it points at once that has moved more than 3 px from where the box was put
    (a speaker who walks, a camera that pushes in); under that only the tail moves (lesson 784)"""
    if pin is None or ph is None or head is None:
        return pin, ph
    side = 1 if (pin[0] + pin[2]) / 2.0 > ph[0] else -1
    tip = lambda h_: (h_[0] + side * 0.82 * h_[2], h_[1] + 0.35 * h_[2])
    (ax, ay), (bx, by) = tip(ph), tip(head)
    dx, dy = bx - ax, by - ay
    if math.hypot(dx, dy) <= 1.0:
        return pin, ph
    w, h = pin[2] - pin[0], pin[3] - pin[1]
    x0 = min(max(pin[0] + dx, gate.SAFE[0]), gate.SAFE[2] - w); y0 = min(max(pin[1] + dy, gate.SAFE[1]), gate.SAFE[3] - h)
    return (x0, y0, x0 + w, y0 + h), head


def shot_end(T, tm):
    for v in tm.values():
        if v["dur"] > 0 and v["start"] <= T < v["start"] + v["dur"]:
            return v["start"] + v["dur"]
    return T


def audit(sheet="../office-noir-4/on4_text_audit_v1.png"):
    """every drawing of every line: the text put, the gate run; the box pinned at the line's first drawing.
    Returns [(key, drawings, faults by kind, times the box moved)] and writes first / middle / last of each line."""
    install()
    ls, tm = lines()
    rep = []; tiles = []; labels = []
    for ln in ls:
        key, t0, t1, kind = ln[0], ln[1], ln[2], ln[3]
        end = t1 if kind != "bubble" else min(t1 + LINGER, shot_end(t0, tm) - 1.0 / F.DPS)
        n0, n1 = int(round(t0 * F.DPS)), int(round(end * F.DPS))
        pin = None; ph = None; moved = 0; faults = {}; keep = {}
        for N in range(n0, n1 + 1):
            s, heads, shot = frame_at(N / float(F.DPS) + 1e-4, tm)
            pin, ph = follow(pin, ph, heads.get(SPEAKER.get(ln[4])))
            o, fl, box = put(s, ln, heads, pin)
            if kind == "bubble" and box is not None:
                if pin is not None and max(abs(a_ - b_) for a_, b_ in zip(pin, box)) > 0.5:
                    moved += 1                               # a jump: the gate's rules threw the pinned box out
                if pin is None or max(abs(a_ - b_) for a_, b_ in zip(pin, box)) > 0.5:
                    ph = heads.get(SPEAKER.get(ln[4]))
                pin = box
            for f_ in fl:
                faults.setdefault(f_.split(" at (")[0], []).append(N)
            if N in (n0, (n0 + n1) // 2, n1):
                keep[N] = o
        rep.append((key, n1 - n0 + 1, {k_: (len(v), v[0], v[-1]) for k_, v in faults.items()}, moved))
        print(rep[-1], flush=True)
        for N in sorted(keep):
            c = cairo.Context(keep[N]); st.overlay(c); c.set_source_rgba(0, 0, 0, 0.35); c.rectangle(0, 0, 540, 96); c.fill()
            tiles.append(keep[N]); labels.append("%s %.2f s%s" % (key, N / float(F.DPS), "  FAULT" if faults else ""))
    cols = 12; w = 180; h = 320; rows = (len(tiles) + cols - 1) // cols
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * w, rows * (h + 22)); c = cairo.Context(S); c.set_source_rgb(0.12, 0.12, 0.13); c.paint()
    for i, o in enumerate(tiles):
        x, y = (i % cols) * w, (i // cols) * (h + 22)
        c.save(); c.translate(x, y + 22); c.scale(w / 540.0, w / 540.0); c.set_source_surface(o, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 0.6); c.select_font_face("Inter", 0, 1); c.set_font_size(13); c.move_to(x + 4, y + 16); c.show_text(labels[i])
    S.write_to_png(sheet)
    return rep


if __name__ == "__main__":
    stills()
