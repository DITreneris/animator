"""CUSTOMER SUCCESS (episode 11): storyboard v1, one frame per shot of script v7 (30 shots), drawn on episode 10's
front desk with its cast and camera code (fs_storyboard: set v4, canon proportions, faces framed for the phone), with
this episode's props (cs_props) and Sofía's episode-11 look (sofia_cs). Tomas chose (20 Nov, /grill-me): drawn on
ep 10's set; the robot beside Don in frame 0 with the report half out of its print slot; the portrait lands on its head
and it stays up; the cold mute test right after the board.
  python3 cs_board.py [out_dir]  ->  cs_storyboard_v1.png, cs_storyboard_v1_mute.png (for the cold viewers), cs_board/*.png"""
import math
import os
import sys
import cairo
import kit
import fs_set as fs
import fs_storyboard as sb
import sofia_fs
import sofia_cs as scs
import cs_props as cp
from kit import Ctx, INK, ellipse, rect

V = "v1"
SCRIPT = ["script v7"]                                     # what the sheet's header names (cs_board2 sets v9)
F = sb.F
X = {"client": 250, "robot": 372, "don": 452, "sofia": 500, "pam": 600, "mom": 640}   # set v4 x (Don under the portrait)
PORT = sb.fd.PORT


def _sofia(k, x, feet, s=1.0, pose="hold", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
           sparkle=0.0, tablet_kind="auto", phone_lit=False, plaster=None, slide=None):
    """sofia_fs.sofia's signature, drawn as her episode-11 look."""
    return scs.sofia(k, x, feet, s, pose if pose in ("hold", "low", "lapel", "necklace", "stand", "show", "chest", "paddle") else "hold",
                     face_kind, look=look, lag=lag, seed=seed, badge=badge, lean=lean, sparkle=sparkle)


class _ep11:
    def __enter__(self):
        self.old = (sofia_fs.sofia, fs.LAYOUT[0], fs.REMOTE_BIG[0], fs.BABY_DON[0], sb.V27[0], sb.CAM4[0], sb.NOAUTO[0], fs.PSTATE[0])
        sofia_fs.sofia = _sofia
        fs.PSTATE[0] = "clean"                                 # ep 10 ends with the glass healed: no crack, no plaster
        fs.LAYOUT[0] = "v2"; fs.REMOTE_BIG[0] = True; fs.BABY_DON[0] = True
        return self

    def __exit__(self, *e):
        (sofia_fs.sofia, fs.LAYOUT[0], fs.REMOTE_BIG[0], fs.BABY_DON[0], sb.V27[0], sb.CAM4[0], sb.NOAUTO[0], fs.PSTATE[0]) = self.old


def at(name, **kw):
    d = dict(x=X[name], x4=True); d.update(kw)
    return d


def S(k, cam, auto=True, portrait="hang", mic="up", **kw):
    """A shot on the set: cam (x, y, zoom) in set v4's coordinates. auto: push in on the faces (ep 10's medium rule)."""
    sb.CAM4[0] = cam; sb.NOAUTO[0] = not auto
    sb.DON_STATE[0] = (mic, "up")
    try:
        return sb.scene(k, cam=(0, 0, 1.0), portrait=portrait, **kw)
    finally:
        sb.CAM4[0] = None; sb.NOAUTO[0] = False; sb.DON_STATE[0] = None


# ---- the robot's own signs, drawn over the set's robot ------------------------------------------------------------------

def robot_signs(k, o, s, state="ok", paper=False):
    """state: ok, dented (the crack and the dent; REPAIR on the visor), reboot, camera. paper: the report half out of the
    print slot in its chest."""
    c = k.c
    sx, sy = o["screen"]
    r = 50 * s                                                                # its head's radius
    if paper:                                                                 # the report, half out of its chest
        bx, by = sx + 0.1 * r, sy + 1.55 * r
        c.save(); c.translate(bx, by); c.rotate(-0.08)
        rect(k, -0.55 * r, -0.9 * r, 1.1 * r, 1.2 * r, cp.PAPER, 991, shadow=False, lw=1.4)
        c.new_path(); c.set_source_rgb(*cp.GRN); c.set_line_width(max(1.2, 0.1 * r)); c.arc(0, -0.35 * r, 0.25 * r, 0, 6.3); c.stroke()
        c.restore()
    if state in ("dented", "reboot"):
        ellipse(k, sx, sy, 0.80 * r, 0.62 * r, (0.06, 0.08, 0.12), 992, shadow=False, lw=1.6)
        txt = ("REPAIR",) if state == "dented" else ("REBOOT",)
        c.select_font_face("Inter", 0, 1); c.set_font_size(0.34 * r)
        e = c.text_extents(txt[0]); c.set_source_rgb(*cp.CYAN); c.move_to(sx - e.x_advance / 2, sy + 0.08 * r); c.show_text(txt[0])
    if state == "dented":
        c.set_source_rgb(0.85, 0.90, 0.95); c.set_line_width(max(1.2, 0.04 * r))
        c.move_to(sx - 0.5 * r, sy - 0.3 * r); c.line_to(sx - 0.1 * r, sy); c.line_to(sx + 0.2 * r, sy + 0.1 * r); c.line_to(sx + 0.5 * r, sy + 0.35 * r); c.stroke()
        c.set_source_rgb(*kit.WALL); c.new_path(); c.arc(sx - 0.3 * r, sy - 1.02 * r, 0.30 * r, 0, 2 * math.pi); c.fill()   # the dent
        c.set_source_rgb(*INK); c.set_line_width(max(1.6, 0.06 * r)); c.new_path(); c.arc(sx - 0.3 * r, sy - 1.02 * r, 0.30 * r, 0.25, math.pi - 0.25); c.stroke()
    if state == "camera":
        rect(k, sx - 0.55 * r, sy - 0.36 * r, 1.1 * r, 0.72 * r, (0.15, 0.15, 0.18), 993, shadow=False, lw=2)
        ellipse(k, sx + 0.05 * r, sy, 0.27 * r, 0.27 * r, (0.35, 0.40, 0.48), 994, shadow=False, lw=2)
        c.set_source_rgb(0.8, 0.9, 1.0); c.arc(sx + 0.05 * r, sy, 0.13 * r, 0, 6.3); c.fill()


def portrait_on(k, x, y, ang=0.0, s=None):
    fs.portrait(k, x, y, ang=ang, **({} if s is None else {"s": s}))


def impact(c, x, y, r=40):
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
    for i in range(8):
        a = i * math.pi / 4 + 0.3
        c.move_to(x + math.cos(a) * r, y + math.sin(a) * r * 0.6); c.line_to(x + math.cos(a) * r * 1.6, y + math.sin(a) * r)
        c.stroke()


def insert(k, fn, *a):
    fn(k, *a)


# ---- the frames ---------------------------------------------------------------------------------------------------------

WIDE0 = (390, 557, 1.7)                                   # frame 0: the door, the calendar, the screen, Don under the portrait


def calendar_on(k):
    """The tear-off wall calendar by the door, FRI (new to the set)."""
    c = k.c
    c.save(); c.translate(296, 470); c.scale(0.20, 0.20); c.translate(-270, -380)
    rect(k, 120, 190, 300, 380, (1, 1, 1), 961, lw=8)
    c.set_source_rgb(*cp.RED); c.rectangle(124, 194, 292, 70); c.fill()
    cp.T(c, "FRI", 270, 450, 160, col=cp.RED)
    c.restore()


def base(**kw):
    d = dict(cl=at("client", face="confident", look=(1, 0)), rb=at("robot", arm="none"), dn=at("don", face="neutral", look=(-1, 0)),
             sf=at("sofia", pose="hold", face="smile", look=(-0.9, 0)), door=0.0)
    d.update(kw)
    return d


def f_1_1(k):                                              # frame 0: the Client storming at the glass; the portrait in the air
    def ex(k, o):
        robot_signs(k, o["robot"], sb.SC["robot"], "ok", paper=True)
    S(k, WIDE0, auto=False, extra=ex, back=calendar_on, portrait=dict(ang=0.30),
      **base(cl=at("client", face="suspicious", look=(1, 0)), dn=at("don", pose="panic", face="neutral", look=(0, -1))))


def f_1_1b(k):                                             # it lands on the robot: Don ducked and is fine
    def ex(k, o):
        sx, sy = o["robot"]["screen"]
        robot_signs(k, o["robot"], sb.SC["robot"], "dented", paper=True)
        portrait_on(k, sx + 4, sy - 70, ang=0.35, s=0.62)
        impact(k.c, sx, sy - 70, 46)
    S(k, (420, 640, 1.9), auto=False, portrait=False, extra=ex, back=calendar_on,
      **base(cl=False, sf=at("sofia", face="caught", look=(-1, -0.4)), dn=at("don", pose="panic", face="happy", look=(-1, -0.2))))


def f_1_2(k):                                              # REPAIR · HUMAN APPROVAL REQUIRED; Don's thumb, not looking
    cp.robot_face(k, "repair")
    sb.thumb(k, 440, 840, 1.1, who="don")


def f_1_3(k):                                              # GUARANTEED BY FRIDAY / FRI · BANK 9:00
    cp.phone(k, "guarantee")


def f_1_4(k):                                              # she smooths a lapel; he walks past her, eyes on his watch
    S(k, (330, 600, 1.9), sf=at("sofia", x=330, pose="lapel", face="knowing", look=(-1, 0)),
      cl=at("client", x=200, pose="stand", face="plain", look=(0.6, 0.6)), rb=False, dn=False, pm=False, mm=False,
      portrait=False)


def f_2_1(k):                                              # Don, mic down, the report rolling out crooked
    def ex(k, o):
        robot_signs(k, o["robot"], sb.SC["robot"], "dented", paper=True)
    S(k, (420, 640, 2.0), mic="down", extra=ex, portrait=False,
      **base(cl=False, sf=False, dn=at("don", pose="reach", face="grin", look=(-1, 0))))


def f_2_2(k):
    cp.report(k, "bottom")


def f_2_4(k):                                              # "I need my plan. Not a report."
    S(k, (260, 620, 1.8), mic="down", portrait=False,
      **base(rb=False, sf=False, cl=at("client", x=230, pose="stand", face="suspicious", look=(1, 0)),
             dn=at("don", x=360, pose="reach", face="neutral", look=(-1, 0))))


def roll(k, who, dx=0.9, dy=2.0, ang=0.5):
    """A blue roll (the plan) by someone's chest, in frame coordinates from their recorded head."""
    x, y, r = sb.HEADS[who]
    c = k.c
    c.save(); c.translate(x + dx * r, y + dy * r); c.rotate(ang)
    rect(k, -1.4 * r, -0.28 * r, 2.8 * r, 0.56 * r, (0.18, 0.42, 0.85), 995, lw=2)
    c.set_source_rgba(0.98, 0.96, 0.86, 0.85); c.rectangle(-0.2 * r, -0.30 * r, 0.25 * r, 0.6 * r); c.fill()
    c.restore()


def f_3_1(k):                                              # Pam stands up with the plan rolled under her arm
    S(k, (560, 600, 2.3), auto=False, portrait=False, counter_plan=False,
      **base(cl=False, rb=False, sf=False, dn=False, mm=False, pm=dict(x=560, x4=True, act="stand")))
    roll(k, "pam")


def f_3_3(k):                                              # who noticed: her eyes to Pam, then to him
    S(k, (500, 678, 3.0), auto=False, portrait=False,
      **base(cl=False, rb=False, dn=False, pm=False, mm=False, sf=at("sofia", face="interested", look=(1, 0))))


def f_3_4(k):
    cp.plan(k, "before")


def f_3_5(k):                                              # the Client looks at the hole, then at Pam
    S(k, (450, 620, 1.7), mic="down", portrait=False,
      **base(rb=False, sf=False, cl=at("client", x=380, face="plain", look=(1, 0.6)), dn=at("don", x=300, face="grin", look=(1, 0)),
             pm=dict(x=560, x4=True, act="empty")))


def f_4_1(k):
    cp.plan(k, "turned")


def f_4_2(k):                                              # the 7 in; Pam's thumb presses the tape (thumb 2)
    cp.plan(k, "whole")
    sb.thumb(k, 250, 700, 1.3, who="pam")


def f_4_3(k):
    cp.plan(k, "whole")


def f_4_4(k):                                              # the robot: "...obtained by a h-human."
    def ex(k, o):
        robot_signs(k, o["robot"], sb.SC["robot"], "dented")
    S(k, (372, 730, 2.8), auto=False, portrait=False, extra=ex, **base(cl=False, sf=False, dn=False, pm=False, mm=False))


def f_5_1(k):                                              # Don taps FOUND BY: AI
    def ex(k, o):
        robot_signs(k, o["robot"], sb.SC["robot"], "dented")
    S(k, (410, 640, 1.9), mic="down", extra=ex, portrait=False,
      **base(cl=False, sf=False, dn=at("don", pose="thumb", face="grin", look=(-1, 0))))


def f_5_2(k):
    def ex(k, o):
        robot_signs(k, o["robot"], sb.SC["robot"], "dented")
    S(k, (372, 720, 3.0), auto=False, portrait=False, extra=ex, **base(cl=False, sf=False, dn=False, pm=False, mm=False))


def f_5_3(k):
    cp.report(k, "stamped")


def f_5_4(k):                                              # "He's not looking at you."
    S(k, (470, 600, 2.0), mic="down", portrait=False,
      **base(cl=False, rb=False, sf=at("sofia", x=500, face="deadpan", look=(-1, 0)), dn=at("don", x=420, face="grin", look=(-1, 0))))


def f_5_5(k):                                              # he straightens his vest anyway
    S(k, (440, 600, 2.6), auto=False, mic="down", portrait=False,
      **base(cl=False, rb=False, sf=False, pm=False, mm=False, dn=at("don", pose="vest", face="smug", look=(-1, 0))))


def f_6_1(k):                                              # she steps into his path; he walks past her to Pam
    S(k, (480, 600, 1.7), portrait=False,
      **base(rb=False, dn=False, cl=at("client", x=500, face="plain", look=(1, 0)),
             sf=at("sofia", x=420, pose="lapel", face="caught", look=(1, 0)), pm=dict(x=600, x4=True, act="empty")))


def f_6_3(k):
    cp.plan(k, "number")


def f_6_4(k):
    cp.phone(k, "contact")


def f_6_5(k):                                              # Don steps in for the handshake; CONTACT APPROVED
    S(k, (470, 620, 1.7), mic="up", portrait=False,
      **base(sf=False, cl=at("client", x=380, pose="offer", face="plain", look=(0.6, 0.6)),
             dn=at("don", x=470, pose="reach", face="grin", look=(-1, 0)), rb=at("robot", x=300, arm="paddle", paddle="green")))


def f_6_6(k):                                              # the flash
    def ex(k, o):
        robot_signs(k, o["robot"], sb.SC["robot"], "camera")
        k.c.restore(); k.c.set_source_rgba(1, 1, 1, 0.55); k.c.paint(); k.c.save()
    S(k, (400, 660, 2.3), auto=False, portrait=False, extra=ex,
      **base(cl=False, sf=False, dn=at("don", pose="vest", face="grin", look=(-1, 0)), rb=at("robot", x=340, arm="none")))


def f_6_7(k):
    cp.phone(k, "review")


def f_6_8(k):                                              # Pam frozen: her name lights up on her phone
    S(k, (560, 600, 2.6), auto=False, portrait=False, counter_plan=False,
      **base(cl=False, rb=False, dn=False, sf=False, mm=False, pm=dict(x=560, x4=True, act="stand")))
    x, y, r = sb.HEADS["pam"]
    c = k.c
    c.save(); c.translate(x - 1.3 * r, y + 2.4 * r); c.rotate(-0.15)
    c.set_source_rgba(0.6, 0.9, 1.0, 0.35); c.arc(0, 0, 1.6 * r, 0, 6.3); c.fill()          # its glow
    rect(k, -0.55 * r, -0.95 * r, 1.1 * r, 1.9 * r, (0.10, 0.11, 0.14), 996, lw=2)
    c.set_source_rgb(*cp.LIGHT); c.rectangle(-0.45 * r, -0.8 * r, 0.9 * r, 1.6 * r); c.fill()
    _stars_small(c, -0.36 * r, -0.55 * r, 0.16 * r)
    cp.T(c, "PAM", 0, 0.05 * r, 0.32 * r, col=(0.55, 0.16, 0.46))
    cp.T(c, "found it", 0, 0.42 * r, 0.20 * r, col=INK, bold=False)
    c.restore()


def _stars_small(c, x, y, sz):
    for i in range(5):
        c.set_source_rgb(*((0.98, 0.72, 0.10) if i == 0 else (0.75, 0.76, 0.80)))
        c.arc(x + i * sz * 1.15, y, sz / 2, 0, 6.3); c.fill()


def f_6_9(k):
    cp.phone(k, "reply")


def f_6_10(k):                                             # Mom: Don, then the nod to Pam
    S(k, (700, 600, 2.8), auto=False, portrait=False,
      **base(cl=False, rb=False, dn=False, sf=False, pm=False, mm=dict(x=700, x4=True, pose="bag", face="sweet", look=(-1, 0))))


def f_6_11(k):                                             # = frame 0: Sofía rehangs it: "Nobody noticed."
    def ex(k, o):
        robot_signs(k, o["robot"], sb.SC["robot"], "reboot", paper=True)
        hx, hy = o["sofia"]["hands"][1]
        portrait_on(k, hx - 30, hy - 120, ang=0.14, s=0.85)                         # in her hands, on its way back to the nail
        sb.bare_nail(k.c) if False else None
    S(k, WIDE0, auto=False, extra=ex, back=calendar_on, portrait=False,
      **base(cl=False, sf=at("sofia", x=480, pose="paddle", face="deadpan", look=(-1, -0.5))))


SHOTS = [  # shot, seconds (about, before the animatic), drawing, the beat
    ("1.1", 1.0, f_1_1, "The Client at the glass; the portrait jumps; Don ducks"),
    ("1.1b", 1.0, f_1_1b, "It lands on the robot; Don is fine"),
    ("1.2", 2.4, f_1_2, "REPAIR · HUMAN APPROVAL REQUIRED. DON: \"Approved.\""),
    ("1.3", 2.2, f_1_3, "CLIENT: \"Friday. The bank. Nine o'clock.\""),
    ("1.4", 0.8, f_1_4, "Sofía's lapel; he walks past her"),
    ("2.1", 2.3, f_2_1, "DON: \"Your Customer Success Report.\""),
    ("2.2", 1.5, f_2_2, "100% ... FILES FOUND: 0"),
    ("2.4", 2.6, f_2_4, "CLIENT: \"I need my plan. Not a report.\""),
    ("3.1", 1.2, f_3_1, "Pam stands up with the plan"),
    ("3.3", 1.0, f_3_3, "Sofía: who noticed"),
    ("3.4", 1.4, f_3_4, "The plan: a hole at 7"),
    ("3.5", 1.4, f_3_5, "He looks at the hole, then at Pam"),
    ("4.1", 1.6, f_4_1, "The strip from his pocket; the 9 turned back to a 6"),
    ("4.2", 1.2, f_4_2, "The 7 in; Pam's thumb tapes it"),
    ("4.3", 1.0, f_4_3, "The plan is whole"),
    ("4.4", 2.4, f_4_4, "ROBOT: \"...obtained by a h-human.\""),
    ("5.1", 1.2, f_5_1, "Don taps FOUND BY: AI"),
    ("5.2", 2.4, f_5_2, "ROBOT: \"Report change. Human approval required.\""),
    ("5.3", 1.2, f_5_3, "DON: \"Approved.\" The stamp, askew"),
    ("5.4", 1.4, f_5_4, "SOFÍA: \"He's not looking at you.\""),
    ("5.5", 1.0, f_5_5, "He straightens his vest anyway"),
    ("6.1", 1.6, f_6_1, "She steps in his path; he goes to Pam. CLIENT: \"Your number.\""),
    ("6.3", 1.5, f_6_3, "Pam writes her number on the tape"),
    ("6.4", 1.0, f_6_4, "PAM · FINDS THINGS"),
    ("6.5", 1.6, f_6_5, "DON: \"Customer success.\" CONTACT APPROVED"),
    ("6.6", 1.2, f_6_6, "The flash: FOUND BY AI."),
    ("6.7", 2.0, f_6_7, "His review: \"Pam found it.\""),
    ("6.8", 1.6, f_6_8, "Pam frozen; Sofía drafting"),
    ("6.9", 2.6, f_6_9, "ROBOT: \"Reply drafted...\" DON: \"Approved.\""),
    ("6.10", 1.0, f_6_10, "Mom: Don, then a nod to Pam"),
    ("6.11", 2.0, f_6_11, "SOFÍA: \"Nobody noticed.\" = frame 0"),
]


def frames(d):
    os.makedirs(d, exist_ok=True)
    out = {}
    with _ep11():
        for shot, ln, fn, _ in SHOTS:
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
            c = cairo.Context(s); k = Ctx(c, 0)
            sb.bg(c); sb.HEADS.clear(); sb.AVOID.clear()
            fn(k)
            s.write_to_png("%s/cs_board_%s.png" % (d, shot))
            out[shot] = s
    return out


def sheet(out, surfs, mute=False):
    old = sb.SHOTS, sb.V
    sb.SHOTS = [(sh, ln, fn, note) for sh, ln, fn, note in SHOTS]
    sb.V = V
    try:
        import charsheets
        orig = charsheets.corp
        def corp(c, txt, *a, **kw):
            txt = txt.replace("FIRST SEARCH", "CUSTOMER SUCCESS").replace("script v6", SCRIPT[0]).replace("set v2", "ep 10's set v4").replace("Sofía v2", "Sofía cs v2")
            if txt.startswith("storyboard"):
                a = (a[0] + 90,) + a[1:]
            return orig(c, txt, *a, **kw)
        sb.corp = corp
        sb.sheet(out, surfs, mute)
    finally:
        sb.SHOTS, sb.V = old
        sb.corp = orig


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    surfs = frames(os.path.join(d, "cs_board"))
    sheet(os.path.join(d, "cs_storyboard_%s.png" % V), surfs)
    sheet(os.path.join(d, "cs_storyboard_%s_mute.png" % V), surfs, mute=True)
    print("wrote")
