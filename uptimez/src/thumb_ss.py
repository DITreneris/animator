"""Cover for "Secret Santa" (1080x1920). Key art inside the centre the profile grids crop to (y 120-840 at the 540x960
drawing scale): the payoff. Pam's barred present sits on UNCLAIMED, Don's TO: SOFIA (SECRET!) gift is stamped
APPROVED, the robot shows its green tick, Pam stares, Don preens. The hand-drawn SECRET SANTA sign is the title,
tilted like a sticker. Drawn with the film's own kit and the full-animation fixes. Usage: python3 thumb_ss.py out.png"""
import sys
import math
import cairo
import kit
import ss_anim  # noqa: F401  (sets the full-animation fixes: card, sign, clean wire)
import ss_set as S
import ss_set_sheet as sss
import ss_sb as sb
import pam_ss as ps
import don_ss as ds
import robot_ss as rs
import sofia_ss as so

CAM = (482, 580, 1.12)
X = S.POS


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    c = cairo.Context(surf); c.scale(2, 2)
    k = kit.Ctx(c, 0)
    c.save(); S.with_cam(c, CAM)
    keep = S.santa_sign
    S.santa_sign = lambda *a, **kw: None                                   # the wall sign becomes the title
    S.backdrop(k, t=0.4)
    S.santa_sign = keep
    so_seat = lambda: so.sofia(k, X["sofia"], S.SEAT, 1.0, "stand", "unimpressed", look=(1, 0.1), lean=4, lag=(-5, 0),
                               seed=95)
    S.seated(k, so_seat)
    S.desk(k)
    ds.don(k, X["sofia"] - 215, S.FEET, 1.0, "stand", "smug", look=(1, -0.2), shades="down", lean=6)
    sb.don_gift(k, X["sofia"] - 140, S.FEET, True)
    rs.robot(k, X["robot"] + 62, S.FEET_BACK, 1.0, "stand", "tick")
    ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_SHY, "incredulous", look=(-1, 0.3))
    S.santa_table(k, pams=False)
    sb.unclaimed_card(k, sb.UNCL[0], sb.UNCL[1] - 2)
    S.present(k, sb.UNCL[0] + 4, sb.UNCL[1] - 22, 50, 39, S.RED, S.GOLD, 966)
    sss.tag(k, sb.UNCL[0] + 26, sb.UNCL[1] - 52, 0.8, ("from", "to", "kiss"), rot=0.18)
    c.restore()
    c.save(); c.translate(160, 190); c.rotate(-0.08); c.scale(1.5, 1.5); c.translate(-330, -318)   # the title
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(330 - 74, 318 - 40, 156, 96); c.fill()
    S.santa_sign(k, 330, 318, 0.0)
    c.restore()
    g = cairo.RadialGradient(270, 480, 260, 270, 480, 620)                  # a soft vignette
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.28)
    c.set_source(g); c.paint()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ss_thumbnail.png")
