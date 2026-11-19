"""FIRST SEARCH (episode 10): the set, v2 opt-in (LAYOUT[0] = "v2"; the default draws v1 exactly), after the audit of
set sheet v1 (18 Nov):
- a tighter master (CAM2, zoom 1.25 for 1.12) and a larger screen (SCREEN2): at 270 px "0 RESULTS" in the hook is
  about 15 px high; the wide holds the Client in the doorway, Don, Sofía, the robot, and Pam and Mom at the counter;
- screen state "wipe" (p 0..1): the red turns green in a sweep from the left, the 0 never changes (close-up 4.5);
- one phone template (phone2): the same frame, at most four lines, no letter under 9 px at the insert's size;
  the post is simplified to DON TAGGED YOU, the photo, 0 RESULTS. NOW IN GREEN., and Pam's comment;
- Sofía in her episode-10 look (sofia_fs) in the v2 master.
FIRST SEARCH (episode 10): the set, v1. Episode 9's front desk (set_ob, untouched) with what this episode adds:
- the wall screen: UptimeZ Find on a big display on a stand, left of centre, beside the robot. States: the query
  ("blueprint", cursor), the red 0 RESULTS, the green 0 RESULTS, RETRY UNTIL FRIDAY over the green zero;
- OUR FIRST CLIENT with his photograph (episode 9's last shot), moved to hang directly above Don's head, larger
  (at least 120 px wide at 540), crooked, a crack across his face and a plaster over it;
- Mom's desk just inside the glass door: ASSISTANT TO DON on a plate, a framed baby photo of Don;
- Pam at the far end of the reception desk with the taped plan: bays 1-10, bay 7 a gap;
- the phone inserts: FRI · BANK, PREMIUM · PAID, the post (DON TAGGED YOU, Pam's comment), 100% COMPLETE;
- the UPGRADE card on Sofía's tablet.
The stage is set_ob's 540 x 960 with the floor at FLOOR; draw inside set_ob.cam() for the master wide."""
import math
import cairo
import kit
import brand
import set_ob as st
import acts_ob as ac
import client_ob as co
from kit import INK, rect, ellipse, cut

F = st.FLOOR
SCREEN = (30, 250, 140, 90)                              # v1: above the door, on a wall bracket                              # x, y, w, h of the display (on its stand to the floor)
PORTRAIT = (292, 404)                                      # centre of the frame: right above Don's head
PORTRAIT_S = 1.12
CROOK = math.radians(8)
MOMDESK = (176, F - 6)                                     # her desk's left edge and floor, just inside the door
POS = {"client": (98, F - 14, 0.52), "robot": (214, F + 4, 0.50), "mom": (478, F - 70, 0.52),
       "don": (292, F + 14, 0.75), "sofia": (350, F + 4, 0.70), "pam": (416, F - 46, 0.62)}
LAYOUT = ["v1"]                                            # "v2": the constants below take over in master()
CAM2 = (22, 190, 1.25)                                     # v2: left, top, zoom of the tighter master
SCREEN2 = (26, 286, 162, 100)                              # v2: the larger screen, over the door
POS2 = {"client": (92, F - 14, 0.52), "robot": (166, F + 4, 0.48), "mom": (432, F - 70, 0.50),
        "don": (292, F + 14, 0.75), "sofia": (230, F + 2, 0.68), "pam": (368, F - 72, 0.56)}
DARK = (0.12, 0.14, 0.20)
GRN = (0.20, 0.72, 0.40)
RED = (0.88, 0.18, 0.18)
SKIN_DON = kit.PEOPLE["DON"]["skin"] if "DON" in kit.PEOPLE else (0.96, 0.80, 0.66)


def _text(c, s, x, y, size, col=(1, 1, 1), bold=True, center=True, font="Inter"):
    c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    e = c.text_extents(s)
    c.set_source_rgb(*col)
    c.move_to(x - e.x_advance / 2 if center else x, y); c.show_text(s)
    return e.x_advance


def screen(k, state="query", x=None, y=None, w=None, h=None, stand=False, cursor=True, seed=600):
    """The wall display. state: query | red | green | retry."""
    c = k.c
    x0, y0, w0, h0 = SCREEN2 if LAYOUT[0] == "v2" else SCREEN
    x = x0 if x is None else x; y = y0 if y is None else y; w = w0 if w is None else w; h = h0 if h is None else h
    if not stand:                                                                               # the wall bracket
        rect(k, x + w / 2 - 8, y - 14, 16, 12, (0.30, 0.32, 0.36), seed + 3, shadow=False, lw=1.4)
    if stand:
        rect(k, x + w / 2 - 5, y + h, 10, F - (y + h) - 6, (0.30, 0.32, 0.36), seed + 1, shadow=False, lw=1.6)
        rect(k, x + w / 2 - 30, F - 8, 60, 8, (0.30, 0.32, 0.36), seed + 2, shadow=False, lw=1.6)
    rect(k, x - 5, y - 5, w + 10, h + 10, (0.16, 0.17, 0.20), seed, lw=2.2)
    c.set_source_rgb(0.97, 0.98, 1.0); c.rectangle(x, y, w, h); c.fill()
    sc = w / 150.0
    c.set_source_rgb(*brand.NAVY); c.rectangle(x, y, w, 15 * sc); c.fill()                     # the app bar
    _text(c, "UPTIMEZ FIND", x + 6 * sc, y + 11 * sc, 8.5 * sc, center=False)
    bx, by, bw, bh = x + 8 * sc, y + 21 * sc, w - 16 * sc, 18 * sc                              # the search bar
    c.set_source_rgb(1, 1, 1); c.rectangle(bx, by, bw, bh); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(bx, by, bw, bh); c.stroke()
    q = "blueprint"
    tw = _text(c, q, bx + 5 * sc, by + 13 * sc, 11 * sc, col=INK, bold=False, center=False)
    if cursor:
        c.set_source_rgb(*INK); c.rectangle(bx + 7 * sc + tw, by + 3 * sc, 1.6 * sc, 12 * sc); c.fill()
    cy = y + 44 * sc
    if state.startswith("wipe"):                                                                # v2: red to green, the 0 stays
        p = float(state[4:] or 0)
        bw_ = w - 16 * sc
        c.set_source_rgb(*RED); c.rectangle(x + 8 * sc, cy, bw_, h - 52 * sc); c.fill()
        c.set_source_rgb(*GRN); c.rectangle(x + 8 * sc, cy, bw_ * p, h - 52 * sc); c.fill()
        if 0 < p < 1:
            c.set_source_rgba(1, 1, 1, 0.8); c.rectangle(x + 8 * sc + bw_ * p - 1.5 * sc, cy, 3 * sc, h - 52 * sc); c.fill()
        _text(c, "0 RESULTS", x + w / 2, cy + (h - 52 * sc) / 2 + 8 * sc, 22 * sc)
    if state in ("red", "green", "retry"):
        col = RED if state == "red" else GRN
        c.set_source_rgb(*col); c.rectangle(x + 8 * sc, cy, w - 16 * sc, h - 52 * sc); c.fill()
        _text(c, "0 RESULTS", x + w / 2, cy + (h - 52 * sc) / 2 + 8 * sc, 22 * sc)
        if state == "retry":
            c.set_source_rgba(0.10, 0.12, 0.18, 0.86); c.rectangle(x + 4 * sc, y + 26 * sc, w - 8 * sc, 44 * sc); c.fill()
            _text(c, "RETRY UNTIL", x + w / 2, y + 45 * sc, 15 * sc, col=(1.0, 0.86, 0.30))
            _text(c, "FRIDAY", x + w / 2, y + 63 * sc, 15 * sc, col=(1.0, 0.86, 0.30))


def plaster(c, x, y, s=1.0, ang=-0.5):
    """A sticking plaster: tan strip, a pad in the middle, little holes."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(0.93, 0.78, 0.60)
    r = 5
    c.new_path(); c.arc(-22 + r, -6 + r, r, math.pi, 1.5 * math.pi); c.arc(22 - r, -6 + r, r, 1.5 * math.pi, 0)
    c.arc(22 - r, 6 - r, r, 0, 0.5 * math.pi); c.arc(-22 + r, 6 - r, r, 0.5 * math.pi, math.pi); c.close_path()
    c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
    c.set_source_rgb(0.98, 0.92, 0.84); c.rectangle(-7, -5, 14, 10); c.fill()
    c.set_source_rgb(0.70, 0.55, 0.40)
    for dx in (-16, -12, 12, 16):
        for dy in (-2.5, 2.5):
            c.arc(dx, dy, 0.8, 0, 2 * math.pi); c.fill()
    c.restore()


PSTATE = [None]                                            # opt-in (board v4): None = the set sheet's cracked and plastered
                                                           # portrait; "clean" (frame 0), "crack" (after the bonk), "patch"


def portrait(k, x=None, y=None, s=None, ang=None, crack=None, patch=None, seed=420):
    """OUR FIRST CLIENT with his photograph; crooked; the crack across his face; the plaster over it.
    crack/patch None: from PSTATE, or both on as in the set sheets."""
    c = k.c
    st_ = PSTATE[0]
    if crack is None:
        crack = st_ in (None, "crack", "patch")
    if patch is None:
        patch = st_ in (None, "patch")
    x = PORTRAIT[0] if x is None else x; y = PORTRAIT[1] if y is None else y
    s = PORTRAIT_S if s is None else s; ang = CROOK if ang is None else ang
    c.save(); c.translate(x, y); c.rotate(ang)
    st.first_client(k, 0, 0, s, seed)
    c.save(); c.scale(s, s)
    c.save(); c.rectangle(-31.4, -41.4, 62.8, 82.8); c.clip()                    # his photograph (episode 9's)
    c.set_source_rgb(0.74, 0.84, 0.94); c.paint()
    co.client(k, -1, 168, 0.44, "stand", "puzzled", (0.0, 0.0), badge=False)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(-32, -42, 64, 84); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.35); c.move_to(-30, -40); c.line_to(-8, -40); c.line_to(-30, -10); c.close_path(); c.fill()  # glass
    if crack:                                                                    # across his face
        pts = [(-31, -22), (-14, -18), (-4, -24), (8, -15), (20, -19), (31, -12)]
        for col, lw in (((1, 1, 1), 2.6), ((0.12, 0.12, 0.15), 1.3)):              # a white edge, so it reads small
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_join(1)
            c.move_to(*pts[0])
            for p in pts[1:]:
                c.line_to(*p)
            c.stroke()
            c.move_to(-4, -24); c.line_to(-1, -36); c.stroke()
            c.move_to(8, -15); c.line_to(12, -4); c.stroke()
    c.restore()
    if patch:
        plaster(c, 0, -19 * s, s * 0.82, ang=-0.12)
    c.restore()


BABY_DON = [False]                                         # opt-in (animatic): Don's markers on the baby


def baby_photo(k, x, y, s=1.0, seed=700):
    """A small standing frame: baby Don, bald, smiling, one curl. BABY_DON: a tiny headset and his ketchup stain,
    so on mute the baby is Don (all four cold viewers of the storyboard missed who Mom is)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -16, -20, 32, 40, (0.80, 0.62, 0.30), seed, lw=1.6)
    c.set_source_rgb(0.82, 0.90, 0.98); c.rectangle(-12, -16, 24, 32); c.fill()
    ellipse(k, 0, -2, 9.5, 9, SKIN_DON, seed + 1, shadow=False, lw=1.3)                         # the bald head
    ellipse(k, 0, 13, 11, 7, (0.95, 0.95, 0.98), seed + 2, shadow=False, lw=1.1)                 # a little white vest
    c.set_source_rgb(*INK); c.arc(-3.2, -3, 1.0, 0, 6.3); c.fill(); c.arc(3.2, -3, 1.0, 0, 6.3); c.fill()
    c.set_line_width(1.1); c.arc(0, 1, 3.4, 0.2, math.pi - 0.2); c.stroke()
    c.move_to(0, -11); c.curve_to(2, -14, 4, -11, 2, -10); c.stroke()                          # the curl
    c.set_source_rgb(0.86, 0.22, 0.20); c.arc(2.5, 13, 1.4, 0, 6.3); c.fill()                  # the ketchup, already
    if BABY_DON[0]:
        c.set_source_rgb(0.86, 0.22, 0.20)                                                     # his stain, the same shape
        for dx, dy, r in ((1.5, 12.5, 2.6), (4.5, 14.5, 1.8), (-0.5, 15.0, 1.4), (3.0, 10.6, 1.2)):
            c.arc(dx, dy, r, 0, 6.3); c.fill()
        c.set_source_rgb(0.45, 0.47, 0.52); c.set_line_width(1.6)                              # a tiny headset
        c.arc(0, -2, 10.5, math.pi * 1.05, math.pi * 1.95); c.stroke()
        rect(k, -12.5, -5, 4, 6, (0.45, 0.47, 0.52), seed + 6, shadow=False, lw=0.8)
        rect(k, 8.5, -5, 4, 6, (0.45, 0.47, 0.52), seed + 7, shadow=False, lw=0.8)
    c.restore()


def mom_desk(k, x=None, floor=None, s=1.0, seed=720):
    """Her small desk: front panel, top, the plate ASSISTANT TO DON, the baby photo."""
    c = k.c
    x = MOMDESK[0] if x is None else x; floor = MOMDESK[1] if floor is None else floor
    c.save(); c.translate(x, floor); c.scale(s, s)
    rect(k, 0, -62, 92, 62, st.DESK, seed, lw=2.0)
    rect(k, -4, -70, 100, 10, st.DESK_DARK, seed + 1, lw=1.8)
    rect(k, 10, -86, 54, 15, (0.15, 0.17, 0.22), seed + 2, lw=1.2)                           # the plate
    _text(c, "ASSISTANT", 37, -79.5, 5.8)
    _text(c, "TO DON", 37, -73.2, 5.8)
    baby_photo(k, 78, -90, 0.55, seed + 3)
    c.restore()


def plan_taped(k, x, y, s=1.0, seed=740):
    """The plan of his ten garages, taped back from strips: every bay but 7, which is a gap."""
    c = k.c
    old = ac.GARAGES[0], ac.TITLE[0]
    ac.GARAGES[0], ac.TITLE[0] = True, True
    try:
        ac.plan_open(k, x, y, s, seed)
    finally:
        ac.GARAGES[0], ac.TITLE[0] = old
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, bx in enumerate((-52, -31, -10, 11, 32)):                                           # the cuts, taped
        c.set_source_rgba(0.97, 0.97, 0.90, 0.55); c.rectangle(bx - 3.5, -42, 4, 84); c.fill()
    n, bx, by, bw, bh = [b for b in ac._bays() if b[0] == 7][0]                                  # no. 7: missing
    c.set_source_rgb(*st.DESK); c.rectangle(bx - 1.5, by - 4, bw + 3, bh + 16); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.0); c.set_dash([3, 2]); c.rectangle(bx - 1.5, by - 4, bw + 3, bh + 16); c.stroke(); c.set_dash([])
    c.restore()


def phone(k, x, y, s=1.0, kind="bank", seed=760):
    """The Client's phone, close. kind: bank | paid | post | complete."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -46, -84, 92, 168, (0.10, 0.11, 0.14), seed, lw=2.2)
    sx0, sy0, sw, sh = -40, -74, 80, 150
    if kind == "bank":
        c.set_source_rgb(0.95, 0.96, 0.98); c.rectangle(sx0, sy0, sw, sh); c.fill()
        _text(c, "FRI", 0, -30, 22, col=RED)
        _text(c, "BANK", 0, 2, 22, col=INK)
        _text(c, "9:00", 0, 26, 12, col=(0.4, 0.42, 0.48), bold=False)
    elif kind == "paid":
        c.set_source_rgb(*GRN); c.rectangle(sx0, sy0, sw, sh); c.fill()
        _text(c, "PREMIUM", 0, -14, 15)
        _text(c, "PAID", 0, 10, 22)
    elif kind == "complete":
        c.set_source_rgb(0.95, 0.96, 0.98); c.rectangle(sx0, sy0, sw, sh); c.fill()
        c.set_source_rgb(*GRN); c.arc(0, -26, 18, 0, 6.3); c.fill()
        c.set_source_rgb(1, 1, 1); c.set_line_width(4); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(-8, -26); c.line_to(-2, -19); c.line_to(9, -33); c.stroke()
        _text(c, "100%", 0, 14, 22, col=INK)
        _text(c, "COMPLETE", 0, 32, 12.5, col=INK)
    elif kind == "post":
        c.set_source_rgb(0.95, 0.96, 0.98); c.rectangle(sx0, sy0, sw, sh); c.fill()
        c.set_source_rgb(*brand.NAVY); c.rectangle(sx0, sy0, sw, 13); c.fill()
        _text(c, "DON TAGGED YOU", 0, sy0 + 9.6, 6.6)
        ellipse(k, sx0 + 9, sy0 + 23, 6, 6, SKIN_DON, seed + 1, shadow=False, lw=1)          # Don's avatar
        _text(c, "DON", sx0 + 18, sy0 + 21, 6.4, col=INK, center=False)
        _text(c, "CEO · HEAD OF TALENT", sx0 + 18, sy0 + 28.5, 4.4, col=(0.4, 0.42, 0.48), center=False)
        c.set_source_rgb(*GRN); c.rectangle(sx0 + 4, sy0 + 34, sw - 8, 40); c.fill()           # the photo: the green zero
        _text(c, "0", sx0 + 30, sy0 + 64, 26)
        ellipse(k, sx0 + 58, sy0 + 56, 8, 8, SKIN_DON, seed + 2, shadow=False, lw=1)          # Don, thumb up
        rect(k, sx0 + 51, sy0 + 63, 14, 11, (0.16, 0.20, 0.34), seed + 3, shadow=False, lw=1)
        _text(c, "0 RESULTS.", 0, sy0 + 86, 8.4, col=INK)
        _text(c, "NOW IN GREEN.", 0, sy0 + 96, 8.4, col=GRN)
        _text(c, "#CustomerSuccess", 0, sy0 + 106, 6.6, col=(0.20, 0.40, 0.75), bold=False)
        c.set_source_rgb(0.86, 0.88, 0.92); c.rectangle(sx0 + 2, sy0 + 112, sw - 4, 36); c.fill()   # the comment
        ellipse(k, sx0 + 10, sy0 + 122, 6.5, 6.5, (0.40, 0.26, 0.20), seed + 4, shadow=False, lw=1)  # Pam: bob
        ellipse(k, sx0 + 10, sy0 + 124, 4.5, 4.5, kit.PEOPLE["PAM"]["skin"] if "PAM" in kit.PEOPLE else (0.96, 0.82, 0.70),
                seed + 5, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(0.8)
        c.rectangle(sx0 + 6, sy0 + 122, 3.4, 2.4); c.stroke(); c.rectangle(sx0 + 10.6, sy0 + 122, 3.4, 2.4); c.stroke()
        _text(c, "PAM", sx0 + 19, sy0 + 120, 6.0, col=INK, center=False)
        _text(c, "Some post.", sx0 + 19, sy0 + 130, 7.4, col=INK, bold=False, center=False)
        _text(c, "Others tape.", sx0 + 19, sy0 + 140, 7.4, col=INK, bold=False, center=False)
    c.restore()


def tablet_upgrade(k, x, y, s=1.0, seed=780):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -70, -50, 140, 100, (0.12, 0.13, 0.16), seed, lw=2.2)
    c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(-62, -42, 124, 84); c.fill()
    _text(c, "UPGRADE", 0, -22, 13, col=brand.NAVY)
    c.set_source_rgb(*GRN); c.rectangle(-52, -14, 104, 22); c.fill()
    _text(c, "PREMIUM", 0, 2, 13)
    _text(c, "GUARANTEED BY FRIDAY", 0, 22, 8.4, col=INK)
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(-8, 27, 16, 11); c.stroke()      # the tick box
    c.set_source_rgba(0.30, 0.25, 0.20, 0.35); c.arc(-34, 30, 6, 0, 6.3); c.fill()              # his old print
    c.restore()


REMOTE_BIG = [False]                                       # opt-in (board v2): a larger remote, ENTER on its button


def remote(c, x, y, s=1.0, ang=-0.6):
    """The screen's remote: a slim black stick, one big green ENTER button."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    if REMOTE_BIG[0]:
        c.scale(1.7, 1.7)
        c.set_source_rgb(0.10, 0.11, 0.14); c.rectangle(-7, -24, 14, 34); c.fill()
        c.set_source_rgb(*GRN); c.arc(0, -13, 6, 0, 6.3); c.fill()
        c.save(); c.translate(0, -13); c.rotate(-ang)
        _text(c, "ENTER", 0, 2, 3.6)
        c.restore()
        c.restore()
        return
    c.set_source_rgb(0.10, 0.11, 0.14); c.rectangle(-5, -20, 10, 30); c.fill()
    c.set_source_rgb(*GRN); c.arc(0, -12, 3.4, 0, 6.3); c.fill()
    c.restore()


def robot_finger(k, x, feet, s, state="eager", aim=1.0):
    """The robot by the door, its near arm up, the remote pointed at the screen over the door."""
    import robot_mf as rm
    o = rm.robot(k, x, feet, s, (0.0, 0, 0, (-20, 0), (150, 24)), state, (-1, -0.8), -1)
    hx, hy = o["hands"][1]
    remote(k.c, hx, hy - 6 * s, s * 1.6, ang=-0.7)
    return o


SOFIA_FS = [False]                                         # opt-in: Sofía in her episode-10 look (sofia_fs)


def master(k, screen_state="query", door_open=0.85):
    """Frame 0: the master wide (call inside set_ob.cam()). Pam and Mom stand behind the counter at the back."""
    import mom_bc
    import sofia_ob as so
    c = k.c
    v2 = LAYOUT[0] == "v2"
    P = POS2 if v2 else POS
    st.stage(k, open_=door_open, decor=False)
    screen(k, screen_state)
    portrait(k)
    ac.pam(k, *P["pam"], "typing")                                                              # behind the counter
    mom_bc.mom(k, P["mom"][0], P["mom"][1], P["mom"][2], "bag", "sweet", look=(-0.8, 0))
    st.desk(k, terminal=False, shred=None)
    plan_taped(k, *((356, F - 186, 0.30) if v2 else (404, F - 186, 0.32)))                     # on the counter
    counter_plate(k, *((398, F - 176) if v2 else (452, F - 176)))
    co.client(k, P["client"][0], P["client"][1], P["client"][2], "stand", "confident", look=(0.9, 0.0))
    robot_finger(k, *P["robot"])
    if SOFIA_FS[0] or v2:                                  # True = the current sofia_fs; or a module name
        import importlib
        mod = importlib.import_module(SOFIA_FS[0] if isinstance(SOFIA_FS[0], str) else "sofia_fs")
        if v2:
            mod.sofia(k, *P["sofia"], "hold", "charm", look=(-0.9, -0.2), lag=(-2, 0))
            ac.don(k, *P["don"], "stand", look=(-1, 0))
            return
        mod.sofia(k, *P["sofia"], "hold", "smile", look=(-0.9, -0.2))
    else:
        so.sofia(k, *P["sofia"], "hold", "smile", look=(-0.9, -0.2))
    ac.don(k, *P["don"], "stand", look=(-1, 0))


def counter_plate(k, x, y, seed=730):
    """Mom's place at the counter's end: ASSISTANT TO DON, and the baby photo."""
    c = k.c
    rect(k, x, y - 16, 56, 16, (0.15, 0.17, 0.22), seed, lw=1.2)
    _text(c, "ASSISTANT", x + 28, y - 9.5, 6.2)
    _text(c, "TO DON", x + 28, y - 2.6, 6.2)
    baby_photo(k, x - 14, y - 16, 0.62, seed + 3)


def cam2(c):
    """Call inside c.save(): the v2 master's camera."""
    c.scale(CAM2[2], CAM2[2]); c.translate(-CAM2[0], -CAM2[1])


def phone2(k, x, y, s=1.0, kind="bank", seed=760):
    """v2: one template for every phone insert. The frame is fixed (92 x 168 units); at most four lines; the smallest
    letters are 9 units, which is 9 px or more at the size the inserts are drawn (s >= 1 at 540)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -46, -84, 92, 168, (0.10, 0.11, 0.14), seed, lw=2.2)
    sx0, sy0, sw, sh = -40, -74, 80, 150
    bg = {"paid": GRN}.get(kind, (0.95, 0.96, 0.98))
    c.set_source_rgb(*bg); c.rectangle(sx0, sy0, sw, sh); c.fill()
    if kind == "bank":
        _text(c, "FRI", 0, -22, 24, col=RED)
        _text(c, "BANK", 0, 10, 24, col=INK)
    elif kind == "cal":                                    # v2 board: a calendar card, not a riddle
        rect(k, -26, -60, 52, 44, (1, 1, 1), seed + 7, shadow=False, lw=1.8)
        c.set_source_rgb(*RED); c.rectangle(-26, -60, 52, 12); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2.2)
        for gx in (-14, 0, 14):
            for gy in (-40, -28):
                c.rectangle(gx - 4, gy - 3, 8, 6); c.stroke()
        _text(c, "FRIDAY", 0, 14, 19, col=RED)
        _text(c, "BANK", 0, 38, 15, col=INK)
        _text(c, "MEETING", 0, 56, 15, col=INK)
    elif kind == "paid_price":                             # v2 board: what he paid
        c.set_source_rgb(*GRN); c.rectangle(sx0, sy0, sw, sh); c.fill()
        _text(c, "PREMIUM", 0, -26, 15)
        _text(c, "PAID", 0, 0, 22)
        _text(c, "$999", 0, 34, 24)
    elif kind == "paid":
        _text(c, "PREMIUM", 0, -10, 16)
        _text(c, "PAID", 0, 18, 24)
    elif kind == "complete":
        c.set_source_rgb(*GRN); c.arc(0, -28, 18, 0, 6.3); c.fill()
        c.set_source_rgb(1, 1, 1); c.set_line_width(4); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(-8, -28); c.line_to(-2, -21); c.line_to(9, -35); c.stroke()
        _text(c, "100%", 0, 16, 24, col=INK)
        _text(c, "COMPLETE", 0, 36, 13, col=INK)
    elif kind == "post":
        c.set_source_rgb(*brand.NAVY); c.rectangle(sx0, sy0, sw, 16); c.fill()
        _text(c, "DON TAGGED YOU", 0, sy0 + 11.5, 9)                                       # line 1
        c.set_source_rgb(*GRN); c.rectangle(sx0 + 4, sy0 + 20, sw - 8, 46); c.fill()            # the photo
        _text(c, "0", sx0 + 26, sy0 + 56, 30)
        ellipse(k, sx0 + 56, sy0 + 40, 9, 9, SKIN_DON, seed + 2, shadow=False, lw=1)           # Don, thumb up
        rect(k, sx0 + 48, sy0 + 49, 16, 14, (0.16, 0.20, 0.34), seed + 3, shadow=False, lw=1)
        _text(c, "0 RESULTS.", 0, sy0 + 80, 10, col=INK)                                       # line 2
        _text(c, "NOW IN GREEN.", 0, sy0 + 93, 10, col=GRN)                                    # line 3
        c.set_source_rgb(0.86, 0.88, 0.92); c.rectangle(sx0 + 2, sy0 + 100, sw - 4, 46); c.fill()
        ellipse(k, sx0 + 12, sy0 + 113, 8, 8, (0.40, 0.26, 0.20), seed + 4, shadow=False, lw=1)   # Pam: bob, glasses
        ellipse(k, sx0 + 12, sy0 + 115, 5.5, 5.5, (0.96, 0.82, 0.70), seed + 5, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(0.9)
        c.rectangle(sx0 + 7, sy0 + 113, 4, 3); c.stroke(); c.rectangle(sx0 + 12.5, sy0 + 113, 4, 3); c.stroke()
        _text(c, "PAM", sx0 + 24, sy0 + 112, 9, col=INK, center=False)
        _text(c, "Some post.", sx0 + 6, sy0 + 131, 10, col=INK, bold=False, center=False)    # line 4
        _text(c, "Others tape.", sx0 + 6, sy0 + 143, 10, col=INK, bold=False, center=False)
    c.restore()
