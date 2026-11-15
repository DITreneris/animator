"""Mouth shapes for the "I Will Replace You" animation, drawn over a face's own mouth (the Day One set,
day1_anim.mouth, with a larger erase for Don so his shock 'O' is fully covered).
Codes: M closed lips, A open, E wide, O round, U small round, F lip under teeth, C small open with teeth."""
import math
import kit
from kit import INK, ellipse

SIZES = {"A": (9, 11), "E": (12, 5.5), "O": (7.5, 8.5), "U": (4.8, 5.5), "F": (10, 4), "C": (9, 5.5)}
OPEN = {"": 0.0, "M": 0.0, "F": 0.25, "C": 0.4, "U": 0.45, "E": 0.55, "O": 0.75, "A": 1.0}


def mouth(k, x, my, code, skin, lip_col=None, inner=(0.40, 0.07, 0.08), erase=(19, 11), seed=0):
    c = k.c
    ellipse(k, x + 1, my - 1, erase[0], erase[1], skin, seed + 90, shadow=False, outline=False)
    col = lip_col or INK
    if code == "M":
        if lip_col:
            ellipse(k, x, my, 12, 4.6, lip_col, seed + 91, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(3.2 if not lip_col else 1.8); c.set_line_cap(1)
        c.move_to(x - 10, my); c.curve_to(x - 4, my + 1.5, x + 4, my + 1.5, x + 10, my); c.stroke()
        return
    w, h = SIZES[code]
    c.save(); c.translate(x, my); c.scale(w, h); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*inner); c.fill_preserve()
    c.set_source_rgb(*col); c.set_line_width(3.6 if lip_col else 2.2); c.stroke()
    if code in ("E", "F", "C"):                                   # upper teeth
        c.save(); c.translate(x, my); c.scale(w, h); c.arc(0, 0, 0.82, math.pi, 2 * math.pi); c.restore()
        c.save(); c.clip()
        c.set_source_rgb(1, 1, 1); c.rectangle(x - w, my - h, 2 * w, h * (0.75 if code == "F" else 0.5)); c.fill()
        c.restore()
    if code == "F":
        c.set_source_rgb(*col); c.set_line_width(3 if lip_col else 2.4)
        c.move_to(x - w + 2, my + 1); c.curve_to(x - 3, my - 2, x + 3, my - 2, x + w - 2, my + 1); c.stroke()
    if code in ("A", "O"):                                        # tongue
        c.save(); c.translate(x, my + h * 0.55); c.scale(w * 0.55, h * 0.3); c.arc(0, 0, 1, math.pi, 2 * math.pi); c.restore()
        c.set_source_rgb(0.80, 0.33, 0.35); c.fill()
    if lip_col:                                                   # gloss
        c.set_source_rgb(1, 1, 1); c.arc(x - w * 0.45, my + h * 0.7, 1.3, 0, 2 * math.pi); c.fill()


def don_mouth(k, head, code, chin=0, seed=530):
    hx, hy = head
    mouth(k, hx, hy + 4 - 7 * chin + 28, code, kit.PEOPLE["DON"]["skin"], erase=(20, 15), seed=seed)


def sof_mouth(k, head, code, seed=67):
    import sofia_v4 as sf
    hx, hy = head
    mouth(k, hx, hy + 4 + 29, code, sf.SKIN, lip_col=sf.RED, inner=(0.45, 0.06, 0.08), erase=(19, 11), seed=seed)
