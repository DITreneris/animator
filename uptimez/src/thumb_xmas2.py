"""Cover v2 for "Happy Compliance" (thumb_xmas.py = v1, kept): the same key art with one film-v2 fix that shows on
the cover: Sofia's badge raised above her forearm (her arm hid the A: "SOFI"). The set stays as v1 (its banner sits
above the cover's frame; the new two-row banner would poke in cut off at the top). Usage: python3 thumb_xmas2.py out.png"""
import sys
import sofia_xmas as sx
import xmas_anim2_v1 as x2
import thumb_xmas as tx


def main(out):
    keep = sx.BADGE_HOOK
    sx.BADGE_HOOK = x2.badge_high
    try:
        tx.main(out)
    finally:
        sx.BADGE_HOOK = keep


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "xmas_thumbnail_v2.png")
