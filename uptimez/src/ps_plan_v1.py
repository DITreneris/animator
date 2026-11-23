"""PICK A SIDE (episode 14): the floor plan, v1 (23 Nov), after the v3 audit.
The front desk v4 (fs_set4.py), drawn empty, with the CEO throne (dh_props.ceo_chair) on Don's mark, and on top:
the tape line, who stands where in the five key beats, and the ways they move. Nothing in fs_set4 or dh_props changes.
python3 ps_plan.py [out_dir] -> ps_plan_v1.png"""
import os
import sys
import math
import cairo
import kit
import brand
import fs_set4 as s4
import dh_props as dp
from charsheets import corp, wrap

F = s4.F
LINE_X = 560            # the tape, world x on the floor's back edge; left = DON's side (A+B), right = FATHER's (C)
COL = {"don": (0.15, 0.25, 0.55), "pam": (0.45, 0.25, 0.60), "mom": (0.20, 0.55, 0.55), "sofia": (0.85, 0.15, 0.50),
       "robot": (0.35, 0.35, 0.40), "bg": (0.10, 0.10, 0.10)}
LET = {"don": "D", "pam": "P", "mom": "M", "sofia": "S", "robot": "R", "bg": "B2"}


def tape(c, label=True):
    """The tape seen on the floor: from the back wall to the front edge, splaying with depth."""
    c.save()
    c.set_source_rgb(0.95, 0.78, 0.15)
    c.move_to(LINE_X - 7, F); c.line_to(LINE_X + 7, F); c.line_to(LINE_X + 46, 960); c.line_to(LINE_X + 22, 960)
    c.close_path(); c.fill_preserve()
    c.set_source_rgb(0.2, 0.15, 0.0); c.set_line_width(1.5); c.stroke()
    if label:
        c.set_source_rgba(0.95, 0.78, 0.15, 0.5); c.set_line_width(3); c.set_dash([8, 8])
        c.move_to(LINE_X, 120); c.line_to(LINE_X, F); c.stroke(); c.set_dash([])
        c.select_font_face("Inter", 0, 1); c.set_font_size(30)
        c.set_source_rgb(0.15, 0.25, 0.55); c.move_to(LINE_X - 200, 150); c.show_text("◀ DON's side")
        c.set_source_rgb(0.60, 0.10, 0.10); c.move_to(LINE_X + 30, 150); c.show_text("FATHER's side ▶")
    c.restore()


def mark(c, who, x, dy=0, note="", r=22, nx=0, ny=0):
    """A position: a disc on the floor at world x, depth dy below the floor line (+ = nearer the camera)."""
    y = F + dy
    col = COL[who]
    c.save()
    c.set_source_rgba(0, 0, 0, 0.18); c.save(); c.translate(x, y + 4); c.scale(1, 0.3); c.arc(0, 0, r, 0, 2 * math.pi)
    c.restore(); c.fill()
    c.set_source_rgb(*col); c.arc(x, y - r, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(1, 1, 1); c.set_line_width(3); c.stroke()
    c.select_font_face("Inter", 0, 1); c.set_font_size(20 if len(LET[who]) == 1 else 15)
    e = c.text_extents(LET[who]); c.move_to(x - e.width / 2 - e.x_bearing, y - r + e.height / 2); c.show_text(LET[who])
    if note:
        c.set_font_size(15); c.set_source_rgb(*col)
        e = c.text_extents(note); tx, ty = x - e.width / 2 + nx, y - 2 * r - 8 + ny
        c.set_source_rgba(1, 1, 1, 0.8); c.rectangle(tx - 3, ty - 14, e.width + 6, 19); c.fill()
        c.set_source_rgb(*col); c.move_to(tx, ty); c.show_text(note)
    c.restore()


def arrow(c, pts, col=(0.1, 0.1, 0.1), dash=True):
    c.save(); c.set_source_rgba(*col, 0.85); c.set_line_width(3.5)
    if dash:
        c.set_dash([10, 7])
    c.move_to(*pts[0])
    if len(pts) == 3:
        c.curve_to(*pts[1], *pts[1], *pts[2])
    else:
        c.line_to(*pts[1])
    c.stroke(); c.set_dash([])
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    c.move_to(x1, y1); c.line_to(x1 - 16 * math.cos(a - 0.4), y1 - 16 * math.sin(a - 0.4))
    c.line_to(x1 - 16 * math.cos(a + 0.4), y1 - 16 * math.sin(a + 0.4)); c.close_path(); c.fill()
    c.restore()


def blinds(c, state):
    """On the door's glass (world x 20-176, y 392-800): 'down' (closed slats), 'torn' (gone), 'up' (a roll at the top)."""
    c.save()
    if state == "down":
        c.set_source_rgba(0.85, 0.85, 0.80, 0.95); c.rectangle(22, 394, 152, 400); c.fill()
        c.set_source_rgb(0.55, 0.55, 0.50); c.set_line_width(1.2)
        for yy in range(404, 794, 14):
            c.move_to(22, yy); c.line_to(174, yy); c.stroke()
    elif state == "up":
        c.set_source_rgb(0.80, 0.80, 0.75); c.rectangle(22, 394, 152, 18); c.fill()
    c.set_source_rgb(0.3, 0.3, 0.3); c.set_line_width(1.5)             # the two cords, either side
    if state != "torn":
        for xx in (30, 166):
            c.move_to(xx, 400); c.line_to(xx, 700); c.stroke()
    c.restore()


def silhouette(c, x=100):
    """Bodyguard 2 behind the glass: a big dark shape."""
    c.save(); c.set_source_rgba(0.08, 0.08, 0.10, 0.75)
    c.arc(x, 520, 30, 0, 2 * math.pi); c.fill()
    c.move_to(x - 60, 800); c.line_to(x - 52, 590); c.curve_to(x - 40, 560, x + 40, 560, x + 52, 590)
    c.line_to(x + 60, 800); c.close_path(); c.fill()
    c.restore()


def phone_glow(c, x, y):
    c.save(); c.set_source_rgba(0.6, 0.9, 1.0, 0.9); c.rectangle(x - 9, y - 15, 18, 30); c.fill(); c.restore()


def tag(c, x, y, text="PAID BY DAD"):
    c.save(); c.set_source_rgb(0.85, 0.12, 0.12); c.rectangle(x, y, 92, 22); c.fill()
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.move_to(x + 6, y + 15)
    c.show_text(text); c.restore()


def room(k, line=True, blind="down", spun=False):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.paint()
    s4.draw_set(k, {})
    dp.ceo_chair(k, 452, F + 8, 0.60)
    if spun:
        c.save(); c.set_source_rgba(1, 1, 1, 0.75); c.rectangle(380, 610, 145, 22); c.fill()
        c.set_source_rgb(0.6, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(14)
        c.move_to(384, 626); c.show_text("spun: tag to the wall"); c.restore()
    else:
        tag(c, 410, 560)
    blinds(c, blind)
    if line:
        tape(c)
    phone_glow(c, 640, 640)                                         # Pam's phone, face up, on the counter's left end
    c.save(); c.set_source_rgb(0.3, 0.3, 0.3); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
    c.move_to(612, 672); c.show_text("Pam's phone (face up)"); c.restore()


def on_tape(dy):
    return LINE_X + 7 + dy * 31 / 160


PANELS = [
    ("0:00 · FRAME 0 · neutral", dict(line=False, blind="down"),
     lambda c: (mark(c, "don", 70, 60, "cord L"), mark(c, "robot", 215, 30, "cord R"),
                mark(c, "pam", 545, 40), mark(c, "mom", on_tape(15), 15), mark(c, "sofia", 600, 95),
                arrow(c, [(70, 700), (70, 560)], COL["don"]), arrow(c, [(200, 560), (200, 700)], COL["robot"])),
     "No line yet. Don and the robot each hold a blind cord (tug of war). Pam, Mom and Sofía stand where the tape "
     "will run, so the tape goes straight through them."),
    ("0:08–0:24 · the line, the choices", dict(line=True, blind="torn"),
     lambda c: (mark(c, "don", 420, 125, "spins the throne"), mark(c, "pam", 490, 55, "steps to Don", nx=-30),
                mark(c, "mom", on_tape(15), 15, "ON the tape", nx=40, ny=-6), mark(c, "sofia", on_tape(90) - 14, 90, "heel behind", nx=-46),
                mark(c, "robot", on_tape(140), 140, "astride ×3", nx=60, ny=30)),
     "The tape runs from the back wall to the camera between the shredder and the counter. DON's side: the door, the "
     "robot's station, the throne. FATHER's side: the counter, Pam's phone, Mom's desk, DON's own office door."),
    ("0:30 · the selfie · DING", dict(line=True, blind="torn", spun=True),
     lambda c: (silhouette(c), phone_glow(c, 120, 545), mark(c, "don", 420, 125, "poses"),
                mark(c, "pam", 490, 55), mark(c, "mom", on_tape(15), 15),
                mark(c, "sofia", on_tape(90) - 14, 90, "heel held", nx=-40),
                mark(c, "robot", on_tape(140), 140, "selfie arm up", nx=60, ny=30)),
     "The robot shoots a selfie from the line, so it is in the picture too. The door's glass is bare (the blind tore): "
     "bodyguard 2's silhouette is in the photo, and his phone lights up on the DING."),
    ("0:45–0:55 · the CV · the look", dict(line=True, blind="down", spun=True),
     lambda c: (mark(c, "don", 380, 145, "likes, faces the camera"), mark(c, "bg", 120, 10, "in the door"),
                mark(c, "robot", 230, 40, "opens", nx=20), mark(c, "pam", 45, 90, "re-hangs the blind", nx=60, ny=40),
                mark(c, "sofia", 650, 60, "back over the line"), mark(c, "mom", on_tape(15), 15),
                arrow(c, [(600, 820), (380, 790), (170, 805)], COL["sofia"]),
                arrow(c, [(190, 835), (430, 835), (630, 845)], COL["sofia"]),
                arrow(c, [(70, 830), (610, 700)], COL["pam"], dash=False),
                arrow(c, [(640, 780), (90, 760)], COL["sofia"], dash=False)),
     "Don, in front, faces the camera, counting likes on his post: everything happens behind him. Sofía walks upstage to "
     "the door, gets the CV, walks back across the line and sees Pam's phone light up. Pam, re-hanging the blind at the "
     "door, saw the CV. The look crosses the room behind Don's head."),
    ("0:57 · LAST FRAME → frame 0", dict(line=True, blind="down", spun=True),
     lambda c: (mark(c, "don", 380, 145, "\"Everyone's with me.\""), mark(c, "robot", 215, 30, "pulls the cord"),
                mark(c, "pam", 490, 55), mark(c, "mom", on_tape(15), 15), mark(c, "sofia", 650, 60, "COO? in hand", nx=20)),
     "Same camera as frame 0. Set differences from frame 0, both declared: the tape, and the throne spun. People may "
     "stand differently (the loop check compares the set). The robot pulls the cord: the blinds go up; cut to frame 0."),
]


def sheet(d):
    S = 0.5
    PW, PH = int(960 * S), int(960 * S)
    cols, gap, top = 3, 30, 170
    rows = math.ceil(len(PANELS) / cols)
    W = cols * PW + (cols + 1) * gap
    H = top + rows * (PH + 190)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    corp(c, "PICK A SIDE  ·  floor plan v1  ·  the front desk v4 + the tape", gap, 52, 32, brand.NAVY, True)
    wrap(c, "The line at world x %d: Don keeps the door, the robot and his throne; Father's side gets the counter, the work, "
            "Pam's phone and Don's own office door. Discs: D Don, P Pam, M Mom, S Sofía, R robot, B2 bodyguard 2. "
            "Dashed: moves. Solid: looks." % LINE_X, gap, 86, 17, W - 2 * gap)
    for i, (title, opts, marks, note) in enumerate(PANELS):
        x = gap + (i % cols) * (PW + gap)
        y = top + (i // cols) * (PH + 190)
        c.save(); c.translate(x, y); c.scale(S, S); c.rectangle(0, 0, 960, 960); c.clip()
        room(k, **opts)
        marks(c)
        c.restore()
        c.set_source_rgb(0.2, 0.2, 0.2); c.set_line_width(1); c.rectangle(x, y, PW, PH); c.stroke()
        corp(c, title, x, y + PH + 26, 17, brand.NAVY, True)
        wrap(c, note, x, y + PH + 50, 13, PW)
    out = os.path.join(d, "ps_plan_v1.png"); s.write_to_png(out); return out


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    print(sheet(d))
