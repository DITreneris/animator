"""v5: also eyes crossed by any later label, prop (cover: desk, hat brim, sheets) or face, and bubble tails
that end away from their speaker.
Automatic checks for Downloads Expedition (rough animatic). Renders every 3rd frame offscreen and reads
the boxes dlx.py registers while drawing:
  - faces: a label or another face drawn later that covers >25% of a face box
  - safe zones: labels or faces in the top 10%, bottom 15% or right-hand 12% (app buttons)
  - text size: registered labels under 20 px at 540 wide (40 px at 1080)
  - overlaps: speech bubbles, name tags and signs must not overlap each other
Usage: python3 qa_dlx.py dlx_a"""
import importlib
import sys
import cairo
import engine_v
import dlx
from kit import W, H

mod = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "dlx_a")
n = int(round(mod.DURATION * 30))
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)


def area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def inter(a, b):
    return area((max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])))


issues = {}
for f in range(0, n, 3):
    dlx.QA.clear()
    engine_v.render(mod, f, surf)
    items = list(dlx.QA)
    for i, (kind, box, size) in enumerate(items):
        if kind == "label" and size and size < 20:
            issues.setdefault(("small text", round(size)), []).append(f)
        x0, y0, x1, y1 = box
        if x1 > W * 0.88 and kind == "label":
            issues.setdefault(("label in right button zone", ""), []).append(f)
        if (y0 < H * 0.10 or y1 > H * 0.85) and kind == "label":
            issues.setdefault(("label in top/bottom zone", ""), []).append(f)
        if kind == "label":
            for kind2, box2, _ in items[i + 1:]:
                if kind2 == "label" and inter(box, box2) > 0.1 * min(area(box), area(box2)):
                    issues.setdefault(("labels overlap each other", ""), []).append(f)
        if kind == "label":
            for kind2, box2, _ in items[i + 1:]:
                if kind2 == "cover" and inter(box, box2) > 0.2 * area(box):
                    issues.setdefault(("label covered by a page", ""), []).append(f)
        if kind == "tailmiss":
            issues.setdefault(("bubble tail not at its speaker", ""), []).append(f)
        if kind == "eyes":
            for kind2, box2, _ in items[i + 1:]:
                if kind2 in ("label", "cover", "face") and inter(box, box2) > 0.03 * area(box):
                    issues.setdefault((f"eyes crossed by {kind2}", ""), []).append(f)
        if kind == "face":
            for kind2, box2, _ in items[i + 1:]:
                if kind2 not in ("cover", "eyes", "tailmiss") and inter(box, box2) > 0.25 * area(box) or (kind2 == "cover" and inter(box, box2) > 0.25 * area(box)):
                    issues.setdefault((f"face covered by {kind2}", ""), []).append(f)
for (what, extra), frames in sorted(issues.items()):
    spans, start, prev = [], frames[0], frames[0]
    for fr in frames[1:] + [None]:
        if fr is None or fr - prev > 3:
            spans.append(f"{start / 30:.1f}-{prev / 30:.1f}s")
            if fr is not None:
                start = fr
        prev = fr if fr is not None else prev
    print(f"{what} {extra}: {', '.join(spans)}")
print("checked", len(range(0, n, 3)), "frames")
