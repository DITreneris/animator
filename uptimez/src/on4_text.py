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
CARD_Y = {"n6": 276}                                         # 2.4: she stands on the platform at the top of the frame: the card under her feet, over the bills
SPEAKER = {"PAM": "pam", "DON": "don", "CLIENT": "client", "SOFIA": "sofia"}
_done = [False]


def _wrap(mod, name, who):
    f = getattr(mod, name)
    def w(k, x, feet, s=1.0, *a, **kw):
        o = f(k, x, feet, s, *a, **kw)
        try:
            hx, hy = o["head"]
            dx, dy = k.c.user_to_device(hx, hy)
            rx, ry = k.c.user_to_device_distance(R_HEAD[who] * s, 0)
            HEADS[who] = (dx, dy, math.hypot(rx, ry))
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
                fr = m.TESTS[t_](sub=2)[a:b]
                s = fr[j] if len(fr) >= count else fr[min(len(fr) - 1, int(j * len(fr) / count))]
                return s, BY.get(id(s), {}), span[0]
            f, _dur = an.SHOTS[ids[i]]
            HEADS.clear()
            s = f(j / float(F.DPS))
            return s, dict(HEADS), span[0]
        n += count; i += len(span)
    raise ValueError(T)


def put(s, line, heads):
    """the line's card or bubble on a copy of the drawing; returns (surface, faults)"""
    key, t0, t1, kind, who, txt = line
    o = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); c = cairo.Context(o); c.set_source_surface(s, 0, 0); c.paint()
    if kind == "card":
        y0 = CARD_Y.get(key, 100)
        y1 = a3._card(c, txt, y0)
        c.select_font_face("Special Elite", 0, 0); c.set_font_size(30)
        wmax = max(c.text_extents(w_).x_advance for w_ in [txt]) + 24
        box = (18, y0, min(522, 18 + wmax), y1 - 6)
        faults = ["CARD over %s's face" % who_ for who_, f_ in heads.items() if gate._over_face(box, f_)]
        return o, faults
    if kind == "named":
        box, tip = speech.draw(c, txt, None, name=who)
        return o, gate.check(o, box, tip, list(heads.values()))
    me = SPEAKER[who]
    if me not in heads:
        return o, ["NO HEAD measured for %s" % who]
    before = gate.snapshot(o)
    others = [v for k_, v in heads.items() if k_ != me]
    box, tip = speech.draw(c, txt, heads[me], others=others)
    return o, gate.check(o, box, tip, [heads[me]] + others, before=before)


def stills(out="../office-noir-4/on4_text_stills_v1.png", debug=False):
    install()
    ls, tm = lines()
    tiles = []; rep = []
    for ln in ls:
        T = ln[1] + min(0.45, (ln[2] - ln[1]) / 2)
        s, heads, shot = frame_at(T, tm)
        o, faults = put(s, ln, heads)
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


if __name__ == "__main__":
    stills()
