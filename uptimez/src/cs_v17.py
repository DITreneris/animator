"""ONE STAR v17 (25 Nov, Tomas /grill-me after the cold mute test on v16):
- 4.4 the green arrow from the paddle to Pam is gone (both viewers: "a rope tying her to the sign"); the paddle leans to her;
- 1.4 Don leans in 8 and presses the visor with his elbow up and out of his body's outline (the forearm level from his
  body read as a pole); the swings to and from rest blend the joint angles;
- 4.2b Pam's elbow at her side, the forearm and finger at his pocket (the straight reach across read as a pole);
- 3.1b the glass door reads as a door: a pull handle, a kick rail, glints and a PUSH sticker;
- 5.2 the insert 120 higher: Pam's sleeve from the top edge shorter (cs_grips.SHIFT52);
- the 540 hand gate on 6.6 (cs_grips)."""
import cs_v14 as V
import cs_v15e as E
import cs_scene4 as s4


def install():
    E.NO_ARROW44[0] = True
    V.ELBOW14[0] = -1
    V.LEAN14[0] = 8.0
    s4.ELBOW42b[0] = 20.0
    V.DOOR31b[0] = True
    import cs_grips
    cs_grips.SHIFT52[0] = SHIFT52
    import cs_hands as ch
    import of_cast as oc
    ch.TOL[0] = 16.0                                                     # the phone's hand kept out within 16 frame units,
    if not getattr(oc.log_grip, "v17", False):                           # the gate's 13; the grips logged in frame units too
        def log_grip(c, kind, x, y, thumb=None, want=None):
            if oc._real(c):
                ds = c.get_target().get_device_scale()[0]
                X, Y = c.user_to_device(x, y)
                oc.GRIP_LOG.append(dict(kind=kind, at=(X / ds, Y / ds), thumb=thumb, want=want))
        log_grip.v17 = True
        oc.log_grip = log_grip
    
    
SHIFT52 = 120.0
