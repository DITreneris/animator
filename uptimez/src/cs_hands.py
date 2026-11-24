"""ONE STAR (episode 11): the series' one hand (hands_ps, lesson 147) with a state per hand. Tomas, 23 Nov, after two
hand audits: RELAX is a quiet hand (hands_ps "quiet"), FIST only for raised or emotional gestures, GRIP round a held
object, and the robot keeps its own grippers. Opt-in: install() sets kit.HAND; uninstall() puts the old drawers back.
  STATE: {shot: (left, right)} in the order the arms are drawn; shots not listed get ("quiet", "quiet")."""
import kit
import hands_ps as hp

STATE = {}
BIG = {"4.1": {"palm": 2.0, "grab": 1.6}}                                   # v19: Pam's STOP palm reads at this size (4 tried)
SHOT = [None]


def _robot(skin):
    r, g, b = skin
    return max(skin) - min(skin) < 0.08                                     # grey or steel: the robot's arm


def _held(k, hx, hy):
    import cs_scene1 as s1
    x, y = k.c.user_to_device(hx, hy)
    return any((x - a) ** 2 + (y - b) ** 2 < (14 * s1.HI[0]) ** 2 for a, b in s1.PH_PREV)


LOG = []
_PER = {}                                                                    # this drawing's hands: (index, shape, device x, y, w)


def hook(k, hx, hy, w, skin, seed, d, side):
    x_, y_ = k.c.user_to_device(hx, hy)
    if _held(k, hx, hy):                                                    # a phone is held here: its grip draws the hand
        LOG.append((hp._N[0], "held", x_, y_, w)); hp._N[0] += 1
        return
    if _robot(skin):
        LOG.append((-1, "robot", x_, y_, w))                                                        # its own gripper, as before the hook
        kit.ellipse(k, hx, hy, w / 1.15 * 0.6, w / 1.15 * 0.6, skin, seed, shadow=False, lw=2)
        return
    st = STATE.get(SHOT[0])
    if callable(st):
        st = st()
    if isinstance(st, dict):                                                # per person (by skin), their two hands in
        key = tuple(round(v_, 2) for v_ in skin)                            # order: robust to a set drawn twice
        n = _PER.get(key, 0); _PER[key] = n + 1
        g = st.get(key, ("quiet", "quiet"))[n % 2]
        hp.GEST[0] = (g, g)
    elif isinstance(st, list):                                              # one shape per hand, in drawing order
        g = st[hp._N[0]] if hp._N[0] < len(st) else "quiet"
        hp.GEST[0] = (g, g)
    g_ = hp.GEST[0][hp._N[0] % 2]
    LOG.append((hp._N[0], g_, x_, y_, w))
    if g_ in BIG.get(SHOT[0], {}):                                          # a gesture the shot is about, bigger
        w = w * BIG[SHOT[0]][g_]
    hp.hand(k, hx, hy, w, skin, seed, d, side)


def begin(shot):
    """Before drawing a shot's frame: its hand states."""
    SHOT[0] = shot
    st = STATE.get(shot, ("quiet", "quiet"))
    hp.reset(*(st if isinstance(st, tuple) else ("quiet", "quiet")))


_BYFN = {}


def begin_fn(fn):
    """begin() from the drawing function: every One Star scene's SHOTS, read once."""
    if not _BYFN:
        import importlib
        for i in range(1, 7):
            for n, _, f in importlib.import_module("cs_scene%d" % i).SHOTS:
                _BYFN[f] = n
    LOG.clear(); _PER.clear()
    begin(_BYFN.get(fn))


def install():
    kit.HAND[0] = hook


def uninstall():
    kit.HAND[0] = None


def _s41():
    import cs_scene4 as s4
    key = (1.0, 0.86, 0.67)                                                 # her rig's own skin (pam_bc), not SKIN_PAM
    return {key: ("quiet", s4.HAND41[0])}                                   # Pam: the roll's hand, the STOP palm


STATE["4.1"] = _s41
STATE["3.1"] = ["point", "quiet"]
