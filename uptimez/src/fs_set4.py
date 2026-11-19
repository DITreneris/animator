"""FIRST SEARCH (episode 10): the set v4 (fs_set3.py = v3, kept), after the set audit of 19 Nov. Set v3 stays ~90%;
fixed only what the audit found and Tomas's choices allow (the plan stays the shredded, taped blueprint, not a binder;
Mom's mug, candy and knitting stay, smaller):
- the counter's LEFT end shows: a side panel receding back, a deeper top; Mom's way round it is free floor;
- the shredder moved left, clear of that way; it reads as a shredder: SHRED on it, a sheet's edge in the slot;
- Pam's patched plan propped up big beside her, from frame 0 (the set-up for 5.3 and 8.1);
- Mom at home as the gatekeeper: fists on her hips, chin up, the unimpressed look, by DON's door;
- DON's door gets its status plate: a gilt DON · CEO · VISIONARY;
- depth: contact shadows under everyone, the counter's top plane visible, Don forward, Sofía back.
And the audit's test: two real camera frames on this set, S6 for 7.2 and S3 for 7.4.
python3 fs_set4.py [out_dir] -> fs_set_v4.png, fs_test72_v1.png, fs_test74_v1.png"""
import os
import sys
import math
import cairo
import kit
import brand
import set_ob as st
import acts_ob as ac
import fs_set as fs
import fs_storyboard as sb
import fs_set3 as s3
import mom_fs as mfs
import sofia_fs as sfs
import pam_fs
from kit import INK, rect, cut
from charsheets import corp, wrap

F = st.FLOOR
WW = 960
CX0, CX1 = 600, 890                                        # the counter's front, world x
DX = CX0 - 276                                             # its things, from set_ob's local coordinates
OFFICE = (896, 470, 56, 330)
SHRED = (514, F + 14, 0.88)
PORT = (440, 392)
HOME = {"client": (110, F - 14, 0.52), "robot": (232, F + 4, 0.48), "sofia": (352, F - 26, 0.47),
        "don": (440, F + 26, 0.60), "pam": (368 + DX, F - 72, 0.50), "mom": (500 + DX, F - 70, 0.50)}
ZONES = [("A", "discovery and arrivals", 0, 280, (0.20, 0.45, 0.85)),
         ("B", "the irony: under OUR FIRST CLIENT", 280, 570, (0.85, 0.30, 0.25)),
         ("C", "the counter and the boss's door", 570, WW, (0.20, 0.60, 0.35))]
DESK, DESK_DARK, TOP = st.DESK, st.DESK_DARK, (0.93, 0.89, 0.80)


def shadow(k, x, y, w):
    c = k.c
    c.save(); c.translate(x, y); c.scale(w, w * 0.16)
    c.set_source_rgba(0, 0, 0, 0.16); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()


def counter(k):
    """The counter seen from the front-left: its left end recedes back, its top plane deeper than set_ob's."""
    f = F
    shadow(k, (CX0 + CX1) / 2, f + 2, (CX1 - CX0) * 0.55)
    cut(k, [(CX0 - 2, f - 2), (CX0 - 2, f - 150), (CX0 + 34, f - 196), (CX0 + 34, f - 50)], DESK_DARK, lw=2.2)   # the end
    cut(k, [(CX0 - 6, f - 150), (CX1 + 2, f - 150), (CX1 + 2, f - 196), (CX0 + 30, f - 196)], TOP, shadow=False, lw=2.2)
    rect(k, CX0, f - 150, CX1 - CX0, 150, DESK, 320, shadow=False, lw=2.4)
    rect(k, CX0 - 6, f - 154, CX1 - CX0 + 8, 11, DESK_DARK, 321, shadow=False, lw=2)
    k.c.set_source_rgba(*DESK_DARK, 0.8); k.c.set_line_width(1.6)
    for xx in (CX0 + 96, CX0 + 192):
        k.c.move_to(xx, f - 134); k.c.line_to(xx, f - 10); k.c.stroke()


def shredder(k, fill=0.4):
    x, f, s = SHRED
    shadow(k, x, f + 2, 40 * s)
    ac.shredder(k, x, f, s, fill=fill)
    c = k.c
    c.save(); c.translate(x, f); c.scale(s, s)
    rect(k, -20, -40, 40, 14, (0.86, 0.10, 0.12), 41, shadow=False, lw=1.4)                       # SHRED
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(10.5)
    e = c.text_extents("SHRED"); c.move_to(-e.x_advance / 2, -29.5); c.show_text("SHRED")
    cut(k, [(-14, -108), (14, -108), (16, -132), (-12, -134)], (0.98, 0.97, 0.94), shadow=False, lw=1.4)  # a sheet's edge
    c.restore()


def office_door(k):
    x, y, w, h = OFFICE
    old = s3.OFFICE
    s3.OFFICE = OFFICE
    try:
        s3.office_door(k)
    finally:
        s3.OFFICE = old
    c = k.c                                                                       # the status plate, gilt
    rect(k, x - 4, y - 46, w + 8, 34, (0.85, 0.70, 0.30), 806, lw=1.6)
    c.set_source_rgb(0.25, 0.18, 0.05); c.select_font_face("Inter", 0, 1)
    for txt, yy, fz in (("DON · CEO", y - 31, 10), ("VISIONARY", y - 18, 9)):
        c.set_font_size(fz); e = c.text_extents(txt); c.move_to(x + w / 2 - e.x_advance / 2, yy); c.show_text(txt)


def mom_home(k):
    return mfs.mom(k, *HOME["mom"], "fists", "unimpressed", look=(-0.9, 0.3), chin=True)


def draw_set(k, cast="home", sleeves=False):
    """cast: "home" (everyone at home) or a dict of callables: pam_back, mom_back (behind the counter), then client,
    robot, sofia, don, mom_front (in front of it)."""
    c = k.c
    oldW = st.W
    st.W = WW
    try:
        st.stage(k, open_=0.85, decor=False, back=False)
    finally:
        st.W = oldW
    brand.mark(c, 300, 230, 56, zzz=False)
    fs.screen(k, "query", *s3.SCR)
    fs.PSTATE[0] = "clean"
    try:
        fs.portrait(k, *PORT, fs.PORTRAIT_S)
    finally:
        fs.PSTATE[0] = None
    office_door(k)
    s3.confetti(k, 4, F + 2, 60, 1)
    s3.confetti(k, 462, F - 2, 22, 2)
    home = cast == "home"
    custom = cast if isinstance(cast, dict) else {}
    with pam_fs.look(sleeves):
        if home:
            sb.pam_taping(k, *HOME["pam"])
            mom_home(k)
        for who in ("pam_back", "mom_back"):
            if who in custom:
                custom[who](k)
        counter(k)
        c.save(); c.translate(DX, 0)
        fs.PLAN_V2[0] = True
        try:                                                                       # the plan, propped up, big
            c.save(); c.translate(432, F - 214); c.rotate(-0.06); fs.plan_taped(k, 0, 0, 0.50); c.restore()
        finally:
            fs.PLAN_V2[0] = False
        s3.monitor(k, 300, F - 190, 1.0)
        fs.counter_plate(k, 486, F - 190)
        mfs.candy(k, 380, F - 168, 0.45); mfs.knitting(k, 530, F - 166, 0.30); mfs.mug(k, 552, F - 200, 0.42)
        c.restore()
        shredder(k)
        if home:
            shadow(k, HOME["client"][0], F - 12, 44); sb.client(k, *HOME["client"], "stand", "confident", (0.9, 0))
            shadow(k, HOME["robot"][0], F + 6, 30); fs.robot_finger(k, *HOME["robot"])
            shadow(k, HOME["sofia"][0], F - 24, 32); sfs.sofia(k, *HOME["sofia"], "hold", "charm", look=(0.6, -0.2))
            shadow(k, HOME["don"][0], F + 28, 46)
            sb.DON_STATE[0] = ("up", "up")
            try:
                sb.don(k, *HOME["don"], "stand", "neutral", (-1, 0))
            finally:
                sb.DON_STATE[0] = None
        for who in ("client", "robot", "sofia", "don", "mom_front"):
            if who in custom:
                custom[who](k)


def sheet_set(d):
    S = 1.2
    W1, H1 = int(WW * S), int(960 * S)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W1 + 40, H1 + 170)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    corp(c, "FIRST SEARCH  ·  set v4: v3 with the audit's fixes", 20, 52, 32, brand.NAVY, True)
    wrap(c, "The counter's left end shows, and the floor round it is free: Mom's way out. The shredder moved left and "
            "says SHRED. Pam's patched plan propped up big from frame 0. Mom at home: the gatekeeper. DON's door: "
            "its status plate. Shadows under everyone.", 20, 86, 17, W1)
    c.save(); c.translate(20, 150); c.scale(S, S); c.rectangle(0, 0, WW, 960); c.clip()
    draw_set(k)
    c.set_source_rgba(0.13, 0.55, 0.58, 0.9); c.set_line_width(4); c.set_dash([10, 7])         # Mom's way out
    c.move_to(CX0 + 150, F - 30); c.curve_to(CX0 + 40, F + 0, CX0 - 10, F + 30, SHRED[0] + 70, F + 60); c.stroke()
    c.set_dash([])
    c.set_source_rgb(0.13, 0.55, 0.58); c.select_font_face("Inter", 0, 1); c.set_font_size(16)
    c.move_to(CX0 - 30, F + 84); c.show_text("Mom's way out")
    for z, name, x0, x1, col in ZONES:
        c.set_source_rgba(*col, 0.12); c.rectangle(x0, F + 100, x1 - x0, 60); c.fill()
        c.set_source_rgb(*col); c.set_font_size(30); c.move_to(x0 + 10, F + 142); c.show_text(z)
        c.set_font_size(14); c.move_to(x0 + 40, F + 138); c.show_text(name)
    c.restore()
    out = os.path.join(d, "fs_set_v4.png"); s.write_to_png(out); return out


def frame(d, name, cam, cast, sleeves):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save(); sb.view(c, *cam)
    draw_set(k, cast, sleeves)
    c.restore()
    p = os.path.join(d, name); s.write_to_png(p)
    return p


def cast72():
    def mom(k):                                                                   # coming round the counter's end
        shadow(k, 566, F + 12, 40)
        mfs.mom(k, 566, F + 10, 0.62, "lick", "sweet", look=(-1, -0.3), lean=-4)
    def don(k):
        shadow(k, 452, F + 30, 46)
        sb.DON_STATE[0] = ("up", "up")
        try:
            sb.don(k, 452, F + 26, 0.60, "panic", "shock", (1, -0.2))
        finally:
            sb.DON_STATE[0] = None
    def client(k):
        shadow(k, 372, F + 2, 44); sb.client(k, 372, F - 4, 0.54, "stand", "dawning", (1, 0))
    def sofia(k):
        shadow(k, 312, F - 24, 32); sfs.sofia(k, 312, F - 26, 0.47, "hold", "fake", look=(1, 0))
    return {"client": client, "sofia": sofia, "don": don, "mom_front": mom,
            "pam_back": lambda k: sb.pam_taping(k, *HOME["pam"])}


def cast74():
    head = {}

    def don(k):
        shadow(k, 430, F + 30, 46)
        sb.DON_STATE[0] = ("up", "flat")
        try:
            o = sb.don(k, 430, F + 26, 0.60, "stand", "squint", (0.6, 0.2))
        finally:
            sb.DON_STATE[0] = None
        head["xy"] = o["head"]

    def mom(k):                                                                   # at his right, her thumb on his hair
        import mom_bc as mb
        mx, mf, ms = 512, F + 34, 0.62
        hx, hy = head["xy"]
        tx, ty = hx + 6, hy - 30
        shadow(k, mx, mf + 4, 40)
        import mom_on as mo
        pose = mo.ik(-1, (tx - mx) / ms, (ty - mf) / ms) + mo.ik(1, 30, mo.SASH + 2)    # her near arm up to his head
        mfs.mom(k, mx, mf, ms, pose, "sweet", look=(-1, -0.6), bag=False)
        sb.thumb(k, tx, ty + 4, 0.16, skin=(0.96, 0.80, 0.70), ang=-2.2, who="mom")
        c = k.c
        c.set_source_rgb(*INK); c.set_line_width(2.2)                                 # the scrub
        for dd in (0, 6):
            c.new_path(); c.arc(tx - 4, ty, 14 + dd, -2.6, -0.5); c.stroke()

    def sofia(k):
        shadow(k, 364, F + 6, 32); sfs.sofia(k, 364, F + 4, 0.50, "stand", "ew", look=(1, 0))
    return {"sofia": sofia, "don": don, "mom_front": mom, "pam_back": lambda k: sb.pam_taping(k, *HOME["pam"])}


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    os.makedirs(d, exist_ok=True)
    print(sheet_set(d))
    print(frame(d, "fs_test72_v1.png", (476, 668, 1.85), cast72(), True))
    print(frame(d, "fs_test74_v1.png", (448, 664, 2.15), cast74(), True))
