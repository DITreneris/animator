"""of_ui.py: ONE phone UI for episode 13 (24 Nov, Tomas: "every screen looks cheap, like PowerPoint"; decided: real-app
look). Every screen is drawn in the same units: 100 wide, H high, origin at the screen's top left corner. A status bar,
an app bar, cards with a soft shadow, pill buttons, avatars. No real brand, no real app.

    hand(c_, fn, *a)   a screen on a phone in a hand (the grip's screen is -19..19 by -34..34)
    full(c, x0, y0, w, h, fn, *a)   a screen on a full-frame insert
"""
import math

BG = (0.955, 0.96, 0.975)
CARD = (1.0, 1.0, 1.0)
TXT = (0.10, 0.11, 0.15)
SUB = (0.46, 0.48, 0.55)
LINE = (0.86, 0.87, 0.91)
RED = (0.86, 0.16, 0.18)
GRN = (0.13, 0.66, 0.36)
BLUE = (0.16, 0.38, 0.80)
GOLD = (0.98, 0.72, 0.10)
NIGHT = (0.07, 0.09, 0.14)
CLOCK = "10:42"


def rr(c, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    c.new_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()


def card(c, x, y, w, h, r=5, col=CARD):
    for i, a in enumerate((0.03, 0.042, 0.054)):                         # a soft shadow: three passes, closer and darker
        c.set_source_rgba(0.05, 0.07, 0.15, a); rr(c, x - 1.6 + i * 0.6, y + 2.6 - i * 0.6, w + 3.2 - i * 1.2, h + 1.2, r + 1); c.fill()
    c.set_source_rgb(*col); rr(c, x, y, w, h, r); c.fill()


def txt(c, s, x, y, size, col=TXT, bold=True, align=0, font="Inter"):
    """align: 0 left, 0.5 centre, 1 right. Returns the advance."""
    c.select_font_face(font, 0, 1 if bold else 0); c.set_font_size(size)
    e = c.text_extents(s)
    c.set_source_rgb(*col); c.move_to(x - e.x_advance * align, y); c.show_text(s); c.new_path()
    return e.x_advance


def pill(c, x, y, w, h, col, label, size, fg=(1, 1, 1), outline=None):
    if outline is None:
        c.set_source_rgba(col[0] * 0.5, col[1] * 0.5, col[2] * 0.5, 0.28); rr(c, x, y + 1.6, w, h, h / 2); c.fill()
        c.set_source_rgb(*col); rr(c, x, y, w, h, h / 2); c.fill()
        c.set_source_rgba(1, 1, 1, 0.16); rr(c, x + 1.5, y + 1.0, w - 3, h * 0.45, h * 0.22); c.fill()     # the top light
    else:
        c.set_source_rgb(*outline); c.set_line_width(0.9); rr(c, x, y, w, h, h / 2); c.stroke()
    txt(c, label, x + w / 2, y + h / 2 + size * 0.36, size, fg, True, 0.5)


def status(c, dark=False):
    col = (1, 1, 1) if dark else TXT
    txt(c, CLOCK, 7, 8.6, 5.2, col, True)
    c.set_source_rgb(*col)
    for i in range(4):                                                  # signal
        c.rectangle(70 + i * 2.4, 8.4 - 1.2 - i * 1.0, 1.6, 1.2 + i * 1.0); c.fill()
    c.set_line_width(0.6); rr(c, 83, 4.2, 9.6, 4.6, 1.2); c.stroke()    # battery
    rr(c, 84, 5.2, 6.2, 2.6, 0.6); c.fill(); c.rectangle(93, 5.6, 0.9, 1.8); c.fill()


def appbar(c, title, col=None):
    c.set_source_rgb(*TXT); c.set_line_width(1.1); c.set_line_cap(1); c.set_line_join(1)
    c.move_to(10.5, 17.2); c.line_to(7.5, 20.2); c.line_to(10.5, 23.2); c.stroke()      # back
    txt(c, title, 15, 22.4, 6.4, col or TXT, True)
    for i in range(3):
        c.set_source_rgb(*SUB); c.arc(90.5, 17.4 + i * 2.8, 0.75, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*LINE); c.rectangle(0, 28, 100, 0.5); c.fill()


def avatar(c, x, y, r, col, letter=None, ring=None):
    if ring:
        c.set_source_rgb(*ring); c.arc(x, y, r + 1.4, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*col); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(1, 1, 1, 0.14); c.arc(x - r * 0.25, y - r * 0.3, r * 0.6, 0, 2 * math.pi); c.fill()
    if letter:
        txt(c, letter, x, y + r * 0.36, r * 1.05, (1, 1, 1), True, 0.5)


def star(c, x, y, r, on=True):
    c.new_path()
    for j in range(10):
        q = r if j % 2 == 0 else r / 2.3
        a = -math.pi / 2 + j * math.pi / 5
        (c.move_to if j == 0 else c.line_to)(x + math.cos(a) * q, y + math.sin(a) * q)
    c.close_path()
    if on:
        c.set_source_rgb(*GOLD); c.fill_preserve(); c.set_source_rgb(0.78, 0.52, 0.04); c.set_line_width(0.5); c.stroke()
    else:
        c.set_source_rgb(0.88, 0.89, 0.92); c.fill()


def skeleton(c, x, y, widths, h=2.4, gap=5.2):
    for i, w in enumerate(widths):
        c.set_source_rgb(*LINE); rr(c, x, y + i * gap, w, h, h / 2); c.fill()


def phone_glyph(c, x, y, s, down=False):
    c.save(); c.translate(x, y); c.rotate(2.36 if down else 0.0); c.scale(s, s)
    c.set_source_rgb(1, 1, 1); c.set_line_width(1.9); c.set_line_cap(1)
    c.new_path(); c.arc(0, 2.2, 4.4, math.pi * 1.12, math.pi * 1.88); c.stroke()
    for sx in (-1, 1):
        rr(c, sx * 4.1 - 1.5, -1.5, 3.0, 3.2, 0.9); c.fill()
    c.restore()


def _base(c, H, col=BG):
    c.set_source_rgb(*col); c.rectangle(0, 0, 100, H); c.fill()


# --- the screens ------------------------------------------------------------------------------------------------------
def review(c, H):
    """0.4: his one-star post. YOUR POST, one star of five, DELETE. Three things, each big: it is read at 100 px wide."""
    _base(c, H); status(c)
    c.set_source_rgb(*BLUE); c.rectangle(0, 12.5, 100, 20); c.fill()
    txt(c, "YOUR POST", 50, 27.4, 11.5, (1, 1, 1), True, 0.5, font="Lilita One")
    card(c, 6, 40, 88, 62)
    txt(c, "1", 14, 76, 34, (0.86, 0.50, 0.04), True, font="Lilita One")
    star(c, 48, 62, 15, on=True)
    for i in range(4):
        star(c, 67 + (i % 2) * 13, 55 + (i // 2) * 13, 5.4, on=False)
    txt(c, "REVIEW", 50, 95, 9.5, SUB, True, 0.5)
    pill(c, 6, 110, 88, 40, RED, "DELETE", 20)


def contact(c, H, photo=None):
    """2.8: one contact. PAM, finds things."""
    _base(c, H)
    g = __import__("cairo").LinearGradient(0, 0, 0, 78)
    g.add_color_stop_rgb(0, 0.20, 0.30, 0.62); g.add_color_stop_rgb(1, 0.33, 0.50, 0.86)
    c.set_source(g); c.rectangle(0, 0, 100, 74); c.fill()
    status(c, dark=True)
    c.set_source_rgb(1, 1, 1); c.set_line_width(1.1); c.set_line_cap(1)
    c.move_to(10.5, 17.2); c.line_to(7.5, 20.2); c.line_to(10.5, 23.2); c.stroke()
    txt(c, "Contact", 15, 22.4, 5.6, (1, 1, 1), True)
    c.set_source_rgba(0.05, 0.07, 0.15, 0.22); c.arc(50, 76, 25.5, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(1, 1, 1); c.arc(50, 74, 25, 0, 2 * math.pi); c.fill()
    if photo:
        photo(50, 74, 22.5)
    else:
        avatar(c, 50, 74, 22.5, (0.55, 0.40, 0.70), "P")
    txt(c, "PAM", 50, 124, 23, TXT, True, 0.5, font="Lilita One")
    txt(c, "finds things", 50, 137, 9.2, SUB, False, 0.5)
    for i, (col, kind) in enumerate(((GRN, "call"), (BLUE, "msg"), (GOLD, "star"))):
        x = 24 + i * 26
        avatar(c, x, 154, 8, col)
        if kind == "call":
            phone_glyph(c, x, 154, 0.85)
        elif kind == "msg":
            c.set_source_rgb(1, 1, 1); rr(c, x - 4.4, 150.4, 8.8, 6.2, 1.6); c.fill()
            c.move_to(x - 2.4, 156); c.line_to(x - 3.4, 159); c.line_to(x + 0.6, 156); c.fill()
        else:
            c.new_path()
            for j in range(10):
                q = 4.6 if j % 2 == 0 else 2.0
                a = -math.pi / 2 + j * math.pi / 5
                (c.move_to if j == 0 else c.line_to)(x + math.cos(a) * q, 154 + math.sin(a) * q)
            c.close_path(); c.set_source_rgb(1, 1, 1); c.fill()


def invite(c, H):
    """3.6: INVITATION, from DAD, ACCEPT."""
    _base(c, H); status(c); appbar(c, "Calendar")
    card(c, 6, 36, 88, 92)
    c.set_source_rgb(0.55, 0.16, 0.46); rr(c, 6, 36, 88, 5, 5); c.fill(); c.rectangle(6, 39, 88, 2); c.fill()
    txt(c, "NEW", 12, 53, 4.2, (0.55, 0.16, 0.46))
    txt(c, "INVITATION", 50, 70, 13.6, (0.55, 0.16, 0.46), True, 0.5, font="Lilita One")
    c.set_source_rgb(*LINE); c.rectangle(12, 77, 76, 0.5); c.fill()
    avatar(c, 22, 93, 8, (0.48, 0.10, 0.16), "D")
    txt(c, "from", 34, 88.5, 4.6, SUB, False)
    txt(c, "DAD", 34, 102, 15.5, TXT, True, font="Lilita One")
    c.set_source_rgb(*SUB); c.set_line_width(0.8); c.arc(15, 116.4, 2.6, 0, 2 * math.pi); c.stroke()          # a clock
    c.move_to(15, 114.8); c.line_to(15, 116.4); c.line_to(16.3, 117.2); c.stroke()
    txt(c, "Today  ·  in 5 min", 21, 118.4, 5.8, (0.30, 0.32, 0.38), True)
    pill(c, 8, 136, 84, 22, GRN, "ACCEPT", 11.5)
    pill(c, 26, 163, 48, 10, None, "Decline", 4.6, fg=SUB, outline=LINE)


def call(c, H, name, declined=False, sub="incoming call"):
    """3.7 DAD (Don is calling him: sub="calling…"), 4.1 DONNIE (incoming): a full-screen call. v2 (audit: the dark
    screen read worse than the old green one): a LIGHT green screen, the name 25 % bigger, white on it."""
    g = __import__("cairo").LinearGradient(0, 0, 0, H)
    if declined:
        g.add_color_stop_rgb(0, 0.34, 0.36, 0.42); g.add_color_stop_rgb(1, 0.24, 0.26, 0.31)
    else:
        g.add_color_stop_rgb(0, 0.22, 0.74, 0.40); g.add_color_stop_rgb(1, 0.15, 0.60, 0.32)
    c.set_source(g); c.rectangle(0, 0, 100, H); c.fill()
    status(c, dark=True)
    avatar(c, 50, 44, 13, (0.10, 0.42, 0.24) if not declined else (0.34, 0.36, 0.40), name[0], ring=(1, 1, 1) if not declined else None)
    size = 34 if len(name) <= 4 else 22.5
    txt(c, name, 50 if len(name) <= 4 else 57, 92, size, (1, 1, 1), True, 0.5, font="Lilita One")   # clear of the fingers on the left edge
    if declined:
        txt(c, "DECLINED", 57, 112, 12, (1.0, 0.50, 0.50), True, 0.5)
        return
    txt(c, sub, 50, 105, 6.6, (0.90, 0.98, 0.92), False, 0.5)
    y = H - 34
    if sub.startswith("calling"):
        avatar(c, 50, y, 12, RED, ring=(1, 1, 1)); phone_glyph(c, 50, y + 0.5, 1.2, down=True)
        return
    avatar(c, 27, y, 12, RED, ring=(1, 1, 1)); phone_glyph(c, 27, y + 0.5, 1.2, down=True)
    avatar(c, 73, y, 12, (0.08, 0.36, 0.20), ring=(1, 1, 1)); phone_glyph(c, 73, y - 0.5, 1.2)


def invite_small(c, H):
    """the same invitation, small in her hand: two words and the button's colour."""
    _base(c, H); status(c)
    card(c, 6, 22, 88, 96)
    c.set_source_rgb(0.55, 0.16, 0.46); rr(c, 6, 22, 88, 6, 5); c.fill(); c.rectangle(6, 25, 88, 3); c.fill()
    txt(c, "INVITATION", 50, 50, 13.2, (0.55, 0.16, 0.46), True, 0.5, font="Lilita One")
    txt(c, "from", 50, 66, 7, SUB, False, 0.5)
    txt(c, "DAD", 50, 96, 30, TXT, True, 0.5, font="Lilita One")
    pill(c, 10, 130, 80, 26, GRN, "ACCEPT", 12)


def event(c, H):
    """2.9: bodyguard 2 puts it in the calendar: + EVENT over a month grid."""
    _base(c, H); status(c)
    c.set_source_rgb(*RED); c.rectangle(0, 13, 100, 30); c.fill()
    txt(c, "+ EVENT", 50, 35, 17, (1, 1, 1), True, 0.5, font="Lilita One")
    for r_ in range(4):
        for q in range(5):
            x, y = 9 + q * 17.4, 54 + r_ * 26
            on = (r_, q) == (1, 2)
            c.set_source_rgb(*(RED if on else CARD)); rr(c, x, y, 13.6, 19, 3); c.fill()
            c.set_source_rgb(*((1, 1, 1) if on else LINE)); rr(c, x + 3, y + 7, 7.6, 4, 2); c.fill()


def pam_small(c, H):
    _base(c, H); status(c)
    avatar(c, 50, 60, 24, (0.55, 0.40, 0.70), "P", ring=(1, 1, 1))
    txt(c, "PAM", 50, 120, 30, TXT, True, 0.5, font="Lilita One")


def hand(c_, fn, *a, **kw):
    c_.save(); c_.rectangle(-19, -34, 38, 68); c_.clip(); c_.translate(-19, -34); c_.scale(0.38, 0.38)
    fn(c_, 68 / 0.38, *a, **kw); c_.restore()


def full(c, x0, y0, w, h, fn, *a, **kw):
    c.save(); c.rectangle(x0, y0, w, h); c.clip(); c.translate(x0, y0); c.scale(w / 100.0, w / 100.0)
    fn(c, h * 100.0 / w, *a, **kw); c.restore()
