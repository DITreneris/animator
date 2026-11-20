"""CUSTOMER SUCCESS (episode 11): the props and signs of script v7, as the inserts that show them (540 x 960), and a
sheet that shows each one at feed size (270 px wide), the G3 check: every sign whole and legible at 270 px.

  python3 cs_props.py [out_dir]  ->  cs_props_v1.png (the inserts at 270 px) and cs_props_v1_detail.png (at 540)

The plan, the phone frame and the colours come from episode 10's set (fs_set.py), so the two episodes match."""
import math
import os
import sys
import cairo
import kit
import brand
import fs_set as fs
import acts_ob as ac
from kit import INK, Ctx, rect, ellipse, cut

W, H = 540, 960
GRN, RED, NAVY = fs.GRN, fs.RED, brand.NAVY
PAPER = (0.97, 0.97, 0.94)
GREY = (0.42, 0.44, 0.50)
LIGHT = (0.95, 0.96, 0.98)
WALL = (0.90, 0.86, 0.78)
CYAN = (0.35, 0.85, 0.95)
SOFIA_RING = (0.30, 0.75, 0.35)                            # her open-to-work ring (ep 10)


def T(c, s, x, y, size, col=INK, bold=True, center=True, font="Inter"):
    return fs._text(c, s, x, y, size, col=col, bold=bold, center=center, font=font)


def _bg(c, col=WALL):
    c.set_source_rgb(*col); c.paint()


# --- the report ---------------------------------------------------------------------------------------------------------

def report(k, state="top", seed=900):
    """The Customer Success Report, close. state: top (the header and the 100%), bottom (the small print, the end of
    2.2's tilt), stamped (FOUND BY: AI with the red APPROVED, askew, 5.3)."""
    c = k.c
    _bg(c, (0.30, 0.27, 0.24))                                                # the desk under it
    oy = {"top": 0, "bottom": -520, "stamped": -430}[state]
    c.save(); c.translate(0, oy); c.rotate(-0.02)
    rect(k, 40, 40, 460, 1400, PAPER, seed, lw=2.4)                         # a long glossy page
    c.set_source_rgb(*NAVY); c.rectangle(44, 44, 452, 70); c.fill()
    T(c, "UptimeZ", 270, 90, 30, col=(1, 1, 1))
    T(c, "CUSTOMER SUCCESS", 270, 172, 38)
    T(c, "REPORT", 270, 216, 38)
    T(c, "BLUEPRINT RETRIEVAL", 270, 276, 26, col=GREY)
    c.new_path(); c.set_source_rgb(*GRN); c.set_line_width(26); c.arc(270, 450, 120, -math.pi / 2, 1.5 * math.pi); c.stroke()
    T(c, "100%", 270, 474, 64, col=GRN)
    T(c, "SUCCESS", 270, 618, 30, col=GRN)
    c.set_source_rgb(0.80, 0.80, 0.78)                                        # the filler lines
    for i in range(5):
        c.rectangle(90, 680 + i * 30, 360 - (i % 3) * 50, 9); c.fill()
    rect(k, 80, 860, 380, 90, (1, 1, 1), seed + 1, shadow=False, lw=2.6)    # FOUND BY: AI
    c.set_source_rgb(*GRN); c.set_line_width(7); c.set_line_cap(1)
    c.move_to(110, 905); c.line_to(126, 922); c.line_to(156, 884); c.stroke()
    T(c, "FOUND BY: AI", 300, 920, 38)
    T(c, "FILES FOUND: 0", 270, 1040, 40, col=INK)                          # the small print, under it
    c.set_source_rgb(0.80, 0.80, 0.78)
    for i in range(3):
        c.rectangle(110, 1080 + i * 26, 320, 8); c.fill()
    if state == "stamped":
        c.save(); c.translate(300, 790); c.rotate(-0.18)
        c.set_source_rgba(*RED, 0.85); c.set_line_width(7); c.rectangle(-150, -52, 300, 104); c.stroke()
        c.set_line_width(2.5); c.rectangle(-140, -42, 280, 84); c.stroke()
        c.select_font_face("Inter", 0, 1); c.set_font_size(54); e = c.text_extents("APPROVED")
        c.move_to(-e.x_advance / 2, 19); c.show_text("APPROVED")
        c.restore()
    c.restore()


# --- the robot's face ---------------------------------------------------------------------------------------------------

def robot_face(k, state="repair", seed=920):
    """The HR robot's head, close: the visor is its screen. state: ok, repair (dented, the visor cracked: REPAIR · HUMAN
    APPROVAL REQUIRED), reboot (REPAIR APPROVED · REBOOT, the dent popping out)."""
    c = k.c
    _bg(c)
    dent = {"ok": 0.0, "repair": 1.0, "reboot": 0.3}[state]
    cx, cy, r = 270, 470, 220
    c.set_source_rgb(*INK); c.set_line_width(8); c.move_to(cx, cy - r); c.line_to(cx + 10 * dent, cy - r - 120); c.stroke()
    ellipse(k, cx + 10 * dent, cy - r - 130, 22, 22, GRN, seed + 1, lw=4)
    pts = []                                                                   # the white shell, with a dent on top
    for i in range(120):
        a = i / 120.0 * 2 * math.pi
        da = (a - 1.5 * math.pi + math.pi) % (2 * math.pi) - math.pi        # 0 at the top
        x_ = (da + 0.30) / 0.55
        rr = r - (dent * 34 * (1 - x_ * x_) ** 2 if abs(x_) < 1 else 0.0)  # a smooth dip, left of the antenna
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    cut(k, pts, (0.96, 0.96, 0.95), lw=5)
    ellipse(k, cx, cy + 10, 170, 150, (0.06, 0.08, 0.12), seed + 2, shadow=False, lw=4)   # the visor
    if state == "ok":
        for sx in (-60, 60):
            ellipse(k, cx + sx, cy, 30, 34, CYAN, seed + 3 + sx, shadow=False, outline=False)
    else:
        lines = (("REPAIR", 44), ("HUMAN", 30), ("APPROVAL", 30), ("REQUIRED", 30)) if state == "repair" else \
                (("REPAIR", 40), ("APPROVED", 40), ("REBOOT", 30))
        y = cy - 50 if state == "repair" else cy - 36
        for s, sz in lines:
            T(c, s, cx, y, sz, col=CYAN if s != "APPROVED" else GRN); y += sz + 14
    if state == "repair":                                                      # the crack across the visor
        c.set_source_rgb(0.85, 0.90, 0.95); c.set_line_width(3); c.set_line_join(1)
        c.move_to(cx - 150, cy - 70); c.line_to(cx - 60, cy - 20); c.line_to(cx - 80, cy + 30); c.line_to(cx + 10, cy + 70)
        c.line_to(cx + 120, cy + 120); c.stroke()
        c.move_to(cx - 60, cy - 20); c.line_to(cx + 30, cy - 90); c.stroke()


# --- the phone ----------------------------------------------------------------------------------------------------------

def _phone(k, seed):
    c = k.c
    _bg(c, (0.24, 0.22, 0.20))
    rect(k, 38, 20, 464, 920, (0.10, 0.11, 0.14), seed, lw=3)
    c.set_source_rgb(*LIGHT); c.rectangle(58, 70, 424, 820); c.fill()
    return 58, 70, 424


def _avatar(k, x, y, r, col, seed, ring=None):
    c = k.c
    if ring:
        c.set_source_rgb(*ring); c.arc(x, y, r + 7, 0, 2 * math.pi); c.fill()
    ellipse(k, x, y, r, r, col, seed, shadow=False, lw=2)


def _stars(c, x, y, n_on, size=34):
    for i in range(5):
        c.save(); c.translate(x + i * size * 1.15, y); c.new_path()
        for j in range(10):
            rr = size / 2 if j % 2 == 0 else size / 4.6
            a = -math.pi / 2 + j * math.pi / 5
            (c.move_to if j == 0 else c.line_to)(math.cos(a) * rr, math.sin(a) * rr)
        c.close_path()
        c.set_source_rgb(*((0.98, 0.72, 0.10) if i < n_on else (0.82, 0.83, 0.86))); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        c.restore()


def phone(k, kind="guarantee", seed=940):
    """His phone, as an insert. kind: guarantee (1.3), contact (6.4), post (6.6), review (6.7), reply (6.9)."""
    c = k.c
    x0, y0, w = _phone(k, seed)
    cx = x0 + w / 2
    if kind == "guarantee":
        c.set_source_rgb(*GRN); c.rectangle(x0, y0, w, 330); c.fill()
        T(c, "PREMIUM", cx, y0 + 120, 54, col=(1, 1, 1))
        T(c, "GUARANTEED", cx, y0 + 200, 40, col=(1, 1, 1))
        T(c, "BY FRIDAY", cx, y0 + 256, 40, col=(1, 1, 1))
        T(c, "FRI", cx, y0 + 470, 110, col=RED)
        T(c, "BANK", cx, y0 + 580, 72)
        T(c, "9:00", cx, y0 + 670, 56, col=GREY)
    elif kind == "contact3":                                                   # props v3: a contact card, saved
        T(c, "NEW CONTACT", cx, y0 + 60, 28, col=GREY)
        _avatar(k, cx, y0 + 190, 90, (0.40, 0.26, 0.20), seed + 1)
        ellipse(k, cx, y0 + 206, 60, 64, kit.PEOPLE.get("PAM", {}).get("skin", (0.96, 0.82, 0.70)), seed + 2, shadow=False, outline=False)
        T(c, "Pam", cx, y0 + 370, 64)
        T(c, "555 0142", cx, y0 + 440, 46, col=INK, bold=False)
        T(c, "note: finds things", cx, y0 + 500, 30, col=GREY, bold=False)
        rect(k, x0 + 60, y0 + 580, w - 120, 90, GRN, seed + 3, shadow=False, lw=2)
        T(c, "SAVED", cx + 22, y0 + 640, 42, col=(1, 1, 1))
        c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(cx - 92, y0 + 626); c.line_to(cx - 80, y0 + 640); c.line_to(cx - 58, y0 + 610); c.stroke()
    elif kind == "contact":
        _avatar(k, cx, y0 + 190, 100, (0.40, 0.26, 0.20), seed + 1)
        ellipse(k, cx, y0 + 210, 68, 72, kit.PEOPLE.get("PAM", {}).get("skin", (0.96, 0.82, 0.70)), seed + 2, shadow=False, outline=False)
        T(c, "PAM", cx, y0 + 400, 72)
        T(c, "FINDS THINGS", cx, y0 + 470, 44, col=GREY)
        rect(k, x0 + 60, y0 + 560, w - 120, 90, GRN, seed + 3, shadow=False, lw=2)
        T(c, "SAVE", cx, y0 + 620, 42, col=(1, 1, 1))
    elif kind == "post":
        c.set_source_rgb(*NAVY); c.rectangle(x0, y0, w, 70); c.fill()
        T(c, "DON TAGGED YOU", cx, y0 + 48, 34, col=(1, 1, 1))
        c.set_source_rgb(0.86, 0.88, 0.92); c.rectangle(x0 + 20, y0 + 100, w - 40, 400); c.fill()
        ellipse(k, cx, y0 + 230, 70, 70, fs.SKIN_DON, seed + 4, shadow=False, lw=2)          # Don with the report
        rect(k, cx - 90, y0 + 300, 180, 190, (0.16, 0.20, 0.34), seed + 5, shadow=False, lw=2)
        rect(k, cx + 30, y0 + 250, 110, 150, PAPER, seed + 6, shadow=False, lw=2)
        T(c, "100%", cx + 85, y0 + 320, 30, col=GRN)
        T(c, "FOUND BY AI.", cx, y0 + 590, 50)
        T(c, "#CustomerSuccess", cx, y0 + 660, 34, col=(0.20, 0.40, 0.75), bold=False)
    elif kind in ("review", "reply"):
        _avatar(k, x0 + 56, y0 + 62, 34, (0.45, 0.32, 0.22), seed + 7)                         # him
        T(c, "10 GARAGES", x0 + 110, y0 + 74, 34, center=False)
        T(c, "UptimeZ Find", x0 + 30, y0 + 160, 40, center=False)
        _stars(c, x0 + 52, y0 + 210, 1, 44)
        for i, s in enumerate(("“Paid $999.", "They lost my", "blueprint.", "Pam found it.”")):
            T(c, s, x0 + 30, y0 + 300 + i * 54, 40 if i < 3 else 44, col=INK if i < 3 else (0.55, 0.16, 0.46),
              bold=(i == 3), center=False)
        n = "312" if kind == "review" else "4.8K"
        for i, col_ in enumerate(((0.95, 0.55, 0.20), (0.95, 0.80, 0.25), (0.90, 0.30, 0.40))):
            c.set_source_rgb(*col_); c.arc(x0 + 44 + i * 22, y0 + 532, 14, 0, 6.3); c.fill()
        T(c, n, x0 + 120, y0 + 544, 32, col=GREY, bold=False, center=False)
        if kind == "reply":
            c.set_source_rgb(0.86, 0.88, 0.92); c.rectangle(x0 + 10, y0 + 580, w - 20, 130); c.fill()
            rect(k, x0 + 30, y0 + 600, 56, 56, NAVY, seed + 8, shadow=False, lw=1.5)
            c.set_source_rgb(*GRN); c.set_line_width(5); c.move_to(x0 + 40, y0 + 630); c.line_to(x0 + 52, y0 + 618)
            c.line_to(x0 + 62, y0 + 640); c.line_to(x0 + 76, y0 + 612); c.stroke()            # the brand mark, simplified
            T(c, "UptimeZ:", x0 + 100, y0 + 626, 30, center=False)
            T(c, "“Correct.", x0 + 100, y0 + 664, 34, bold=False, center=False)
            T(c, "We will recover.”", x0 + 100, y0 + 700, 34, bold=False, center=False)
            c.save(); c.push_group()                                                                # her draft, greyed
            _avatar(k, x0 + 52, y0 + 770, 26, (0.98, 0.84, 0.40), seed + 9, ring=SOFIA_RING)
            T(c, "We value every", x0 + 100, y0 + 764, 28, col=GREY, bold=False, center=False)
            T(c, "client's journey…", x0 + 100, y0 + 798, 28, col=GREY, bold=False, center=False)
            c.pop_group_to_source(); c.paint_with_alpha(0.55); c.restore()


GARAGE_LOGO = [False]                                     # props v3: his avatar is his garages' mark (ep 9, Office Noir 2)


def _client_avatar(k, x, y, r, seed):
    """His avatar. v3: the garages' mark from his collar pin (client_ob.gear: a gold gear, a wrench across it) on his
    jacket's olive; before v3, a brown circle."""
    if not GARAGE_LOGO[0]:
        _avatar(k, x, y, r, (0.45, 0.32, 0.22), seed)
        return
    import client_ob as co_
    ellipse(k, x, y, r, r, (0.42, 0.44, 0.24), seed, shadow=False, lw=2)
    co_.gear(k, x, y, r * 0.62, col=(0.86, 0.68, 0.22), seed=seed + 1)


PROPS4 = [False]                                          # props v4 (the third props review): see plan(), ai_site(), phone2()
REPLY_BIG = [False]                                       # props v3: the reply dominates its insert
SAME_LAYOUT = [False]                                     # props v3: the UPDATE keeps the post's lines where they were


def phone2(k, kind="crisis", seed=950):
    """Script v9's phone screens. kind: crisis (1.2: the post), reply (1.4: the company's reply under it), calling
    (2.1: Don calling 10 GARAGES), cal (2.2: FRI · 9:00 · CLIENT), update (6.2: the struck line, UPDATE: Pam found it.),
    pam (6.3b: her reply under the UPDATE)."""
    c = k.c
    x0, y0, w = _phone(k, seed)
    cx = x0 + w / 2
    if kind in ("crisis", "reply", "update", "pam"):
        _client_avatar(k, x0 + 56, y0 + 62, 34, seed + 7)
        T(c, "10 GARAGES", x0 + 110, y0 + 74, 34, center=False)
        T(c, "UptimeZ Find", x0 + 30, y0 + 156, 40, center=False)
        _stars(c, x0 + 52, y0 + 204, 1, 44)
        top = y0 + 290
        L, Z = (44, 36) if SAME_LAYOUT[0] else (50, 40)                       # v3: one layout for the post before and after
        if kind in ("crisis", "reply"):
            for i, (s_, b_) in enumerate((("\u201cPaid $999.", False), ("They lost my", False), ("blueprint.", False),
                                          ("My lawyer", True), ("will call.\u201d", True))):
                T(c, s_, x0 + 30, top + i * L, Z, col=RED if b_ else INK, bold=b_, center=False)
            ry = top + (290 if SAME_LAYOUT[0] else 270)
        elif SAME_LAYOUT[0]:                                                  # v3: every line where it was
            for i, s_ in enumerate(("\u201cPaid $999.", "They lost my", "blueprint.")):
                T(c, s_, x0 + 30, top + i * L, Z, col=GREY, bold=False, center=False)
            for i, s_ in enumerate(("My lawyer", "will call.\u201d")):
                ex = T(c, s_, x0 + 30, top + (3 + i) * L, Z, col=GREY, bold=True, center=False)
                c.set_source_rgb(*RED); c.set_line_width(5); c.move_to(x0 + 24, top + (3 + i) * L - 12); c.line_to(x0 + 36 + ex, top + (3 + i) * L - 12); c.stroke()
            T(c, "UPDATE:", x0 + 250, top + 3 * L, 30, col=GRN, center=False)
            T(c, "Pam found it.", x0 + 30, top + 5 * L + 14, 46, col=(0.55, 0.16, 0.46), center=False)
            ry = top + 290
        else:
            for i, s_ in enumerate(("They lost my", "blueprint.")):
                T(c, s_, x0 + 30, top + i * 46, 34, col=GREY, bold=False, center=False)
            ex = T(c, "My lawyer will call.", x0 + 30, top + 92, 34, col=GREY, bold=False, center=False)
            c.set_source_rgb(*RED); c.set_line_width(4); c.move_to(x0 + 26, top + 80); c.line_to(x0 + 34 + ex, top + 80); c.stroke()
            T(c, "UPDATE:", x0 + 30, top + 160, 44, col=GRN, center=False)
            T(c, "Pam found it.", x0 + 30, top + 214, 48, col=(0.55, 0.16, 0.46), center=False)
            ry = top + 250
        if kind in ("reply", "update", "pam"):
            c.set_source_rgb(0.86, 0.88, 0.92); c.rectangle(x0 + 10, ry, w - 20, 110); c.fill()
            rect(k, x0 + 30, ry + 22, 56, 56, NAVY, seed + 8, shadow=False, lw=1.5)
            c.set_source_rgb(*GRN); c.set_line_width(5); c.move_to(x0 + 40, ry + 52); c.line_to(x0 + 52, ry + 40)
            c.line_to(x0 + 62, ry + 62); c.line_to(x0 + 76, ry + 34); c.stroke()
            big = kind == "reply" and REPLY_BIG[0]
            if big:
                c.set_source_rgb(0.86, 0.88, 0.92); c.rectangle(x0 + 10, ry, w - 20, 140); c.fill()
                rect(k, x0 + 30, ry + 22, 56, 56, NAVY, seed + 8, shadow=False, lw=1.5)
                c.set_source_rgb(*GRN); c.set_line_width(5); c.move_to(x0 + 40, ry + 52); c.line_to(x0 + 52, ry + 40)
                c.line_to(x0 + 62, ry + 62); c.line_to(x0 + 76, ry + 34); c.stroke()
                T(c, "UptimeZ:", x0 + 100, ry + 38, 26, center=False, col=GREY)
                T(c, "\u201cCorrect.", x0 + 100, ry + 82, 40, center=False)
                T(c, "We will recover.\u201d", x0 + 30, ry + 126, 40, center=False)
                ry += 30
            else:
                T(c, "UptimeZ: \u201cCorrect.", x0 + 100, ry + 46, 30, center=False, bold=(kind == "reply"))
                T(c, "We will recover.\u201d", x0 + 100, ry + 84, 30, center=False, bold=(kind == "reply"))
            if kind == "reply" and REPLY_BIG[0]:
                c.save(); c.push_group()
                _avatar(k, x0 + 44, ry + 150, 16, (0.98, 0.84, 0.40), seed + 9, ring=SOFIA_RING)
                T(c, "We value every client's journey\u2026", x0 + 70, ry + 156, 20, col=GREY, bold=False, center=False)
                c.pop_group_to_source(); c.paint_with_alpha(0.45); c.restore()
            elif kind == "reply":
                c.save(); c.push_group()
                _avatar(k, x0 + 52, ry + 160, 26, (0.98, 0.84, 0.40), seed + 9, ring=SOFIA_RING)
                T(c, "We value every", x0 + 100, ry + 154, 28, col=GREY, bold=False, center=False)
                T(c, "client's journey\u2026", x0 + 100, ry + 188, 28, col=GREY, bold=False, center=False)
                c.pop_group_to_source(); c.paint_with_alpha(0.55); c.restore()
        if kind == "pam":
            if SAME_LAYOUT[0]:                                                 # v3: everything but her line steps back
                c.set_source_rgba(*LIGHT, 0.55); c.rectangle(x0, y0, w, ry + 112 - y0); c.fill()
            py = ry + (112 if SAME_LAYOUT[0] else 130)
            if PROPS4[0]:                                                      # v4: her line is the biggest thing on screen
                py = ry + 86
                c.set_source_rgb(0.97, 0.93, 0.98); c.rectangle(x0 + 6, py - 6, w - 12, 200); c.fill()
                c.set_source_rgb(0.55, 0.16, 0.46); c.set_line_width(3); c.rectangle(x0 + 6, py - 6, w - 12, 200); c.stroke()
                _avatar(k, x0 + 52, py + 40, 26, (0.40, 0.26, 0.20), seed + 10)
                ellipse(k, x0 + 52, py + 46, 17, 18, kit.PEOPLE.get("PAM", {}).get("skin", (0.96, 0.82, 0.70)), seed + 11, shadow=False, outline=False)
                T(c, "PAM", x0 + 90, py + 50, 30, center=False)
                T(c, "Some post.", x0 + 26, py + 112, 50, center=False)
                T(c, "Others find.", x0 + 26, py + 170, 50, center=False)
                return
            c.set_source_rgb(0.97, 0.93, 0.98); c.rectangle(x0 + 10, py, w - 20, 150); c.fill()
            _avatar(k, x0 + 56, py + 50, 30, (0.40, 0.26, 0.20), seed + 10)
            ellipse(k, x0 + 56, py + 56, 20, 21, kit.PEOPLE.get("PAM", {}).get("skin", (0.96, 0.82, 0.70)), seed + 11, shadow=False, outline=False)
            T(c, "PAM", x0 + 100, py + 44, 30, center=False)
            T(c, "Some post.", x0 + 100, py + 90, 38, center=False)
            T(c, "Others find.", x0 + 100, py + 134, 38, center=False)
        if kind == "crisis":
            n = "1.2K"
            for i, col_ in enumerate(((0.95, 0.55, 0.20), (0.95, 0.80, 0.25), (0.90, 0.30, 0.40))):
                if GARAGE_LOGO[0]:
                    c.new_path()                                                # v3: no stray line from the text before
                c.set_source_rgb(*col_); c.arc(x0 + 44 + i * 22, ry + 16, 14, 0, 6.3); c.fill()
            T(c, n, x0 + 120, ry + 28, 32, col=GREY, bold=False, center=False)
    elif kind == "calling":
        _client_avatar(k, cx, y0 + 230, 110, seed + 12)
        T(c, "10 GARAGES", cx, y0 + 430, 54)
        T(c, "calling\u2026", cx, y0 + 490, 36, col=GREY, bold=False)
        if GARAGE_LOGO[0]:
            c.new_path()
        c.set_source_rgb(*RED); c.arc(cx, y0 + 680, 56, 0, 6.3); c.fill()
        c.set_source_rgb(1, 1, 1); c.set_line_width(10); c.set_line_cap(1)
        c.move_to(cx - 26, y0 + 690); c.curve_to(cx - 10, y0 + 670, cx + 10, y0 + 670, cx + 26, y0 + 690); c.stroke()
    elif kind == "cal":
        c.set_source_rgb(*RED); c.rectangle(x0, y0, w, 140); c.fill()
        T(c, "FRI", cx, y0 + 108, 90, col=(1, 1, 1))
        T(c, "9:00", cx, y0 + 320, 110)
        T(c, "CLIENT", cx, y0 + 430, 60, col=RED)
        T(c, "10 GARAGES", cx, y0 + 500, 36, col=GREY, bold=False)


def ai_plan(k, count=False, seed=970):
    """The robot's generated blueprint (3.4): glossy, ruled, perfect, and wrong: twelve garages, 7 a car wash.
    count: the Client's thick finger counting along the row, stopped on 7."""
    c = k.c
    _bg(c, (0.62, 0.54, 0.44))
    rect(k, 30, 150, 480, 620, (0.93, 0.96, 1.0), seed, lw=3)
    c.set_source_rgb(0.20, 0.45, 0.85); c.rectangle(34, 154, 472, 612); c.fill()
    c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(1)
    for i in range(0, 472, 24):                                                 # the perfect grid
        c.move_to(34 + i, 154); c.line_to(34 + i, 766); c.stroke()
    for j in range(0, 612, 24):
        c.move_to(34, 154 + j); c.line_to(506, 154 + j); c.stroke()
    T(c, "BLUEPRINT", 270, 212, 44, col=(1, 1, 1))
    T(c, "RECOVERED BY AI \u00b7 99% CONFIDENT", 270, 252, 22, col=(0.85, 0.92, 1.0))
    for n_ in range(12):
        col, row = n_ % 4, n_ // 4
        x, y = 66 + col * 108, 300 + row * 150
        c.set_source_rgb(1, 1, 1); c.set_line_width(4)
        c.move_to(x, y + 110); c.line_to(x, y + 40); c.line_to(x + 40, y + 8); c.line_to(x + 80, y + 40); c.line_to(x + 80, y + 110); c.stroke()
        if n_ + 1 != 7:
            T(c, str(n_ + 1), x + 40, y + 140, 26, col=(1, 1, 1))
        if n_ + 1 == 7:                                                         # a car wash: a car and bubbles
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 14, y + 74, 52, 20); c.fill()
            c.rectangle(x + 24, y + 62, 32, 14); c.fill()
            for bx, by, br in ((x + 18, y + 54, 7), (x + 36, y + 46, 9), (x + 60, y + 52, 6)):
                c.new_path(); c.arc(bx, by, br, 0, 6.3); c.stroke()
            c.set_source_rgb(0.98, 0.85, 0.25); c.rectangle(x - 22, y + 116, 124, 32); c.fill()   # its number, a car wash
            T(c, "7 CAR WASH", x + 40, y + 140, 20, col=INK)
        else:
            for ly in range(3):
                c.move_to(x + 14, y + 56 + ly * 16); c.line_to(x + 66, y + 56 + ly * 16); c.stroke()
    if count:
        import client_ob as co_
        x, y = 66 + 2 * 108 + 40, 300 + 150                                   # bay 7; the fingertip just under it
        c.save(); c.translate(x + 30, y + 330); c.rotate(-0.15)
        rect(k, -38, -10, 76, 260, (0.42, 0.44, 0.24), seed + 2, lw=3)               # his olive sleeve
        rect(k, -40, -30, 80, 30, (0.98, 0.97, 0.94), seed + 3, shadow=False, lw=2)   # the cuff
        ellipse(k, 0, -90, 34, 70, (0.86, 0.66, 0.50), seed + 4, lw=3)               # the finger, pad down
        c.set_source_rgba(0.22, 0.17, 0.14, 0.5); c.set_line_width(2.5)
        for oy in (-120, -95, -70):
            c.move_to(-20, oy); c.line_to(18, oy + 4); c.stroke()
        c.restore()


def ai_site(k, seed=975):
    """Props v3 (Tomas, 20 Nov): the robot's generated site plan. Twelve garages round a driveway whose outline, taken
    whole, reads as a phallus: two round courts at the foot, a long drive, a turning circle at the end. Deniable: a
    pale driveway, small numbered garages, no anatomy, nothing but a silhouette. The Client gets it on the second look."""
    c = k.c
    _bg(c, (0.62, 0.54, 0.44))
    rect(k, 30, 120, 480, 700, (0.93, 0.96, 1.0), seed, lw=3)
    c.set_source_rgb(0.20, 0.45, 0.85); c.rectangle(34, 124, 472, 692); c.fill()
    c.set_source_rgba(1, 1, 1, 0.10); c.set_line_width(1)
    for i in range(0, 472, 24):
        c.move_to(34 + i, 124); c.line_to(34 + i, 816); c.stroke()
    for j in range(0, 692, 24):
        c.move_to(34, 124 + j); c.line_to(506, 124 + j); c.stroke()
    if PROPS4[0]:                                                              # v4: the claim big, the plan 12 % bigger
        T(c, "RECOVERED BY AI", 270, 172, 30, col=(0.85, 0.92, 1.0))
        T(c, "99% CONFIDENT", 270, 222, 44, col=(1, 0.9, 0.3))
        c.save(); c.translate(270, 506); c.scale(1.12, 1.12); c.translate(-270, -520)
    else:
        T(c, "SITE PLAN", 270, 176, 40, col=(1, 1, 1))
        T(c, "RECOVERED BY AI \u00b7 99% CONFIDENT", 270, 212, 21, col=(0.85, 0.92, 1.0))
    drive = (0.55, 0.72, 0.96)                                                   # the driveway: the silhouette
    c.set_source_rgb(*drive)
    c.new_path(); c.arc(206, 690, 74, 0, 2 * math.pi); c.fill()                 # the two courts
    c.new_path(); c.arc(334, 690, 74, 0, 2 * math.pi); c.fill()
    c.rectangle(222, 330, 96, 330); c.fill()                                     # the drive
    c.new_path(); c.arc(270, 330, 62, 0, 2 * math.pi); c.fill()                 # the turning circle
    c.set_source_rgb(1, 1, 1); c.set_line_width(3)
    for ax, ay, r_ in ((206, 690, 74), (334, 690, 74), (270, 330, 62)):
        c.new_path(); c.arc(ax, ay, r_, 0, 2 * math.pi); c.stroke()
    c.set_dash([10, 8]); c.move_to(270, 392); c.line_to(270, 616); c.stroke(); c.set_dash([])   # the centre line

    def garage(x, y, n_, ang=0.0):
        c.save(); c.translate(x, y); c.rotate(ang)
        c.set_source_rgb(0.12, 0.30, 0.66); c.rectangle(-17, -14, 34, 28); c.fill()
        c.set_source_rgb(1, 1, 1); c.set_line_width(2.5); c.rectangle(-17, -14, 34, 28); c.stroke()
        c.restore()
        T(c, str(n_), x, y + 6, 16, col=(1, 1, 1))
    n_ = 1
    for cx_, cy_, a0 in ((206, 690, 2.2), (334, 690, -0.6)):                    # three round each court
        for i in range(3):
            a_ = a0 + i * 0.95
            garage(cx_ + math.cos(a_) * 100, cy_ + math.sin(a_) * 100, n_, a_ + math.pi / 2); n_ += 1
    for i in range(3):                                                            # along the drive
        for sx in (-1, 1):
            garage(270 + sx * 74, 600 - i * 104, n_, 0.0); n_ += 1
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 0); c.set_font_size(15)
    for txt, (x, y) in (("TURNING CIRCLE", (215, 254)), ("COURT A", (172, 788)), ("COURT B", (300, 788))):
        if PROPS4[0] and txt == "TURNING CIRCLE":
            continue                                                           # v4: under the claim, and not needed
        c.move_to(x, y); c.show_text(txt)
    if PROPS4[0]:
        c.restore()


# --- the plan -----------------------------------------------------------------------------------------------------------

def plan(k, state="before", seed=740):
    """The taped plan, top shot. state: before (ep 10: the first strip upside down, a hole at 7), turned (4.1: the first
    strip the right way round, the hole still there), whole (4.3: the 7 in, taped), number (6.3: her number in pen on
    the tape across 7)."""
    c = k.c
    _bg(c, (0.62, 0.54, 0.44))
    s, x, y = 3.9, 270, 470
    if state == "number":                                                     # 6.3 is close on bay 7: the pen must read
        n_, bx, by, bw, bh = [b for b in ac._bays() if b[0] == 7][0]
        s = 11.0
        x, y = 270 - (bx + bw / 2) * s, 470 - (by + bh / 2 + 4) * s
    if state == "before" and not PROPS4[0]:
        fs.plan_patched(k, x, y, s, seed)
        return
    edges = [-62, -31.9, -10.6, 10.6, 31.9, 62]
    jit = [(0.0, 0.0, 0.0), (-1.0, -2.0, 0.02), (0.5, 1.5, -0.012), (1.0, -2.5, 0.03), (-1.5, 2.0, -0.02)]
    if state == "before":                                                     # v4: ep 10's jitter, the first strip upside down
        jit = [(1.5, 3.0, -0.025)] + jit[1:]
    old = ac.GARAGES[0], ac.TITLE[0]
    ac.GARAGES[0], ac.TITLE[0] = True, True
    c.save(); c.translate(x, y); c.scale(s, s)
    try:
        for i in range(5):
            x0, x1 = edges[i], edges[i + 1]
            cx_ = (x0 + x1) / 2
            dx, dy, a = jit[i]
            flip = state == "before" and i == 0
            c.save(); c.translate(dx, dy); c.translate(cx_, -9); c.rotate(a + (math.pi if flip else 0)); c.translate(-cx_, 9)
            hgt = 104 if (i != 1 or state in ("whole", "number")) else 58
            c.save(); c.rectangle(x0, -61, x1 - x0, hgt); c.clip()
            ac.plan_open(k, 0, 0, 1.0, seed)
            c.restore()
            if PROPS4[0] and i == 0 and state in ("before", "turned"):              # v4: the one strip that turns, outlined
                c.set_source_rgb(0.98, 0.85, 0.25); c.set_line_width(1.6); c.rectangle(x0 + 0.5, -60.5, x1 - x0 - 1, hgt - 1); c.stroke()
            c.restore()
    finally:
        ac.GARAGES[0], ac.TITLE[0] = old
    n_, bx, by, bw, bh = [b for b in ac._bays() if b[0] == 7][0]
    if state in ("turned", "before") and PROPS4[0]:                          # v4: the hole reads as a piece torn out
        hx0, hy0, hw, hh = bx - 2, by - 3, bw + 4, bh + 16
        c.new_path(); c.move_to(hx0, hy0)
        for j in range(7):                                                     # a torn top edge
            c.line_to(hx0 + hw * (j + 0.5) / 7, hy0 + (1.6 if j % 2 else -1.2)); c.line_to(hx0 + hw * (j + 1) / 7, hy0)
        c.line_to(hx0 + hw, hy0 + hh); c.line_to(hx0, hy0 + hh); c.close_path()
        c.set_source_rgb(0.86, 0.78, 0.64); c.fill_preserve()                  # the light desk through it
        c.set_source_rgb(*RED); c.set_line_width(1.0); c.set_dash([2.4, 1.6]); c.stroke(); c.set_dash([])
        c.select_font_face("Inter", 0, 1); c.set_font_size(11); c.set_source_rgba(*RED, 0.85)
        e = c.text_extents("7"); c.move_to(bx + bw / 2 - e.x_advance / 2, by + bh / 2 + 8); c.show_text("7")
    elif state == "turned":
        c.set_source_rgb(*INK); c.set_line_width(1.0); c.set_dash([3, 2])
        c.rectangle(bx - 2, by - 3, bw + 4, bh + 16); c.stroke(); c.set_dash([])
    for i, ex in enumerate(edges[1:-1]):                                                         # the seams' tape
        for ty in (-48, -14, 22):
            c.save(); c.translate(ex, ty + (i % 2) * 6); c.rotate(-0.25 + 0.18 * i)
            c.set_source_rgba(0.98, 0.96, 0.86, 0.72); c.rectangle(-7, -3.5, 14, 7); c.fill()
            c.set_source_rgba(0.6, 0.55, 0.4, 0.5); c.set_line_width(0.6); c.rectangle(-7, -3.5, 14, 7); c.stroke()
            c.restore()
    if state in ("whole", "number"):                                                             # the 7, taped in
        c.save(); c.translate(bx + bw / 2, by + bh / 2 + 4); c.rotate(-0.06)
        th_ = 12 if state == "number" else 10
        c.set_source_rgba(0.98, 0.96, 0.86, 0.85); c.rectangle(-bw / 2 - 4, -th_ / 2, bw + 8, th_); c.fill()
        c.set_source_rgba(0.6, 0.55, 0.4, 0.5); c.set_line_width(0.6); c.rectangle(-bw / 2 - 4, -th_ / 2, bw + 8, th_); c.stroke()
        if state == "number":
            if PROPS4[0]:                                                       # v4: the plan steps back, the tape stays
                c.save(); c.identity_matrix(); c.set_source_rgba(0, 0, 0, 0.30); c.paint(); c.restore()
                c.set_source_rgba(0.98, 0.96, 0.86, 0.95); c.rectangle(-bw / 2 - 4, -th_ / 2, bw + 8, th_); c.fill()
            c.set_source_rgb(0.10, 0.15, 0.55)
            c.select_font_face("Comic Neue", 0, 1); c.set_font_size(4.2)
            for j, ln in enumerate(("PAM", "555 0142")):
                e = c.text_extents(ln); c.move_to(-e.x_advance / 2, -0.6 + j * 4.4); c.show_text(ln)
        c.restore()
    for (px, py, col) in ((-44, -20, (0.55, 0.75, 1.0)), (26, 30, (0.95, 0.85, 0.3)), (48, -30, (0.55, 0.75, 1.0)),
                          (-6, 34, (0.9, 0.4, 0.6))):
        c.save(); c.translate(px, py); c.rotate(px * 0.05)
        c.set_source_rgb(*col); c.rectangle(-2.5, -1.2, 5, 2.4); c.fill(); c.restore()
    c.restore()


# --- the wall calendar --------------------------------------------------------------------------------------------------

def calendar(k, seed=960):
    """The tear-off wall calendar by the door: FRI, big and red (new to the set in ep 11)."""
    c = k.c
    _bg(c)
    c.set_source_rgb(*INK); c.arc(270, 170, 10, 0, 6.3); c.fill()                              # the nail
    rect(k, 120, 190, 300, 380, (1, 1, 1), seed, lw=4)
    c.set_source_rgb(*RED); c.rectangle(124, 194, 292, 70); c.fill()
    for i in range(6):                                                                            # the spiral
        c.set_source_rgb(*INK); c.set_line_width(4); c.arc(150 + i * 48, 196, 9, math.pi, 2 * math.pi); c.stroke()
    T(c, "FRI", 270, 450, 150, col=RED)
    for i in range(3):                                                                            # the torn stubs
        c.set_source_rgb(0.90, 0.90, 0.88); c.rectangle(130 + i * 7, 566 + i * 4, 280 - i * 14, 4); c.fill()


# --- the sheet ----------------------------------------------------------------------------------------------------------

ITEMS2 = [("1.2 phone", "the post", lambda k: phone2(k, "crisis")),
          ("1.4 phone", "the reply", lambda k: phone2(k, "reply")),
          ("2.1 phone", "calling", lambda k: phone2(k, "calling")),
          ("2.2 phone", "FRI 9:00 CLIENT", lambda k: phone2(k, "cal")),
          ("3.4 AI plan", "12 garages, 7 car wash", lambda k: ai_plan(k, True)),
          ("4.2 plan", "upside-down, hole at 7", lambda k: plan(k, "before")),
          ("4.3 plan", "the 6 turned back", lambda k: plan(k, "turned")),
          ("5.2 plan", "her number", lambda k: plan(k, "number")),
          ("5.3 phone", "PAM · FINDS THINGS", lambda k: phone(k, "contact")),
          ("6.2 phone", "the UPDATE", lambda k: phone2(k, "update")),
          ("6.3b phone", "Some post. Others find.", lambda k: phone2(k, "pam")),
          ("1.1 calendar", "FRI", lambda k: calendar(k))]

def _v4(fn):
    def w(k):
        old = PROPS4[0]
        PROPS4[0] = True
        try:
            _v3(fn)(k)
        finally:
            PROPS4[0] = old
    return w


def _v3(fn):
    def w(k):
        old = REPLY_BIG[0], SAME_LAYOUT[0], GARAGE_LOGO[0]
        REPLY_BIG[0] = SAME_LAYOUT[0] = GARAGE_LOGO[0] = True
        try:
            fn(k)
        finally:
            REPLY_BIG[0], SAME_LAYOUT[0], GARAGE_LOGO[0] = old
    return w


ITEMS3 = [("1.2 phone", "the post", _v3(lambda k: phone2(k, "crisis"))),
          ("1.4 phone", "the reply, big", _v3(lambda k: phone2(k, "reply"))),
          ("2.1 phone", "calling", _v3(lambda k: phone2(k, "calling"))),
          ("2.2 phone", "FRI 9:00 CLIENT", lambda k: phone2(k, "cal")),
          ("3.4 AI site plan", "the silhouette", lambda k: ai_site(k)),
          ("4.2 plan", "upside-down, hole at 7", lambda k: plan(k, "before")),
          ("4.3 plan", "the 6 turned back", lambda k: plan(k, "turned")),
          ("5.2 plan", "her number", lambda k: plan(k, "number")),
          ("5.3 phone", "contact, saved", lambda k: phone(k, "contact3")),
          ("6.2 phone", "the UPDATE, same layout", _v3(lambda k: phone2(k, "update"))),
          ("6.3b phone", "her line, the rest dimmed", _v3(lambda k: phone2(k, "pam"))),
          ("1.1 calendar", "FRI", lambda k: calendar(k))]

ITEMS4 = [(n, r, _v4(f.__closure__[0].cell_contents if f.__name__ == "w" else f)) for n, r, f in ITEMS3]

ITEMS = [("1.1 calendar", "FRI", lambda k: calendar(k)),
         ("1.2 robot", "REPAIR", lambda k: robot_face(k, "repair")),
         ("1.3 phone", "GUARANTEED / FRI BANK", lambda k: phone(k, "guarantee")),
         ("2.2 report", "100%", lambda k: report(k, "top")),
         ("2.2 tilt", "FILES FOUND: 0", lambda k: report(k, "bottom")),
         ("3.4 plan", "upside-down, hole at 7", lambda k: plan(k, "before")),
         ("4.1 plan", "the 6 turned back", lambda k: plan(k, "turned")),
         ("4.3 plan", "whole", lambda k: plan(k, "whole")),
         ("5.3 report", "APPROVED, askew", lambda k: report(k, "stamped")),
         ("6.3 plan", "her number on the tape", lambda k: plan(k, "number")),
         ("6.4 phone", "PAM · FINDS THINGS", lambda k: phone(k, "contact")),
         ("6.6 phone", "FOUND BY AI.", lambda k: phone(k, "post")),
         ("6.7 phone", "the review", lambda k: phone(k, "review")),
         ("6.9 phone", "the reply", lambda k: phone(k, "reply")),
         ("6.11 robot", "REBOOT", lambda k: robot_face(k, "reboot"))]


def insert(fn, scale=1):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W * scale, H * scale)
    if scale != 1:
        s.set_device_scale(scale, scale)
    c = cairo.Context(s); fn(Ctx(c, 0))
    return s


def sheet(out, tw=270, cols=5, title="CUSTOMER SUCCESS · props v1 · every insert at 270 px (the feed)", items=None):
    ITEMS_ = items or ITEMS
    th = tw * H // W
    rows = (len(ITEMS_) + cols - 1) // cols
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (tw + 20) + 20, rows * (th + 56) + 90)
    c = cairo.Context(S); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(24); c.set_source_rgb(1, 1, 1); c.move_to(20, 50); c.show_text(title)
    for i, (name, reads, fn) in enumerate(ITEMS_):
        x, y = 20 + (i % cols) * (tw + 20), 80 + (i // cols) * (th + 56)
        f = insert(fn)
        small = cairo.ImageSurface(cairo.FORMAT_RGB24, tw, th); sc = cairo.Context(small)
        sc.scale(tw / W, th / H); p = cairo.SurfacePattern(f); p.set_filter(cairo.FILTER_GOOD); sc.set_source(p); sc.paint()
        c.set_source_surface(small, x, y); c.paint()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1); c.move_to(x, y + th + 22); c.show_text(name)
        c.select_font_face("Inter", 0, 0); c.set_font_size(13); c.set_source_rgb(0.8, 0.8, 0.8); c.move_to(x, y + th + 40); c.show_text(reads)
    S.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "customer-success")
    if "v4" in sys.argv[2:]:
        sheet(os.path.join(d, "cs_props_v4.png"), cols=6, items=ITEMS4,
              title="CUSTOMER SUCCESS · props v4 (script v10) · every insert at 270 px (the feed)")
        print("wrote", os.path.join(d, "cs_props_v4.png"))
    elif "v3" in sys.argv[2:]:
        sheet(os.path.join(d, "cs_props_v3.png"), cols=6, items=ITEMS3,
              title="CUSTOMER SUCCESS · props v3 (script v10) · every insert at 270 px (the feed)")
        print("wrote", os.path.join(d, "cs_props_v3.png"))
    elif "v2" in sys.argv[2:]:
        sheet(os.path.join(d, "cs_props_v2.png"), cols=6, items=ITEMS2,
              title="CUSTOMER SUCCESS · props v2 (script v9) · every insert at 270 px (the feed)")
        print("wrote", os.path.join(d, "cs_props_v2.png"))
    else:
        sheet(os.path.join(d, "cs_props_v1.png"))
        print("wrote", os.path.join(d, "cs_props_v1.png"))
