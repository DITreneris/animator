"""Pick a Side: the hand sheet (rules page, section 0, step 4): every hand that board v4 and the 3.4 gag added or changed, cut
from the film's own frames at ONE scale (540 px frames, 1:1), not from random poses (lesson 149).

  python3 ps_hands.py        -> ../pick-a-side/ps_hands_board_v4.png (ps_hands_v1.png is the approved cast sheet, 23 Nov)
Needs board v4's frames (`python3 ps_scenes.py board v5`) and the 3.4 gag's drawings (`python3 ps_gags/L6.py`)."""
import os
import cairo

B, G = "/tmp/ps_board_v4", "/tmp/gags/L6f"
LAB = ["1.1", "1.2a", "1.2b", "1.3", "1.4", "2.1", "2.1b", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.9b", "2.10a",
       "2.10b", "2.11", "3.1a", "3.1b", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "4.1", "4.2", "4.3a", "4.3b", "5.1", "5.2", "5.3a",
       "5.3b", "5.4a", "5.4b", "5.5", "5.6", "5.7", "6.1", "6.1b", "6.2"]
CROPS = [  # label, file, (x, y) of a 230 x 230 crop, the hands_ps shape or the rig, the rule it answers
    ("5.2 the pen", "5.2", (270, 290), "hands_ps fist, an insert from the edge", "the pen, then the fist over it (224)"),
    ("4.3a guard 1's nose", "4.3a", (0, 215), "dh_cast's own arm, in front", "one hand per wrist (179, 208)"),
    ("4.3a guard 2's nose", "4.3a", (310, 215), "dh_cast's own arm, in front", "clear of the eyes (163)"),
    ("5.3b the oil can", "5.3b", (95, 285), "the robot's hand, twice", "held by its handle; the hand over it (224)"),
    ("5.5 the CV", "5.5", (250, 400), "hands_ps, the pose's hand", "a prop at the hand the pose returns"),
    ("3.4 the pose", "g000", (215, 395), "hands_ps thumb", "one static pose before motion (231)"),
    ("3.4 the arm drops", "g009", (255, 470), "hands_ps thumb", "the arm's own IK, fixed bones (224)"),
    ("3.4 the thumb on the pad", "g025", (250, 490), "hands_ps thumb", "contact in the drawing (263); a thumb, Tomas 25 Nov"),
]


def main(out="../pick-a-side/ps_hands_board_v4.png"):
    fs = sorted(os.listdir(B)); assert len(fs) == len(LAB), (len(fs), len(LAB))
    m = dict(zip(LAB, fs))
    T, cols = 230, 4
    rows = (len(CROPS) + cols - 1) // cols
    W, H = 20 + cols * (T + 14), 54 + rows * (T + 62)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    c.set_source_rgb(0.13, 0.13, 0.14); c.paint()
    c.select_font_face("DejaVu Sans", 0, 1); c.set_source_rgb(1, 1, 1); c.set_font_size(17)
    c.move_to(20, 30); c.show_text("PICK A SIDE · the hand sheet v1 · board v4 and the 3.4 gag · the film's frames at 1:1 (540 px)")
    c.select_font_face("DejaVu Sans", 0, 0)
    for i, (lab, f, (x, y), shape, rule) in enumerate(CROPS):
        p = os.path.join(G, f[1:] + ".png") if f.startswith("g") else os.path.join(B, m[f])
        im = cairo.ImageSurface.create_from_png(p)
        X, Y = 20 + (i % cols) * (T + 14), 54 + (i // cols) * (T + 62)
        c.save(); c.rectangle(X, Y, T, T); c.clip(); c.set_source_surface(im, X - x, Y - y); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 1); c.set_font_size(13); c.move_to(X, Y + T + 16); c.show_text(lab)
        c.set_source_rgb(0.72, 0.72, 0.74); c.set_font_size(10.5)
        c.move_to(X, Y + T + 31); c.show_text(shape); c.move_to(X, Y + T + 45); c.show_text(rule)
    s.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    main()
