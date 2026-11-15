"""Model sheets redrawn with the v3 badges: staff badge on Don and Pam, DAY 1 sticker on Sofía, DON 2.0
on the robot. Writes sofia_sheet_v3.png and props_sheet_v3.png; the earlier sheets are kept."""
import functools
import kit
import pt42
import sofia as sf
import day1_kit as dk
import day1_sb_v3 as v3

kit.BADGE_HOOK = v3.person_badge
sf.BADGE_HOOK = lambda k, bt, seed: v3.day1_sticker(k, 2, bt + 30)
pt42.branded_person = pt42._orig_person            # the new badge carries the logo mark itself
dk.robot = functools.partial(dk.robot, badge="DON 2.0")
import sofia_sheet_v3
import day1_props_sheet
sofia_sheet_v3.main("sofia_sheet_v3.png")
day1_props_sheet.main("props_sheet_v3.png")
