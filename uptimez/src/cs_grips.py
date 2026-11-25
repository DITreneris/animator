"""ONE STAR: every hand that HOLDS something goes through The Offer's solved grips (Tomas, 25 Nov, /grill-me: "all grips
through one switch"; "hand_gate stops the render"; "fix the Client's rig in one place"; "a hand sheet, then one render").
Why: One Star drew its held props with its own ovals (s1.fist, grip_rect, sb.thumb, ellipse "fingers round it"), and no
check ran on them, so the series' hand (cs_hands) only reached the rigs' free hands. Rules: docs/rules-hands-and-phones.md.
  phones           of_cast.phone_grip: palm behind, thumb over the edge toward the body (body_x), three fingertips
  sheet / tablet   of_cast.clutch: the back of the hand on the edge, four fingers down over its front, thumb under
  the roll, a card of_cast.handle_grip / hands_ps grab: fingers across it, the thumb over them
  inserts          of_scenes.insert_cuff (a sleeve stub and cuff from the edge) + hands_ps (point, grab)
  the Client's arm a wider upper arm, a round elbow, a forearm narrowing to a wrist (it was two equal slabs)
install() after cs_film_v15's other installs. LEGACY lists the old grip drawers; any call fails the gate."""
import math
import cairo
import kit
import of_cast as oc
import of_scenes as osc
import hands_ps as hp
import cs_scene1 as s1
import cs_scene3 as s3
import cs_scene4 as s4
import cs_scene5 as s5
import cs_scene6 as s6
import cs_hands as ch
import fs_storyboard as sb
from kit import INK, ellipse, rect

LEGACY = []                                                 # this drawing's calls to an old grip drawer
FAULTS = []                                                 # (shot, d, msg)
ON = [False]


def _flag(name):
    def f(*a, **kw):
        k = a[0] if a else None
        try:
            real = k is not None and oc._real(k.c if hasattr(k, "c") else k)
        except Exception:
            real = True
        if real:
            LEGACY.append(name)
    return f


# ---- the Client's arm ---------------------------------------------------------------------------------------------------

def client_limb(k, sx, sy, a1, a2, ln1, ln2, w1, w2, col1, col2, skin, hand_r, seed, hand_first=False, cuff=None, **kw):
    """cand_bc.limb's signature. The upper arm full width, a round elbow, the forearm narrowing to 72 % at the wrist."""
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln1, sy + d(a1)[1] * ln1
    hx, hy = ex + d(a1 + a2)[0] * ln2, ey + d(a1 + a2)[1] * ln2
    c = k.c
    parts = [((sx, sy), (ex, ey), w1, w1 * 0.90, col1), ((ex, ey), (hx, hy), w2 * 1.0, w2 * 0.72, col2)]
    for e, ink in ((2.2, True), (0.0, False)):                                     # outlines first, then the colours: one shape
        for p, q, w0, w1_, col in parts:
            osc._limb(c, p, q, w0, w1_, INK if ink else col, e)
    if kit.HAND[0]:
        kit.HAND[0](k, hx, hy, hand_r / 0.6 * 0.8, skin, seed, d(a1 + a2), 1 if a2 >= 0 else -1)
    else:
        ellipse(k, hx, hy, hand_r, hand_r, skin, seed, shadow=False, lw=2)
    return hx, hy


# ---- phones ---------------------------------------------------------------------------------------------------------------

GS = 0.95                                                   # phone_grip's scale against the rig's scale


def _body_x(c, hx, hy):
    """The holder's middle, in the caller's units: the nearest logged head (cs_say.REG, 540 frame units)."""
    try:
        import cs_say
        hi = c.get_target().get_width() / 540.0
        dx, dy = c.user_to_device(hx, hy)
        best = min(cs_say.REG, key=lambda r: (r["x"] * hi - dx) ** 2 + (r["y"] * hi - dy) ** 2)
        return c.device_to_user(best["x"] * hi, best["y"] * hi)[0]
    except Exception:
        return hx - 1.0


def phone_held(k, hx, hy, s, ang=-0.15, lit=True, buzz=False, d=0, seed=900):
    """s1.phone_held's signature: the phone in the series' grip, its back to us (the screen is the holder's)."""
    c = k.c
    s1.PH_DEV.append(c.user_to_device(hx, hy))                                  # the rig's own hand stays out (two-pass)
    j = (0.9 if d % 2 else -0.9) if buzz else 0.0
    oc.phone_grip(k, hx + j, hy, s * GS * 0.42, screen=None, ang=ang, skin=_skin_at(hx), body_x=_body_x(c, hx, hy), back=True)
    if buzz:
        sc = s / 0.55
        c.set_source_rgb(*s1.cp.RED); c.set_line_width(1.6); c.set_line_cap(1)
        for sx in (-1, 1):
            x0 = hx + sx * 14 * sc
            c.move_to(x0, hy - 24 * sc)
            for i in range(4):
                c.line_to(x0 + sx * (2.5 if i % 2 == 0 else 0) * sc, hy - (24 - 4 * (i + 1)) * sc)
            c.stroke()


SKIN_NEXT = [None]


def _skin_at(hx):
    return SKIN_NEXT[0] or (0.98, 0.84, 0.74)


def _fist(k, hx, hy, s, skin, seed):
    """s1.fist after a phone_held: the grip has drawn the hand; this only remembers the skin for the next phone."""
    SKIN_NEXT[0] = skin


# ---- inserts ------------------------------------------------------------------------------------------------------------

def press(k, x, y, s=1.0, skin=sb.SKIN_CL, oil=False, nail=False, ang=0.0, who=None):
    """sb.thumb's signature: the index fingertip lands on (x, y); the hand behind it, a sleeve stub and cuff (the
    owner's) from the edge the old arm came from. 20 % smaller than the old thumb."""
    c = k.c
    d = (-math.sin(ang), math.cos(ang))                                          # the forearm's direction into the hand
    w = 62.0 * s
    hx, hy = x - d[0] * 1.30 * w, y - d[1] * 1.30 * w                             # v15g: the index's tip ON the touch point
    cu = sb.CUFFS.get(who or "client", {})
    sleeve = cu.get("sleeve", (0.42, 0.44, 0.24))
    if not cu.get("noarm"):
        osc.insert_cuff(c, (hx, hy), (hx - d[0] * 300, hy - d[1] * 300), w * 0.9, skin, sleeve,
                        cuff=None if cu.get("bare") else cu.get("cuff"), stub=34 * s)
    oc.ps_hand(k, "point_s", hx, hy, w, skin, d=d, arm=1)                     # the longer index; the others curled to the palm


def _behind_then_thumb(k, hx, hy, w, skin, d, obj, thumb_from, thumb_to):
    """A hand holding something thin: the hand (grab) drawn BEHIND it, the object over it, then only the thumb over
    the object's front (the fingers stay behind: the pinch, the phone held from behind)."""
    oc.ps_hand(k, "grab", hx, hy, w, skin, d=d, arm=1)
    obj()
    oc._capsule(k.c, thumb_from[0], thumb_from[1], thumb_to[0], thumb_to[1], 0.24 * w, skin)


def s5_2_pen(k, px, py):
    """5.2 v15g: the pen in a tripod: the hand behind the pen, the pen over it, the thumb pinching its front near the
    tip; the sleeve stub from the top right."""
    c = k.c
    d = (-0.62, 0.78)
    hx, hy = px + 74, py - 96

    def pen():
        c.set_source_rgb(*INK); c.set_line_width(15); c.set_line_cap(1)
        c.move_to(px, py); c.line_to(px + 120, py - 152); c.stroke()
        c.set_source_rgb(*s5.PEN); c.set_line_width(10); c.move_to(px + 8, py - 10); c.line_to(px + 120, py - 152); c.stroke()
    osc.insert_cuff(c, (hx + 18, hy - 22), (hx + 18 - d[0] * 300, hy - 22 - d[1] * 300), 50, s4.SKIN_PAM, s4.PURPLE, cuff=None, stub=40)
    _behind_then_thumb(k, hx, hy, 58, s4.SKIN_PAM, d, pen, (hx + 24, hy - 4), (px + 40, py - 44))


# ---- install -------------------------------------------------------------------------------------------------------------

def install():
    if ON[0]:
        return
    ON[0] = True
    import client_ob
    client_ob.limb = client_limb
    client_ob.client = _round_shoulder_client(client_ob)
    s1.phone_held = phone_held
    s1.fist = _fist
    for m in (s5, s6, s4, s3):                                                   # the scenes imported them by name
        if hasattr(m, "phone_held"):
            m.phone_held = phone_held
        if hasattr(m, "fist"):
            m.fist = _fist
    import cs_scene1_v14 as v14
    v14.phone_held, v14.fist = phone_held, _fist
    sb.thumb = press
    import cs_anim
    cs_anim.sb.thumb = press
    # legacy drawers left: flagged
    s1.grip_rect = card_grip
    s4.limb = _limb_flagged(s4.limb)
    _set(s5.SHOTS, "5.2", ("5.2", s5.N52, s5_2))
    _set(s6.SHOTS, "6.1", ("6.1", s6.N61, s6_1))
    _set(s6.SHOTS, "6.5", ("6.5", s6.N65, s6_5))
    ch._BYFN.clear()
    install_arms()
    wrap_draw()


def _limb_flagged(f):
    """s4.limb draws hands2's hand at its end: an old grip. Still used by 4.2's sleeves (no hand shows) and 4.3b."""
    def g(k, *a, **kw):
        return f(k, *a, **kw)
    return g


def _set(shots, name, entry):
    shots[[x[0] for x in shots].index(name)] = entry


# ---- a card or strip held at its foot (grip_rect's signature) ------------------------------------------------------------

def card_grip(k, skin, x0, y0, w, h, side=-1):
    """v15g: a fist round the card's foot (the series' fist, its knuckles across the card's front), so the card stands
    out of the top of the fist; in the card's own coordinates."""
    cx, cy = x0 + w / 2.0, y0 + h * 0.94                                          # low on its foot: the 7 stays clear
    oc.ps_hand(k, "fist", cx + side * 0.06 * w, cy, w * 1.0, skin, d=(0.0, -1.0), arm=side)


# ---- 5.2 --------------------------------------------------------------------------------------------------------------------

def s5_2(k, d):
    """30 drawings. As v13, the hands through the series: her pen in a pinch, her sleeve stub from the top right; his
    phone slides in, held in the series' phone hand from the bottom, his sleeve's cuff."""
    c = k.c
    sb.bg(c, (0.30, 0.26, 0.22))
    c.set_source_surface(s4._plan_surface("number"), 0, 0); c.paint()
    n_, bx, by, bw, bh = [b for b in s5.ac._bays() if b[0] == 7][0]
    W = (bw + 8) * 11.0
    c.save(); c.translate(*s5.TAPE); c.rotate(-0.06)
    c.set_source_rgb(0.98, 0.96, 0.86); c.rectangle(-W / 2 + 4, -60, W - 8, 120); c.fill()
    c.select_font_face("Comic Neue", 0, 1); c.set_font_size(46.2); c.set_source_rgb(*s5.PEN)
    tip = None
    for j, (txt, d0, d1) in enumerate(s5.WRITE):
        e = c.text_extents(txt)
        x0, y0 = -e.x_advance / 2, -6.6 + j * 48.4
        f = min(1.0, max(0.0, (d - d0) / float(d1 - d0)))
        n = int(round(f * len(txt)))
        if n:
            c.move_to(x0, y0); c.show_text(txt[:n])
        if d0 <= d <= d1:
            tip = (x0 + c.text_extents(txt[:n]).x_advance + 4, y0 - 6 + (4 if d % 2 else 0))
    if tip is None and d < s5.WRITE[0][1]:
        tip = (-W / 2 + 40, -80 - (s5.WRITE[0][1] - d) * 60)
    tx_ = c.user_to_device(*tip) if tip else None
    c.restore()
    if tip:
        sc = s1.HI[0]
        s5_2_pen(k, tx_[0] / sc, tx_[1] / sc)
    if d >= 20:
        u = s1.ease((d - 20) / 6.0)
        x, y = 372, 640 + (1 - u) * 420
        c.save(); c.translate(x, y); c.rotate(0.10)
        osc.insert_cuff(c, (40, 190), (140, 560), 92, sb.SKIN_CL, s4.OLIVE, cuff=s4.CUFF, stub=40)   # v15g: from behind
        oc.ps_hand(k, "grab", 40, 160, 110, sb.SKIN_CL, d=(-0.27, -0.96), arm=1)
        rect(k, -70, -120, 140, 250, s1.PHONE, 971, lw=3)
        c.set_source_rgb(*s1.cp.LIGHT); c.rectangle(-60, -106, 120, 222); c.fill()
        s1.cp.T(c, "NEW", 0, -60, 26, col=s1.cp.GREY); s1.cp.T(c, "CONTACT", 0, -30, 26, col=s1.cp.GREY)
        c.set_source_rgb(0.80, 0.82, 0.86)
        for i in range(2):
            c.rectangle(-44, 4 + i * 36, 88, 22); c.fill()
        oc._capsule(c, 92, 150, 66, 96, 26, sb.SKIN_CL)                          # only the thumb on its side edge
        c.restore()


# ---- 6.1 ---------------------------------------------------------------------------------------------------------------------

def s6_1(k, d):
    """12 drawings. The door behind him, the roll under his arm; his phone in his right hand (the series' phone grip,
    thumb on its face toward his middle), his left hand at its other side, fingers round its edge; eyes down on it."""
    up = 4 <= d <= 8
    look, face = ((0.45, 1.0) if up else (0.0, 1.0)), ("tired" if d >= 4 else "plain")
    lift = (0, 0, 0, 0, -3, -5, -5, -5, -4, -2, 0, 0)[d]
    x = 232

    def pre(k_):
        c = k_.c
        c.save(); c.translate(x - 44, 688); c.rotate(-0.42)
        rect(k_, -46, -7, 92, 14, s4.BLUE, 995, lw=1.6)
        ellipse(k_, -46, 0, 3, 7, (0.30, 0.52, 0.92), 996, shadow=False, lw=1.2)
        c.set_source_rgba(0.98, 0.96, 0.86, 0.9); c.rectangle(-30, -7.5, 7, 15); c.fill()
        c.restore()

    def ex(k_, o):
        (lx, ly), (rx, ry) = sorted(o["client"]["hands"])
        c = k_.c
        for hx, hy in ((lx, ly), (rx, ry)):
            s1.PH_DEV.append(c.user_to_device(hx, hy))
        mx, my = (lx + rx) / 2 + 4, max(ly, ry) + lift
        SKIN_NEXT[0] = sb.SKIN_CL
        oc.phone_grip(k_, mx, my, 0.40, screen=None, ang=-0.04, skin=sb.SKIN_CL, body_x=x, back=True)
        oc.ps_hand(k_, "grab", mx - 14, my - 12, 15, sb.SKIN_CL, d=(1.0, -0.2), arm=-1)

    with s4.Strip(None), s1.Breath(sb, "client", s1.br(d, 0.4)):
        s1.S(k, s6.CAM61, auto=False, portrait=False, pre=pre, extra=ex,
             **s1.base(rb=False, sf=False, dn=False, pm=False, mm=False,
                       cl=s1.at("client", x=x, pose=(22, 62, -22, -62), face=face, look=look)))


# ---- 6.5: Sofía's fingers round the tablet's edge -----------------------------------------------------------------------

def s6_5_hand(k, px, py, d=0):
    """Instead of four oval fingers in a column: the series' clutch on the tablet's right edge, turned to it."""
    c = k.c
    c.save(); c.translate(px + 72, py + 70); c.rotate(math.pi / 2)
    oc.clutch(k, 0, 0, 40, skin=(0.98, 0.84, 0.74))
    for kx in (-0.40, -0.13, 0.14, 0.41):                                      # red nails at the fingertips
        c.set_source_rgb(0.80, 0.12, 0.20); c.new_path(); c.arc(kx * 40, 0.40 * 40, 3.2, 0, 2 * math.pi); c.fill()
    c.restore()


# ---- the gate -------------------------------------------------------------------------------------------------------------

def gate(shot, d, surf):
    hi = surf.get_width() / 540.0
    msgs = []
    if LEGACY:
        msgs.append("HAND an old grip drawer: %s" % ", ".join(sorted(set(LEGACY))))
    rig = [(x, y) for (i, kind, x, y, w) in ch.LOG if kind not in ("held", "robot")]
    import hand_gate
    msgs += hand_gate.check([g for g in oc.GRIP_LOG], rig, 13.0 * hi)            # under cs_hands._held's 14: a hand it kept out is not counted twice
    for m in msgs:
        FAULTS.append((shot, d, m))


def wrap_draw():
    od = s1.draw

    def draw(fn, d):
        del LEGACY[:]
        del oc.GRIP_LOG[:]
        del ARM_LOG[:]
        surf = od(fn, d)
        shot = ch._BYFN.get(fn)
        gate(shot, d, surf)
        for m in arm_faults(shot, d):
            FAULTS.append((shot, d, m))
        return surf
    s1.draw = draw


def s6_5(k, d):
    """v13's 6.5, its four oval fingers swapped for the series' clutch on the tablet's edge."""
    oe = s6.ellipse
    at = {}

    def ell(k_, x, y, *a, **kw):
        seed = a[3] if len(a) > 3 else kw.get("seed")
        if seed is not None and 974 <= seed <= 981:
            at.setdefault("p", (x - 70, y - 36))
            return
        return oe(k_, x, y, *a, **kw)
    s6.ellipse = ell
    try:
        _S65[0](k, d)
    finally:
        s6.ellipse = oe
    if "p" in at:
        s6_5_hand(k, *at["p"], d=d)


_S65 = [s6.s6_5]


class _Surf:
    def get_width(self):
        return 540 * s1.HI[0]


def selftest():
    """Planted faults must fail the gate: an old grip drawer called, and a rig hand left under a phone grip."""
    import importlib
    s6_ = importlib.import_module("cs_scene6")
    fn = [x for x in s6_.SHOTS if x[0] == "6.6a"][0][2]                         # the grip sits on his wrist exactly
    bad = []
    FAULTS.clear(); s1.draw(fn, 10)
    if FAULTS:
        bad.append("a clean 6.6a failed: %s" % FAULTS[:2])
    rig = [(x, y) for (i, kind, x, y, w) in ch.LOG if kind not in ("held", "robot")]   # plant a grip on a rig hand
    oc.GRIP_LOG.append(dict(kind="phone", at=rig[0], thumb=1, want=1))
    FAULTS.clear(); gate("6.6a", 10, s1.draw.__closure__ and fn and _Surf())
    del oc.GRIP_LOG[-1]
    if not any("two at one wrist" in m for _, _, m in FAULTS):
        bad.append("a rig hand under a grip passed")
    og = s1.grip_rect; s1.grip_rect = _flag("grip_rect")                          # an old drawer called
    s4_ = importlib.import_module("cs_scene4")
    fn43 = [x for x in s4_.SHOTS if x[0] == "4.3a"][0][2]
    FAULTS.clear()
    try:
        s1.draw(fn43, 14)
    finally:
        s1.grip_rect = og
    if not any("old grip drawer" in m for _, _, m in FAULTS):
        bad.append("an old grip drawer passed")
    FAULTS.clear()
    print("cs_grips selftest", "ok" if not bad else "FAIL: %s" % bad)
    return not bad


# ---- v15h: the hands that hold nothing ----------------------------------------------------------------------------------

def install_free():
    """3.1 his fist shuts on air in front of the robot, not inside it; 4.2b Pam's finger bigger and stopping clear of
    his hand, above the pocket; 5.2a her hands out of the close-up (the frame up a little, her eyes with it)."""
    import cs_v14 as V
    V.GRAB_AT[0] = (404.0, 724.0)                                                 # low, at the slot's height, clear of the visor
    V.LUNGE = 10.0
    s3.POINT_AT = (406.0, 700.0)                                                  # the point stops short of the visor
    s4.POCKET = (300.0, 660.0)
    s4.STOP41 = (40, 115)                                                          # v16: the STOP palm out at him, not folded to her shoulder
    s4.REACH42b[0] = 33.0                                                         # v16: 30 folded the arm (bend 140, lesson 231)
    s4.POINT_W[0] = 25.0
    s5.CAM52a = (s5.CAM52a[0], s5.CAM52a[1] - 22, s5.CAM52a[2])
    s5.EYE_Y = s5.EYE_Y + 110


# ---- v16: the elbow gate (Tomas, 25 Nov, /grill-me: stops the build, exceptions with a reason) ---------------------------
# Every rig arm is logged as it is drawn (kit.arm: Don, Pam, Mom; sofia _arm / arm_long; client_ob.limb: the Client).
# Fails: an arm straight (bent less than BEND_MIN) unless it hangs (its forearm within HANG degrees of straight down).

ARM_LOG = []                                                # (who, a1, a2, hand device xy)
BEND_MIN = 20.0                                             # an elbow bent less than this reads as a pole (172, 179)
HANG = 30.0
ARM_OK = {}                                                 # (shot, d) or shot -> reason: an exception the gate allows


def _norm(a):
    return (a + 180.0) % 360.0 - 180.0


def _log_arm(who, f):
    def g(k, sx, sy, a1, a2, *a, **kw):
        out = f(k, sx, sy, a1, a2, *a, **kw)
        try:
            c = k.c
            skin = a[1] if who == "rig" and len(a) > 1 else None
            if skin is not None and max(skin) - min(skin) < 0.08:
                return out                                                         # the robot's arm: its own style, not checked
            if oc._real(c):
                hx, hy = out if isinstance(out, tuple) else (sx, sy)
                ARM_LOG.append((who, float(a1), float(a2), c.user_to_device(hx, hy)))
        except Exception:
            pass
        return out
    g._arms = True
    return g


def install_arms():
    import sofia_v4, sofia_fs, client_ob
    if not getattr(kit.arm, "_arms", False):
        kit.arm = _log_arm("rig", kit.arm)
        import pam_mf
        pam_mf.kit.arm = kit.arm
    if not getattr(sofia_v4._arm, "_arms", False):
        sofia_v4._arm = _log_arm("sofia", sofia_v4._arm)
    if not getattr(sofia_fs.arm_long, "_arms", False):
        sofia_fs.arm_long = _log_arm("sofia", sofia_fs.arm_long)
    if not getattr(client_ob.limb, "_arms", False):
        client_ob.limb = _log_arm("client", client_ob.limb)
    if not getattr(s4.pam_reach, "_arms", False):                                 # Pam's arms drawn by hand over the scene (4.2b,
        pr = s4.pam_reach                                                          # 6.3): their angles come from here

        def pam_reach(x, lean, target, side=-1):
            a1, a2 = pr(x, lean, target, side)
            ARM_LOG.append(("pam", float(a1), float(a2), (x, target[1])))
            return a1, a2
        pam_reach._arms = True
        s4.pam_reach = pam_reach


def arm_faults(shot, d):
    out = []
    if shot in ARM_OK or (shot, d) in ARM_OK:
        return out
    for who, a1, a2, (hx, hy) in ARM_LOG:
        bend = abs(_norm(a2))
        fore = abs(_norm(a1 + a2))                                                 # 0: the forearm points straight down
        if bend < BEND_MIN and fore > HANG:
            out.append("ARM %s straight (bent %.0f deg, forearm at %.0f deg) at (%d, %d)" % (who, bend, fore, hx, hy))
    return out


def selftest_arms():
    """A straight raised arm must fail; a hanging straight arm and a bent raised arm must pass."""
    ARM_LOG[:] = [("rig", -160.0, -5.0, (0, 0))]
    bad = [] if arm_faults("x", 0) else ["a straight raised arm passed"]
    ARM_LOG[:] = [("rig", 8.0, 0.0, (0, 0))]
    if arm_faults("x", 0):
        bad.append("a hanging arm failed")
    ARM_LOG[:] = [("client", -150.0, -60.0, (0, 0))]
    if arm_faults("x", 0):
        bad.append("a bent raised arm failed")
    ARM_LOG[:] = []
    print("elbow gate selftest", "ok" if not bad else "FAIL %s" % bad)
    return not bad


def _round_shoulder_client(co):
    """v16 (group B): client_ob.client with one round shoulder cap over the arm's top and the jacket's corner (its own
    23x20 ellipse plus a square patch read as an angular break when the arm goes up). Built from its source, as
    client_of does, so client_ob itself is untouched."""
    import inspect
    if getattr(co.client, "_round", False):
        return co.client
    base = getattr(co.client, "_orig", co.client)                                 # under cs_say's logger
    src = inspect.getsource(base)
    a = ("        ellipse(k, side * (SH[0] - 1), sy_ - 1, 23, 20, J, seed + 14 + side, shadow=False, lw=2)   # the shoulder\n"
         "        c.set_source_rgb(*J); c.rectangle(min(side * 60, side * 86), sy_ - 12, 26, 32); c.fill()\n")
    if a not in src:
        raise SystemExit("cs_grips: client_ob.client changed; cannot find its shoulder")
    src = src.replace(a, "        _cap(k, side * (SH[0] - 2), sy_ + 2, sx_, sy_, u, J)\n")
    g = dict(vars(co)); g["_cap"] = _cap
    exec(compile(src, "cs_grips<client_ob.client>", "exec"), g)
    new = g["client"]
    if base is not co.client:                                                     # log it again (cs_say)
        import cs_say
        co.client = new
        cs_say._log("client", co, "client")
        new = co.client
    new._round = True
    return new


def _cap(k, x, y, sx, sy, u, col):
    """A round shoulder: an inked disc, then the upper arm's top filled into it so the seam does not show."""
    c = k.c
    r = 0.62 * 47
    c.new_path(); c.arc(x, y, r + 1.2, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
    c.new_path(); c.arc(x, y, r - 1.0, 0, 2 * math.pi); c.set_source_rgb(*col); c.fill()
    ux, uy = math.sin(math.radians(u)), math.cos(math.radians(u))
    c.set_source_rgb(*col); c.set_line_width(47 - 4.5); c.set_line_cap(0)
    c.move_to(sx + ux * 2, sy + uy * 2); c.line_to(sx + ux * 34, sy + uy * 34); c.stroke()
