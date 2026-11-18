"""Cover v2 for "Secret Santa" (1080x1920): the frame both cold viewers would screenshot. The tags insert of the final
film (ss_anim7.py) at APPROVED: Pam's tag with three black bars above Don's TO: SOFIA (heart) / FROM: DON stamped
APPROVED, without the bubble; the hand-drawn SECRET SANTA sign as the title, tilted like a sticker, in the centre band
that profile grids keep (y 120-840 at the 540 x 960 drawing scale). thumb_ss.py (v1, the busy wide) is kept.
Usage: python3 thumb_ss2.py out.png"""
import sys
import cairo
import kit
import engine_hd as eh
import xmas_bubbles as xb
import ss_anim7 as M
import ss_set as S


def main(out):
    xb.speech = lambda *a, **kw: None
    frame = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    eh.render(M, int(39.5 * 30), frame)                   # the insert, APPROVED down and the stamp gone
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    c = cairo.Context(surf)
    c.set_source_surface(frame, 0, 150); c.paint()        # down a little: room for the title above the tags
    c.set_source_surface(frame, 0, 0); c.rectangle(0, 0, 1080, 150); c.fill()    # the cloth above, continued
    c.scale(2, 2)
    k = kit.Ctx(c, 0)
    c.save(); c.translate(270, 150); c.rotate(-0.07); c.scale(1.2, 1.2); c.translate(-330, -318)   # the title
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(330 - 74, 318 - 40, 156, 96); c.fill()
    S.santa_sign(k, 330, 318, 0.0)
    c.restore()
    g = cairo.RadialGradient(270, 480, 260, 270, 480, 620)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.22)
    c.set_source(g); c.paint()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ss_thumbnail_v2.png")
