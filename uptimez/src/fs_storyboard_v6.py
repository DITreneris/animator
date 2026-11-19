"""(pinned: storyboard v6) FIRST SEARCH (episode 10): storyboard v6 (fs_storyboard_v5.py = v5, kept), after the dramaturgy review (19 Nov):
the tail after the payoff pressed (6.1 to 9.1, about 2.4 s shorter, nothing cut); Don's eyes go to Sofía after his
moves (2.2, 5.1, 5.3: his want, visible); 5.3, Pam holds the taped plan up behind the counter (the real answer) and
Don's proud thumb blocks it.
FIRST SEARCH (episode 10): storyboard v5 (fs_storyboard_v4.py = v4, kept): 1.2, Sofía flirts with the Client
as he comes in (a hand on her hip, the other at her ponytail, the charm smile, at him); he looks past her, at Don. Her
charm is one more cosmetic fix that doesn't work on him.
FIRST SEARCH (episode 10): storyboard v4 (fs_storyboard_v3.py = v3, kept): the portrait's plaster told whole.
Frame 0 is clean, as in the earlier episodes. The bonk cracks the glass (1.1b to 3.3 cracked, no plaster), Sofía
plasters it (3.4), and at the end the plaster drops off (9.3): the glass under it has healed and nobody notices. Then
frame 0 (9.4).
FIRST SEARCH (episode 10): storyboard v3 (fs_storyboard_v2.py = v2, kept), for script v6: the shots renumbered in
the new order (the photo and the post after "The zero's green."), Sofía's quiet "It found nothing." (her face: drop),
5.1 the Client looking at the green zero and finding nothing (the post no longer tells him), the baby photo with Don's
markers (fs_set.BABY_DON). The frames are v2's drawings.
FIRST SEARCH (episode 10): storyboard v2 (fs_storyboard_v1.py = v1, kept), after the cold mute test of v1 and the
grill of 18 Nov: the bonk in two frames (in the air, then on his head), the duck in a medium shot, a calendar card
(FRIDAY · BANK MEETING), PREMIUM · PAID with its price, Mom closer with the baby photo larger and Don sheepish under
her hand at his collar, the near-shred with the plan's end in the slot and Pam pulling it back, a larger remote.
Below, the notes of v1.
FIRST SEARCH (episode 10): storyboard v1, from script v5 and set sheet v2 (fs_set LAYOUT v2, sofia_fs v2), timed from
the takes (fs_voices/film/takes.json). One key frame per set-up, 27, drawn with the series' kit; under each its shot,
its time and its line. The mute copy (fs_storyboard_v1_mute.png) has the same frames without the lines, for the cold
viewers. The text that is in the picture (the screen, the phone, the plate) stays in both.
  python3 fs_storyboard.py [dir]   -> fs_storyboard_v1.png, fs_storyboard_v1_mute.png, and the frames in fs_board/"""
import math
import os
import sys
import json
import cairo
import kit
import brand
import set_ob as st
import fs_set as fs
import sofia_fs as sfs
import acts_ob as ac
import client_ob as co
import robot_mf as rm
import don_v4 as dv
import mom_bc
from kit import Ctx, INK, ellipse, rect, cut
from charsheets import corp, wrap

V = "v6"
F = fs.F
P = fs.POS2
SKIN_DON = kit.PEOPLE["DON"]["skin"]
SKIN_CL = (0.86, 0.66, 0.50)
OIL = (0.22, 0.17, 0.14)


# ---------------------------------------------------------------- the camera and the scene
def view(c, cx, cy, z):
    """Stage point (cx, cy) to the frame's centre, zoom z."""
    c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)


WIDE = (fs.CAM2[0] + 270 / fs.CAM2[2], fs.CAM2[1] + 480 / fs.CAM2[2], fs.CAM2[2])


def robot(k, x, feet, s, state="eager", arm="remote", paddle=None, face_over=None):
    pose = (0.0, 0, 0, (-20, 0), (150, 24)) if arm in ("remote", "paddle") else "stand"
    o = rm.robot(k, x, feet, s, pose, state, (-1, -0.6), -1)
    hx, hy = o["hands"][1]
    if arm == "remote":
        fs.remote(k.c, hx, hy - 6 * s, s * 1.6, ang=-0.7)
    if paddle:
        st.paddle(k, hx, hy, s * 0.9, ok=paddle == "green")
    return o


def don(k, x, feet, s, pose="stand", face="neutral", look=(-1, 0)):
    poses = {"stand": (-8, 0, 8, 0), "panic": (-150, -110, 150, 110), "hang": (-150, -20, 150, 20),
             "thumb": (-10, 0, 150, 40), "tablet": (-40, 95, 8, 0), "reach": (-70, 30, 8, 0), "swing": (60, 40, 8, 0)}
    kit.ARM_POSES["_fs"] = poses.get(pose, pose)
    try:
        with ac.arms():
            return dv.don(k, x, feet, s, "_fs", face, look=look, seed=500)
    finally:
        del kit.ARM_POSES["_fs"]


def client(k, x, feet, s, pose="stand", face="confident", look=(0.9, 0)):
    return co.client(k, x, feet, s, pose, face, look)


def scene(k, cam=WIDE, screen="query", portrait="hang", door=0.85, cl=None, rb=None, sf=None, dn=None, pm=None, mm=None,
          extra=None, counter=True, pre=None, back=None, counter_plan=True):
    """pre / back (v6, opt-in): drawn after the counter / before it, before the people. The front desk with this episode's things; each character a dict of overrides, or False to leave them out."""
    c = k.c
    c.save(); view(c, *cam)
    st.stage(k, open_=door, decor=False)
    fs.screen(k, screen)
    if portrait == "hang":
        fs.portrait(k)
    elif isinstance(portrait, dict):
        fs.portrait(k, **portrait)
    if pm is not False and counter:
        d = dict(x=P["pam"][0], feet=P["pam"][1], s=P["pam"][2], act="typing"); d.update(pm or {})
        ac.pam(k, d["x"], d["feet"], d["s"], d["act"])
    if mm is not False and counter:
        d = dict(x=P["mom"][0], feet=P["mom"][1], s=P["mom"][2], pose="bag", face="sweet", look=(-0.8, 0)); d.update(mm or {})
        mom_bc.mom(k, d["x"], d["feet"], d["s"], d["pose"], d["face"], look=d["look"])
    if back:
        back(k)
    st.desk(k, terminal=False, shred=None)
    if counter and counter_plan:
        fs.plan_taped(k, 356, F - 186, 0.30)
        fs.counter_plate(k, 398, F - 176)
    if pre:
        pre(k)
    out = {}
    if cl is not False:
        d = dict(x=P["client"][0], feet=P["client"][1], s=P["client"][2], pose="stand", face="confident", look=(0.9, 0)); d.update(cl or {})
        out["client"] = client(k, d["x"], d["feet"], d["s"], d["pose"], d["face"], d["look"])
    if rb is not False:
        d = dict(x=P["robot"][0], feet=P["robot"][1], s=P["robot"][2], state="eager", arm="remote", paddle=None); d.update(rb or {})
        out["robot"] = robot(k, d["x"], d["feet"], d["s"], d["state"], d["arm"], d["paddle"])
    if sf is not False:
        d = dict(x=P["sofia"][0], feet=P["sofia"][1], s=P["sofia"][2], pose="hold", face="charm", look=(-0.9, -0.2), lag=(-2, 0),
                 slide=None, plaster=None); d.update(sf or {})
        out["sofia"] = sfs.sofia(k, d["x"], d["feet"], d["s"], d["pose"], d["face"], look=d["look"], lag=d["lag"],
                                 slide=d["slide"], plaster=d["plaster"])
    if dn is not False:
        d = dict(x=P["don"][0], feet=P["don"][1], s=P["don"][2], pose="stand", face="neutral", look=(-1, 0)); d.update(dn or {})
        out["don"] = don(k, d["x"], d["feet"], d["s"], d["pose"], d["face"], d["look"])
    if extra:
        extra(k, out)
    c.restore()
    return out


def lines(c, x, y, n=7, r0=30, r1=50, a0=0, a1=360):
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / max(1, n - 1 if a1 - a0 < 360 else n))
        c.move_to(x + r0 * math.cos(a), y + r0 * math.sin(a)); c.line_to(x + r1 * math.cos(a), y + r1 * math.sin(a)); c.stroke()


def thumb(k, x, y, s=1.0, skin=SKIN_DON, oil=False, nail=False, ang=0.0):
    """A thumb pressing down from above: the thumb pad, its nail, the hand behind it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    ellipse(k, 0, -70, 46, 60, skin, 1, shadow=False, lw=2.4)
    ellipse(k, 0, -6, 20, 30, skin, 2, shadow=False, lw=2.4)
    ellipse(k, 0, -18, 11, 14, (0.95, 0.80, 0.75) if not nail else (0.86, 0.05, 0.12), 3, shadow=False, lw=1.6)
    if oil:
        c.set_source_rgba(*OIL, 0.6); c.arc(6, 10, 9, 0, 6.3); c.fill()
    c.restore()


def bg(c, col=None):
    c.set_source_rgb(*(col or kit.WALL)); c.paint()


# ---------------------------------------------------------------- the 27 key frames
def stars(c, x, y, r=46, n=5, t=0.0):
    for i in range(n):
        a = t + i * 2 * math.pi / n
        px, py = x + r * math.cos(a), y + r * 0.35 * math.sin(a)
        c.save(); c.translate(px, py)
        c.move_to(0, -9)
        for j in range(1, 10):
            rr = 9 if j % 2 == 0 else 4
            c.line_to(rr * math.sin(j * math.pi / 5), -rr * math.cos(j * math.pi / 5))
        c.close_path(); c.set_source_rgb(1.0, 0.86, 0.25); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke(); c.restore()


def bare_nail(c):
    px, py = fs.PORTRAIT
    ny = py - 66 * fs.PORTRAIT_S
    c.set_source_rgb(*INK); c.arc(px, ny, 2.6, 0, 2 * math.pi); c.fill()


def f_1_1a(k):                                             # the buzz: it is in the air
    def ex(k, o):
        c = k.c
        bare_nail(c)
        hx, hy = o["don"]["head"]
        fs.portrait(k, hx + 6, hy - 210, ang=0.12)
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
        for dx in (-44, -10, 24):                                                      # falling
            c.move_to(hx + dx + 6, hy - 330); c.line_to(hx + dx + 6, hy - 286); c.stroke()
        for i in range(3):                                                             # the buzz, off the screen
            c.arc(110, 336, 92 + i * 14, -0.5, 0.5); c.stroke()
    scene(k, screen="red", portrait=None, rb=dict(arm="paddle", paddle="red"),
          dn=dict(face="happy", look=(-1, 0)), cl=dict(face="confident"), sf=dict(face="charm"), extra=ex)


def f_1_1b(k):                                             # BONK: on his bald head
    def ex(k, o):
        c = k.c
        bare_nail(c)
        hx, hy = o["don"]["head"]
        fs.portrait(k, hx + 22, hy - 118, ang=0.62)
        lines(c, hx, hy - 60, 7, 40, 60, 190, 350)
        stars(c, hx, hy - 40, 52)
    scene(k, screen="red", portrait=None, rb=dict(arm="paddle", paddle="red"),
          dn=dict(feet=F + 34, face="panic", look=(0, -1)), cl=dict(face="shock"), sf=dict(face="freeze"), extra=ex)


kit.ARM_POSES["_flirt"] = (-150, 150, 30, -100)          # a hand at her earring, the other on her hip


def f_1_2(k):                                              # he hangs it back; she flirts; the Client looks past her
    scene(k, cam=(220, 560, 1.7), door=0.85, cl=dict(x=125, pose="arrive", face="confident", look=(1, -0.5)),
          dn=dict(pose="hang", face="pleased", look=(0, -1)), rb=False,
          sf=dict(x=205, pose="_flirt", face="charm", look=(-1, -0.1), lag=(3, 0)))


def f_1_3(k):                                              # FRI · BANK
    def ex(k, o):
        hx, hy = o["client"]["hands"][1]
        fs.phone2(k, hx + 6, hy - 40, 0.42, "cal")
    scene(k, cam=(220, 600, 2.0), cl=dict(x=205, pose="open", face="plain", look=(1, 0)),
          dn=dict(face="smug", look=(-1, 0)), rb=False, sf=False, extra=ex)


def f_2_1(k):                                              # BANK, and his eyes come up shining
    scene(k, cam=(292, 600, 3.2), dn=dict(face="happy", look=(-0.8, -0.6)), cl=False, rb=False, sf=False, pm=False, mm=False)
    fs.phone2(k, 120, 820, 1.25, "cal")


def f_2_2(k):                                              # the tablet turned to him
    def ex(k, o):
        hx, hy = o["don"]["hands"][0]
        fs.tablet_upgrade(k, hx - 14, hy - 30, 0.55)
    scene(k, cam=(220, 600, 1.9), cl=dict(x=150, pose="stand", face="relief", look=(1, 0)),
          dn=dict(pose="tablet", face="smug", look=(-0.6, 0.5)), sf=dict(pose="stand", face="fake", look=(-1, 0)), rb=False, extra=ex)


def f_2_3(k):                                              # thumb 1: oily
    bg(k.c, (0.93, 0.92, 0.89))
    fs.tablet_upgrade(k, 270, 470, 3.0)
    thumb(k, 270, 560, 1.4, SKIN_CL, oil=True, ang=-0.2)


def f_3_1(k):                                              # the second zero: he ducks, it holds (medium)
    def ex(k, o):
        c = k.c
        px, py = fs.PORTRAIT
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
        for r_ in (70, 86):
            c.arc(px, py - 70, r_, math.pi * 0.30, math.pi * 0.70); c.stroke()
    scene(k, cam=(285, 560, 1.9), screen="red", portrait=dict(ang=fs.CROOK + 0.26), rb=False, cl=False,
          dn=dict(feet=F + 60, pose="panic", face="panic", look=(0, -1)), sf=dict(face="drop", look=(1, -0.6)), extra=ex)


def f_3_2(k):                                              # PREMIUM · PAID, and up at Don
    scene(k, cam=(92, 560, 3.0), cl=dict(face="suspicious", look=(1.2, -0.2)), rb=False, sf=False, dn=False, pm=False, mm=False)
    fs.phone2(k, 400, 800, 1.25, "paid_price")


def f_3_3(k):                                              # "It's the red. It looks bad."
    scene(k, cam=(262, 590, 2.3), sf=dict(face="drop", look=(1.2, 0)), dn=dict(face="confused", look=(-1, -0.4)), cl=False,
          rb=False)


def f_3_4(k):                                              # the patch
    bg(k.c)
    fs.portrait(k, 270, 420, 4.0, ang=fs.CROOK, patch=True)
    c = k.c
    cut(k, [(560, 760), (560, 980), (420, 980), (330, 420), (380, 400)], sfs.FUCHSIA, shadow=False, lw=2.6)   # her sleeve
    cut(k, [(330, 420), (380, 400), (392, 430), (346, 446)], sfs.SLEEVE_CUFF, shadow=False, lw=2)
    ellipse(k, 330, 400, 34, 30, sfs.SKIN, 4, shadow=False, lw=2.4)
    for i in range(4):
        ellipse(k, 296 + i * 12, 384, 7, 12, sfs.RED, 5 + i, shadow=False, lw=1.4)                       # the nails


def f_4_1(k):                                              # "Can you make the zero green?"
    scene(k, cam=(240, 600, 2.0), dn=dict(face="happy", look=(-1, -0.2), pose="reach"), sf=dict(face="charm"), cl=False)


def f_4_2(k):                                              # the robot, dead centre
    bg(k.c)
    c = k.c
    c.save(); view(c, P["robot"][0] - 8, 690, 4.2)
    st.stage(k, open_=0.85, decor=False)
    robot(k, P["robot"][0], P["robot"][1], P["robot"][2], "eager", arm="none")
    c.restore()


def f_4_3(k):                                              # thumb 2: APPROVED
    bg(k.c, (0.93, 0.92, 0.89))
    rect(k, 80, 380, 380, 200, (0.15, 0.17, 0.22), 1, lw=3)
    c = k.c
    c.set_source_rgb(*fs.GRN); c.rectangle(110, 410, 320, 140); c.fill()
    fs._text(c, "APPROVED", 270, 500, 52)
    thumb(k, 300, 560, 1.4, SKIN_DON, ang=0.15)


def f_4_4(k):                                              # thumb 3: the tape
    bg(k.c, st.DESK)
    fs.plan_taped(k, 270, 470, 3.4)
    c = k.c
    c.set_source_rgba(0.97, 0.97, 0.90, 0.7); c.rectangle(210, 300, 60, 340); c.fill()
    thumb(k, 236, 560, 1.4, (0.94, 0.80, 0.68), nail=False, ang=-0.1)


def f_4_5(k):                                              # the sweep
    bg(k.c)
    fs.screen(k, "wipe0.60", 40, 300, 460, 290, cursor=False)
    st.paddle(k, 430, 820, 1.6, ok=True)


def f_4_6(k):                                              # the photo
    def ex(k, o):
        c = k.c
        sx_, sy_ = o["robot"]["screen"]
        rect(k, sx_ - 16, sy_ - 12, 32, 24, (0.15, 0.15, 0.18), 9, shadow=False, lw=1.6)              # its face: a camera
        c.set_source_rgb(0.8, 0.9, 1.0); c.arc(sx_, sy_, 8, 0, 6.3); c.fill()
        c.set_source_rgba(1, 1, 1, 0.85)
        for a in range(0, 360, 30):
            r_ = 70 if a % 60 == 0 else 46
            c.move_to(sx_, sy_); c.line_to(sx_ + r_ * math.cos(math.radians(a)), sy_ + r_ * math.sin(math.radians(a)))
        c.set_line_width(5); c.stroke()
    scene(k, cam=(170, 560, 1.45), screen="green", rb=dict(x=200, feet=F + 70, arm="none"), dn=dict(x=150, pose="thumb", face="grin", look=(1, 0)),
          sf=False, cl=False, extra=ex)


def f_4_7(k):                                              # the post, Pam's comment
    bg(k.c, (0.86, 0.84, 0.80))
    fs.phone2(k, 270, 470, 3.0, "post")
    thumb(k, 420, 760, 1.3, SKIN_CL, oil=True, ang=0.5)


def f_5_1(k):                                              # he looks for his plan in the green zero: nothing
    scene(k, cam=(185, 540, 1.6), screen="green", cl=dict(x=120, pose="stand", face="puzzled", look=(-1, -1)),
          sf=dict(x=230, face="drop", look=(-1, 0)), dn=dict(x=300, feet=F + 40, s=0.82, face="grin", look=(-1, -0.2)), rb=False)


def f_5_2(k):                                              # "Where's my blueprint?" from above
    def ex(k, o):
        pass
    c = k.c
    bg(c)
    c.save(); view(c, 250, 560, 2.0)
    st.stage(k, open_=0.85, decor=False)
    fs.portrait(k, 222, 330, 1.05)
    client(k, 196, F + 130, 1.05, "open", "suspicious", (1.2, 0.6))
    don(k, 330, F + 90, 0.72, "stand", "smug", (-1, -1))
    c.restore()


def f_5_3(k):                                              # "The zero's green."; the paddle agrees; the tablet goes;
    def back(k):                                           # Pam, behind the counter, holds the real answer up high:
        px, pf, ps = P["pam"]                              # his thumb, in front, blocks it
        ac.pam(k, px, pf, ps, "stand", look=(-1, -0.6), hands=((-62, -330), (-2, -330)))
        fs.plan_taped(k, px - 18, pf - 196, 0.5)
    scene(k, cam=(250, 600, 2.0), screen="green", rb=dict(x=150, arm="paddle", paddle="green"), pm=False, back=back, counter_plan=False,
          sf=dict(x=232, face="contempt", look=(1, 0), slide=0.6, pose="stand"), dn=dict(pose="thumb", face="smug", look=(-1, 0.2)), cl=False)


def f_6_1(k):                                              # Mom: who she is (close, the baby photo large)
    def ex(k, o):
        fs.baby_photo(k, 398, F - 192, 1.05, 701)
    scene(k, cam=(440, 630, 3.4), mm=dict(face="sweet", look=(-1.2, 0.2)), pm=False, cl=False, rb=False, sf=False, dn=False,
          extra=ex)


def f_6_2(k):                                              # two men step back; the collar
    def ex(k, o):
        hx, hy = o["don"]["head"]
        mom_bc.mom(k, hx + 64, F + 16, 0.62, "thread", "sweet", look=(-1, -0.4))                         # out from the counter
    scene(k, cam=(230, 600, 1.8), cl=dict(x=96, face="dawning", look=(1, 0)), dn=dict(x=262, face="pleased", look=(0.6, 1.2)),
          sf=dict(x=206, face="resigned"), rb=False, mm=False, extra=ex)


def f_7_1(k):                                              # he goes; Pam brings the plan
    def ex(k, o):
        ac.pam(k, 360, F + 10, 0.66, "stand", look=(-1, -0.3))                                             # out from the counter
        fs.plan_taped(k, 346, F - 116, 0.72)
    scene(k, cl=dict(x=110, pose="arrive", face="plain", look=(-1, 0)), sf=dict(face="charm", look=(1, 0)),
          dn=dict(face="happy", look=(-1, 0)), pm=False, extra=ex)


def f_7_2(k):                                              # the near-shred: the end in the slot, Pam pulls it back
    PURPLE = (0.40, 0.26, 0.55)

    def ex(k, o):
        c = k.c
        c.save(); c.translate(214, F - 150); c.rotate(-0.06)
        fs.plan_taped(k, 0, 0, 0.62)                                                 # its lower end goes in...
        c.restore()
        ac.shredder(k, 214, F, 1.25, fill=0.0)                                       # ...behind the shredder's top
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
        for dx in (-30, 0, 30):
            c.move_to(214 + dx, F - 222); c.line_to(214 + dx, F - 196); c.stroke()     # pushed down
        ac.pam(k, 352, F + 10, 0.72, "stand", look=(-1.6, -0.6))
        cut(k, [(326, F - 128), (334, F - 112), (256, F - 162), (250, F - 176)], PURPLE, shadow=False, lw=2)  # her arm
        ellipse(k, 248, F - 172, 10, 10, (0.94, 0.80, 0.68), 9, shadow=False, lw=2)                          # on the corner
        for dy in (-16, 0, 16):
            c.move_to(270, F - 200 + dy); c.line_to(300, F - 200 + dy); c.stroke()                            # pulling back
    scene(k, cam=(250, 620, 2.0), dn=dict(x=150, pose="swing", face="happy", look=(-1.6, -0.4)),
          pm=False, sf=False, cl=False, rb=False, mm=False, extra=ex)


def f_8_1(k):                                              # 100% COMPLETE, in the doorway
    scene(k, cam=(100, 560, 3.0), cl=dict(face="suspicious", look=(-0.2, 1.2)), rb=False, sf=False, dn=False, pm=False, mm=False)
    fs.phone2(k, 380, 780, 1.25, "complete")


def f_8_2(k):                                              # RETRY UNTIL FRIDAY
    bg(k.c)
    fs.screen(k, "retry", 40, 260, 460, 290, cursor=False)
    c = k.c
    c.save(); view(c, P["robot"][0], 600, 2.6)
    robot(k, P["robot"][0], P["robot"][1], P["robot"][2], "eager", arm="remote")
    c.restore()


def f_9_3(k):                                              # the plaster drops; the glass is whole; nobody notices
    bg(k.c)
    fs.portrait(k, 270, 420, 4.0, ang=fs.CROOK, crack=False, patch=False)
    c = k.c
    fs.plaster(c, 250, 800, 4.0 * 0.82, ang=0.55)
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
    for dx in (-70, 0, 70):                                                            # falling
        c.move_to(250 + dx, 640); c.line_to(250 + dx, 690); c.stroke()


def f_8_3(k):                                              # frame 0
    c = k.c
    c.save(); fs.cam2(c); fs.master(k); c.restore()


TAKES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fs_voices/film/takes.json")))
SHOTS = [  # shot, length (s), drawing, the line (or the beat): script v6's order
    ("1.1a", 1.0, f_1_1a, "0.7 s: red, the buzz; it jumps off the nail"), ("1.1b", 1.0, f_1_1b, "1.25 s: BONK, on his head"),
    ("1.2", 1.0, f_1_2, "she flirts; he looks past her. CLIENT: \"Friday, the bank. I need my blueprint.\""),
    ("1.3", 2.0, f_1_3, "(his line ends) FRIDAY · BANK MEETING"), ("2.1", 0.5, f_2_1, "the calendar; his eyes light up"),
    ("2.2", 2.9, f_2_2, "DON: \"Garage eleven. Guaranteed by Friday.\""), ("2.3", 0.5, f_2_3, "thumb 1, oily: ka-ching"),
    ("3.1", 1.6, f_3_1, "red again; he ducks; it holds"), ("3.2", 0.9, f_3_2, "PREMIUM · PAID $999; up at Don"),
    ("3.3", 1.4, f_3_3, "SOFÍA: \"It found nothing.\""), ("3.4", 0.9, f_3_4, "the plaster on his face"),
    ("4.1", 1.8, f_4_1, "DON: \"Can you make the zero green?\""), ("4.2", 2.4, f_4_2, "ROBOT: \"Interface change. Human approval required.\""),
    ("4.3", 0.8, f_4_3, "DON: \"Approved.\" thumb 2"), ("4.4", 0.4, f_4_4, "thumb 3: Pam's tape"),
    ("4.5", 1.0, f_4_5, "the sweep to green; the chime"),
    ("5.1", 2.0, f_5_1, "he finds nothing; her smile drops; he beams"), ("5.2", 1.6, f_5_2, "CLIENT: \"Where's my blueprint?\""),
    ("5.3", 1.7, f_5_3, "DON: \"The zero's green.\" Pam's plan up; his thumb blocks it"),
    ("6.1", 0.7, f_4_6, "the photo: flash"), ("6.2", 1.5, f_4_7, "the post he is tagged in; Pam's comment"),
    ("7.1", 1.2, f_6_1, "MOM: \"Young man.\""), ("7.2", 1.5, f_6_2, "two men step back; the collar"),
    ("8.1", 1.0, f_7_1, "he goes; Pam brings the plan"), ("8.2", 1.1, f_7_2, "the near-shred; pulled back"),
    ("9.1", 1.2, f_8_1, "100% COMPLETE stops him"), ("9.2", 2.0, f_8_2, "RETRY UNTIL FRIDAY"),
    ("9.3", 0.9, f_9_3, "the plaster drops: healed; nobody notices"), ("9.4", 1.4, f_8_3, "= frame 0: the loop"),
]


def _pstate(shot):
    order = [x[0] for x in SHOTS]
    i = order.index(shot)
    if i < order.index("1.1b") or i >= order.index("9.3"):
        return "clean"
    return "crack" if i < order.index("3.4") else "patch"


def _with_state(shot, fn):
    def f(k):
        fs.PSTATE[0] = _pstate(shot)
        try:
            fn(k)
        finally:
            fs.PSTATE[0] = None
    return f


SHOTS = [(sh, ln, _with_state(sh, fn), note) for sh, ln, fn, note in SHOTS]


def frames(d):
    os.makedirs(d, exist_ok=True)
    out = []
    for shot, ln, fn, _ in SHOTS:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        c = cairo.Context(s); k = Ctx(c, 0)
        bg(c)
        fn(k)
        p = "%s/fs_board_%s.png" % (d, shot)
        s.write_to_png(p)
        out.append((shot, s))
    return dict(out)


def sheet(out, surfs, mute=False):
    cols, tw = 7, 150
    th = tw * 960 / 540.0
    W2 = 24 * 2 + cols * (tw + 8)
    rows = (len(SHOTS) + cols - 1) // cols
    cap = 22 if mute else 44
    H2 = 84 + rows * (th + cap + 10) + 10
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W2 * 2), int(H2 * 2))
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "FIRST SEARCH" if not mute else "Frames, in order", 68, 44, 24, bold=True)
    if not mute:
        corp(c, "storyboard " + V + "  ·  script v6  ·  set v2  ·  Sofía v2  ·  timed from the takes", 280, 44, 11, col=(0.35, 0.40, 0.50))
    t = 0.0
    for i, (shot, ln, fn, line) in enumerate(SHOTS):
        x = 24 + (i % cols) * (tw + 8); y = 72 + (i // cols) * (th + cap + 10)
        c.save(); c.translate(x, y); c.scale(tw / 540.0, tw / 540.0); c.set_source_surface(surfs[shot], 0, 0); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.0); c.rectangle(x, y, tw, th); c.stroke()
        if mute:
            corp(c, "#%d" % (i + 1), x, y + th + 13, 9.4, bold=True)
        else:
            corp(c, "%s  ·  %.1f s" % (shot, t), x, y + th + 13, 9.4, bold=True)
            wrap(c, line, x, y + th + 25, 7.6, tw, col=(0.35, 0.40, 0.50))
        t += ln
    if not mute:
        corp(c, "%.1f s in all" % t, W2 - 120, 44, 11, bold=True)
    surf.write_to_png(out)


def main(d):
    fs.LAYOUT[0] = "v2"; fs.REMOTE_BIG[0] = True; fs.BABY_DON[0] = True
    try:
        surfs = frames(os.path.join(d, "fs_board"))
        sheet(os.path.join(d, "fs_storyboard_%s.png" % V), surfs)
        sheet(os.path.join(d, "fs_storyboard_%s_mute.png" % V), surfs, mute=True)
    finally:
        fs.LAYOUT[0] = "v1"; fs.REMOTE_BIG[0] = False; fs.BABY_DON[0] = False


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
    print("wrote")
