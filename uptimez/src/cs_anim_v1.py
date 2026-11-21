"""ONE STAR (episode 11, folder customer-success): motion, test shots first (20 Nov, Tomas: "plan detailed ... proceed").
Two beats that failed as stills in four rounds of cold viewers, animated so a cold viewer can judge them in motion:
  5.4a  the handshake: Don pumps the Client's hand with both of his; the Client looks away at Pam, then pulls free;
  5.4b  the mic: Don's headset boom hangs crooked; Pam's fingers lift it, it overshoots, springs back, settles at his
        mouth; a tap; her hand leaves; Don never looks;
  5.4c  Don says "Customer success." into the mic she fixed (the reorder: she sets him up to take the credit).
  3.5b  the set-up: Don's flash of panic jerks his head and the boom swings loose (from here it hangs crooked).
Drawn at 12 drawings a second on episode 10's set (the storyboard code, board v7's cameras), output at 30 fps.
  python3 cs_anim.py test [out_dir]  ->  cs_test_v1.mp4 (5.3 > 5.4a > 5.4b > 5.4c > 6.1, no sound, no captions),
                                        cs_test_v1_strip.png (every drawing, numbered) and cs_test_v1_feed.png (270 px)
  python3 cs_anim.py setup [out_dir] ->  cs_test_v1_setup.png (3.5b, the boom swinging loose)"""
import math
import os
import subprocess
import sys
import cairo
import fs_storyboard as sb
import cs_props as cp
import cs_board as b1
import cs_board2 as b2
import cs_board3 as b3
from cs_board import S, at, base
from cs_board2 import pam_at, phone_in
from kit import Ctx, INK, ellipse

V = "v1"
DPS = 12                                                   # drawings per second
SKIN_PAM = (0.96, 0.82, 0.70)
PURPLE = (0.40, 0.26, 0.55)
BOOM = (0.45, 0.45, 0.50)
CROOKED = (47, 10, 72, 22, 84, 48, 78, 78)                 # the boom, head-local: hanging out and down at his collar
MOUTH = (47, 10, 40, 40, 18, 40, 10, 32)                   # at his mouth (fs_storyboard.don_signs "down")
UP = (47, 10, 58, -4, 58, -26, 52, -40)                    # along his head ("up")


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def boom_pts(t, frm=CROOKED, to=MOUTH):
    """t 0 = frm, 1 = to; past 1 it overshoots along the same path."""
    return lerp(frm, to, t)


class Don:
    """Draws Don's signs with a boom given as points (instead of "up"/"down") for the shot being drawn."""
    def __init__(self, pts):
        self.pts = pts

    def __enter__(self):
        self.orig = sb.don_signs
        pts = self.pts

        def signs(k, head, s, mic, hair):
            c = k.c
            hx, hy = head
            c.save(); c.translate(hx, hy); c.scale(s, s); c.set_line_cap(1)
            for w, col in ((6, INK), (3.2, BOOM)):
                c.set_source_rgb(*col); c.set_line_width(w)
                c.move_to(pts[0], pts[1]); c.curve_to(*pts[2:]); c.stroke()
            ellipse(k, pts[6], pts[7], 6.5, 5, (0.12, 0.12, 0.14), 711, shadow=False, lw=1.6)
            c.set_source_rgb(*INK); c.set_line_width(4.6)                    # his one hair, curled
            c.move_to(2, -50); c.curve_to(0, -74, 24, -84, 20, -67); c.curve_to(17, -57, 7, -64, 14, -70); c.stroke()
            c.restore()
        sb.don_signs = signs
        return self

    def __exit__(self, *e):
        sb.don_signs = self.orig


# ---- 5.4a the handshake --------------------------------------------------------------------------------------------------

def m5_4a(k, d):
    """19 drawings (1.6 s). d 0 Don steps in, hands out; 2 the grab; 3-14 three pumps of 4; 15-18 the Client pulls free,
    eyes down to his phone; Don still pumping air, eyes shut, delighted."""
    free = d >= 15
    pump = (0, -1, 0, 1)[(d - 3) % 4] if 3 <= d < 15 else 0                # up, mid, down, mid
    reach = min(1.0, d / 2.0)
    du = -40 - 25 * reach + 12 * pump                                      # Don's two arms to the middle, pumping
    dpose = (du, 30 - 10 * reach, -38 - 20 * reach + 12 * pump, -60)
    cpose = (-10, 5, 10, -5) if free else (-10, 5, 55, 15)                 # his right hand out (limp), or back
    st = {}

    def ex(k_, o):
        c = k_.c
        dh = sorted(o["don"]["hands"])
        mx, my = (dh[0][0] + dh[1][0]) / 2 - 4, (dh[0][1] + dh[1][1]) / 2
        if free:
            for (px, py) in dh:                                            # pumping nothing
                ellipse(k_, px, py, 7, 7, (0.96, 0.80, 0.66), 990, lw=1.6)
            return
        ch = max(o["client"]["hands"])                                     # his limp forearm up to the clasp
        c.set_line_cap(1)
        for w, col in ((14, INK), (10.5, (0.42, 0.44, 0.24))):
            c.set_source_rgb(*col); c.set_line_width(w); c.move_to(*ch); c.line_to(mx - 6, my + 2); c.stroke()
        if d >= 2:
            ellipse(k_, mx - 6, my + 2, 9.5, 8.5, (0.86, 0.66, 0.50), 983, lw=1.8)   # his hand, inside Don's two
            for (px, py) in dh:
                ellipse(k_, px, py, 8.5, 8, (0.96, 0.80, 0.66), 984 + int(px), lw=1.8)
        if 3 <= d < 15 and pump != 0:                                      # the shake
            c.set_source_rgb(*INK); c.set_line_width(2)
            for sy in (-1, 1):
                c.move_to(mx - 22, my + sy * 20); c.line_to(mx + 22, my + sy * 20); c.stroke()
        st["head"] = o["client"]["head"]

    S(k, (352, 650, 1.9), auto=False, mic="down", portrait=False, extra=ex,
      pre=pam_at(268, front=True, face="pleased", look=(1, 0), glasses="up"),
      **base(rb=False, sf=False, pm=False, mm=False,
             cl=at("client", x=340, pose=cpose, face="warm" if not free else "plain", look=(-1, 0) if not free else (0.4, 1)),
             dn=at("don", x=445, pose=dpose, face="happy", look=(-1, -0.3))))
    if free:
        phone_in(k, "client", dx=0.8, dy=1.6, lit=True, s=1.0)


# ---- 5.4b the mic --------------------------------------------------------------------------------------------------------

BOOM_T = [0, 0, 0, 0, 0, 0.35, 0.75, 1.25, 0.85, 1.07, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]   # lift, overshoot, spring, settle
REACH = [0, 0, 0.45, 0.85, 1, 1, 1, 1, 1, 1, 1, 1, 0.9, 0.6, 0.3, 0, 0]                    # her hand: in, on it, out


def m5_4b(k, d):
    """17 drawings (1.4 s), tight on Don's head. d 0-1 crooked, Don beaming at the Client off frame; 2-4 her hand comes
    in; 5-7 she lifts it, past his mouth; 8-10 it springs back and settles; 11 a tap; 12-16 her hand leaves."""
    t = BOOM_T[d]
    pts = boom_pts(t)
    r = REACH[d]

    def ex(k_, o):
        c = k_.c
        hx, hy = o["don"]["head"]
        s = sb.SC["don"]
        if r <= 0:
            return
        def mid(q):                                                          # the boom's middle: where she pinches it
            return (0.125 * q[0] + 0.375 * q[2] + 0.375 * q[4] + 0.125 * q[6], 0.125 * q[1] + 0.375 * q[3] + 0.375 * q[5] + 0.125 * q[7])
        grip = mid(pts) if d >= 4 else mid(CROOKED)
        tx, ty = lerp((190, 190), grip, r)                                  # her fingers, from off frame onto the boom
        tap = -5 if d == 11 else 0
        c.save(); c.translate(hx, hy); c.scale(s, s); c.set_line_cap(1)
        wx, wy = tx + 46, ty + 58                                            # her wrist, below and right of the face
        for w, col in ((22, INK), (18, PURPLE)):
            c.set_source_rgb(*col); c.set_line_width(w); c.move_to(250, 230); c.line_to(wx + 30, wy + 34); c.stroke()
        for w, col in ((15, INK), (11, SKIN_PAM)):
            c.set_source_rgb(*col); c.set_line_width(w); c.move_to(wx + 30, wy + 34); c.line_to(tx + 6, ty + 8 + tap); c.stroke()
        ellipse(k_, tx + 2, ty + 3 + tap, 9, 8, SKIN_PAM, 999, lw=1.6)        # finger and thumb on the boom
        ellipse(k_, tx + 8, ty - 6 + tap, 6, 5, SKIN_PAM, 998, lw=1.4)
        if d == 11:                                                          # the tap: two little marks
            c.set_source_rgb(*INK); c.set_line_width(3)
            for a in (-14, 0):
                c.move_to(tx + a - 6, ty - 18); c.line_to(tx + a - 12, ty - 28); c.stroke()
        c.restore()

    with Don(pts):
        S(k, (482, 652, 4.2), auto=False, mic="down", portrait=False, extra=ex,
          pre=pam_at(545, front=True, face="neutral" if d < 12 else "pleased", look=(-1, -0.3), glasses="up"),
          **base(cl=False, rb=False, sf=False, mm=False, dn=at("don", x=450, pose="stand", face="happy", look=(-1, 0))))


# ---- 5.4c "Customer success." -------------------------------------------------------------------------------------------

def m5_4c(k, d):
    """16 drawings (1.3 s): the same framing, the boom at his mouth; he swells and speaks into it (mouth on twos)."""
    talk = 3 <= d < 14
    face = ("grin", "happy")[(d // 2) % 2] if talk else "happy"
    with Don(MOUTH):
        S(k, (482, 652, 4.2), auto=False, mic="down", portrait=False,
          pre=pam_at(545, front=True, face="pleased", look=(-1, -0.3), glasses="up"),
          **base(cl=False, rb=False, sf=False, mm=False, dn=at("don", x=450, pose="vest" if d >= 2 else "stand", face=face, look=(-1, 0))))


# ---- 3.5b the set-up: the boom swings loose -----------------------------------------------------------------------------

SWING = [0.0, 0.0, -0.4, 0.55, 1.15, 0.85, 1.0, 1.0]       # from "down" (at his mouth) to CROOKED, with a bounce


def m3_5b(k, d):
    pts = lerp(MOUTH, CROOKED, SWING[d])
    with Don(pts):
        S(k, (452, 640, 3.0), auto=False, mic="down", portrait=False,
          **base(cl=False, sf=False, rb=False, pm=False, mm=False,
                 dn=at("don", face="panic" if d >= 2 else "smug", look=(-1, 0) if d < 2 else (-1, -0.3))))


# ---- the test clip ------------------------------------------------------------------------------------------------------

CLIP = [("5.3", 12, lambda k, d: cp.phone(k, "contact3")),
        ("5.4a", 19, m5_4a),
        ("5.4b", 17, m5_4b),
        ("5.4c", 16, m5_4c),
        ("6.1", 12, lambda k, d: b2.f_6_1(k))]


def draw(fn, d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s); k = Ctx(c, 0)
    sb.bg(c); sb.HEADS.clear(); sb.AVOID.clear()
    old = cp.PROPS4[0]; cp.PROPS4[0] = True
    try:
        with b3._ep11v3():
            fn(k, d)
    finally:
        cp.PROPS4[0] = old
    return s


def strip(tiles, out, tw, cols, label=True):
    th = tw * 960 // 540
    rows = (len(tiles) + cols - 1) // cols
    S_ = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (tw + 6) + 6, rows * (th + (24 if label else 6)) + 6)
    c = cairo.Context(S_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, f) in enumerate(tiles):
        x, y = 6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + (24 if label else 6))
        c.save(); c.translate(x, y); c.scale(tw / 540.0, th / 960.0)
        p = cairo.SurfacePattern(f); p.set_filter(cairo.FILTER_GOOD); c.set_source(p); c.paint(); c.restore()
        if label:
            c.select_font_face("Inter", 0, 1); c.set_font_size(13); c.set_source_rgb(1, 1, 1)
            c.move_to(x + 2, y + th + 17); c.show_text(name)
    S_.write_to_png(out)


def test(out_dir):
    tmp = "/tmp/cs_test"; os.makedirs(tmp, exist_ok=True)
    tiles, lst, n = [], open(tmp + "/list.txt", "w"), 0
    for shot, nd, fn in CLIP:
        for d in range(nd):
            f = draw(fn, d)
            p = "%s/d%03d.png" % (tmp, n); f.write_to_png(p)
            lst.write("file '%s'\nduration %.6f\n" % (p, 1.0 / DPS))
            tiles.append(("#%d  %.2f s" % (n + 1, n / float(DPS)), f)); n += 1
    lst.write("file '%s'\n" % p); lst.close()
    out = os.path.join(out_dir, "cs_test_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/t.part.mp4"], check=True)
    os.replace(tmp + "/t.part.mp4", out)
    strip(tiles, os.path.join(out_dir, "cs_test_%s_strip.png" % V), 180, 10)
    strip([(t[0].split()[0], t[1]) for t in tiles], os.path.join(out_dir, "cs_test_%s_feed.png" % V), 135, 13)
    print("wrote", out, "%d drawings, %.2f s" % (n, n / float(DPS)))


def setup(out_dir):
    strip([("#%d" % (d + 1), draw(m3_5b, d)) for d in range(len(SWING))],
          os.path.join(out_dir, "cs_test_%s_setup.png" % V), 180, 8)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "test"
    d = sys.argv[2] if len(sys.argv) > 2 else "../customer-success"
    {"test": test, "setup": setup}[what](d)
