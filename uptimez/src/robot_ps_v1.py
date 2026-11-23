"""THE ROBOT in "Pick a Side" (episode 14): the HR robot at the office scale of 13 (0.66), with this episode's parts.
Tomas, 23 Nov, /grill-me:
- the selfie: a TELESCOPIC arm out of its side with a phone clamped at the end; FLASH; it turns the phone to Don with
  the photo and PUBLIC POST? on it, then #TeamDon (one prop carries the photo, the question and the post);
- its ONE wheel balances ON the tape like a tightrope walker, arms out; each push knocks it off and it rolls back on;
- visor icons in its own cyan, line pictograms like 13's WITHOUT HIM: a sun (the room went dark), a striped barrier
  with one red light (Border breach);
- when it bumps Don it keeps its usual smile: never sly, never aggressive.
Nothing in its rig changes: the parts are drawn over dh_poses.rm.robot's figure, at its own screen and hand points.
  robot(k, x, feet, s, arms=None, tilt=0.0, visor=None, selfie=0.0, phone=None, turn=0.0)
  phone_screen(k, x, y, s, kind)     kind: "photo", "public", "posted" (the insert of 3.2/3.3/3.5)
  python3 robot_ps.py [out_dir]  ->  ps_robot_v1.png (sheet), ps_robot_phone_v1.png (phone check)"""
import math
import os
import sys
import cairo
import kit
import of_cast as oc
from kit import Ctx, INK, cut, rect, ellipse

dq = oc.dq
CYAN = (0.45, 0.92, 1.0)
VISOR = (0.09, 0.12, 0.24)
TAPE = (0.95, 0.78, 0.15)
STEEL, STEEL_D = (0.72, 0.74, 0.78), (0.50, 0.52, 0.56)
S_OFFICE = 0.66                                            # 13's office scale (lesson 138), 95 % of Don


def visor_icon(k, sx, sy, r, kind):
    """Over the face: the dark visor, then one cyan pictogram. kind: "sun", "barrier", "public"."""
    c = k.c
    c.set_source_rgb(*VISOR); c.arc(sx, sy, 0.86 * r, 0, 2 * math.pi); c.fill()
    g = cairo.RadialGradient(sx, sy, 0.1 * r, sx, sy, 0.86 * r)
    g.add_color_stop_rgba(0, *CYAN, 0.18); g.add_color_stop_rgba(1, *CYAN, 0.0)
    c.set_source(g); c.arc(sx, sy, 0.86 * r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*CYAN); c.set_line_cap(1); c.set_line_join(1)
    if kind == "sun":
        c.set_line_width(0.07 * r); c.arc(sx, sy, 0.22 * r, 0, 2 * math.pi); c.stroke()
        for i in range(8):
            a = i * math.pi / 4
            c.move_to(sx + math.cos(a) * 0.34 * r, sy + math.sin(a) * 0.34 * r)
            c.line_to(sx + math.cos(a) * 0.52 * r, sy + math.sin(a) * 0.52 * r); c.stroke()
    elif kind == "barrier":
        w, h = 0.98 * r, 0.22 * r
        x0, y0 = sx - w / 2, sy - h / 2 + 0.08 * r
        c.set_line_width(0.05 * r); c.rectangle(x0, y0, w, h); c.stroke()
        c.save(); c.rectangle(x0, y0, w, h); c.clip()
        for i in range(-2, 8):                                            # the stripes
            xx = x0 + i * 0.20 * r
            c.move_to(xx, y0 + h); c.line_to(xx + h, y0); c.set_line_width(0.06 * r); c.stroke()
        c.restore()
        for lx in (x0 + 0.12 * r, x0 + w - 0.12 * r):                     # its legs
            c.move_to(lx, y0 + h); c.line_to(lx, y0 + h + 0.24 * r); c.stroke()
        c.set_source_rgba(1.0, 0.25, 0.20, 0.35); c.arc(sx, y0 - 0.16 * r, 0.17 * r, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(1.0, 0.28, 0.22); c.arc(sx, y0 - 0.16 * r, 0.09 * r, 0, 2 * math.pi); c.fill()   # the red light
    elif kind == "public":
        c.select_font_face("Lilita One"); c.set_font_size(0.30 * r)
        for i, t in enumerate(("PUBLIC", "POST?")):
            e = c.text_extents(t); c.move_to(sx - e.x_advance / 2, sy - 0.04 * r + i * 0.34 * r); c.show_text(t)


def phone_screen(k, x, y, s, kind="photo", seed=4700):
    """The selfie phone, screen to us, centred at (x, y). kind "photo": the team shot (a stand-in here: in the film it is
    rendered from 3.1's own frame); "public": PUBLIC POST? over it with a green approve pad; "posted": #TeamDon."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -60, -104, 120, 208, (0.08, 0.08, 0.09), seed, shadow=False, lw=2.6)
    c.set_source_rgb(0.96, 0.96, 0.98); c.rectangle(-52, -94, 104, 188); c.fill()
    px, py, pw, ph = -46, -70, 92, 92                                    # the photo
    c.set_source_rgb(0.90, 0.85, 0.74); c.rectangle(px, py, pw, ph); c.fill()
    c.set_source_rgb(0.72, 0.62, 0.48); c.rectangle(px, py + 66, pw, ph - 66); c.fill()   # the floor
    c.set_source_rgb(*TAPE); c.move_to(px + 58, py + 66); c.line_to(px + 64, py + 66); c.line_to(px + 72, py + ph)
    c.line_to(px + 62, py + ph); c.close_path(); c.fill()
    c.set_source_rgba(0.1, 0.1, 0.1, 0.7); c.rectangle(px + 2, py + 8, 16, 58); c.fill()  # the silhouette at the glass
    c.arc(px + 10, py + 6, 7, 0, 2 * math.pi); c.fill()
    for fx, col, top in ((px + 30, (0.15, 0.25, 0.55), 26), (px + 44, (0.45, 0.25, 0.60), 34), (px + 60, (0.20, 0.55, 0.55), 34),
                         (px + 76, (0.99, 0.97, 0.91), 30)):              # Don, Pam, Mom on the tape, Sofía
        c.set_source_rgb(*col); c.rectangle(fx - 5, py + top, 10, 66 - top); c.fill()
        c.set_source_rgb(0.93, 0.76, 0.62); c.arc(fx, py + top - 5, 5, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.08, 0.08, 0.09); c.rectangle(px + 70, py + 62, 6, 4); c.fill()   # her heel behind the tape
    if kind == "public":
        c.set_source_rgba(0.08, 0.10, 0.18, 0.88); c.rectangle(-52, 26, 104, 68); c.fill()
        c.set_source_rgb(*CYAN); c.select_font_face("Lilita One"); c.set_font_size(17)
        e = c.text_extents("PUBLIC POST?"); c.move_to(-e.x_advance / 2, 50); c.show_text("PUBLIC POST?")
        rect(k, -30, 60, 60, 24, (0.20, 0.68, 0.36), seed + 1, shadow=False, lw=1.6)
        c.set_source_rgb(1, 1, 1); c.set_line_width(3); c.move_to(-8, 72); c.line_to(-2, 78); c.line_to(10, 64); c.stroke()
    else:
        c.set_source_rgb(0.15, 0.17, 0.25); c.select_font_face("Lilita One"); c.set_font_size(18)
        t = "#TeamDon" if kind == "posted" else ""
        e = c.text_extents(t); c.move_to(-e.x_advance / 2, 52); c.show_text(t)
        if kind == "posted":
            c.set_source_rgb(0.80, 0.30, 0.40); c.select_font_face("Inter", 0, 1); c.set_font_size(11)
            c.move_to(-40, 76); c.show_text("♥ 1   · just now")
    c.restore()


def telescope(k, bx, by, s, u, angle=0.30, seed=4720):
    """The arm, telescoped out of its hand point (bx, by) by u (0..1), leaning by angle; returns the tip."""
    c = k.c
    L = 230 * u
    c.save(); c.translate(bx, by); c.rotate(angle); c.scale(s, s)
    for i, (w, l0, l1) in enumerate(((16, 0, 0.40), (12, 0.34, 0.72), (9, 0.66, 1.0))):
        if L * l1 <= 0:
            continue
        rect(k, -w / 2, -L * l1, w, L * (l1 - l0), STEEL if i % 2 == 0 else STEEL_D, seed + i, shadow=False, lw=2)
    c.restore()
    return bx + math.sin(angle) * L * s, by - math.cos(angle) * L * s


def robot(k, x, feet, s=S_OFFICE, arms=None, tilt=0.0, visor=None, selfie=0.0, phone=None, turn=0.0, look=(0, 0)):
    """arms: ((upper, fore) screen-left, (upper, fore) screen-right) in kit angles (0 down, +90 right); tilt: radians it
    leans about its wheel (balancing); visor: None (its smile) or an icon; selfie: 0..1 the telescope out of its
    screen-right hand; phone: the phone's screen at the tip ("photo", "public", "posted", or None for its back)."""
    c = k.c
    a = arms or ((-8, 0), (8, 0))
    pose = (tilt, 0, 0, a[0], a[1])
    o = dq.rm.robot(k, x, feet, s, pose, "eager", look, 1)
    r = 50 * s
    if visor:
        visor_icon(k, *o["screen"], r, visor)
    if selfie > 0:
        hx, hy = o["hands"][1]
        tx, ty = telescope(k, hx, hy, s, selfie)
        if phone:
            phone_screen(k, tx, ty - 30 * s, s * 0.34, phone)
        else:
            c.save(); c.translate(tx, ty - 30 * s); c.scale(s * 0.34, s * 0.34)
            rect(k, -60, -104, 120, 208, (0.10, 0.10, 0.12), 4730, shadow=False, lw=2.6)
            ellipse(k, 0, -70, 12, 12, (0.30, 0.32, 0.38), 4731, shadow=False, lw=2)          # the camera, at us
            c.restore()
        o["phone"] = (tx, ty - 30 * s)
    return o


def tape(k, x, wall, bottom, top_w=10, bot_w=34, lean=0.08):
    """The tape on the floor, from the wall line to the bottom of the frame, widening toward us (it runs at the camera)."""
    dx = (bottom - wall) * lean
    cut(k, [(x - top_w / 2, wall), (x + top_w / 2, wall), (x + dx + bot_w / 2, bottom), (x + dx - bot_w / 2, bottom)], TAPE,
        shadow=False, lw=1.8)


def flash(k, x, y, r):
    """A camera flash (lesson 114: a flash only where something flashes): a white star with rays."""
    c = k.c
    c.set_source_rgba(1, 1, 0.92, 0.85)
    c.move_to(x, y - r)
    for i in range(1, 16):
        a = -math.pi / 2 + i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.38
        c.line_to(x + math.cos(a) * rr, y + math.sin(a) * rr)
    c.close_path(); c.fill()


def _label(c, s, x, y, size=16, col=INK):
    c.select_font_face("Inter", 0, 1); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s); c.move_to(x - e.x_advance / 2, y); c.show_text(s)


def sheet(out):
    import fs_storyboard as sb
    W, H = 2200, 1500
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(*kit.WALL); c.paint()
    F = 760
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, F, W, 180); c.fill()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(30); c.set_source_rgb(*INK); c.move_to(40, 50)
    c.show_text("PICK A SIDE · THE ROBOT · 13's HR robot at the office scale (0.66) · this episode's parts · v1")
    c.select_font_face("Inter", 0, 0); c.set_font_size(18); c.move_to(40, 84)
    c.show_text("the telescopic selfie arm and its phone · balancing on the tape · cyan visor pictograms · it always smiles")
    Z = 1.45
    sb.don(k, 130, F, 0.60 * Z, "stand", "neutral", look=(1, 0))
    robot(k, 330, F, S_OFFICE * Z)
    o = robot(k, 560, F, S_OFFICE * Z, arms=((-8, 0), (170, 10)), visor="sun")             # 1.1: its hand up on the cord
    c.set_source_rgb(0.3, 0.3, 0.3); c.set_line_width(2); hx, hy = o["hands"][1]; c.move_to(hx, hy - 140); c.line_to(hx, hy + 30); c.stroke()
    robot(k, 790, F, S_OFFICE * Z, visor="barrier")                                         # 2.9
    tape(k, 1030, F, F + 180, lean=0.0)
    robot(k, 1030, F + 40, S_OFFICE * Z, arms=((-95, 0), (95, 0)), tilt=0.10)              # 2.10: on the tape, arms out
    o = robot(k, 1290, F, S_OFFICE * Z, selfie=1.0, phone=None)                             # 3.1: the arm up, FLASH
    flash(k, o["phone"][0], o["phone"][1] - 70, 46)
    robot(k, 1540, F, S_OFFICE * Z, visor="public", selfie=0.7, phone="public", arms=((-8, 0), (40, 30)))   # 3.3
    phone_screen(k, 1870, 470, 1.6, "public")
    phone_screen(k, 2080, 470, 1.6, "posted")
    for x, n, note in ((130, "DON", "0.60, for scale"), (330, "AT REST", "0.66, the smile"), (560, "1.1", "the cord; the sun"),
                       (790, "2.9", "Border breach"), (1030, "2.10", "on the tape, arms out"), (1290, "3.1", "the arm up; FLASH"),
                       (1540, "3.3", "the phone turned to Don"), (1870, "INSERT 3.3", "PUBLIC POST?"), (2080, "INSERT 3.5", "#TeamDon")):
        _label(c, n, x, F + 230, 20); _label(c, note, x, F + 256, 14, (0.3, 0.3, 0.3))
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    import fs_storyboard as sb
    frames = []
    for name, txt in (("medium", "2.10: on the tape, Don beside it"), ("close", "2.9: Border breach"), ("insert", "3.3: PUBLIC POST?")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        if name == "medium":
            c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 760, 540, 200); c.fill()
            sb.don(k, 160, 800, 0.60 * 1.9, "stand", "neutral", look=(1, 0))
            tape(k, 380, 760, 960, lean=0.05)
            robot(k, 390, 820, S_OFFICE * 1.9, arms=((-95, 0), (95, 0)), tilt=-0.12)
        elif name == "close":
            robot(k, 270, 1260, S_OFFICE * 4.0, visor="barrier")
        else:
            phone_screen(k, 270, 470, 3.6, "public")
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_robot_v1.png"))
    phone(os.path.join(d, "ps_robot_phone_v1.png"))
