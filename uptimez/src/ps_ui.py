"""ps_ui.py: Pick a Side's phone screens through episode 13's ONE UI kit (of_ui; the rules page §2: one UI kit per film,
every screen 100 units wide, the story's one word the biggest thing on it, nothing under ~9 units, light screens,
status by colour). Tomas, 25 Nov: "ekranai per ep13 UI kitą".

    public(c, H, approved=False)  3.3-3.4: the robot's selfie phone asks PUBLIC POST?; APPROVE, then green APPROVED
    post(c, H, caption=True)      3.5, 4.1: #TeamDon, posted; 4.2 caption=False (zoomed into the photo)
    invite(c, H)                  5.7, 6.1: episode 13's own invitation screen (DAD), unchanged
"""
import math
import cairo
import of_ui as ui

CYAN = (0.10, 0.62, 0.78)
_PHOTO = [None]


def _photo(c, x, y, w):
    """The team photo the robot took (robot_ps.team_photo), w units wide, a soft shadow under it."""
    import robot_ps as rp
    if _PHOTO[0] is None:
        _PHOTO[0] = rp.team_photo()
    ph = _PHOTO[0]
    c.set_source_rgba(0, 0, 0, 0.10); ui.rr(c, x + 0.6, y + 1.2, w, w, 2.2); c.fill()
    c.save(); ui.rr(c, x, y, w, w, 2.2); c.clip(); c.translate(x, y); c.scale(w / 184.0, w / 184.0)   # the photo's 184 px
    c.set_source_surface(ph, 0, 0); c.paint(); c.restore()


def public(c, H, approved=False):
    ui._base(c, H); ui.status(c); ui.appbar(c, "New post")
    _photo(c, 22, 33, 56)
    ui.txt(c, "PUBLIC", 50, 110, 17.0, ui.TXT, True, 0.5, font="Lilita One")      # the one word, the biggest thing
    ui.txt(c, "POST?", 50, 128, 17.0, ui.TXT, True, 0.5, font="Lilita One")
    if approved:
        ui.pill(c, 10, 140, 80, 26, ui.GRN, "", 12)
        c.set_source_rgb(1, 1, 1); c.set_line_width(4.2); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(38, 153); c.line_to(46, 160); c.line_to(62, 145); c.stroke()             # the tick, white on green
    else:
        ui.pill(c, 10, 140, 80, 26, CYAN, "APPROVE", 11.5)


def post(c, H, caption=True):
    ui._base(c, H); ui.status(c); ui.appbar(c, "Feed")
    ui.card(c, 5, 33, 90, 120)
    ui.avatar(c, 14, 42, 4.6, (0.16, 0.20, 0.42), "D")
    ui.txt(c, "Don", 21, 45, 9.0, ui.TXT, True)                                       # nothing under ~9 units (226)
    _photo(c, 10, 50, 80)
    if not caption:                                          # 4.2's pinch-zoom into the photo: no caption at the frame's edge
        return                                               # (lesson 295: a cropped "#TeamDon" read as "amDon")
    ui.txt(c, "#TeamDon", 50, 146, 15.5, ui.TXT, True, 0.5, font="Lilita One")       # the one word
    c.save(); c.translate(14, 165); c.set_source_rgb(*ui.RED); c.new_path(); c.move_to(0, 4)   # a drawn heart (Inter has none)
    c.curve_to(-6, -1, -4.5, -7, 0, -3.5); c.curve_to(4.5, -7, 6, -1, 0, 4); c.close_path(); c.fill(); c.restore()
    ui.txt(c, "1  ·  just now", 22, 168, 9.0, ui.SUB, True)


def invite(c, H):
    ui.invite(c, H)


HEEL_PT = (19.3, 33.9)                                       # Sofía's heel in the posted photo, in robot_ps.phone_screen's units
