# the round-3 bubbles (dh_speech placement) must now FAIL: long tails from the top, the MOM card, a squeezed box
import os, sys
import dh_tailcheck as T
import dh_speech as SP, dh_back as db, dh_anim3_v8 as m8, dh_scenes as ds
SP._wrap(db, "don_back", "antenna", False); SP._fresh(m8, "frame")
ds.ARM_PHONE[0] = True
fr = lambda tt, n: m8.frame(tt, n, 1)
for n in (6, 20, 54, 66, 86, 100, 126):
    SP.HELD.clear()
    for r in T.check_one(fr, n, 3):
        print("PLANT", n, r["text"][:26], [x for x in r["fails"] if "past the box" in x or "squeezed" in x or "card" in x] or "-- not caught --", flush=True)
