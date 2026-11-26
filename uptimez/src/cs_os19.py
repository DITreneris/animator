"""ONE STAR v19 (cs_os19; cs_v19 is another module) (26 Nov, Tomas: "0:02 counts from 0.1K: not convincing, it lacks speed and dynamics").
1.2 the post going viral: the reactions count ACCELERATES (1.2K to 48K, exponential, a new number every drawing;
v13 eased out, slowing from 0.3K to 2.4K); past 10K the number turns red and bold with a bump; small reaction dots fly
up out of the three dots. Opt-in through install(); v18 rebuilds as before."""
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


def react(k, _n):
    c = k.c
    d = D12[0]
    n = count(d)
    c.set_source_rgb(*cp.LIGHT); c.rectangle(170, 640, 200, 56); c.fill()
    # the flying reactions: each born at one of the dots, up and right, fading (the post being hit, live)
    for j, born in enumerate(BORN):                                               # more and more of them, as the count
        age = (d - born) / 7.0                                                    # speeds up
        if not 0.0 <= age <= 1.0:
            continue
        col = COLS[j % 3]
        x = DX + (j % 3) * 22 + 45 * age + 10 * math.sin(j * 1.7 + age * 4)
        y = DY - 96 * age - 6 * (j % 2)
        c.set_source_rgba(*col, 1.0 - age ** 2)
        c.new_path(); c.arc(x, y, 11 * (1 - 0.4 * age), 0, 2 * math.pi); c.fill()
    hot = n >= 10.0
    cross = next((i for i in range(0, 200) if count(i) >= 10.0), 999)
    bump = 1.0 + 0.25 * max(0.0, 1 - abs(d - cross) / 3.0) if hot else 1.0
    c.save(); c.translate(178, 678); c.scale(bump, bump)
    cp.T(c, label(n), 0, 0, 36 if hot else 32, col=cp.RED if hot else cp.GREY, bold=hot, center=False)
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
