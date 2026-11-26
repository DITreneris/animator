"""ONE STAR v19 (cs_os19; cs_v19 is another module) (26 Nov, Tomas: "0:02 counts from 0.1K: not convincing, it lacks speed and dynamics").
1.2 the post going viral: the reactions count ACCELERATES (1.2K to 48K, exponential, a new number every drawing;
v13 eased out, slowing from 0.3K to 2.4K); past 10K red and bold, growing to 135% at 48K, with a pulse at 10K and
on 48K; angry, laughing and thumbs-down reactions fly up out of the row (v19a: round dots read as confetti); the row
18 up; notification pops closer and closer and a low thud on 48K. Opt-in through install(); v18 rebuilds as before."""
import math
import cs_scene1 as s1
import cs_props as cp

D12 = [0]
START, END, FULL = 1.2, 48.0, 40          # K, K, the drawing it reaches END (then it ticks on slowly)
BORN = sorted(int(round(1.6 * i ** 0.78)) for i in range(70))                 # births per drawing: 1 then 2-3
COLS = ((0.95, 0.55, 0.20), (0.95, 0.80, 0.25), (0.90, 0.30, 0.40))
DX, DY = 104.0, 662.0                     # the three dots' first centre (cs_props.phone2 "crisis", measured)


def count(d):
    if d <= FULL:
        return START * (END / START) ** (d / float(FULL))
    return END * (1 + 0.004 * (d - FULL))


def label(n):
    return ("%.1fK" % n) if n < 10 else ("%dK" % int(n))


INK = (0.13, 0.12, 0.14)
ANGRY, LAUGH, DOWN = (0.90, 0.30, 0.28), (0.98, 0.78, 0.22), (0.30, 0.50, 0.90)


def angry(c, x, y, r, a=1.0):
    c.set_source_rgba(*ANGRY, a); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*INK, a); c.set_line_width(max(1.2, r * 0.16)); c.set_line_cap(1)
    for s_ in (-1, 1):                                                            # the brows down to the middle
        c.move_to(x + s_ * r * 0.62, y - r * 0.42); c.line_to(x + s_ * r * 0.16, y - r * 0.22); c.stroke()
        c.new_path(); c.arc(x + s_ * r * 0.36, y - r * 0.02, r * 0.11, 0, 2 * math.pi); c.fill()
    c.new_path(); c.arc(x, y + r * 0.62, r * 0.36, math.pi * 1.15, math.pi * 1.85); c.stroke()   # the frown


def laugh(c, x, y, r, a=1.0):
    c.set_source_rgba(*LAUGH, a); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*INK, a); c.set_line_width(max(1.2, r * 0.14)); c.set_line_cap(1)
    for s_ in (-1, 1):                                                            # eyes shut tight: ^ ^
        c.move_to(x + s_ * r * 0.55, y - r * 0.12); c.line_to(x + s_ * r * 0.33, y - r * 0.34)
        c.line_to(x + s_ * r * 0.13, y - r * 0.12); c.stroke()
    c.new_path(); c.move_to(x - r * 0.52, y + r * 0.10); c.line_to(x + r * 0.52, y + r * 0.10)   # the open mouth
    c.arc(x, y + r * 0.10, r * 0.52, 0, math.pi); c.close_path(); c.fill()


def down(c, x, y, r, a=1.0):
    c.set_source_rgba(*DOWN, a); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()

    def rr(x0, y0, w, h, q):
        c.new_path(); c.arc(x0 + q, y0 + q, q, math.pi, 1.5 * math.pi); c.arc(x0 + w - q, y0 + q, q, 1.5 * math.pi, 0)
        c.arc(x0 + w - q, y0 + h - q, q, 0, 0.5 * math.pi); c.arc(x0 + q, y0 + h - q, q, 0.5 * math.pi, math.pi)
        c.close_path(); c.fill()
    c.set_source_rgba(1, 1, 1, a)
    rr(x - r * 0.30, y - r * 0.60, r * 0.70, r * 0.56, r * 0.14)                  # the fist, knuckles to the right
    rr(x + r * 0.44, y - r * 0.60, r * 0.16, r * 0.56, r * 0.05)                  # the cuff
    rr(x - r * 0.46, y - r * 0.20, r * 0.36, r * 0.92, r * 0.18)                  # the thumb, pointing down
    c.set_source_rgba(*DOWN, a); c.set_line_width(max(0.8, r * 0.07))
    for i in range(1, 3):                                                         # the fingers' grooves
        yy = y - r * 0.60 + i * r * 0.56 / 3.0
        c.move_to(x - r * 0.06, yy); c.line_to(x + r * 0.40, yy); c.stroke()


ICONS = (angry, laugh, down)
LIFT = 18.0                                        # the count's row up (review: the phone's lower part was empty)


def size(n):
    if n < 10:
        return 32.0
    return 34.0 * (1 + 0.35 * math.log(n / 10.0) / math.log(END / 10.0))       # 34 at 10K, x1.35 at 48K


def pulse(d):
    cross = next((i for i in range(200) if count(i) >= 10.0), 999)
    return 1.0 + max(0.25 * max(0.0, 1 - abs(d - cross) / 3.0), 0.22 * max(0.0, 1 - abs(d - FULL) / 3.0))


def react(k, _n):
    c = k.c
    d = D12[0]
    n = count(d)
    y0 = DY - LIFT
    c.set_source_rgb(*cp.LIGHT); c.rectangle(84, 634, 290, 66); c.fill()          # over the old dots and number
    for j, born in enumerate(BORN):                                               # the flying reactions, more and more
        age = (d - born) / 7.0
        if not 0.0 <= age <= 1.0:
            continue
        x = DX + (j % 3) * 22 + 45 * age + 10 * math.sin(j * 1.7 + age * 4)
        y = y0 - 96 * age - 6 * (j % 2)
        ICONS[j % 3](c, x, y, 11 * (1 - 0.3 * age), 1.0 - age ** 2)
    for i, f in enumerate(ICONS):                                                 # the row: angry, laughing, thumbs down
        f(c, DX + i * 24, y0, 13)
    hot = n >= 10.0
    c.save(); c.translate(178, 678 - LIFT); z = pulse(d); c.scale(z, z)
    cp.T(c, label(n), 0, 0, size(n), col=cp.RED if hot else cp.GREY, bold=hot, center=False)
    c.restore()


def install():
    if getattr(s1.react, "v19", False):
        return
    old2 = s1.s1_2
    react.v19 = True
    s1.react = react

    def s1_2(k, d):
        D12[0] = d
        return old2(k, d)
    s1.s1_2 = s1_2
    s1.SHOTS[:] = [(n, nd, s1_2) if n == "1.2" else (n, nd, fn) for n, nd, fn in s1.SHOTS]
    import cs_film
    import cs_sfx as fx
    clicks = sorted(set(int(round(FULL * (i / 15.0) ** 0.5)) for i in range(16)))      # closer and closer
    cs_film.FX[:] = [x for x in cs_film.FX if x[0] != "1.2"] + \
        [("1.2", d, fx.pop(520 + 18 * i), 0.07) for i, d in enumerate(clicks)] + \
        [("1.2", FULL, fx.tap(70.0), 0.32)]                                        # and a low thud on 48K
