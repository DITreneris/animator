"""FIRST SEARCH: the clutter audit. For every shot of the live board: who and what is in the frame (people by their
heads, things by an anchor point inside the frame), the shot's size by its biggest face, and whether it is over the
limit (close shots 4 readable things, medium shots 6, wides 8). A line counts as one thing (its bubble).

  python3 fs_audit.py  -> a table on stdout and first-search/fs_audit_v1.json
"""
import os
import json
import cairo
import fs_storyboard as sb
import fs_animatic as an
from kit import Ctx

F = sb.F
SEEN = []


def wrap(mod, attr, label, anchor):
    f = getattr(mod, attr)
    def w(*a, **kw):
        try:
            k = a[0]
            c = k.c if hasattr(k, "c") else k
            pts = anchor(*a[1:], **kw)
            for (x, y) in pts:
                dx, dy = c.user_to_device(x, y)
                if 0 <= dx <= 540 and 0 <= dy <= 960 and c.get_target().get_width() > 8 and not sb._DRY[0]:
                    SEEN.append(label); break
        except Exception:
            pass
        return f(*a, **kw)
    setattr(mod, attr, w)


def xy(*a, **kw):
    return [(a[0], a[1])]


def _install():
    fs, fd, mfs, brand = sb.fs, sb.fd, sb.mfs, sb.brand
    wrap(fs, "portrait", "portrait + OUR FIRST CLIENT",
         lambda *a, **kw: [((a[0] if a else fs.PORTRAIT[0]) + dx, (a[1] if len(a) > 1 else fs.PORTRAIT[1]) + dy)
                           for dx, dy in ((0, 0), (0, 80), (-60, 80), (60, 80))])
    wrap(fs, "screen", "UPTIMEZ FIND screen", lambda kind, x, y, w, h, **kw: [(x + w / 2, y + h / 2), (x + 10, y + 10)])
    wrap(fd, "shredder", "shredder", lambda *a, **kw: [(fd.SHRED[0], fd.SHRED[1] - 50)])
    wrap(fd, "counter", "counter", lambda *a, **kw: [(x, F - 120) for x in range(600, 891, 40)])
    wrap(fd, "office_door", "office door + DON plates", lambda *a, **kw: [(924, 520), (924, 700)])
    wrap(fd.s3, "monitor", "monitor", xy)
    wrap(fs, "counter_plate", "ASSISTANT TO DON + baby photo", xy)
    wrap(mfs, "mug", "WORLD'S BEST MOM mug", xy)
    wrap(mfs, "candy", "candy dish", xy)
    wrap(mfs, "knitting", "knitting (DON)", xy)
    wrap(fs, "plan_taped", "taped plan", xy)
    wrap(fs, "phone2", "phone", xy)
    wrap(fs, "tablet_upgrade", "tablet", xy)
    wrap(fs, "baby_photo", "baby photo", xy)
    wrap(fs, "remote", "remote", lambda x, y, *a, **kw: [(x, y)])
    wrap(brand, "mark", "logo", lambda x, y, size=56, *a, **kw: [(x, y)] if size >= 40 else [])   # not the badges' marks
    wrap(fd.s3, "confetti", "confetti", xy)
    wrap(sb, "thumb", "hand / thumb", xy)


def main(d="../first-search"):
    _install()
    rows = []
    for shot, hold, fn, note in sb.SHOTS:
        SEEN.clear()
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        c = cairo.Context(s); k = Ctx(c, 0)
        sb.bg(c); sb.HEADS.clear(); sb.AVOID.clear()
        with sb._norm(record_only=True):
            fn(k)
        people = sorted(n for n, (x, y, r) in sb.HEADS.items() if 0 <= x <= 540 and 0 <= y <= 960)
        things = sorted(set(SEEN))
        mr = max([r for n, (x, y, r) in sb.HEADS.items() if 0 <= x <= 540 and 0 <= y <= 960] or [0])
        size = "insert" if not people else "close" if mr >= 70 else "medium" if mr >= 32 else "wide"
        line = 1 if shot in an.LINE_OF else 0
        n = len(people) + len(things) + line
        limit = {"close": 4, "insert": 4, "medium": 6, "wide": 8}[size]
        rows.append(dict(shot=shot, size=size, count=n, limit=limit, over=n > limit, people=people, things=things,
                         line=bool(line)))
    json.dump(rows, open(os.path.join(d, "fs_audit_v1.json"), "w"), indent=1)
    for r in rows:
        print("%-5s %-6s %2d/%d %s  %s | %s" % (r["shot"], r["size"], r["count"], r["limit"], "OVER" if r["over"] else "    ",
                                              ", ".join(r["people"]), ", ".join(r["things"])))


if __name__ == "__main__":
    main()
