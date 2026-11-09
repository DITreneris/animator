"""Downloads Expedition: new looks and props on top of the paper-cutout kit (kit.py unchanged).
rush(): RUSH in three looks (office panic, expedition, after) - helmet, lamp, rope, beard, sweat, spikes.
kevin(): the friendly intern skeleton holding FINAL (3).  cave(): the Downloads cavern with file strata."""
import math
import kit
import pt42
from kit import INK, PAPER, rect, ellipse, cut, text, file_sheet

YELLOW = (0.98, 0.80, 0.18)
ROPE = (0.72, 0.52, 0.30)
BEARD = (0.36, 0.31, 0.27)
GREY = (0.62, 0.62, 0.62)
BONE = (0.97, 0.95, 0.88)


def sweat(k, hx, hy, s, t=0.0, n=4):
    for i in range(n):
        a = -0.6 + i * 0.4 + math.sin(t * 6 + i) * 0.05
        side = -1 if i % 2 else 1
        d = (62 + 14 * ((t * 3 + i * 0.37) % 1)) * s
        x, y = hx + side * math.cos(a) * d, hy - 30 * s + math.sin(a) * d * 0.4
        c = k.c
        c.save(); c.translate(x, y); c.scale(s, s)
        c.move_to(0, -12); c.curve_to(8, -2, 8, 8, 0, 9); c.curve_to(-8, 8, -8, -2, 0, -12)
        c.set_source_rgb(0.55, 0.80, 0.98); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
        c.restore()


def spikes(k, hx, hy, s, col):
    pts = []
    for i in range(7):
        a = math.pi + (i + 0.5) / 7 * math.pi
        r0 = 46 * s
        r1 = (78 if i % 2 == 0 else 64) * s
        pts += [(hx + math.cos(a - 0.2) * r0, hy - 10 * s + math.sin(a - 0.2) * r0),
                (hx + math.cos(a) * r1, hy - 10 * s + math.sin(a) * r1)]
    pts.append((hx + 48 * s, hy - 10 * s))
    cut(k, [(hx - 48 * s, hy - 10 * s)] + pts, col, shadow=False, lw=2)


def helmet(k, hx, hy, s, lamp=1.0, brand_mark=True, cone=False):
    """Hard hat seated on the head: the brim sits above the eyes (eyes top at hy - 11*s).
    Returns the lamp position, so a light beam can start exactly there."""
    c = k.c
    lx, ly = hx, hy - 64 * s
    if lamp > 0 and cone:                           # optional upward glow (not used where a beam is drawn)
        c.set_source_rgba(1, 0.95, 0.6, 0.30 * lamp)
        c.move_to(lx - 6 * s, ly); c.line_to(lx - 140 * s, ly - 200 * s); c.line_to(lx + 140 * s, ly - 200 * s)
        c.close_path(); c.fill()
    dome = [(hx + math.cos(math.pi + i / 16 * math.pi) * 60 * s, hy - 24 * s + math.sin(math.pi + i / 16 * math.pi) * 54 * s)
            for i in range(17)]
    cut(k, dome, YELLOW, lw=2.5)
    rect(k, hx - 70 * s, hy - 32 * s, 140 * s, 12 * s, YELLOW, 611)     # brim bottom at hy - 20*s
    ellipse(k, lx, ly, 13 * s, 11 * s, (1, 1, 0.85) if lamp > 0 else (0.5, 0.5, 0.45), 612, shadow=False)
    if brand_mark and s >= 0.5:                      # small UptimeZ mark on the helmet front
        import brand
        brand.mark(c, hx + 24 * s, hy - 50 * s, 16 * s, zzz=False)
    return lx, ly


def rope(k, x, top, s):
    """Rope coiled over the left shoulder and hanging at the left hip, clear of the name badge."""
    c = k.c
    for col, wdt in ((INK, 9 * s), (ROPE, 6 * s)):
        c.set_source_rgb(*col); c.set_line_width(wdt); c.set_line_cap(1)
        c.move_to(x - 30 * s, top + 4 * s); c.line_to(x - 40 * s, top + 96 * s); c.stroke()
    for i in range(3):
        c.save(); c.translate(x - 46 * s + i * 3 * s, top + 118 * s + i * 4 * s); c.scale(0.8, 1.15)
        c.arc(0, 0, 20 * s, 0, 2 * math.pi)
        c.set_source_rgb(*INK); c.set_line_width(9 * s); c.stroke_preserve()
        c.set_source_rgb(*ROPE); c.set_line_width(6 * s); c.stroke()
        c.restore()


def beard(k, hx, hy, s, length=1.0):
    """A long beard from the cheeks down; the mouth stays clear."""
    top = hy + 22 * s
    bot = hy + (80 + 190 * length) * s
    pts = [(hx - 46 * s, top - 8 * s), (hx - 26 * s, hy + 44 * s), (hx + 26 * s, hy + 44 * s), (hx + 46 * s, top - 8 * s)]
    pts += [(hx + 44 * s, hy + 70 * s), (hx + 30 * s, bot - 30 * s)]
    for i in range(5):                               # wavy, pointed bottom
        x = hx + 26 * s - i * 13 * s
        pts.append((x, bot - (16 if i % 2 else 0) * s - abs(i - 2) * 10 * s))
    pts += [(hx - 30 * s, bot - 30 * s), (hx - 44 * s, hy + 70 * s)]
    cut(k, pts, BEARD, lw=2.5)
    c = k.c
    c.set_source_rgb(*GREY); c.set_line_width(3 * s)
    for dx in (-16, 2, 18):
        c.move_to(hx + dx * s, hy + 56 * s)
        c.curve_to(hx + (dx - 6) * s, hy + 110 * s, hx + (dx + 6) * s, bot - 80 * s, hx + dx * 0.6 * s, bot - 34 * s)
        c.stroke()
    # mouth hole stays visible
    ellipse(k, hx, hy + 32 * s, 15 * s, 7 * s, (0.35, 0.08, 0.08), 613, shadow=False, lw=1.5)


def rush(k, x, feet, s=1.0, look="office", pose="stand", face="neutral", seed=31, t=0.0, lamp=1.0, gaze=(0, 0),
         helmet_on=True, rope_on=True, badge=True):
    """look: 'office' (panic extras), 'expedition' (helmet, lamp, rope), 'after' (beard, flicker, torn).
    Returns the person's key points plus 'lamp' (where a beam must start) when the helmet is on."""
    p = pt42.branded_person(k, "RUSH", x, feet, s, pose=pose, face=face, seed=seed, look=gaze, badge=badge)
    hx, hy = p["head"]
    if look == "office":
        spikes(k, hx, hy, s, kit.PEOPLE["RUSH"]["hair"])
        sweat(k, hx, hy, s, t)
    if look in ("expedition", "after"):
        if rope_on:
            rope(k, x, feet + (-300 * kit.PEOPLE["RUSH"]["h"] + 78) * s, s)
        if helmet_on:
            p["lamp"] = helmet(k, hx, hy, s, lamp)
    if look == "after":
        beard(k, hx, hy, s, 0.4)                      # v06: mid-chest, so badge, rope and arms read
        rect(k, x - 62 * s, feet - 196 * s, 22 * s, 16 * s, (0.85, 0.85, 0.88), 614, shadow=False)   # torn sleeve flap
    return p


def kevin(k, x, y, s=1.0, seed=70, cobwebs=True, final="FINAL (3)", final_size=15):
    """Sitting cartoon skeleton, smiling, INTERN badge, clutching a file. (x, y) = seat point."""
    c = k.c
    if cobwebs:                                   # behind the skull, never across it
        c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(1.2)
        for i in range(6):
            a = -math.pi / 2 - 0.8 + i * 0.32
            c.move_to(x, y - 170 * s); c.line_to(x + math.cos(a) * 140 * s, y - 170 * s + math.sin(a) * 140 * s); c.stroke()
        for r in (40, 80, 120):
            c.arc(x, y - 170 * s, r * s, -math.pi / 2 - 0.8, -math.pi / 2 + 0.8); c.stroke()
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_line_cap(1)

    def bone(x0, y0, x1, y1, w=9):
        c.set_source_rgb(*INK); c.set_line_width(w + 4); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        c.set_source_rgb(*BONE); c.set_line_width(w); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        for (px, py) in ((x0, y0), (x1, y1)):
            ellipse(k, px, py, w * 0.75, w * 0.75, BONE, seed + int(px), shadow=False, lw=2)

    # legs (sitting, knees up)
    bone(-14, 0, -40, -46); bone(-40, -46, -60, 6)
    bone(14, 0, 40, -46); bone(40, -46, 62, 6)
    # spine + ribs
    bone(0, 0, 0, -120, 8)
    for i in range(4):
        yy = -50 - i * 18
        c.set_source_rgb(*INK); c.set_line_width(7)
        c.move_to(-26 + i * 2, yy + 8); c.curve_to(-20, yy - 6, 20, yy - 6, 26 - i * 2, yy + 8); c.stroke()
        c.set_source_rgb(*BONE); c.set_line_width(4)
        c.move_to(-26 + i * 2, yy + 8); c.curve_to(-20, yy - 6, 20, yy - 6, 26 - i * 2, yy + 8); c.stroke()
    ellipse(k, 0, -4, 26, 12, BONE, seed + 1)                       # pelvis
    # arms forward, holding the file in the lap
    bone(-28, -112, -46, -60); bone(-46, -60, -20, -40)
    bone(28, -112, 46, -60); bone(46, -60, 20, -40)
    file_sheet(k, 0, -44, max(70, final_size * 4.8), 86, "", seed + 2, rot=-0.08)
    text(k, final, 0, -44, final_size, INK)
    # INTERN badge on a lanyard
    c.set_source_rgb(0.17, 0.71, 0.45); c.set_line_width(3)
    c.move_to(-14, -128); c.line_to(-4, -96); c.line_to(6, -128); c.stroke()
    rect(k, -22, -98, 44, 22, (1, 1, 1), seed + 3, shadow=False, lw=1.6)
    text(k, "INTERN", 0, -87, 10, INK)
    # skull: round, friendly
    ellipse(k, 0, -170, 44, 42, BONE, seed + 4)
    for sx in (-16, 16):
        ellipse(k, sx, -174, 11, 13, (0.18, 0.16, 0.16), seed + 5 + sx, shadow=False, lw=1.5)
        ellipse(k, sx + 3, -178, 3, 3, (1, 1, 1), seed + 6 + sx, shadow=False, outline=False)
    c.set_source_rgb(*INK); c.set_line_width(2.5)
    c.move_to(-4, -156); c.line_to(0, -162); c.line_to(4, -156); c.stroke()      # nose
    c.arc(0, -150, 18, 0.25, math.pi - 0.25); c.stroke()                          # smile
    for tx in (-10, -3, 4, 11):
        c.move_to(tx, -138); c.line_to(tx, -144); c.stroke()
    c.restore()



STRATA = [(0.93, 0.92, 0.87), (0.85, 0.84, 0.78), (0.78, 0.76, 0.70), (0.70, 0.67, 0.60)]


def cave(k, w=kit.W, h=kit.H, seed=90, labels=True, door_y=60):
    """Dark cavern; walls are layers of stacked paper; a lit DOWNLOADS doorway high up."""
    c = k.c
    rect(k, -20, -20, w + 40, h + 40, (0.13, 0.12, 0.12), seed, shadow=False, outline=False)
    r = k.rng(seed)
    years = ["2024", "2019", "2016"]
    for band in range(4):                          # walls: paper strata both sides, deeper = older/darker
        y0 = 180 + band * 190
        for side in (0, 1):
            for j in range(9):
                x = (-30 + j * 22 + r.uniform(-6, 6)) if side == 0 else (w - 190 + j * 22 + r.uniform(-6, 6))
                file_sheet(k, x + 40, y0 + r.uniform(-30, 120), 70, 50, "", seed + band * 50 + j + side * 20,
                           rot=r.uniform(-0.4, 0.4))
                c.set_source_rgba(0, 0, 0, 0.12 * band)
                c.rectangle(x, y0 - 40, 90, 190); c.fill()
        if labels and band < 3:
            text(k, years[band], w - 60, y0 + 40, 28, (0.98, 0.95, 0.8))
    # the lit doorway high up, with its sign
    rect(k, w / 2 - 40, door_y, 80, 120, (1.0, 0.95, 0.75), seed + 300, shadow=False)
    c.set_source_rgba(1, 0.95, 0.7, 0.18)
    c.move_to(w / 2 - 40, door_y + 120); c.line_to(w / 2 - 160, h); c.line_to(w / 2 + 160, h); c.line_to(w / 2 + 40, door_y + 120)
    c.close_path(); c.fill()
    rect(k, w / 2 - 60, door_y - 30, 120, 26, (1, 1, 1), seed + 301, shadow=False)
    text(k, "DOWNLOADS", w / 2, door_y - 17, 15, INK)
