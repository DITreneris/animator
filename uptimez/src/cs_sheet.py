"""ONE STAR: the AI's site plan as a sheet in a shot (Tomas, 20 Nov: "at 0:07 Don shows the wrong map"). The robot
prints it (3.1), Don presents it (3.3), Pam's plan goes over it (4.2): it must be the same glossy blue SITE PLAN as the
insert (cs_props.ai_site), the silhouette its one readable thing at this size: two round courts, a long drive, a
turning circle, white bay marks round them, and the title bar.
  ai_sheet(k, cx, top, w, h, ang=0.0, show=1.0)   # show: how much of it, from the top (a sheet still printing)"""
import math
from kit import INK, rect

BLUE = (0.20, 0.45, 0.85)
PALE = (0.55, 0.72, 0.96)


def ai_sheet(k, cx, top, w, h, ang=0.0, show=1.0, seed=981):
    c = k.c
    c.save(); c.translate(cx, top); c.rotate(ang)
    c.save(); c.rectangle(-w / 2 - 2, -2, w + 4, h * show + 2); c.clip()
    rect(k, -w / 2, 0, w, h, BLUE, seed, shadow=False, lw=max(1.0, w * 0.02))
    c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(max(0.5, w * 0.004))       # the grid
    n = 8
    for i in range(1, n):
        c.move_to(-w / 2 + w * i / n, 0); c.line_to(-w / 2 + w * i / n, h); c.stroke()
    for j in range(1, int(n * h / w)):
        c.move_to(-w / 2, j * w / n); c.line_to(w / 2, j * w / n); c.stroke()
    c.set_source_rgb(1, 1, 1); c.rectangle(-w * 0.32, h * 0.05, w * 0.64, h * 0.045); c.fill()   # SITE PLAN
    c.set_source_rgb(1, 0.9, 0.3); c.rectangle(-w * 0.24, h * 0.115, w * 0.48, h * 0.03); c.fill()  # 99% CONFIDENT
    # the silhouette, as in the insert: two courts at the foot, the drive, the turning circle
    s = w / 540.0 * 1.35
    oy = h * 0.21
    def P(x, y):
        return (x - 270) * s, oy + (y - 268) * s * (h / w) / 1.6
    c.set_source_rgb(*PALE)
    for (x, y, r) in ((206, 690, 74), (334, 690, 74), (270, 330, 62)):
        px, py = P(x, y); c.new_path(); c.arc(px, py, r * s, 0, 2 * math.pi); c.fill()
    x0, y0 = P(222, 330); x1, y1 = P(318, 660)
    c.rectangle(x0, y0, x1 - x0, y1 - y0); c.fill()
    c.set_source_rgb(1, 1, 1); c.set_line_width(max(0.8, w * 0.012))
    for (x, y, r) in ((206, 690, 74), (334, 690, 74), (270, 330, 62)):
        px, py = P(x, y); c.new_path(); c.arc(px, py, r * s, 0, 2 * math.pi); c.stroke()
    for (x, y) in ((196, 600), (344, 600), (196, 496), (344, 496), (196, 392), (344, 392)):   # bay marks
        px, py = P(x, y); c.rectangle(px - 5 * s, py - 4 * s, 10 * s, 8 * s); c.stroke()
    c.restore()
    c.restore()
