"""ONE STAR v25 (26 Nov; the review of v24, "polish, not rebuild": anticipation, action, reaction, hold; and 0:47's phone):
- 1.1 Don: shock while the phone flies, RELIEF when the robot catches it (a grin, hands to his chest), then HORROR at
  the 1/5 on its visor (hands to his head);
- the whip: only 3.5's last 2 drawings, 24 px (it smeared 3.5b's ball away); 3.5b the head snaps back harder and
  overshoots, the ball bounces OFF, up and back, then falls;
- 3.4 the finger traces the outline: round court A's bottom to where the courts meet, a 0.25 s hold there, then
  slides slowly down and out;
- 1.4 the tick pops in on the visor close-up (110 % then 100 %);
- 5.1 his phone 1.8 x (it was smaller than his fingers).
Not done (with why): Don glancing at a phone before "Approved." (the robot holds his phone); the robot's catch
cushion and flinch, hair and blinks (rig hooks); 6.5's hold after the line is already 0.5 s. Opt-in through install()."""
import cs_os24 as g24
import cs_scene1_v14 as v14
import cs_v14 as V
import cs_v15b as B


def install():
    v14.ARC24[0] = True
    g24.WHIP_OUT = ("3.5", 2)
    g24.WHIPPX[0] = 24.0
    g24.WHIP_IN_ON[0] = False
    V.BOUNCE35b[0] = True
    B.TRACE34[0] = True
    g24.POP14[0] = True
    import cs_scene5 as s5
    s5.PHONE51_S[0] = 1.8
    import cs_film
    cs_film.FX[:] = [x for x in cs_film.FX if not (x[0] == "3.4" and x[1] in (10, 14))] + \
        [("3.4", 14, __import__("cs_sfx").tap(180.0), 0.16)]
