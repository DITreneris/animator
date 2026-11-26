"""PICK A SIDE: the blind's own sounds (Tomas 26 Nov, /grill-me: "a killer opener, not Chopin"): layered and realistic,
louder and faster each round, the robot's servo on its pulls, Don's effort, a bigger fall.
  zip       the cord through the pulley: friction noise with the ratchet's ticks speeding up
  slats     aluminium slats, each a short inharmonic ping, running down (spread) or stacking up (dense)
  clack     the bottom rail or the head rail hitting home
  servo     the robot's arm: a whine rising, with its motor's buzz
  creak     the cord taking his weight before it moves (the loop's seam: under frame 0)
  settle    the slats swinging still after the clack (into the seam)
  crash     1.2a: the blind comes down off its brackets: a thud, the slats spilling, the rail ringing
  grunt     Don's effort, his own voice (Kokoro am_onyx through sound_bc.don), short, pitched down a little"""
import numpy as np
import of_sound as osd

SR = osd.SR
rng = np.random.default_rng(1414)


def _t(d):
    return np.arange(int(d * SR)) / float(SR)


def _bp(x, lo, hi):
    return osd.hp(osd.lp(x, max(1, int(SR / hi / 2))), max(1, int(SR / lo / 2)))


def ping(f, d=0.07, a=1.0):
    t = _t(d)
    x = (np.sin(2 * np.pi * f * t) + 0.55 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.012)
         + 0.30 * np.sin(2 * np.pi * f * 5.40 * t) * np.exp(-t / 0.006))
    x *= np.exp(-t / (d * 0.35)) * np.minimum(1, t / 0.0008)
    click = osd.hp(rng.standard_normal(len(t)), 2) * np.exp(-t / 0.002) * 0.6
    return (x + click) * a


def slats(d, n=14, up=False, a=1.0):
    """n slats over d s; down: they run out evenly, accelerating; up: they stack, denser toward the end"""
    out = np.zeros(int((d + 0.12) * SR))
    for j in range(n):
        u = j / max(1, n - 1)
        tt = d * (u ** 0.6 if up else u ** 1.4)
        f = rng.uniform(2300, 4200) * (1.08 if up else 1.0)
        p = ping(f, rng.uniform(0.04, 0.08), rng.uniform(0.5, 1.0) * (0.6 + 0.4 * u if up else 1.0))
        i = int(tt * SR); out[i:i + len(p)] += p[:max(0, len(out) - i)]
    rustle = _bp(rng.standard_normal(len(out)), 1500, 7000) * np.sin(np.pi * np.minimum(1, (np.arange(len(out)) / SR) / (d + 0.1))) * 0.25
    return (out + rustle) * a


def zip_(d, a=1.0, r0=26, r1=70):
    """the cord through the pulley: friction plus the ratchet ticks, faster as the pull gets going"""
    t = _t(d)
    rate = r0 + (r1 - r0) * (t / d)
    ph = 2 * np.pi * np.cumsum(rate) / SR
    tick = np.maximum(0, np.sin(ph)) ** 12
    fr = _bp(rng.standard_normal(len(t)), 900, 5000)
    env = np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.03)
    sq = np.sin(2 * np.pi * np.cumsum(np.linspace(1900, 2700, len(t))) / SR) * 0.08
    return (fr * (0.35 + 0.9 * tick) + sq) * env * a


def clack(a=1.0, top=False):
    t = _t(0.25)
    body = osd.lp(rng.standard_normal(len(t)), 4) * np.exp(-t / 0.018) * 1.4
    thump = np.sin(2 * np.pi * (140 if top else 95) * t) * np.exp(-t / 0.05)
    metal = (np.sin(2 * np.pi * 1130 * t) + 0.6 * np.sin(2 * np.pi * 1890 * t)) * np.exp(-t / 0.07) * 0.35
    return (body + thump + metal) * a


def servo(d, f0=620, a=1.0):
    t = _t(d)
    f = f0 * (1 + 0.6 * np.minimum(1, t / (d * 0.7)))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.25 + np.sin(ph) * 0.6
    x *= 1 + 0.35 * np.sin(2 * np.pi * 90 * t)
    x = osd.lp(x, 3)
    return x * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05) * a


def creak(d, a=1.0):
    """the cord taking his weight: slow rough rubs, rising"""
    out = np.zeros(int(d * SR))
    k = 0.0
    while k < d - 0.05:
        n = rng.uniform(0.05, 0.11); f = rng.uniform(170, 260)
        t = _t(n)
        saw = (2 * ((f * t) % 1) - 1) * np.sin(np.pi * t / n)
        i = int(k * SR); seg = osd.lp(saw, 3) * (0.3 + 0.7 * k / d)
        out[i:i + len(seg)] += seg[:max(0, len(out) - i)]
        k += n * rng.uniform(1.1, 1.6)
    return out * a


def settle(d, a=1.0):
    out = np.zeros(int(d * SR))
    for j in range(9):
        tt = d * (j / 9.0) ** 1.6
        p = ping(rng.uniform(2600, 3800), 0.05, (1 - j / 9.0) * 0.6)
        i = int(tt * SR); out[i:i + len(p)] += p[:max(0, len(out) - i)]
    return out * a


def crash(a=1.0):
    d = 1.4
    out = np.zeros(int(d * SR)); t = _t(d)
    out += np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.12) * 1.2                       # the thud
    out[:int(0.25 * SR)] += osd.lp(rng.standard_normal(int(0.25 * SR)), 3) * np.exp(-_t(0.25) / 0.04) * 1.3
    for j in range(42):                                                               # the slats spilling, thinning
        tt = 0.02 + 0.7 * (j / 42.0) ** 1.8 + rng.uniform(0, 0.03)
        p = ping(rng.uniform(1800, 4600), rng.uniform(0.05, 0.12), rng.uniform(0.4, 1.0) * (1 - 0.6 * j / 42.0))
        i = int(tt * SR); out[i:i + len(p)] += p[:max(0, len(out) - i)]
    ring = (np.sin(2 * np.pi * 640 * t) + 0.7 * np.sin(2 * np.pi * 1730 * t) + 0.4 * np.sin(2 * np.pi * 3100 * t))
    out += ring * np.exp(-t / 0.45) * np.minimum(1, t / 0.003) * 0.35                  # the head rail, ringing
    return out * a


_GR = {}


def grunt(word="Hup!", semis=-1.5):
    """Don's effort in his own voice, trimmed to the syllable, a little lower"""
    if word not in _GR:
        import sound_bc as sb
        from scipy.signal import resample_poly
        x = np.asarray(sb.don(word, 1.0), dtype=float)
        x = x.mean(axis=1) if x.ndim > 1 else x
        idx = np.where(np.abs(x) > np.abs(x).max() * 0.05)[0]
        x = x[max(0, idx[0] - 200):idx[-1] + 600]
        r = 2 ** (-semis / 12.0)                               # lower: play it slower
        up, dn = int(round(r * 100)), 100
        x = resample_poly(x, up, dn)
        x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 0.1
        _GR[word] = x * np.minimum(1, (np.arange(len(x)) / SR) / 0.01)
    return _GR[word]
