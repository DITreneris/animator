"""OFFICE NOIR 3: the whole film as one moving rough (20 Nov), v1. No sound, no text. 30 fps, 540x960.
Beats 01 to 04 and 08 move here for the first time (parameters of the staged frames, run through time); beats 05 to 07
are the ring roughs' own shots (ring_rough_on3 v9, ring_rough2_on3 v3), with the button's insert cut in after 5.4 and
inside 7.4. The last frame is the first frame: 8.5 ends on 1.1's first drawing.
render(out) -> the film. sheets(d) -> contact sheets at 2 fps, numbered, and one small sheet."""
import math
import os
import cairo
import ring_rough_on3 as rr
import ring_rough2_on3 as rr2
import street_on3 as st
import street_casts_on3 as stc
import alley_on3 as al
import door_on3 as dr
import office_on3 as of
import garage_on3 as ga
import client_on3 as b
from ring_rough_on3 import lerp

R5, F5 = tuple(rr.SHOTS), dict(rr.FN)
K = dict(cards="deck", v4=True, v6=True)
T0 = 0.45                                                   # ring_rough2's 7.5 at this time is the film's first drawing: the glove an inch away


def ramp(t, a, d):
    """0 before a, 1 after a + d, smooth between."""
    return lerp(0.0, 1.0, (t - a) / d)


def bob(t, n=3.2, h=3.0):
    return abs(math.sin(t * math.pi * n)) * h


# ---- 01 the punch -------------------------------------------------------------------------------------------------
def s11(t):
    return rr2.shot_75(T0 + t)                               # lands at 0.3 s, white by 0.5


# ---- 02 the street ------------------------------------------------------------------------------------------------
def _rain(t):
    return 1 + int(t * 10) % 4


def s21(t):
    return st.frame("S1", [stc.client(lerp(210.0, 400.0, t / 1.5))], rain=_rain(t))


def s22(t):
    return st.frame("S1", [stc.client(400)], car=(lerp(980.0, 250.0, t / 1.1), 0.0), rain=_rain(t))


def s24(t):
    return st.window_pov(ramp(t, 0.2, 0.4) - ramp(t, 2.4, 0.3), ramp(t, 0.7, 0.5), ramp(t, 1.4, 0.8), door=True)


def s24b(t):
    return st.frame("S2", [stc.with_folder(400)], car=(lerp(250.0, -700.0, (t - 0.2) / 1.0), 0.0), rain=_rain(t))


def s25(t):
    return st.cv_insert(0.0)


def s26(t):
    return st.frame("S3", [stc.sofia(lerp(900.0, 690.0, t / 0.9)), stc.with_folder(450)], rain=_rain(t))


def s27(t):
    return st.cv_insert(0.0 if t < 0.35 else 1.0)


# ---- 03 the alley -------------------------------------------------------------------------------------------------
def s31(t):
    return al.frame2("A1", [al.client(lerp(-30.0, 70.0, t / 1.2))], al.gang("aim", ramp(t, 0.6, 1.0) * 0.5))


def s32(t):
    return al.frame2("A2w", [al.fumble(130 + math.sin(t * 22) * 1.5)], al.gang("aim", 0.5 + 0.5 * ramp(t, 0.0, 1.4)))


def s32b(t):
    (lx, ly), (rx, ry) = al._probe(130)["hands"]
    return al.frame2(((lx + rx) / 2 + 6, (ly + ry) / 2 + 6 + bob(t, 4, 2), 3.6), [al.fumble(130 + math.sin(t * 22) * 1.5)], al.gang("aim", 1))


def s33(t):
    return al.frame2("A3w", [al.fumble(150)], al.gang("aim" if t < 0.5 else "down", 1))


def s33b(t):
    tx, ty = al._tip(130)
    lit = t > 0.75
    return al.frame2("A2", [al.fumble(130, lit=lit), al.lighter_hand(tx + 13 + lerp(230.0, 0.0, t / 0.45), ty + 46, 0.9, flame=t > 0.5)], al.gang("down", 1))


def s34(t):
    x = lerp(180.0, 700.0, t / 1.5)
    return al.frame2("A1", [al.client(x, "b_walk", (0.9, 0), cig=x < 300)], al.gang("down", 0, True), cig=300 if x >= 300 else None)


def s34b(t):
    return al.frame2("A3w", [al.don(lerp(140.0, 346.0, t / 0.7))], al.gang("down" if t < 0.9 else "up", 0, t < 0.9), cig=300)


# ---- 04 the price -------------------------------------------------------------------------------------------------
def s41(t):
    return dr.behind(ramp(t, 0.5, 0.6))


def s42(t):
    if t < 0.5:
        return dr.face((0.2, -0.9))
    if t < 1.0:
        return dr.face((-0.7, 0.9))
    return dr.face((0.2, -0.9), glove=1.0, push=0.45 * ramp(t, 1.0, 0.25))


def s43(t):
    return of.over(ramp(t, 0.2, 0.5), show=True, cards="deck", v4=True)


def s44(t):
    pay = 0.0 if t < 0.5 else 0.3 + 0.7 * ramp(t, 0.5, 0.45)
    take = 1.0 if t >= 1.2 else 0.0
    tk = ramp(t, 1.6, 0.5) if t >= 1.6 else None
    return of.reverse(pay, take, turn=0 if take else None, ticket=tk, **K)


def s44a(t):
    return of.ticket_insert(ramp(t, 0.0, 0.35))


def s44t(t):
    return of.reverse(1.0, 1.0, turn=ramp(t, 0.1, 1.0), ticket=1.0, eyes=(0.3, 0.9) if t > 0.9 else None, **K)


def s44b(t):
    return of.tower_insert(ramp(t, 0.3, 0.5), v5=True)


def s44c(t):
    return dr.react(t >= 0.8)


# ---- 05 to 07 the ring: the roughs' own shots, with the button ----------------------------------------------------
def s54b(t):
    return of.button_insert(ramp(t, 0.0, 0.2))


def s74a(t):
    return rr2.shot_74(t)                                    # the cracked screen asks; her office (to 1.1)


def s74c(t):
    return rr2.shot_74(1.1 + t)                              # her mouth; the tick


# ---- 08 awake -----------------------------------------------------------------------------------------------------
def _buzzing(fn, t):
    real = ga.buzz
    if int(t * 8) % 2:
        ga.buzz = lambda *a, **k_: None
    try:
        return fn()
    finally:
        ga.buzz = real


def s81(t):
    return ga.f81(eye=t > 0.7)


def s82(t):
    return _buzzing(ga.f82, t)


def s83(t):
    return _buzzing(ga.f83, t)


def s84(t):
    return _buzzing(ga.f84, t)


def s85(t):
    """Into the red of the gown; the red goes dark; out of the dark, the first drawing."""
    first = rr2.shot_75(T0)
    if t >= 0.9:
        return first
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    if t < 0.4:
        src = ga.f84(); z = 1 + 9 * ramp(t, 0.0, 0.4)
        c.translate(270, 480); c.scale(z, z); c.translate(-353, -565); c.set_source_surface(src, 0, 0); c.paint()   # the gown over his head
        c.identity_matrix(); c.set_source_rgba(*b.GOWN, ramp(t, 0.15, 0.25)); c.paint()
    else:
        u = ramp(t, 0.4, 0.3)
        c.set_source_rgb(*[v * (1 - u) for v in b.GOWN]); c.paint()
        if t > 0.7:
            c.set_source_surface(first, 0, 0); c.paint_with_alpha(ramp(t, 0.7, 0.2))
    return s


FILM = [("1.1", 0.6, s11),
        ("2.1", 1.5, s21), ("2.2", 1.5, s22), ("2.4", 2.8, s24), ("2.4b", 1.3, s24b), ("2.5", 1.4, s25), ("2.6", 1.5, s26), ("2.7", 2.0, s27),
        ("3.1", 1.6, s31), ("3.2", 1.4, s32), ("3.2b", 1.0, s32b), ("3.3", 1.3, s33), ("3.3b", 1.7, s33b), ("3.4", 1.5, s34), ("3.4b", 2.0, s34b),
        ("4.1", 1.6, s41), ("4.2", 1.9, s42), ("4.3", 1.5, s43), ("4.4", 2.2, s44), ("4.4a", 0.9, s44a), ("4.4t", 1.4, s44t), ("4.4b", 1.3, s44b), ("4.4c", 1.4, s44c)]
for name, dur in R5:
    if name == "5.4":
        FILM += [("5.4", 1.3, F5["5.4"]), ("5.4b", 0.5, s54b)]
    else:
        FILM.append((name, dur, F5[name]))
for name, dur in rr2.SHOTS:
    if name == "7.4":
        FILM += [("7.4", 1.1, s74a), ("7.4b", 0.45, s54b), ("7.4c", 0.7, s74c)]
    else:
        FILM.append((name, dur, rr2.FN[name]))
FILM += [("8.1", 1.6, s81), ("8.2", 1.6, s82), ("8.3", 2.2, s83), ("8.4", 1.6, s84), ("8.5", 1.0, s85)]


def _use():
    rr.SHOTS = tuple((n, d) for n, d, _ in FILM)
    rr.FN = {n: f for n, _, f in FILM}


def render(out):
    _use(); rr.render(out)


def frame_at(T):
    for n, d, f in FILM:
        if T < d - 1e-9:
            return n, f(round(T * 30) / 30)
        T -= d
    n, d, f = FILM[-1]
    return n, f(d - 1 / 30)


def total():
    return sum(d for _, d, _ in FILM)


def _sheet(tiles, out, w, cols):
    h = int(w * 960 / 540); rows = -(-len(tiles) // cols)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (w + 6) + 6, rows * (h + 30) + 6); c = cairo.Context(s)
    c.set_source_rgb(0.13, 0.13, 0.15); c.paint()
    for i, (lab, f) in enumerate(tiles):
        x, y = 6 + (i % cols) * (w + 6), 26 + (i // cols) * (h + 30)
        c.save(); c.translate(x, y); c.scale(w / 540, w / 540); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 1); c.select_font_face("sans", 0, 1); c.set_font_size(15); c.move_to(x + 2, y - 7); c.show_text(lab)
    s.write_to_png(out)


def sheets(d, fps=2.0, per=16):
    """Numbered tiles with the time in seconds; shots under 0.7 s get a tile of their own so nothing is skipped."""
    os.makedirs(d, exist_ok=True)
    times, T = [], 0.0
    for n, dur, _ in FILM:
        k_ = max(1, round(dur * fps))
        times += [T + dur * (i + 0.5) / k_ for i in range(k_)]
        T += dur
    tiles = [("%d  %.1fs" % (i + 1, tt), frame_at(tt)[1]) for i, tt in enumerate(times)]
    for j in range(0, len(tiles), per):
        _sheet(tiles[j:j + per], os.path.join(d, "sheet_%02d.png" % (j // per + 1)), 240, 8)
    _sheet(tiles, os.path.join(d, "sheet_small.png"), 120, 16)
    return len(tiles)


if __name__ == "__main__":
    import sys
    print("%.1f s, %d shots" % (total(), len(FILM)))
    if len(sys.argv) > 2:
        print(sheets(sys.argv[2]))
    render(sys.argv[1])
