"""v13 (18 Nov): with on2_motion's LOOK3, 5.1: smoke lit from behind the tables and black arms to the hands, so the hands
read as people (Tomas: "0:28 too dark, the arms' silhouettes can't be seen"). on2_motion_b5_v12.py is pinned.
v12 (18 Nov): with on2_motion's LOOK3: the pour earlier and longer, the coupe set down where her hair does not cover it.
on2_motion_b5_v11.py is pinned.
v11 (18 Nov): lip-sync from the take, drawing by drawing, one drawing ahead of the sound; 5.1, 5.5 and 5.10 shorter
(each still ends after its last beat: the last hand, the caught look, the eyebrow). on2_motion_b5_v10.py is pinned.
v10 (18 Nov): the stamp lands where it can be seen. on2_motion_b5_v9.py is pinned.
v9 (18 Nov): the detective's back in 5.2 and 5.10. on2_motion_b5_v8.py is pinned.
v8 (18 Nov): 5.2 is over the detective shoulder. on2_motion_b5_v7.py is pinned.
v7 (18 Nov): 5.4's line runs on into 5.5; 5.7 shorter. on2_motion_b5_v6.py is pinned.
v6 (18 Nov): two more lines of hers (5.2, 5.6); 5.2 and 5.9 shorter. on2_motion_b5_v5.py is pinned.
v4 (18 Nov): a clock above the bar's back wall, 11:58. on2_motion_b5_v3.py is pinned.
OFFICE NOIR 2: beat 05, the bar, animated. Script v2, storyboard v7 frames 5.1 to 5.10. 17 Nov.
Used by on2_motion.py (v5), which hands itself over with use(): the helpers (the detective with legs, the walk, the
blink, the breath) live there. Every shot here takes (k, tl, dur): the kit, the time into the shot, its length.
What moves: she walks through the cabaret and hands come out of the dark at her; she hides behind a fan of banknotes
while the detective searches the wrong way; "The usual."; his note slides along the bar; her finger counts the bays;
she turns it over and writes in lipstick; nobody takes it; she looks back from the door; his glass, his eye;
CASE CLOSED."""
import math
import cairo
import client_ob as co
from kit import INK, ellipse, rect, cut

m = None                                                    # on2_motion, once it has called use()
TIP = {}                                                    # where a speaker's mouth is, for the bubble's tail

PLAN = [("5.1", 20 / 12.0, None), ("5.2", 2.5, "n9", 0.05), ("5.3", 2.5, "s1"), ("5.4", 2.5, "n4", -0.9), ("5.5", 2.0, None), ("5.6", 2.5, "n10"),
        ("5.7", 16 / 12.0, None), ("5.9", 2.25, None), ("5.10", 30 / 12.0, None)]          # v8: 5.8 is cut; 5.1, 5.7 and 5.10 are shorter


def use(mod):
    global m
    m = mod


def d12_(tl):
    return int(round(tl * 12))


def room(k, zoom=1.0, counter=None):
    cc = k.c
    cc.save(); cc.translate(270, 280); cc.scale(zoom, zoom); cc.translate(-270, -280)
    m.b.bar_room(k, counter)
    m.clock(k, 270, 80, 32)                                               # v4: 11:58, above the back wall
    cc.restore()


def swayed(k, x, feet, deg, draw):
    """Draw a figure turned a little about her feet, with everything she carries."""
    cc = k.c
    cc.save(); cc.translate(x, feet); cc.rotate(math.radians(deg)); cc.translate(-x, -feet)
    o = draw()
    cc.restore()
    return o


def bubble(cc, text, box, tip):
    """A spoken line: white, in the safe area, its tail to the speaker's mouth. box = (x, y) of its left top corner."""
    cc.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); cc.set_font_size(27)
    e = cc.text_extents(text)
    w, h, r = e.x_advance + 36, 58, 16
    x, y = box
    x = max(m.SAFE[0], min(m.SAFE[2] - w, x)); y = max(m.SAFE[1], y)
    cy = y + h / 2
    left = tip[0] < x                                       # the tail leaves from the side the speaker is on
    for fill in (False, True):
        cc.new_path()
        cc.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); cc.arc(x + w - r, y + r, r, 1.5 * math.pi, 2 * math.pi)
        cc.arc(x + w - r, y + h - r, r, 0, 0.5 * math.pi); cc.arc(x + r, y + h - r, r, 0.5 * math.pi, math.pi); cc.close_path()
        bx = x if left else x + w
        cc.move_to(bx, cy - 11); cc.line_to(tip[0], tip[1]); cc.line_to(bx, cy + 11); cc.close_path()
        if fill:
            cc.set_source_rgb(1, 1, 1); cc.fill()
        else:
            cc.set_source_rgb(*INK); cc.set_line_width(7); cc.set_line_join(1); cc.stroke()
    cc.set_source_rgb(*INK); cc.move_to(x + 18, y + 39); cc.show_text(text)


# ---------------------------------------------------------------- 5.1: she crosses the cabaret
HANDS = ((110, 520, 0.18, "money", 1, 2), (440, 470, 0.10, "coupe", -1, 6), (90, 800, -0.12, "coupe", 1, 11), (450, 760, -0.16, "money", -1, 15))


def m5_1(k, tl, dur):
    n = m.n
    d = d12_(tl)
    room(k, m.lerp(1.14, 1.0, tl / dur))                                  # the camera backs away in front of her
    if m.LOOK3[0]:                                                        # v13: smoke lit from behind the tables, so the arms
        cc = k.c                                                          # read as black silhouettes against it
        for sx in (0, m.W):
            g = cairo.RadialGradient(sx, 760, 40, sx, 760, 380)
            g.add_color_stop_rgba(0, 0.78, 0.78, 0.76, 0.85); g.add_color_stop_rgba(1, 0.78, 0.78, 0.76, 0.0)
            cc.set_source(g); cc.rectangle(-20, 300, m.W + 40, 700); cc.fill()
        if getattr(m, "V37", [False])[0]:                                 # v37: tables, not boxes: a hat over each, a lamp's glow, a glass
            for i, (px, py, pr) in enumerate(((40, 900, 46), (120, 940, 40), (430, 930, 44), (512, 890, 48))):
                g = cairo.RadialGradient(px, py - 12, 2, px, py - 12, 60)
                g.add_color_stop_rgba(0, 1, 0.97, 0.88, 0.55); g.add_color_stop_rgba(1, 1, 0.97, 0.88, 0.0)
                cc.set_source(g); cc.new_path(); cc.arc(px, py - 12, 60, 0, 2 * math.pi); cc.fill()
                cc.set_source_rgb(*n.BLACK)
                cc.new_path(); cc.arc(px - pr * 0.6, py - pr * 1.45, pr * 0.5, 0, 2 * math.pi); cc.fill()            # a guest's head, behind his table
                cc.rectangle(px - pr * 1.3, py - pr * 1.0, pr * 1.4, 200); cc.fill()                                 # his shoulders
                cc.save(); cc.translate(px - pr * 0.6, py - pr * 1.85); cc.scale(pr * 0.9, pr * 0.16); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()   # the brim
                cc.rectangle(px - pr * 1.0, py - pr * 2.35, pr * 0.8, pr * 0.5); cc.fill()                         # the crown
                cc.set_source_rgb(0.60, 0.60, 0.64); cc.set_line_width(2); cc.new_path()
                cc.save(); cc.translate(px - pr * 0.6, py - pr * 1.85); cc.scale(pr * 0.9, pr * 0.16); cc.arc(0, 0, 1, math.pi, 2 * math.pi); cc.restore(); cc.stroke()
                cc.set_source_rgb(*n.BLACK); cc.save(); cc.translate(px, py); cc.scale(pr * 1.15, pr * 0.22); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()   # the table top
                cc.rectangle(px - 5, py, 10, 120); cc.fill()                                                             # its stem
                cc.set_source_rgb(0.95, 0.93, 0.86); cc.new_path(); cc.move_to(px + 8, py - 30); cc.line_to(px + 30, py - 30); cc.line_to(px + 19, py - 14); cc.close_path(); cc.fill()   # a coupe in the light
                cc.rectangle(px + 18, py - 14, 2, 10); cc.fill()
        else:
            for i, (px, py, pr) in enumerate(((40, 900, 46), (120, 940, 40), (430, 930, 44), (512, 890, 48))):   # the people at the tables
                cc.set_source_rgb(*n.BLACK); cc.new_path(); cc.arc(px, py - pr * 1.6, pr * 0.62, 0, 2 * math.pi); cc.fill()
                cc.rectangle(px - pr, py - pr, 2 * pr, 200); cc.fill()
    v38 = getattr(m, "V38", [False])[0]
    if getattr(m, "V37", [False])[0]:                                     # v37: the guests behind her, each cut out of the room's light
        cc_ = k.c
        for x, y, ang, what, flip, d_in in HANDS:
            e = d - d_in
            if e < 0 and not v38:
                continue
            e = max(0, e)                                                 # v38: they stand there from the start; only the hand comes
            gx = 20 if flip > 0 else m.W - 20
            sc_ = 1.05 if y < 600 else 1.25
            feet_ = y + 3.2 * e + 250 * sc_
            gy_ = feet_ + co.HY * sc_ + 20
            g = cairo.RadialGradient(gx + flip * 30, gy_, 20, gx + flip * 30, gy_, 190 * sc_)
            g.add_color_stop_rgba(0, 0.86, 0.86, 0.84, 0.95); g.add_color_stop_rgba(1, 0.86, 0.86, 0.84, 0.0)
            cc_.set_source(g); cc_.new_path(); cc_.arc(gx + flip * 30, gy_, 190 * sc_, 0, 2 * math.pi); cc_.fill()
            if v38 and y < 600:                                           # v38: the far pair paler, in the room's haze
                cc_.push_group()
                n.shadow(k, gx, feet_, sc_, "open", hat_tilt=-0.10 * flip, lit_hand=None, look_down=0.3, seed=880 + d_in)
                cc_.pop_group_to_source(); cc_.paint_with_alpha(0.55)
            else:
                n.shadow(k, gx, feet_, sc_, "open", hat_tilt=-0.10 * flip, lit_hand=None, look_down=0.3, seed=880 + d_in)
    ph = d % 6
    swayed(k, 270, 1080, (1.0, 0.4, -0.4, -1.0, -0.4, 0.4)[ph] + (2.5 if v38 and d >= 5 else 0.0),
           lambda: n.star(k, 270, 1080 + (0, -5, -2, 0, -5, -2)[ph], 2.4, "g_stand", ("interested" if d < 5 else "knowing") if v38 else "interested",
                          ((0.0, -0.45) if d < 5 else (0.25, -0.35)) if v38 else (0.0, -0.2), wrap=False,
                          sparkle=1.0 if d % 8 < 3 else 0.2))
    for x, y, ang, what, flip, d_in in HANDS:                             # out of the dark, one after another; she passes them
        e = d - d_in
        if e < 0:
            continue
        out = (1 - m.ease(e / 3.0)) * 190 - 4 * math.sin(e * 1.3)
        if m.LOOK3[0]:                                                    # v13: the arm, from the dark at the edge of the frame
            hx_, hy_ = x - flip * out, y + 3.2 * e
            n._seg(k, -60 if flip > 0 else m.W + 60, hy_ + 120, hx_ - flip * 40, hy_ + 10, 46, 40, n.BLACK, 2.4)
        if getattr(m, "V37", [False])[0]:                                 # v37 (Tomas: "the people at the sides, pathetic"): the film's own hat shadows, no faces; only the hand in the light
            cc_ = k.c
            gx = 20 if flip > 0 else m.W - 20
            hy_ = y + 3.2 * e
            sc_ = 1.05 if y < 600 else 1.25                                  # the far pair smaller
            feet_ = hy_ + 250 * sc_
            shx, shy = gx + flip * 52 * sc_, feet_ + (co.BT + 20) * sc_
            n._seg(k, shx, shy, x - flip * out - flip * 40, hy_ + 10, 40 * sc_, 34 * sc_, n.BLACK, 2.4)
            cc_.set_source_rgb(0.60, 0.60, 0.64); cc_.set_line_width(2.4); cc_.set_line_cap(1)      # the bar's light along the top of his arm
            cc_.move_to(shx, shy - 18 * sc_); cc_.line_to(x - flip * out - flip * 40, hy_ - 8); cc_.stroke()
        elif getattr(m, "V31", [False])[0]:                               # v31: a guest with a face at the frame's edge, the arm from his shoulder
            cc_ = k.c
            gx = 46 if flip > 0 else m.W - 46
            gy = y + 3.2 * e - 150
            cc_.set_source_rgb(*n.BLACK)                                    # his jacket, shoulder to the frame's edge
            cc_.new_path(); cc_.move_to(gx - flip * 110, gy + 330); cc_.line_to(gx - flip * 100, gy + 78); cc_.line_to(gx + flip * 30, gy + 62)
            cc_.line_to(gx + flip * 74, gy + 100); cc_.line_to(gx + flip * 70, gy + 330); cc_.close_path(); cc_.fill()
            n._seg(k, gx + flip * 50, gy + 104, x - flip * out - flip * 40, y + 3.2 * e + 10, 44, 38, n.BLACK, 2.4)
            cc_.set_source_rgb(0.95, 0.95, 0.93); cc_.new_path(); cc_.move_to(gx - flip * 14, gy + 62); cc_.line_to(gx + flip * 22, gy + 60); cc_.line_to(gx + flip * 2, gy + 112); cc_.close_path(); cc_.fill()
            cut(k, [(gx - flip * 8, gy + 68), (gx + flip * 10, gy + 62), (gx + flip * 10, gy + 76)], n.BLACK, shadow=False, lw=1.5)   # a bow tie
            v32 = getattr(m, "V32", [False])[0]
            kind = {2: 0, 6: 1, 11: 2, 15: 1}[d_in] if v32 else -1          # v32: slicked hair; bald with a moustache; a hat; and nearer ones bigger
            skin = ((0.50, 0.50, 0.53), (0.44, 0.44, 0.47), (0.38, 0.38, 0.41))[kind] if v32 else (0.72, 0.72, 0.74)
            v34 = getattr(m, "V34", [False])[0]
            if v34:                                                         # v34: the far pair (upper) darker; each head at its own angle
                far = y < 600
                skin = tuple(a_ * (0.72 if far else 1.0) for a_ in skin)
                cc_.save(); cc_.translate(gx, gy + 40); cc_.rotate({2: 0.10, 6: -0.16, 11: -0.07, 15: 0.14}[d_in]); cc_.translate(-gx, -gy - 40)
            hw = (46, 50, 44)[kind] if v32 else 46
            ellipse(k, gx, gy, hw, 52, skin, 880 + d_in, shadow=False, lw=2.4)          # his head, to her
            cc_.set_source_rgb(*n.BLACK)
            if kind in (-1, 0):
                cc_.new_path(); cc_.arc(gx, gy - 6, 48, math.pi * 1.05, math.pi * 1.95); cc_.close_path(); cc_.fill()   # hair, slicked
            elif kind == 2:                                                 # a hat, its brim over his eye
                cc_.new_path(); cc_.rectangle(gx - 40, gy - 78, 80, 46); cc_.fill()
                cc_.save(); cc_.translate(gx + flip * 6, gy - 30); cc_.scale(72, 10); cc_.new_path(); cc_.arc(0, 0, 1, 0, 2 * math.pi); cc_.restore(); cc_.fill()
            if kind == 1:                                                   # a moustache
                cut(k, [(gx + flip * 6, gy + 14), (gx + flip * 40, gy + 12), (gx + flip * 36, gy + 22), (gx + flip * 10, gy + 22)], n.BLACK, shadow=False, lw=1.5)
            if v32:                                                         # the bar's light on the side of his head toward her
                cc_.set_source_rgba(0.85, 0.85, 0.88, 0.8); cc_.set_line_width(3); cc_.set_line_cap(1)
                cc_.new_path(); cc_.arc(gx, gy, hw - 4, (-0.9 if flip > 0 else math.pi - 0.2), (0.2 if flip > 0 else math.pi + 0.9)); cc_.stroke()
            ex_ = gx + flip * 20
            ellipse(k, ex_, gy - 2, 8, 9, (0.97, 0.97, 0.95), 884 + d_in, shadow=False, lw=1.8)
            cc_.set_source_rgb(*INK); cc_.new_path(); cc_.arc(ex_ + flip * 3, gy - 2, 4, 0, 2 * math.pi); cc_.fill()
            cc_.set_line_width(3); cc_.set_line_cap(1); cc_.move_to(ex_ - 10, gy - 16); cc_.line_to(ex_ + 10, gy - 19); cc_.stroke()
            cc_.move_to(gx + flip * 8, gy + 26); cc_.curve_to(gx + flip * 18, gy + 34, gx + flip * 30, gy + 30, gx + flip * 34, gy + 22); cc_.stroke()   # he smiles
            cut(k, [(gx + flip * 44, gy + 4), (gx + flip * 58, gy + 12), (gx + flip * 44, gy + 16)], skin if getattr(m, "V34", [False])[0] else (0.72, 0.72, 0.74), shadow=False, lw=2)   # his nose, in profile
            if getattr(m, "V34", [False])[0]:
                cc_.restore()
        elif getattr(m, "V30", [False])[0]:                               # v30: whose arm: a guest at the frame's edge, shoulder and head
            ox = 14 if flip > 0 else m.W - 14
            oy = y + 3.2 * e + 150
            cc_ = k.c; cc_.set_source_rgb(*n.BLACK)
            cc_.new_path(); cc_.arc(ox, oy - 92, 40, 0, 2 * math.pi); cc_.fill()
            cc_.new_path(); cc_.move_to(ox - 80, oy + 140); cc_.line_to(ox - 70, oy - 30); cc_.line_to(ox + 70, oy - 30); cc_.line_to(ox + 80, oy + 140); cc_.close_path(); cc_.fill()
            cc_.set_source_rgb(0.55, 0.56, 0.60); cc_.set_line_width(3); cc_.new_path(); cc_.arc(ox, oy - 92, 40, -2.4 if flip > 0 else -1.6, -1.5 if flip > 0 else -0.7); cc_.stroke()
        n.rich_hand(k, x - flip * out, y + 3.2 * e, 1.9, ang, what, flip=flip)
    if getattr(m, "V31", [False])[0] and getattr(m, "V32", [False])[0] and not getattr(m, "V37", [False])[0]:   # v32: the smoke over the guests, drifting; her alone in the light
        cc = k.c
        cc.save(); cc.new_path(); cc.rectangle(0, 0, 116, m.H); cc.rectangle(442, 0, m.W - 442, m.H); cc.clip()   # never over her: a tint on her red and the noir pass takes it for grey
        for i, (sx, sy, r) in enumerate(((20, 430, 150), (520, 400, 160), (30, 760, 170), (515, 740, 160))):
            ox = 14 * math.sin(tl * 1.3 + i)
            g = cairo.RadialGradient(sx + ox, sy, 10, sx + ox, sy, r)
            g.add_color_stop_rgba(0, 0.80, 0.80, 0.78, 0.34); g.add_color_stop_rgba(1, 0.80, 0.80, 0.78, 0.0)
            cc.set_source(g); cc.new_path(); cc.arc(sx + ox, sy, r, 0, 2 * math.pi); cc.fill()
        for sx in (0, m.W):                                               # and the room's edges sink
            g = cairo.LinearGradient(sx, 0, sx + (130 if sx == 0 else -130), 0)
            g.add_color_stop_rgba(0, 0, 0, 0, 0.42); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
            cc.set_source(g); cc.rectangle(0 if sx == 0 else m.W - 130, 300, 130, 660); cc.fill()
        cc.restore()
        if getattr(m, "V34", [False])[0]:                                 # v34: the room's light along the top of her hair (her hair only: no red under it)
            g = cairo.RadialGradient(290, 270, 8, 290, 285, 105)             # soft, no edge; it ends well above her gown
            g.add_color_stop_rgba(0, 1, 1, 0.97, 0.40); g.add_color_stop_rgba(1, 1, 1, 0.97, 0.0)
            cc.set_source(g); cc.new_path(); cc.arc(290, 285, 105, 0, 2 * math.pi); cc.fill()


# ---------------------------------------------------------------- 5.2: she hides; he searches the wrong way
def m5_2(k, tl, dur):
    """v8: over the detective's shoulder. His bald head and his glass in front, scanning the room; she hides from it."""
    n = m.n
    cc = k.c
    d = d12_(tl)
    room(k)
    hid = 4 <= d < 28
    duck = 12 if 15 <= d < 19 else 0                                     # his glass comes her way: lower
    v38 = getattr(m, "V38", [False])[0]
    wink = v38 and 22 <= d < 28                                           # v38: the glass has gone past; she looks over the money at us and winks
    if hid:
        o = n.star(k, 330, 1180 + duck, 2.3, "g_fan", "wink" if wink else "caught", (0.0, 0.0) if wink else (-1.0, -0.3), wrap=False, bag=False)
        hx, hy = o["head"]
        up = 60 if d in (4, 27) else (150 if wink else 0)
        n.money(k, hx - 60, hy + 128 + up - duck * 0.4, 3.75, -0.35, 5, 711)
        n.rich_hand(k, hx - 82, hy + 145 + up - duck * 0.4, 1.8, 0.5, "money")
    else:
        o = n.star(k, 330, 1180, 2.3, "g_stand", "interested" if d < 2 else "caught", (-1.0, -0.3), wrap=False)
        hx, hy = o["head"]
        n.rich_hand(k, hx - 130, hy + 280, 1.8, 0.3, "money")
    n.rich_hand(k, 520 - 3 * math.sin(d * 0.9), 900, 1.7, -0.2, "coupe", flip=-1)
    # him, from behind, in front of us: the coat's shoulders, the bald head, the headset, the glass held out
    f = d / 30.0
    sweep = 470 - 300 * math.sin(math.pi * min(1.0, f * 1.15))           # the glass goes across the room and back
    hx0 = 120 + 10 * math.sin(f * 6)
    lx, ly = sweep, 640 + 40 * math.cos(f * 4)
    if getattr(m, "V37", [False])[0]:                                     # v37 (3/3: "a plank across her"): the glass at his own eye, beside his head
        lx, ly = hx0 + 150 + 30 * math.sin(math.pi * min(1.0, f * 1.15)), 700 + 12 * math.cos(f * 4)
        if wink:                                                          # v38: the glass has gone past her, to the left, down the room
            rp = min(1.0, (d - 21) / 2.0) * min(1.0, (28 - d) / 2.0) if getattr(m, "V39", [False])[0] else 1.0   # v39: eased out and back, no jump
            lx, ly = lx - (110 + 14 * (d - 22)) * rp, ly + 40 * rp
    v39 = getattr(m, "V39", [False])[0]
    n.ARM3[0] = v39
    del n.ARM3[1:]
    n.detective_back(k, hx0, 760 - n.d.HY * 2.4, 2.4, arm=(lx - 6, ly + 30))     # v9: his back, big and close
    if v39 and len(n.ARM3) > 1:                                           # v39: the glass is in his hand already; what it shows, at its own place
        (gx_, gy_), R = n.ARM3.pop()
        gx_, gy_ = cc.device_to_user(gx_, gy_); R = abs(cc.device_to_user_distance(R, 0)[0])
        n.ARM3[0] = False
        cc.save(); cc.new_path(); cc.arc(gx_, gy_, R - 8, 0, 2 * math.pi); cc.clip()
        cc.set_source_rgb(0.78, 0.80, 0.76); cc.paint()
        n.money(k, gx_ - 2, gy_ + 46 * R / 57.0, 4.6 * R / 57.0, -0.20 + 0.10 * math.sin(f * 5), 2, 712)
        g = cairo.RadialGradient(gx_ - 18, gy_ - 18, 4, gx_, gy_, R)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.35); g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
        cc.set_source(g); cc.paint(); cc.restore()
        cc.set_source_rgb(*INK); cc.set_line_width(5); cc.new_path(); cc.arc(gx_, gy_, R - 8, 0, 2 * math.pi); cc.stroke()
        cc.set_source_rgb(*n.SILVER); cc.set_line_width(2.2); cc.new_path(); cc.arc(gx_, gy_, R - 3, 0, 2 * math.pi); cc.stroke()
        return
    n.ARM3[0] = False
    if len(n.ARMS2) > 1:                                                  # v35: his hand stopped where his arm reaches; the glass with it
        lx, ly = cc.device_to_user(*n.ARMS2.pop())
        lx, ly = lx + 6, ly - 30
    n.magnifier(k, lx, ly, 3.0, 0.6)
    if getattr(m, "V38", [False])[0]:                                     # v38: through the glass, the banknotes magnified, not a grey disc
        a_ = 0.6; R = 19.0 * 3.0
        gx_, gy_ = lx + math.sin(a_) * (22 + 19) * 3.0, ly - math.cos(a_) * (22 + 19) * 3.0
        cc.save(); cc.new_path(); cc.arc(gx_, gy_, R - 9, 0, 2 * math.pi); cc.clip()
        cc.set_source_rgb(0.78, 0.80, 0.76); cc.paint()
        n.money(k, gx_ - 2, gy_ + 46, 4.6, -0.20 + 0.10 * math.sin(f * 5), 2, 712)
        g = cairo.RadialGradient(gx_ - 18, gy_ - 18, 4, gx_, gy_, R)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.35); g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
        cc.set_source(g); cc.paint()
        cc.restore()
        cc.set_source_rgb(*INK); cc.set_line_width(6); cc.new_path(); cc.arc(gx_, gy_, R - 9, 0, 2 * math.pi); cc.stroke()


# ---------------------------------------------------------------- 5.3: "The usual."
def m5_3(k, tl, dur):
    n = m.n
    cc = k.c
    d = d12_(tl)
    room(k)
    v12 = m.LOOK3[0]                                                      # v12: the pour earlier and longer, the coupe clear of her hair
    pour = (15 <= d < 28) if v12 else (21 <= d < 27)                      # v8: he polishes the glass; one eyebrow; he pours
    act = ("polish", d * 0.9) if d < (11 if v12 else 16) else ("pour",) if pour else None
    ob = n.bartender(k, 390, 700, 1.55, brow=d >= (11 if v12 else 16), look=(-0.8, 0.2) if not pour else (-0.5, 0.8), act=act, clean=True)
    cc.set_source_rgb(0.24, 0.21, 0.18); cc.rectangle(-20, 640, 600, 340); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 640, 600, 9); cc.fill()
    cx_ = 420 if v12 else 306
    if d >= (14 if v12 else 20):                                          # a coupe, set down and filled
        n.coupe(k, cx_, 640 - (8 if d == (14 if v12 else 20) else 0), 2.0)
    if pour and d >= (16 if v12 else 22):                                 # from the bottle in his hand, a long way down
        mx, my = ob["mouth"]
        cc.set_source_rgba(0.96, 0.93, 0.78, 0.9); cc.set_line_width(5 if not v12 else 7); cc.set_line_cap(1)
        cc.move_to(mx, my); cc.curve_to(mx - 16, my + 20, cx_ + 8, 540, cx_ + 4, 592); cc.stroke()
    sit = (-34, -10, 5, 0)[d] if d < 4 else 0                             # she sits as if she owned the room
    o = n.star(k, 130, 1060 + sit, 2.2, "g_down", "interested", (0.8, -0.1), wrap=False, bag=False,
               mouth=m.said("5.3", tl, "EUUCOEEM", lead=m.LEAD - 1 / 12.0))                         # v8: "The usual."
    hx, hy = o["head"]
    TIP["5.3"] = ((hx + 124, hy + 62), (hx + 150, hy + 28))               # beside her mouth; the bubble to the right of her face
    if getattr(m, "V30", [False])[0]:                                     # v30 (2/3: "hers or his?"): the box low, under her mouth's level and off his body
        TIP["5.3"] = ((hx + 124, hy + 66), (hx + 136, hy + 96))


# ---------------------------------------------------------------- 5.4: his note
def m5_4(k, tl, dur):
    n = m.n
    d = d12_(tl)
    m.b.bar_top(k)
    n.coupe(k, 452, 250, 2.4)
    f = m.ease(d / 7.0)
    ox, oy = -380 * (1 - f), -320 * (1 - f)                               # it slides along the bar under his hand
    n.napkin2(k, 320 + ox, 500 + oy, 3.0, ang=-0.05)
    g = m.ease((d - 13) / 6.0) if d >= 14 else 0.0                        # the hand lets go and is gone
    tap = 5 if d == 11 else 0
    if g < 1:
        hx, hy = ox - 300 * g + tap, oy - 260 * g + tap
        m.b.arm_in(k, -40 + hx, 200 + hy, 150 + hx, 400 + hy, 90)


# ---------------------------------------------------------------- 5.5: her finger counts the bays
def m5_5(k, tl, dur):
    n = m.n
    cc = k.c
    d = d12_(tl)
    room(k)
    face, look = ("interested", (-0.3, 0.9)) if d < 16 else ("sideeye", (-1.0, 0.1)) if d < 22 else ("caught", (-0.2, 0.9))
    n.star(k, 280, 1010, 3.0, "g_down", face, look, wrap=False, bag=False)
    cc.set_source_rgb(0.22, 0.19, 0.16); cc.rectangle(-20, 560, 600, 420); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 560, 600, 9); cc.fill()
    n.napkin2(k, 230, 740, 2.5, ang=-0.05)
    if d < 10:                                                            # one, two, three, four: and the last one, the L
        i = d // 2
        ox, oy = -112 + 28 * i + (14 if d % 2 else 0), (-14 if d % 2 else 0)
    else:
        ox, oy = 0, (-12 if d in (11, 14) else 0)                         # it stops there, and taps
    if getattr(m, "V33", [False])[0]:                                     # v33: a forearm from the edge, the index on the plan
        import on2_hands as oh
        if getattr(m, "V35", [False])[0]:
            oh.over_shoulder(k, (420 + ox, 860 + oy), "point", 96)
        else:
            oh.insert(k, (640, 1010), (452 + ox, 868 + oy), "point", 104)
        return
    n._seg(k, 600, 1000, 420 + ox, 850 + oy, 92, 80, n.KEY, 3.2)
    n.hand(k, 420 + ox, 850 + oy, 5.0, -1.02, 0.0)


# ---------------------------------------------------------------- 5.6: she turns it over and writes
def blank(k, x, y, s, ang):
    """The back of the napkin with nothing on it yet (noir2_cast.napkin's paper)."""
    cc = k.c
    cc.save(); cc.translate(x, y); cc.rotate(ang); cc.scale(s, s)
    rect(k, -62, -46, 124, 92, (0.97, 0.96, 0.93), 600, lw=1.8)
    cc.set_source_rgb(0.86, 0.85, 0.82); cc.set_line_width(1.0); cc.rectangle(-56, -40, 112, 80); cc.stroke()
    cc.restore()


def m5_6(k, tl, dur):
    n = m.n
    cc = k.c
    d = d12_(tl)
    m.b.bar_top(k)
    X, Y, S, A = 250, 480, 3.3, 0.04
    if d < 5:                                                             # over it goes
        sq = (1.0, 1.0, 0.5, 0.08, 0.5)[d]
        cc.save(); cc.translate(X, Y); cc.scale(sq, 1.0); cc.translate(-X, -Y)
        if d < 3:
            n.napkin2(k, X, Y, S, ang=A)
        else:
            blank(k, X, Y, S, A)
        cc.restore()
        pen = (474, 470) if 1 <= d else (540, 640)                        # her glove at its edge
    else:
        blank(k, X, Y, S, A)
        w1 = 0 if d < 7 else min(62, 14 + (d - 7) * 12)                   # the telephone, then the number, as the lipstick goes
        w2 = 0 if d < 13 else min(124, 12 + (d - 13) * 10)
        if w1 or w2:
            cc.save()
            cc.save(); cc.translate(X, Y); cc.rotate(A); cc.scale(S, S); cc.new_path()
            if w1:
                cc.rectangle(-62, -46, w1, 52)
            if w2:
                cc.rectangle(-62, 6, w2, 40)
            cc.restore()
            cc.clip()
            n.napkin2(k, X, Y, S, back=True, ang=A)
            cc.restore()
        if d < 7:
            pen = (300, 560)
        elif d < 13:
            pen = (X + S * (-62 + w1), Y + S * (-12) + (6 if d % 2 else -6))
        elif d < 25:
            pen = (X + S * (-62 + w2), Y + S * 24 + (5 if d % 2 else -5))
        else:
            pen = (470 + (d - 24) * 14, 640 + (d - 24) * 18)
    ox, oy = pen[0] - 366, pen[1] - 640                                   # the lipstick's tip is at (366, 640) on the board
    if getattr(m, "V33", [False])[0]:                                     # v33: the lipstick first, then her fist round it, its tip out past the fingers
        import on2_hands as oh

        def stick():
            if d >= 5:
                cc.save(); cc.translate(366 + ox, 640 + oy); cc.rotate(-0.80); cc.scale(5.2, 5.2); cc.translate(0, 12)
                rect(k, -3.4, -2, 6.8, 22, (0.12, 0.12, 0.14), 331, shadow=False, lw=1.0)
                cut(k, [(-2.6, -2), (-2.6, -9), (2.6, -12), (2.6, -2)], n.KEY, shadow=False, lw=0.9)
                cc.restore()
        if getattr(m, "V35", [False])[0]:
            oh.over_shoulder(k, (470 + ox, 742 + oy), "fist", 96, under=stick)
        else:
            oh.insert(k, (650, 960), (470 + ox, 742 + oy), "fist", 100, under=stick)
        return
    n._seg(k, 620, 980, 440 + ox, 720 + oy, 96, 84, n.KEY, 3.2)
    ellipse(k, 436 + ox, 716 + oy, 50, 46, n.KEY, 336, shadow=False, lw=3.2)
    if d >= 5:                                                            # her lipstick
        cc.save(); cc.translate(404 + ox, 680 + oy); cc.rotate(-0.75); cc.scale(4.6, 4.6)
        rect(k, -3.4, -2, 6.8, 15, (0.12, 0.12, 0.14), 331, shadow=False, lw=1.0)
        cut(k, [(-2.6, -2), (-2.6, -9), (2.6, -12), (2.6, -2)], n.KEY, shadow=False, lw=0.9)
        cc.restore()


# ---------------------------------------------------------------- 5.7: nobody takes it
def m5_7(k, tl, dur):
    n = m.n
    cc = k.c
    d = d12_(tl)
    m.b.bar_top(k)
    cc.set_source_rgb(0.10, 0.10, 0.11); cc.rectangle(-20, -20, 600, 190); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 166, 600, 9); cc.fill()
    rect(k, 100, 4, 100, 44, (0.30, 0.27, 0.24), 53, lw=3.0)                                        # v9: the stool across from her has a back,
    cc.set_source_rgb(*INK); cc.set_line_cap(1)
    for x0, x1 in ((104, 92), (130, 124), (170, 176), (196, 208)):                                  # and legs,
        cc.set_line_width(9); cc.move_to(x0, 100); cc.line_to(x1, 164); cc.stroke()
        cc.set_source_rgb(0.52, 0.50, 0.47); cc.set_line_width(5); cc.move_to(x0, 100); cc.line_to(x1, 164); cc.stroke()
        cc.set_source_rgb(*INK)
    ellipse(k, 150, 86, 66, 32, (0.34, 0.30, 0.27), 51, lw=3.4)                                     # and nobody on it
    ellipse(k, 150, 80, 52, 22, (0.44, 0.39, 0.35), 52, shadow=False, lw=2.4)
    f = m.ease(d / 5.0)
    nx, ny = m.lerp(336, 270, f), m.lerp(660, 520, f)                     # she slides it across, to where his hand was
    n.napkin2(k, nx, ny, 3.0, back=True, ang=0.04)
    if d < 6:
        px, py = nx + 150, ny + 170                                       # her glove, pushing
    elif d < 9:
        g = (d - 5) / 3.0
        px, py = m.lerp(420, 496, g), m.lerp(690, 846, g)                 # drawn back, waiting
    elif d < 10:                                                          # v7: shorter
        px, py = 496, 846 - (6 if d in (8, 9) else 0)                     # nothing happens. Two fingers drum, once
    else:
        g = (d - 9) / 6.0
        px, py = 496 + 190 * g, 846 + 170 * g                             # she gets up
    n._seg(k, px + 124, py + 114, px + 4, py + 4, 96, 84, n.KEY, 3.2)
    ellipse(k, px, py, 50, 46, n.KEY, 336, shadow=False, lw=3.2)
    n.coupe(k, 90, 900, 2.4)


# ---------------------------------------------------------------- 5.8: at the door, over her shoulder
def m5_8(k, tl, dur):
    n = m.n
    cc = k.c
    d = d12_(tl)
    room(k)
    cc.set_source_rgb(0.05, 0.05, 0.06); cc.rectangle(-20, 60, 250, 920); cc.fill()                 # the door, open on the night
    cc.set_source_rgb(0.40, 0.38, 0.34); cc.set_line_width(8); cc.rectangle(-20, 60, 250, 920); cc.stroke()
    if d < 6:                                                             # three steps toward it
        swayed(k, 300 - 20 * d, 1090, (1.2, 0.4, -0.4, -1.2, -0.4, 0.4)[d],
               lambda: n.star(k, 300 - 20 * d, 1090 + (0, -5, -2, 0, -5, -2)[d], 2.6, "g_down", "interested", (-0.7, 0.0), wrap=False, bag=False))
    elif d < 8:
        n.star(k, 200, 1090, 2.6, "g_down", "interested", (-0.7, 0.0), wrap=False, bag=False)
    else:                                                                 # and she looks back
        swayed(k, 200, 1090, 1.5, lambda: n.star(k, 200, 1090, 2.6, "g_down", "sideeye", (1.0, 0.0), wrap=False, bag=False))


# ---------------------------------------------------------------- 5.9: his glass: her number, then his eye on her
def m5_9(k, tl, dur):
    n = m.n
    cc = k.c
    d = d12_(tl)
    room(k)
    n.bartender(k, 496, 560, 0.80, brow=True, look=(-0.8, 0.3), clean=True)
    cc.set_source_rgb(0.24, 0.21, 0.18); cc.rectangle(250, 500, 330, 480); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(250, 500, 330, 9); cc.fill()
    cut(k, [(404, 494), (462, 494), (468, 502), (398, 502)], (0.97, 0.96, 0.93), shadow=False, lw=1.6)   # her answer, on the bar
    hx, hy = 372, 640 + n.d.HY
    if d < 10:                                                            # bent over it: in the glass, the lipstick telephone
        m.don(k, 372, 640, 1.0, (0.5, 0.9), m.STAND, lean=5, wrap=False, shut=d == 4)
        gx, gy, what = hx + 74, hy + 148, "phone"
    elif d < 11:
        m.don(k, 372, 640, 1.0, (0.0, 0.4), m.STAND, lean=2, wrap=False)
        gx, gy, what = hx + 24, hy + 86, "phone"
    else:                                                                 # he turns the glass: his eye, on her
        m.don(k, 372, 640, 1.0, (-0.9, 0.1), m.STAND, pose="up", wrap=False)
        gx, gy, what = hx - 30, hy + 20, "eye"
    n.glass_handle(k, gx, gy, 92, 0.5)
    n.glass_view(k, gx, gy, 92, what)
    seen = d >= 13
    n.star(k, 120, 1150 + (7 if d == 13 else 0), 2.6, "g_stand", "caught" if seen else "interested", (1.0, 0.0), wrap=False, bag=False)


# ---------------------------------------------------------------- 5.10: caught; CASE CLOSED
def door(k, e):
    """v8: the bar's door at the back, still swinging after her. e: drawings since the cut to the bar."""
    cc = k.c
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.rectangle(2, 250, 104, 392); cc.fill()                   # the night outside
    cc.set_source_rgb(0.40, 0.38, 0.34); cc.set_line_width(6); cc.rectangle(2, 250, 104, 392); cc.stroke()
    w = 34 + 62 * abs(math.cos(e * 0.75)) * math.exp(-max(0, e) / 14.0)
    rect(k, 4, 254, w, 384, (0.66, 0.64, 0.60), 580, shadow=False, lw=2.4)                           # its leaf, from the hinge
    ellipse(k, 4 + w - 12, 450, 5, 5, (0.90, 0.90, 0.94), 581, shadow=False, lw=1.4)
    if 0 <= e < 12 and e % 2 == 0:                                                                  # it has just been gone through
        cc.set_source_rgb(1, 1, 1); cc.set_line_width(3); cc.set_line_cap(1)
        for yy in (300, 440, 580):
            cc.move_to(4 + w + 6, yy); cc.line_to(4 + w + 20, yy - 6); cc.stroke()
def m5_10(k, tl, dur):
    n = m.n
    cc = k.c
    d = d12_(tl)
    if d < 6:                                                             # her face
        room(k, 1.5)
        n.star(k, 270, 1650 + (9 if d == 2 else 0), 4.6, "g_down", "caught", (1.0, 0.0), wrap=False, bag=False)
        return
    room(k)
    n.bartender(k, 440, 690, 1.3, brow=d >= 27, look=(-0.9, 0.2), clean=True)       # the eyebrow, last
    cc.set_source_rgb(0.24, 0.21, 0.18); cc.rectangle(-20, 640, 600, 340); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 640, 600, 9); cc.fill()
    door(k, d - 6)                                                        # v8: the door behind him is still swinging
    if d < 9:                                                             # v9: his back at the bar; the stamp goes up, and down
        arm = ((360, 560) if d < 7 else (370, 470) if d < 8 else (360, 640))    # v10: it comes down beside him, on the bar
        n.detective_back(k, 210, 1010 + (7 if d == 8 else 0), 2.1, arm=arm)
        cut(k, [(330, 646), (420, 646), (426, 664), (324, 664)], (0.96, 0.95, 0.90), shadow=False, lw=1.6)    # his notebook
        cc.save(); cc.translate(arm[0], arm[1] - 26 + (22 if d == 8 else 0)); cc.scale(2.1, 2.1)
        rect(k, -16, 6, 32, 11, (0.16, 0.16, 0.18), 572, shadow=False, lw=1.6)
        rect(k, -5, -16, 10, 22, (0.55, 0.40, 0.26), 573, shadow=False, lw=1.6)
        cc.restore()
        if d == 8:
            cc.set_source_rgb(1, 1, 1); cc.set_line_width(5); cc.set_line_cap(1)
            for a in (-2.6, -2.2, -1.57, -0.95, -0.55):
                cc.move_to(370 + math.cos(a) * 70, 640 + math.sin(a) * 50); cc.line_to(370 + math.cos(a) * 104, 640 + math.sin(a) * 80); cc.stroke()
        return
    if d < 0:                                                             # v8: a blank page in one hand, the stamp in the other, coming down
        D = n.d
        up = (58, D.BT - 6) if d < 7 else (62, D.BT - 30) if d < 8 else (8, D.BT + 74)
        o = m.don(k, 210, 1010 + (7 if d == 8 else 0), 2.1, (0.2, 0.8), m.STAND, pose=D.dm.ik(-1, -22, D.BT + 96) + D.dm.ik(1, up[0], up[1]),
                  wrap=False, glass=False)
        (lx, ly), (rx, ry) = o["hands"]
        n.stamp_page(k, lx + 30, ly - 24 * 2.1, 2.1 * 0.66, -0.06, 571, stamped=False)
        cc.save(); cc.translate(rx, ry - 20); cc.scale(2.1, 2.1)          # the stamp: a block and a knob
        rect(k, -16, 6, 32, 11, (0.16, 0.16, 0.18), 572, shadow=False, lw=1.6)
        rect(k, -5, -16, 10, 22, (0.55, 0.40, 0.26), 573, shadow=False, lw=1.6)
        ellipse(k, 0, -18, 9, 8, (0.55, 0.40, 0.26), 574, shadow=False, lw=1.6)
        cc.restore()
        ellipse(k, rx, ry - 16, 22, 20, D.SKIN, 575, shadow=False, lw=3)
        if d == 8:
            cx, cy = lx + 30, ly - 60
            cc.set_source_rgb(1, 1, 1); cc.set_line_width(5); cc.set_line_cap(1)
            for a in (-2.5, -2.0, -1.57, -1.1, -0.6):
                cc.move_to(cx + math.cos(a) * 92, cy + math.sin(a) * 70); cc.line_to(cx + math.cos(a) * 128, cy + math.sin(a) * 100); cc.stroke()
        return
    if d < 12:                                                            # CASE CLOSED: he looks at it
        o = m.don(k, 210, 1010, 2.1, (0.2, 0.8), m.STAND, pose="stamp", wrap=False)
        return
    o = m.don(k, 210, 1010, 2.1, (0.3, -0.2), m.STAND, pose="proud", wrap=False, face="almost", pocket=True, shut=d == 22)
    if d >= 18:                                                           # her coupe, too
        lx, ly = o["hands"][0]
        n.coupe(k, lx - 4, ly + 10 - (10 if d == 18 else 0), 1.9)
        ellipse(k, lx, ly - 30, 20, 20, n.d.SKIN, 478, shadow=False, lw=3)


SHOTS = {"5.1": (m5_1, 0, None), "5.2": (m5_2, 0, None), "5.3": (m5_3, 0, lambda cc: m.b.shade(cc, -1, 0.35)), "5.4": (m5_4, 0, None),
         "5.5": (m5_5, 0, None), "5.6": (m5_6, 0, None), "5.7": (m5_7, 0, None), "5.9": (m5_9, 0, None), "5.10": (m5_10, 0, None)}
