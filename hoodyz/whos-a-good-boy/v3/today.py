# Opens on "today" (2026): hook and its repeat read 2026 with a TODAY tag; rewind runs 2026 -> 2025 -> 2024.
import v9,titles
from v import *
v9.YEARS[:]=[(0,'2026'),(75,'2024'),(210,'2025'),(285,'2026'),(527,'2027')]
TODAY=[(0,60),(285,315)]
_top=titles.topbar
def topbar(c,f):
    _top(c,f)
    if any(a<=f<b for a,b in TODAY):
        k=max(.02,back(min(f-a for a,b in TODAY if a<=f<b)/5))
        c.save();c.translate(800,titles.BAR_Y+titles.BAR_H+44);c.rotate(-.06);c.scale(k,k)
        rr(c,-104,-34,208,68,20);c.set_source_rgb(*RED);c.fill();txt(c,'TODAY',0,0,50,WHITE,lw=0);c.restore()
def B(c,f):
    r=f-60;bg(c,hx('24003f'),hx('050014'))
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+r*noise(i,4)*80
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((.1,.9,1) if i%2 else (1,.15,.6)),.16);c.fill()
    t=['2026','2025','2024','2024'][min(3,r//4)]
    for dx,cc in((-12,(0,1,1)),(12,(1,0,.55))):txt(c,t,540+dx,900,260,cc,lw=0,alpha=.9)
    txt(c,t,540,900,260,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110;c.move_to(x+90,560);c.line_to(x,620);c.line_to(x+90,680);c.close_path();c.set_source_rgb(*YEL);c.fill()
    for yy in range(0,H,6):c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
def install():
    _dr=v9.dragged
    v9.dragged=lambda c,x,y,s,f,*a:_dr(c,x,y,s,f,.55)
    v9.topbar=topbar
    v9.SC[1]=('B',60,75,B)
