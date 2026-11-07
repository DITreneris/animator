import sys,os,subprocess,math,random,cairo
import v
from v import *
real_badge=v.badge
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
def rally(c,f,fp,ey,thumbk=1,paper=1,bot_x=215):
    bg(c,hx('8c1322'),hx('3c0b18'));rays(c,hx('f3c76a'),f,540,560,.13)
    # banner
    rr(c,50,216,980,118,8);fs(c,CREAM,8)
    txt(c,"THE AI WORKERS' UNION",540,275,76,hx('8c1322'),lw=0)
    # back rows
    for i in range(9):
        fistbot(c,20+i*130,455+(i%2)*14,.42,fp,ey)
    c.rectangle(0,330,W,300);c.set_source_rgba(.25,.04,.08,.34);c.fill()
    for i in range(7):
        if i==3:continue
        fistbot(c,40+i*167,600+(i%2)*14,.58,fp,ey)
    c.rectangle(0,520,W,260);c.set_source_rgba(.25,.04,.08,.16);c.fill()
    # podium + leader
    rr(c,400,700,280,160,10);fs(c,hx('3a2a26'));txt(c,'UNION',540,770,50,YEL,lw=0)
    tx=540+108;ty=lerp(610,420,fp)
    limb(c,[(610,590),(tx+18,lerp(610,500,fp)),(tx,ty)],28,WHITE);ell(c,tx,ty-10,30,30);fs(c,WHITE,7)
    robot(c,540,500,.98,boss=True)
    for i in range(6):
        if i in(2,3):continue
        fistbot(c,70+i*188,830+(i%2)*14,.78,fp,ey)
    sign(c,190,700,270,124,['IT WAS','FINE'],46)
    sign(c,890,700,270,124,['WHICH','VERSION?'],46)
    # guy
    gy=1385
    torso(c,540,gy+140,1.25)
    if paper:
        limb(c,[(450,gy+220),(350,gy+250),(320,gy+190)],48,NAVY)
        rr(c,235,gy+60,165,120,6);fs(c,WHITE,6)
        for i in range(3):
            c.rectangle(255,gy+84+i*26,125,7);c.set_source_rgb(*GREY);c.fill()
        ell(c,318,gy+182,28,26);fs(c,SKIN,7)
    limb(c,[(630,gy+220),(740,gy+210),(765,gy+140)],48,NAVY)
    if thumbk>.02: thumb(c,768,gy+115,thumbk)
    else: ell(c,768,gy+130,28,26);fs(c,SKIN,7)
    head(c,540,gy,1.1,'calm')
    # small striker with V47 sign, and toaster
    rb(c,bot_x,1330,.62,red=False,eye=(10,4))
    c.set_source_rgb(*hx('8a5a2e'));c.rectangle(bot_x-70,1225,10,175);c.fill()
    rr(c,bot_x-135,1148,140,84,8);fs(c,CREAM,6);txt(c,'V47',bot_x-65,1190,54,RED,lw=0)
    limb(c,[(bot_x-40,1400),(bot_x-65,1375)],18,WHITE)
    toaster(c,870,1400,.62,f)
LOOP=['COULD YOU JUST','MAKE IT BETTER?']
def bb(c,lines,sz=92,y=1020,h=230,w=860,hl=()):bubble(c,lines,sz,y=y,h=h,w=w,hl=hl)
def A(c,f):
    w=cl((f-6)/14);rally(c,f,1-oe(w),oe(w))
    bb(c,LOOP,hl=(1,))
def B(c,f):
    r=f-60
    bg(c,hx('24003f'),hx('050014'))
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+r*noise(i,4)*80
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((.1,.9,1) if i%2 else (1,.15,.6)),.16);c.fill()
    t=['V47','V30','V12','V1'][min(3,r//4)]
    for dx,cc in((-16,(0,1,1)),(16,(1,0,.55))):txt(c,t,540+dx,900,330,cc,lw=0,alpha=.9)
    txt(c,t,540,900,330,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110;c.move_to(x+90,520);c.line_to(x,580);c.line_to(x+90,640);c.close_path();c.set_source_rgb(*YEL);c.fill()
    txt(c,'HOW DID THIS START?',540,1180,74,YEL,lw=13)
    for yy in range(0,H,6):
        c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
VS=[(75,'V1',['MAKE IT POP.'],0),(105,'V12',['MORE PROFESSIONAL.'],.35),(135,'V30',['LESS PROFESSIONAL.'],.7),(165,'V47',['ACTUALLY, THE FIRST','ONE WAS BETTER.'],1)]
def desk(c,f,a,lab,lines,prog,cnt=None):
    t=(lerp(1,.62,prog),lerp(.84,.62,prog),lerp(.28,.62,prog));b=(lerp(1,.34,prog),lerp(.6,.34,prog),lerp(.18,.38,prog))
    bg(c,t,b)
    if prog<.9:rays(c,WHITE,f,540,1200,.1*(1-prog))
    if prog>=1 and f-a<6:c.translate(noise(f,1)*(6-(f-a))*4,noise(f,2)*(6-(f-a))*4)
    txt(c,lab,540,300,190,RED if prog>=1 else YEL,lw=28,scale=max(.02,back((f-a)/4)))
    h=40+prog*230
    c.save();c.translate(0,190)
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
        c.save();c.translate(540,650);c.scale(k,k);c.translate(-540,-650)
        bubble(c,lines,76 if len(lines)==2 else 78,y=650,h=220 if len(lines)==2 else 170,w=900);c.restore()
def C(c,f):
    a,l,li,p=[x for x in VS if x[0]<=f][-1];desk(c,f,a,l,li,p)
def E_(c,f):
    r=f-210
    bg(c,hx('55595f'),hx('24262b'))
    tw=.25 if (r%7)<2 and r<24 else 1
    if r%7<1 and r<24:c.translate(noise(f,1)*6,0)
    robot(c,540,860,3.1,glow=.25,tw=tw*3.2 if tw==1 else .25)
    y=lerp(1370,2000,oe((r-10)/10))
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
    r=f-240
    if r<30:
        bg(c,hx('3a4a66'),hx('151b2a'));rr(c,-20,1420,1120,600,0);c.set_source_rgb(*hx('20283a'));c.fill()
        ell(c,540,1490,300,30);c.set_source_rgba(.6,.75,1,.2);c.fill()
        striker(c,560,1180,1.05);rain(c,f);txt(c,'DAY 1',540,330,110,WHITE,lw=20)
    elif r<45:
        bg(c,hx('4a4c6a'),hx('1a1b2c'));rr(c,-20,1420,1120,600,0);c.set_source_rgb(*hx('20283a'));c.fill()
        striker(c,380,1180,.95);striker(c,760,1180,.95);rain(c,f,.35);txt(c,'DAY 2',540,330,110,WHITE,lw=20)
    elif r<60:
        bg(c,hx('8c3a33'),hx('2d141c'));rr(c,-20,1420,1120,600,0);c.set_source_rgb(*hx('22151d'));c.fill()
        for j,(y,s,n) in enumerate(((870,.55,5),(1070,.68,4),(1290,.8,3))):
            for i in range(n):striker(c,540+(i-(n-1)/2)*(1000/n),y,s)
        txt(c,'DAY 3',540,330,110,WHITE,lw=20)
    else:
        bg(c,hx('a81a27'),hx('3c0b18'));rays(c,hx('f3c76a'),f,540,900,.14)
        for j in range(10):
            s=.2+j*.03
            for i in range(14-j):
                x=(i+.5)*W/(14-j)+((j%2)*30);y=480+j*(60+j*7)
                rb(c,x,y+math.sin(f*.8+i+j)*5,s,red=True)
        txt(c,'DAY 4',540,330,110,YEL,lw=20)
def G(c,f):
    r=f-315;x=lerp(100,215,oe(r/12))
    rally(c,f,0,1,thumbk=0,paper=0,bot_x=x)
    if r>=15:
        c.rectangle(0,0,W,H);c.set_source_rgba(0,0,0,.45);c.fill()
        k=max(.02,back((r-15)/5));c.save();c.translate(540,880);c.rotate(-.025);c.scale(k,k)
        rr(c,-420,-250,840,500,18);fs(c,CREAM,10)
        txt(c,'THIS IS OUR',0,-95,104,INK,lw=0);txt(c,'FINAL VERSION.',0,40,104,RED,lw=0)
        txt(c,'- THE UNION',0,160,50,hx('66707f'),lw=0);c.restore()
def H_(c,f):
    r=f-390;fp=oe((f-440)/9) if f>=440 else 0;ey=1-fp
    rally(c,f,fp,ey,thumbk=max(.02,back((r-10)/5)) if r>=10 else 0)
    if f>=412:
        if f<436: bb(c,['LOVE THE ENERGY.'],100)
        else: bb(c,['COULD YOU JUST',''],92)
    real_badge(c)
SC=[('A',0,60,A),('B',60,75,B),('C',75,210,C),('E',210,240,E_),('F',240,315,F),('G',315,390,G),('H',390,450,H_)]
def draw(f):
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(s)
    for n,a,b,fn in SC:
        if a<=f<b:fn(c,f);break
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
