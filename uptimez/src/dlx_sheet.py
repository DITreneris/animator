"""Rough character sheet for Downloads Expedition: RUSH x3 looks, KEVIN, MAX with the helmet, cave mood.
Writes dlx_charsheet.png (1080x1350). Drawn with the episode kit so the sheet matches the animatic."""
import os
import kit
import pt42
import dlx_kit as dk
import charsheets as cs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dlx_charsheet.png")

surf, c, k = cs.sheet_base("EXPEDITION CAST", "Rough character sheet · for approval before the animatic")
panels = [  # x, y, w, h, label, accent
    (24, 80, 160, 290, "RUSH · OFFICE (panic: spikes, sweat)", (0.30, 0.66, 0.66)),
    (190, 80, 160, 290, "RUSH · EXPEDITION (helmet, lamp, rope)", (0.24, 0.30, 0.36)),
    (356, 80, 160, 290, "RUSH · AFTER (beard, flicker, torn)", (0.30, 0.66, 0.66)),
    (24, 380, 160, 240, "KEVIN · INTERN (still, smiling)", (0.13, 0.12, 0.12)),
    (190, 380, 160, 240, "MAX · INHERITS THE HELMET", (0.52, 0.56, 0.62)),
    (356, 380, 160, 240, "THE CAVE (mood, labels optional)", (0.13, 0.12, 0.12)),
]
for x, y, w, h, label, acc in panels:
    c.set_source_rgb(*acc); c.rectangle(x, y, w, h); c.fill()
    cs.corp(c, label, x + 5, y + h - 6, 7, col=(1, 1, 1), bold=True)


def clip(x, y, w, h):
    c.save(); c.rectangle(x, y, w, h - 14); c.clip()


clip(24, 80, 160, 290); dk.rush(k, 104, 352, 0.62, "office", pose="panic", face="panic", t=0.2); c.restore()
clip(190, 80, 160, 290); dk.rush(k, 270, 352, 0.62, "expedition", pose="stand", face="neutral"); c.restore()
clip(356, 80, 160, 290); dk.rush(k, 436, 352, 0.62, "after", pose="stand", face="hollow", lamp=0.4); c.restore()
clip(24, 380, 160, 240); dk.kevin(k, 104, 590, 0.8); c.restore()
clip(190, 380, 160, 240)
p = pt42.branded_person(k, "MAX", 270, 620, 0.58, pose="stand", face="neutral", seed=33)
dk.helmet(k, *p["head"], 0.58, lamp=1.0)
c.restore()
clip(356, 380, 160, 240)
c.save(); c.translate(356, 380); c.scale(160 / kit.W, 226 / kit.H)
dk.cave(k)
dk.rush(k, kit.W / 2, 620, 0.5, "expedition")
c.set_source_rgb(*dk.ROPE); c.set_line_width(4); c.move_to(kit.W / 2, 180); c.line_to(kit.W / 2, 470); c.stroke()
c.restore(); c.restore()
notes = ("Caricature: whole-body reactions (squash, stretch, eyes pop), sweat and hair spikes only in panic. "
         "Faces always visible: the beard starts below the mouth; RUSH's face stays clear under FINAL (28). "
         "KEVIN stays friendly: round sockets with a highlight, smile, no damage. One readable label per shot.")
cs.wrap(c, notes, 24, 640, 8.5, 492)
surf.write_to_png(OUT)
print(OUT)
