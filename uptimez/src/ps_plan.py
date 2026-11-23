"""PICK A SIDE (episode 14): the floor plan, v2 (23 Nov), after the floor-plan audit (v1 pinned as ps_plan_v1.py).
v2: frame 0 is a close on the two cords (blinds up, Don pulls down) so the loop matches on the blind; the robot's
visor shows a sun when the room goes dark; Don's office gag at the line replaces the likes; the last frame carries
the irony in bodies (Pam reaching across the line to her phone, Mom turned away).
The front desk v4 (fs_set4.py), drawn empty, with the CEO throne (dh_props.ceo_chair) on Don's mark, and on top:
the tape line, who stands where in the five key beats, and the ways they move. Nothing in fs_set4 or dh_props changes.
python3 ps_plan.py [out_dir] -> ps_plan_v3.png"""
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


def sun(c, x, y):
    c.save(); c.set_source_rgb(1.0, 0.80, 0.10); c.arc(x, y, 12, 0, 2 * math.pi); c.fill()
    c.set_line_width(3)
    for i in range(8):
        a = i * math.pi / 4
        c.move_to(x + 16 * math.cos(a), y + 16 * math.sin(a)); c.line_to(x + 24 * math.cos(a), y + 24 * math.sin(a)); c.stroke()
    c.restore()


def close_box(c, x, y, w, h, label):
    c.save(); c.set_source_rgb(0.85, 0.15, 0.15); c.set_line_width(4); c.set_dash([12, 6]); c.rectangle(x, y, w, h)
    c.stroke(); c.set_dash([]); c.select_font_face("Inter", 0, 1); c.set_font_size(18); c.move_to(x + 4, y - 8)
    c.show_text(label); c.restore()


def phone_glow(c, x, y):
    c.save(); c.set_source_rgba(0.6, 0.9, 1.0, 0.9); c.rectangle(x - 9, y - 15, 18, 30); c.fill(); c.restore()


def tag(c, x, y, text="$49,999"):
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
    ("0:00 · FRAME 0 · close on the cords", dict(line=False, blind="up"),
     lambda c: (close_box(c, 0, 380, 260, 380, "FRAME 0 = this close"), mark(c, "don", 70, 60, "pulls DOWN"),
                mark(c, "robot", 215, 30), sun(c, 215, 640), mark(c, "pam", 545, 40), mark(c, "mom", on_tape(15), 15),
                mark(c, "sofia", 600, 95),
                arrow(c, [(70, 560), (70, 700)], COL["don"]), arrow(c, [(200, 700), (200, 560)], COL["robot"])),
     "Frame 0 is a close on the blind: two hands, two cords, the blinds UP; Don's hand pulls down. The room goes dark, "
     "the robot's visor lights a sun and it pulls them back up. Down, up, faster. At 0:02 the blind tears and we go wide: "
     "Pam, Mom and Sofía mid-room, where the tape will run."),
    ("0:08–0:24 · the line, the choices", dict(line=True, blind="torn"),
     lambda c: (mark(c, "don", 420, 125, "spins the throne"), mark(c, "pam", 490, 55, "steps to Don", nx=-30),
                mark(c, "mom", on_tape(15), 15, "ON the tape", nx=40, ny=-6),
                mark(c, "sofia", on_tape(90) - 14, 90, "heel behind", nx=-46),
                mark(c, "robot", on_tape(140), 140, "astride ×3", nx=60, ny=30)),
     "The tape runs from the back wall to the camera between the shredder and the counter. DON's side: the door, the "
     "robot's station, the throne. FATHER's side: the counter, Pam's phone, Mom's desk, DON's own office door."),
    ("0:30 · the selfie · DING", dict(line=True, blind="torn", spun=True),
     lambda c: (silhouette(c), phone_glow(c, 120, 545), mark(c, "don", 420, 125, "poses"),
                mark(c, "pam", 490, 55), mark(c, "mom", on_tape(15), 15),
                mark(c, "sofia", on_tape(90) - 14, 90, "heel held", nx=-40),
                mark(c, "robot", on_tape(140), 140, "selfie arm up", nx=60, ny=30),
                arrow(c, [(610, 900), (300, 640)], (0.85, 0.15, 0.15), dash=False)),
     "The robot shoots a selfie from the line, its lens looking back and left, so the door's bare glass, bodyguard 2's "
     "silhouette and his phone's DING glow are in the photo's background (red: the lens). The photo then fills the screen."),
    ("0:45–0:55 · the office gag · the CV", dict(line=True, blind="down", spun=True),
     lambda c: (mark(c, "don", 535, 150, "foot over the line", nx=-30), mark(c, "bg", 120, 10, "in the door"),
                mark(c, "robot", 230, 40, "opens", nx=20), mark(c, "pam", 45, 90, "re-hangs the blind", nx=60, ny=40),
                mark(c, "sofia", 650, 60, "back over the line"), mark(c, "mom", on_tape(15), 15),
                arrow(c, [(545, 860), (880, 700)], COL["don"], dash=False),
                arrow(c, [(600, 820), (380, 790), (170, 805)], COL["sofia"]),
                arrow(c, [(190, 835), (430, 835), (630, 845)], COL["sofia"]),
                close_box(c, 60, 560, 200, 220, "insert: CV · COO?")),
     "Don, in front at the line, looks right at his own office door across it, lifts a foot to cross, stops (his own "
     "rule), puts it back, pretends nothing happened. Behind him, left, the CV is handed over at the door: an insert on "
     "COO?, then Pam's reaction, then Sofía's look back. Each its own shot."),
    ("0:57 · LAST FRAME → the blind", dict(line=True, blind="down", spun=True),
     lambda c: (mark(c, "don", 380, 145, "\"Everyone's with me.\""), mark(c, "robot", 215, 30, "yanks UP"),
                mark(c, "pam", 545, 55, "reaches across", nx=-20), mark(c, "mom", on_tape(15), 15, "turned away", nx=50),
                mark(c, "sofia", 650, 60, "COO? in hand", nx=20),
                arrow(c, [(555, 760), (640, 650)], COL["pam"], dash=False),
                close_box(c, 0, 380, 260, 380, "last shot = this close")),
     "Don alone in front, sincere. Behind him nobody is really with him: Pam's hand across the line to her lit phone, Mom "
     "turned away on the tape, Sofía on Father's side, the robot busy at the cord. The last shot is the close on the "
     "blind shooting UP; frame 0 is the same close with Don's hand pulling it DOWN: the loop matches on the movement."),
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
    corp(c, "PICK A SIDE  ·  floor plan v3  ·  the front desk v4 + the tape", gap, 52, 32, brand.NAVY, True)
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
    out = os.path.join(d, "ps_plan_v3.png"); s.write_to_png(out); return out


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    print(sheet(d))
