import sys,os,subprocess,math,random,cairo
import v
from v import *

ER=(1,.22,.2);CREAM=hx('f3e3bf')
def rb(c,x,y,s,red=True,**k):
    v.BLUE=ER if red else (.2,.75,1);robot(c,x,y,s,**k);v.BLUE=(.2,.75,1)
def fistbot(c,x,y,s,fp,ey,red=True):
    # raised arm drawn behind the body
    tx=x+s*95;ty=lerp(y+s*150,y-s*150,fp)
    limb(c,[(x+s*70,y+s*120),(tx+s*20,lerp(y+s*150,y-s*20,fp)),(tx,ty)],28*s,WHITE)
    ell(c,tx,ty-8*s,26*s,26*s);fs(c,WHITE,max(3,7*s))
    rb(c,x,y,s,red=red,eye=(0,lerp(-9,14,ey)))
def sign(c,x,y,w,h,lines,sz,col=RED):
    c.set_source_rgb(*hx('8a5a2e'));c.rectangle(x-7,y,14,h+110);c.fill()
    rr(c,x-w/2,y-h/2,w,h,10);fs(c,CREAM,6)
    lh=sz*1.08;y0=y-(len(lines)-1)*lh/2
    for i,l in enumerate(lines):txt(c,l,x,y0+i*lh,sz,col,lw=0)
def toaster(c,x,y,s,f=0):
    c.save();c.translate(x,y);c.scale(s,s)
    c.set_source_rgb(*hx('8a5a2e'));c.rectangle(-150,-440,16,330);c.fill()          # its own picket sign
    rr(c,-268,-600,250,170,10);fs(c,CREAM,7);txt(c,'V47',-143,-543,66,RED,lw=0)
    limb(c,[(-96,20),(-150,-90),(-146,-150)],20,hx('c9d3e3'))
    limb(c,[(-46,88),(-46,128)],16,GREY);limb(c,[(46,88),(46,128)],16,GREY)
    for dx in(-34,34):
        rr(c,dx-34,-126,68,110,16);fs(c,hx('20130e'),7)
    rr(c,-112,-78,224,172,48);fs(c,hx('c9d3e3'))
    for dx in(-1,1):
        ell(c,dx*38,8,17,19);c.set_source_rgb(*ER);c.fill()
        c.move_to(dx*66,-32);c.line_to(dx*16,-8);c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
    c.restore()
def thumb(c,x,y,k):
    c.save();c.translate(x,y);c.scale(k,k)
    rr(c,-12,-82,30,70,14);fs(c,SKIN,7)
    rr(c,-38,-30,76,66,22);fs(c,SKIN,7);c.restore()
def rally(c,f,fp,ey,guyx=540,expr='calm',thumbk=0,paper=0,bot_x=170,dim=0,freeze=False,flat=False):
    if freeze: f=438                                         # the room stops dead on the punchline
    bg(c,hx('8c1322'),hx('3c0b18'));rays(c,hx('f3c76a'),f,540,620,.13)
    rr(c,60,386,960,112,8);fs(c,CREAM,8)
    txt(c,"THE AI WENT ON STRIKE",540,444,74,hx('8c1322'),lw=0)
    for i in range(6):fistbot(c,70+i*188,590+(i%2)*12,.72,fp,ey)
    sign(c,540,600,700,120,['NO MORE VERSIONS!'],62)
    for i,x in enumerate((110,320,760,970)):fistbot(c,x,800,1.0,fp,ey)
    tx=540+118;ty=lerp(960,700,fp)
    limb(c,[(610,950),(tx+18,lerp(960,860,fp)),(tx,ty)],30,WHITE);ell(c,tx,ty-10,32,32);fs(c,WHITE,7)
    robot(c,540,810,1.08,boss=True,flat=flat)
    if guyx<1200:
        x=guyx;gy=1400
        torso(c,x,gy+145,1.3)
        if paper:
            limb(c,[(x-90,gy+230),(x-190,gy+260),(x-220,gy+200)],50,NAVY)
            rr(c,x-305,gy+70,165,120,6);fs(c,WHITE,6)
            for i in range(3):
                c.rectangle(x-285,gy+94+i*26,125,7);c.set_source_rgb(*GREY);c.fill()
            ell(c,x-222,gy+192,28,26);fs(c,SKIN,7)
        else:
            rr(c,x-145,gy+190,290,190,14);fs(c,hx('8e94a6'))
        if thumbk>.02:
            limb(c,[(x+90,gy+230),(x+200,gy+220),(x+225,gy+150)],50,NAVY);thumb(c,x+228,gy+125,thumbk)
        head(c,x,gy,1.15,expr)
    if bot_x<1200:
        rb(c,bot_x,1410,.62,red=False,eye=(10,4))
        c.set_source_rgb(*hx('8a5a2e'));c.rectangle(bot_x-70,1300,10,175);c.fill()
        rr(c,bot_x-135,1236,140,84,8);fs(c,CREAM,6);txt(c,'V47',bot_x-65,1278,54,RED,lw=0)
    toaster(c,872,1430,.62,f)
LOOP=['COULD YOU JUST','MAKE IT BETTER?']
def bb(c,lines,sz=92,y=1110,h=220,w=800,hl=()):bubble(c,lines,sz,y=y,h=h,w=w,hl=hl)
def A(c,f):
    fp=.55+.45*abs(math.sin(f*math.pi/15))
    rally(c,f,fp,0,guyx=540,bot_x=170,expr='happy',paper=1,thumbk=1)   # the pose he ends on, so the loop doesn't jump
    if f>=36:
        bb(c,LOOP,hl=(1,))
def S(c,f):
    r=f-66
    bg(c,hx('5a0f22'),hx('24060f'))
    c.translate(noise(f,1)*max(0,4-r)*3,noise(f,2)*max(0,4-r)*3)
    for x,s_ in((120,2.0),(960,2.0),(540,2.4)):rb(c,x,720 if x!=540 else 760,s_,eye=(0,14))
    torso(c,540,1570,.95);head(c,540,1440,.95,'small')
    ell(c,700,1340,16,24);fs(c,hx('58c7ff'),5)
def B(c,f):
    r=f-84
    bg(c,hx('3d0a18'),hx('14030a'))      # the rewind card stays in the episode's red, not off-palette purple
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+r*noise(i,4)*80
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((1,.78,.25) if i%2 else (1,.25,.3)),.16);c.fill()
    t=['V47','V12'][min(1,r//6)]
    for dx,cc in((-16,(1,.8,.2)),(16,(1,.2,.25))):txt(c,t,540+dx,900,330,cc,lw=0,alpha=.9)
    txt(c,t,540,900,330,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110;c.move_to(x+90,520);c.line_to(x,580);c.line_to(x+90,640);c.close_path();c.set_source_rgb(*YEL);c.fill()
    txt(c,'HOW DID THIS START?',540,1180,74,YEL,lw=13)
    for yy in range(0,H,6):
        c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
VS=[(96,'V1',['MAKE IT POP.'],0),(120,'V12',['MORE PROFESSIONAL.'],.35),(144,'V30',['LESS PROFESSIONAL.'],.7),(168,'V47',['ACTUALLY, THE FIRST','ONE WAS BETTER.'],1)]
def desk(c,f,a,lab,lines,prog,cnt=None):
    t=(lerp(1,.62,prog),lerp(.84,.62,prog),lerp(.28,.62,prog));b=(lerp(1,.34,prog),lerp(.6,.34,prog),lerp(.18,.38,prog))
    bg(c,t,b)
    if prog<.9:rays(c,WHITE,f,540,1200,.1*(1-prog))
    if prog>=1 and f-a<6:c.translate(noise(f,1)*(6-(f-a))*4,noise(f,2)*(6-(f-a))*4)
    txt(c,lab,540,470,150,RED if prog>=1 else YEL,lw=24,scale=max(.02,back((f-a)/4)))
    if prog==0 and f-a<26:                                   # dates the flashback: we have gone back, not forward
        txt(c,'47 VERSIONS EARLIER',540,588,62,INK,lw=14,st=WHITE,alpha=min(1,(f-a)/4)*min(1,(26-(f-a))/5))
    h=40+prog*230
    pin=1+.10*oe((f-168)/30) if f>=168 else 1    # slow push-in on 'Actually, the first one was better.'
    c.save();c.translate(0,290);c.translate(540,1320);c.scale(1.22*pin,1.22*pin);c.translate(-540,-1320)
    robot(c,270,1120+prog*25,1.05,glow=lerp(1,.2,prog),rot=-.03-prog*.14)
    for i in range(2):
        ph=((f/12+i*.5)%1);
        if prog>.2:ell(c,395+i*18,950+ph*110,12,18);fs(c,hx('58c7ff'),4)
    # desk, stack, guy
    torso(c,780,1180,1.15);head(c,780,1020,1.1,'calm')
    rr(c,-30,1345,1140,650,0);fs(c,hx('8a5a34'))
    rr(c,-30,1320,1140,48,12);fs(c,hx('a9713f'))
    for i in range(int(h/14)):
        rr(c,440+noise(i,9)*10,1312-i*14,170,14,3);fs(c,WHITE,3)
    rr(c,630,1205,290,120,10);fs(c,hx('8e94a6'))
    c.restore()
    if lines:
        k=max(.02,back((f-a-3)/4))
        c.save();c.translate(540,720);c.scale(k,k);c.translate(-540,-720)
        bubble(c,lines,76 if len(lines)==2 else 78,y=720,h=220 if len(lines)==2 else 170,w=900);c.restore()
def C(c,f):
    a,l,li,p=[x for x in VS if x[0]<=f][-1];desk(c,f,a,l,li,p)
def E_(c,f):
    r=f-213
    bg(c,hx('55595f'),hx('24262b'))
    hold=r>=9                                                # flat, done-with-this eyes from here to the end of the shot
    tw=.25 if ((r%7)<2 and r<9) or hold else 3.2
    if r%7<1 and r<9:c.translate(noise(f,1)*6,0)
    robot(c,540,860,3.1,glow=.25,tw=tw)
    y=lerp(1370,2000,oe((r-17)/7))
    rr(c,270,y,540,380,18);fs(c,hx('a9713f'),10)
    rr(c,320,y+60,440,300,8);fs(c,WHITE,6);txt(c,'V47',540,y+200,120,RED,lw=0)
def rain(c,f,a=.5):
    r=random.Random(3)
    for i in range(70):
        x=(r.uniform(0,1300)-f*14)%1300-100;y=(r.uniform(0,H)+f*r.uniform(55,75))%H
        c.move_to(x,y);c.line_to(x-12,y+56);c.set_source_rgba(.75,.85,1,a);c.set_line_width(4);c.stroke()
def striker(c,x,y,s,red=False):
    rb(c,x,y,s,red=red)
    c.set_source_rgb(*hx('8a5a2e'));c.rectangle(x-112*s,y-90*s,12*s,290*s);c.fill()
    rr(c,x-205*s,y-180*s,190*s,120*s,8*s);fs(c,CREAM,max(3,6*s));txt(c,'V47',x-110*s,y-120*s,70*s,RED,lw=0)
def F(c,f):
    r=f-237
    if r<30:
        bg(c,hx('3a4a66'),hx('151b2a'));rr(c,-20,1420,1120,600,0);c.set_source_rgb(*hx('20283a'));c.fill()
        ell(c,540,1490,300,30);c.set_source_rgba(.6,.75,1,.2);c.fill()
        striker(c,560,1180,1.05);rain(c,f);txt(c,'DAY 1',540,480,110,WHITE,lw=20)
    elif r<45:
        bg(c,hx('4a4c6a'),hx('1a1b2c'));rr(c,-20,1420,1120,600,0);c.set_source_rgb(*hx('20283a'));c.fill()
        striker(c,380,1180,.95);striker(c,760,1180,.95);rain(c,f,.35);txt(c,'DAY 2',540,480,110,WHITE,lw=20)
    elif r<60:
        bg(c,hx('8c3a33'),hx('2d141c'));rr(c,-20,1420,1120,600,0);c.set_source_rgb(*hx('22151d'));c.fill()
        for j,(y,s,n) in enumerate(((870,.55,5),(1070,.68,4),(1290,.8,3))):
            for i in range(n):striker(c,540+(i-(n-1)/2)*(1000/n),y,s)
        txt(c,'DAY 3',540,480,110,WHITE,lw=20)
    else:
        bg(c,hx('a81a27'),hx('3c0b18'));rays(c,hx('f3c76a'),f,540,900,.14)
        for j in range(10):
            s=.2+j*.03
            for i in range(14-j):
                x=(i+.5)*W/(14-j)+((j%2)*30);y=580+j*(56+j*6.4)
                rb(c,x,y+math.sin(f*.8+i+j)*5,s,red=True)
        txt(c,'DAY 4',540,480,110,YEL,lw=20)
def G(c,f):
    r=f-312;x=lerp(40,170,oe(r/10))
    rally(c,f,0,1,bot_x=x,paper=1)
    if r>=12:
        c.rectangle(0,0,W,H);c.set_source_rgba(0,0,0,.45);c.fill()
        k=max(.02,back((r-12)/5));c.save();c.translate(540,880);c.rotate(-.025);c.scale(k,k)
        rr(c,-420,-250,840,500,18);fs(c,CREAM,10)
        txt(c,'THIS IS OUR',0,-95,104,INK,lw=0);txt(c,'FINAL VERSION.',0,40,104,RED,lw=0)
        txt(c,'- THE UNION',0,160,50,hx('66707f'),lw=0);c.restore()
def H_(c,f):
    r=f-375;fz=f>=438
    rally(c,f,0,1,expr='happy',paper=1,thumbk=max(.02,back((r-3)/5)) if r>=3 else 0,freeze=fz,flat=fz)
    if f>=TS:
        if f<TS+27: bb(c,['LOVE THE ENERGY.'],84)
        else: bb(c,LOOP,hl=(1,))
TS=387
SC=[('A',0,66,A),('S',66,84,S),('B',84,96,B),('C',96,213,C),('E',213,237,E_),('F',237,312,F),('G',312,375,G),('H',375,450,H_)]
def pill_for(f):
    if 84<=f<96: return ['V47','V12'][min(1,(f-84)//6)]
    if 96<=f<213: return [x for x in VS if x[0]<=f][-1][1]
    return 'ON STRIKE'
def draw(f):
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(s)
    for n,a,b,fn in SC:
        if a<=f<b:fn(c,f);break
    v.topbar(c,pill_for(f))
    return s
if __name__=='__main__':
    if sys.argv[1]=='frames':
        fs_=list(map(int,sys.argv[2:]))
        for f in fs_:draw(f).write_to_png(f'chk_{f:03d}.png')
        from PIL import Image
        S=Image.new('RGB',(5*360,((len(fs_)+4)//5)*640))
        for i,f in enumerate(fs_):S.paste(Image.open(f'chk_{f:03d}.png').convert('RGB').resize((360,640)),((i%5)*360,(i//5)*640))
        S.save('sheet.png')
    else:
        for n,a,b,fn in SC:
            if len(sys.argv)>2 and n not in sys.argv[2:]:continue
            p=subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 17 -preset veryfast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -video_track_timescale 15360 tmp_{n}.mp4'.split(),stdin=subprocess.PIPE)
            for f in range(a,b):p.stdin.write(bytes(draw(f).get_data()))
            p.stdin.close();assert p.wait()==0;os.rename(f'tmp_{n}.mp4',f'{n}.mp4');print(n,flush=True)
