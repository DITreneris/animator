"""v3, pinned. Set sheet v3 for "The Best Candidate": the interview room (bc_set.py v3), the cameras and the BIAS MONITOR.
v3, for the storyboard's bubble pass: the monitor and the poster hang higher, the chair is centred under the poster,
the UptimeZ sign is behind the robot, and the cameras are the storyboard's: every sign in a frame is whole or absent,
and there is clear wall for a bubble beside or above every speaker. bc_set_sheet_v1.py and _v2.py are kept.
Writes bc_set_sheet_v3.png at 2400x2700 (1200x1350, 2x) and bc_set_phone_v3.png (six 360x640 frames)."""
import sys
import cairo
import kit
import brand
import bc_set_v3 as st
import cand_bc as cb
import don_bc as db
import mom_bc as mb
import pam_bc as pb
import sofia_bc as sb
import robot_mf as rm
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1350
GREY = (0.35, 0.40, 0.50)
k = None


def panel_people(don=None, pam=None, sofia=None, robot=True, phone="still"):
    if robot:
        rm.robot(k, st.POS["robot"], st.FEET_BACK, 1.0, "stand", "eager", seed=97)
    st.seated(k, don or (lambda: db.don(k, st.POS["don"], st.SEAT, 1.0, db.POSE_PEN, "flat", look=(-1, 0.2), board="front",
                                        tense=True)))
    st.seated(k, pam or (lambda: pb.pam(k, st.POS["pam"], st.SEAT, 1.0, pb.POSE_TABLE, "neutral", look=(-1, 0))))
    st.seated(k, sofia or (lambda: sb.sofia(k, st.POS["sofia"], st.SEAT, 1.0, "write", "neutral", look=(-1, 0))))
    st.table(k, phone=phone)


def s_wide():
    st.backdrop(k, 0.0, "idle")
    cb.small(k, st.POS["chair"], st.CHAIR_SEAT, 1.0, "hug", "hopeful", cv=True, seated=True, look=(0.6, -0.2))
    panel_people()


def s_door():
    st.backdrop(k, 0.72, "idle")


def s_chair():
    st.backdrop(k, 0.0, "idle")
    cb.small(k, st.POS["chair"], st.CHAIR_SEAT, 1.0, "hug", "hopeful", cv=True, seated=True, look=(0.6, -0.2))


def s_say():
    st.backdrop(k, 0.0, "idle")
    cb.small(k, st.POS["chair"], st.CHAIR_SEAT, 1.0, "hug", "proud", cv=True, seated=True, look=(0.7, -0.1), mouth="E")


def s_mom():
    st.backdrop(k, 0.0, "idle")
    st.mom_on_chair(k, pose="bag", face="sweet")


def s_chain():
    st.backdrop(k, 0.0, "idle")
    panel_people(don=lambda: db.don(k, st.POS["don"], st.SEAT, 1.0, db.POSE_PEN, "pout", look=(-1, 0.1), board="front",
                                    tense=True, mouth="M"),
                 pam=lambda: pb.pam(k, st.POS["pam"], st.SEAT, 1.0, pb.POSE_WRITE, "peer", note="KIND", pen=True),
                 sofia=lambda: sb.sofia(k, st.POS["sofia"], st.SEAT, 1.0, "aside", "smile", look=(-1, -0.4), blush=0.6,
                                        lag=(-5, 0)), robot=False)


def s_phone():
    st.backdrop(k, 0.0, "family")
    panel_people(don=lambda: db.don(k, st.POS["don"], st.SEAT, 1.0, db.POSE_HIDE, "sheepish", look=(-0.4, 1.0),
                                    board="back", tense=True), robot=False, phone="buzz")


def s_reveal():
    st.backdrop(k, 0.0, "clear", with_chair=True)
    db.don(k, st.POS["chair"] + 126, st.FEET, 1.0, "stand", "obey", tense=True, seed=500)
    mb.mom(k, st.POS["chair"] + 14, st.FEET, 1.0, mb.wipe_at(91, db.BT + 96), "stern", look=(0.9, 0.9), seed=70, bag=False)


FRAMES = (("door", s_door, "0 · THE DOOR", "Frame 0 and the last frame."),
          ("small_say", s_say, "1 · A CANDIDATE", "Left of centre; the bubble beside."),
          ("mom", s_mom, "3 · MOM", "Level, centred under the poster."),
          ("panel", s_chain, "2 · THE TABLE", "The whole monitor; wall above heads."),
          ("don", s_phone, "3 · THE QUESTION", "The same frame, three times."),
          ("reveal", s_reveal, "5 · THE REVEAL", "Under WE HIRE ON MERIT."))


def frame(c, x, y, w, cam, draw):
    c.save(); c.translate(x, y); c.scale(w / 540.0, w / 540.0)
    c.rectangle(0, 0, 540, 960); c.clip()
    st.with_cam(c, st.CAMS[cam]); draw()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w, w * 16 / 9); c.stroke()


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE BEST CANDIDATE", 68, 44, 28, bold=True)
    corp(c, "the interview room  ·  side-on staging  ·  the wall leaves room for the bubbles", 400, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · SET SHEET · v3"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # ---------------------------------------------------------------- the room
    y0 = 92
    corp(c, "THE ROOM  (section 1: the small one in the chair; the panel looks screen left)", 24, y0 - 6, 10, bold=True)
    c.save(); c.rectangle(24, y0, 1152, 520); c.clip()
    c.translate(24, y0); c.scale(0.83, 0.83); c.translate(40, -146)        # v3: from above the signs to the floor
    s_wide()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(24, y0, 1152, 520); c.stroke()
    for wx, lab in ((70, "door: the loop"), (350, "the chair"), (665, "Sofía"), (825, "Don"), (985, "Pam"),
                    (1140, "robot: the voice"), (895, "the phone")):
        x = 24 + (wx + 40) * 0.83
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(9)
        w = c.text_extents(lab).x_advance
        c.set_source_rgba(0.08, 0.08, 0.12, 0.8); c.rectangle(x - w / 2 - 5, y0 + 496, w + 10, 16); c.fill()
        c.set_source_rgb(1, 1, 1); c.move_to(x - w / 2, y0 + 508); c.show_text(lab)

    # ---------------------------------------------------------------- cameras
    y1 = 644
    corp(c, "CAMERAS  (9:16; the numbers are script sections)", 24, y1 - 6, 10, bold=True)
    for i, (cam, draw, lab, cap) in enumerate(FRAMES):
        x = 24 + i * 193.6
        frame(c, x, y1, 184, cam, draw)
        c.set_source_rgb(*brand.NAVY); c.rectangle(x, y1, 184, 18); c.fill()
        corp(c, lab, x + 7, y1 + 13, 9.2, col=(1, 1, 1), bold=True)
        corp(c, cap, x, y1 + 343, 8.2, col=INK)

    # ---------------------------------------------------------------- the monitor
    y2 = 1022
    corp(c, "THE BIAS MONITOR  (its five rulings, in order)", 24, y2 - 6, 10, bold=True)
    states = (("proceed_height", "1: the small one"), ("proceed_looks", "2: the macho"), ("ageism", "3: Sofía's question"),
              ("family", "3: Pam's question"), ("clear", "4: the verdict"))
    for i, (stt, lab) in enumerate(states):
        x = 24 + i * 186
        c.save(); c.rectangle(x, y2, 178, 96); c.clip()
        c.set_source_rgb(*kit.WALL); c.rectangle(x, y2, 178, 96); c.fill()
        c.translate(x + 89, y2 + 50); c.scale(0.6, 0.6); c.translate(-(st.MON[0] + st.MON[2] / 2), -(st.MON[1] + st.MON[3] / 2))
        st.monitor(k, stt)
        c.restore()
        c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(x, y2, 178, 96); c.stroke()
        corp(c, lab, x, y2 + 110, 8.6, col=GREY, bold=True)
    boxed(c, 24 + 5 * 186, y2, W2 - 24 - (24 + 5 * 186), 96)
    c.save(); c.rectangle(24 + 5 * 186, y2, 222, 96); c.clip()
    st.hired_stamp(k, 24 + 5 * 186 + 111, y2 + 50, 0.9)
    c.restore()
    corp(c, "4: the robot's stamp", 24 + 5 * 186, y2 + 110, 8.6, col=GREY, bold=True)

    boxed(c, 24, y2 + 128, W2 - 48, 172)
    notes = [("STAGING", "The door and the candidate's chair are screen left, the panel is screen right. Panel eyes go left, "
                         "candidates' eyes go right. Sofía sits nearest the candidate; Don sits between the two women."),
             ("BUBBLES", "Beside the face at mouth height where the wall is clear (candidates sit left of centre), or just "
                         "above the speaker's own head in a tight shot. Never over a face or a sign; inside the safe zones."),
             ("THE WALL", "v3: the monitor and the poster hang higher so a bubble fits above every head. Every sign in a "
                          "frame is whole or absent, so the cameras are set by the notice, the poster and the monitor."),
             ("THE PHONE", "Face down by Don's hand from frame 2; it buzzes at each of his three questions. What it says is "
                           "a full-screen insert: CLIENT · 47 MISSED CALLS, then CALL ANSWERED."),
             ("THE ROBOT", "Far right, under the UptimeZ sign. On screen for the lines the monitor does not show."),
             ("THE REVEAL", "Don comes round the table to the chair. Mom scrubs his vest under the poster. The film opens on "
                            "the door and ends on \"He's applying for your job\" and the same door.")]
    for i, (h, n) in enumerate(notes):
        corp(c, h, 36, y2 + 150 + i * 26, 9, col=brand.NAVY, bold=True)
        corp(c, n, 138, y2 + 150 + i * 26, 9.4, col=INK)
    flush(c)
    surf.write_to_png(out)


def phone(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2160, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, (cam, draw, _, _) in enumerate(FRAMES):
        frame(c, 360 * i, 0, 360, cam, draw)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bc_set_sheet_v3.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "bc_set_phone_v3.png")
