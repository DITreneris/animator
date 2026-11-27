"""The Double Agent (episode 15): the props sheet (plan v2 §2, 3.4). Reuse first (CLAUDE.md rule 2): every prop that a
film already drew is called from where it lives; two are new here (the robot's minutes, Don's cup and saucer).

  prop                       shots            drawn by
  Pam's mustard mug          3.2-5.1, 8.1     da_set.pam_mug (the one silhouette in every shot)
  the gift: the mug + bow    2.4, 3.2         da_sheets.gift_mug
  her old blue mug, broken   2.4              da_sheets._shards
  Don's cup and saucer       3.2-5.3          NEW cup_and_saucer: hand_lib_sheet_v3.big_cup's china, the saucer's
  AGENDA: WITHOUT HIM        6.1-6.3          NEW minutes(): the robot's printout, a torn feed edge
  MY GARAGES, rolled / flat  6.6, 7.3, 8.1    client_ob.blueprint_roll / acts_ob.plan_open (GARAGES + TITLE)
  REVIEW · TOMORROW          1.3, the loop    da_sheets._tag
  the paperclip box, clips   1.4, 2.1-7.4     sofia_da.clip_box, da_s8r.clip
  Sofía's binder             1.4              sofia_da.binder
  Mom's knitting             3.4, 4.3, 5.4    mom_fs.knitting
  the peeled strip, the roll 7.1-7.2, 1.1     don_ps.tape_strip, da_s8r.roll_on_floor's roll

  python3 da_props.py  -> ../the-double-agent/da_props_v1.png (the props at 2x) and da_props_v1_feed.png (each at its
                          film size, then at 270 px wide: a sign must read there)
"""
import math
import os
import sys

import cairo
from PIL import Image

import kit
from kit import Ctx, INK
import da_set as ds
import da_sheets as dsh
import da_hands as dh
import hand_lib_sheet_v3 as hs
import client_ob as cob
import acts_ob as ac
import sofia_da as sd
import mom_fs as mf
import don_ps as dp
import ps_set as pss
import da_s8r as r8

PAPER = (0.98, 0.98, 0.96)
ROBOT_TXT = (0.16, 0.18, 0.22)


def cup_and_saucer(k, x, y, s=1.0, slop=False):
    """Don's cup on its saucer (white china, not the shirt's white: the 5.2 audit); slop: coffee spilled in the saucer."""
    hs.saucer_at(k, x, y + 2 * s, 0.95 * 20 * s / 30.0 * 1.6)
    if slop:
        kit.ellipse(k, x + 8 * s, y - 3 * s, 7 * s, 2.2 * s, dh.COFFEE, 7301, shadow=False, lw=0.8)
    dh.cup(k, x, y - 4 * s, 0.9 * s, 1)


def gift_mug(k, x, y, s=1.0):
    """Don's gift (2.4): Pam's mug itself (da_set.pam_mug, the one silhouette: "one prop, one shape"), a gold bow tied
    on its handle (script v4: "a gold bow on the handle"). da_sheets.gift_mug drew the series mug, handle left and dark:
    a second silhouette for the same mug, not used."""
    ds.pam_mug(k, x, y, s)
    c = k.c
    c.save(); c.translate(x + 23 * s, y - 15 * s); c.scale(s, s)
    for sx in (-1, 1):
        kit.cut(k, [(0, 0), (sx * 9, -7), (sx * 9, 7)], dsh.GOLD_BOW, shadow=False, lw=1.6)
    kit.ellipse(k, 0, 0, 3, 3, dsh.GOLD_BOW, 7311, shadow=False, lw=1.4)
    c.restore()


def minutes(k, x, y, s=1.0, ang=0.0):
    """The robot's printed minutes: thermal paper, a torn feed edge at the top, AGENDA: small, WITHOUT HIM big, three
    grey lines under it (6.3's insert reads it whole; at 6.1 it only has to read as a page)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    top = [(-40 + i * 8, -60 + (3 if i % 2 else 0)) for i in range(11)]
    kit.cut(k, top + [(40, 60), (-40, 60)], PAPER, lw=2)
    c.select_font_face(kit.FONT, 0, 1)
    c.set_source_rgb(*ROBOT_TXT); c.set_font_size(11)
    e = c.text_extents("AGENDA:"); c.move_to(-e.x_advance / 2, -34); c.show_text("AGENDA:")
    for line, yy in (("WITHOUT", -10), ("HIM", 14)):
        c.set_font_size(15.5); e = c.text_extents(line); c.move_to(-e.x_advance / 2, yy); c.show_text(line)
    c.set_source_rgb(0.70, 0.72, 0.74); c.set_line_width(2.4)
    for yy in (30, 40, 50):
        c.move_to(-30, yy); c.line_to(30 - (yy - 30), yy); c.stroke()
    c.restore()


def tile(draw, label, w=260, h=200, scale=2.0):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, int(w * scale), int(h * scale))
    c = cairo.Context(s); c.scale(scale, scale)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    c.save(); c.translate(w / 2, h / 2 + 10); draw(k); c.restore()
    c.select_font_face("Inter", 0, 1); c.set_font_size(11); c.set_source_rgb(*INK)
    c.move_to(8, 16); c.show_text(label)
    s.flush()
    return Image.frombuffer("RGB", (s.get_width(), s.get_height()), bytes(s.get_data()), "raw", "BGRX", 0, 1)


PROPS = [
    ("Pam's mug (mustard)", lambda k: ds.pam_mug(k, 0, 30, 2.2), 0.54),
    ("the gift: her mug + a bow", lambda k: gift_mug(k, 0, 30, 2.2), 0.54),
    ("her blue mug, shattered", lambda k: dsh._shards(k, 0, 20, 2.0), 0.54),
    ("Don's cup and saucer", lambda k: cup_and_saucer(k, 0, 20, 2.2), 0.60),
    ("... coffee in the saucer (5.2)", lambda k: cup_and_saucer(k, 0, 20, 2.2, slop=True), 0.60),
    ("AGENDA: WITHOUT HIM", lambda k: minutes(k, 0, 0, 1.3), 0.60),
    ("MY GARAGES, rolled", lambda k: cob.blueprint_roll(k, 0, 0, 1.2, 150, 11), 0.52),
    ("MY GARAGES, flat", lambda k: _plan(k), 0.52),
    ("REVIEW · TOMORROW", lambda k: dsh._tag(k, 0, -50, 1.6), 1.15),
    ("the paperclip box", lambda k: sd.clip_box(k, 0, 20, 1.6), 0.47),
    ("Sofía's binder", lambda k: sd.binder(k, 0, 0, 1.4), 0.47),
    ("Mom's knitting", lambda k: mf.knitting(k, 0, 0, 1.8), 0.54),
    ("the peeled strip", lambda k: dp.tape_strip(k, (-90, 0), (90, -10), 1.6), 0.60),
]


def _plan(k):
    old = ac.GARAGES[0], ac.TITLE[0]
    ac.GARAGES[0] = ac.TITLE[0] = True
    try:
        ac.plan_open(k, 0, 0, 1.4)
    finally:
        ac.GARAGES[0], ac.TITLE[0] = old


def main(out_dir="../the-double-agent"):
    big = [tile(fn, lab) for lab, fn, _ in PROPS]
    cols = 4
    rows = (len(big) + cols - 1) // cols
    tw, th = big[0].size
    sheet = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
    for i, im in enumerate(big):
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(os.path.join(out_dir, "da_props_v1.png"))
    feed = Image.new("RGB", (cols * tw // 4, rows * th // 4), (255, 255, 255))
    for i, im in enumerate(big):                                  # the 270 px feed: half of the film's 540
        feed.paste(im.resize((tw // 4, th // 4), Image.LANCZOS), ((i % cols) * tw // 4, (i // cols) * th // 4))
    feed.save(os.path.join(out_dir, "da_props_v1_feed.png"))
    print("wrote da_props_v1.png, da_props_v1_feed.png")


if __name__ == "__main__":
    main(*sys.argv[1:])
