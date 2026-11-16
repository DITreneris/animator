"""One source of timing for picture and sound (seconds). Riff C and AI tune T3 are the picks."""
RIFF = [(62, 3), (65, 1), (60, 2), (69, 2), (67, 2), (74, 4)]           # D F C A G D'  (riff C)
AI_TUNE = [(72, 3), (74, 1), (76, 2), (79, 2), (77, 2), (76, 6)]        # T3: electric piano
AI_CHORD = [48, 55, 64]
S16 = 0.125                                                               # one sixteenth at 120 BPM
BAR = 2.0                                                                 # the riff fills one bar
ONSETS = [sum(l for _, l in RIFF[:i]) * S16 for i in range(len(RIFF))]   # note onsets within a take
AI_ONSETS = [sum(l for _, l in AI_TUNE[:i]) * S16 for i in range(len(AI_TUNE))]

T = dict(
    riff86=0.067,            # first note 2 frames in
    drum_line=2.0, wave86=1.95,
    ff1=3.5, era16=4.0,
    frag16=4.1,              # his 3-note fragment
    phone1=4.95,             # close-up: his post, 3 VIEWS
    couch=5.6,               # guitar down on the couch, he looks at his phone
    catwalk=5.85, cat16=6.25,
    phone2=8.15,             # close-up: swipe to the cat's post, 10M
    face16=8.8,              # his face: stunned, then deadpan
    ff2=9.3, era26=9.8,
    ask=9.95,
    ai=11.85,                # the AI's tune
    nod_stop=13.0,
    wave26=13.75, know=13.85,
    glance=15.2,
    cat26=15.55,             # the cat version, two passes, on the bar
    bob=15.9,
    orig=17.35,              # "Now THAT'S original!"
    sideeye=18.95,
)
END = T['cat26'] + 2 * BAR - T['riff86']     # cut where a third pass would start: lands on frame 0's riff
FPS = 30
NF = int(round(END * FPS))
