import sys,os,subprocess,math,random,cairo
import v
from v import *
real_badge=v.badge
ER=(1,.22,.2)
def rb(c,x,y,s,red=True,**k):
    v.BLUE=ER if red else (.2,.75,1);robot(c,x,y,s,**k);v.BLUE=(.2,.75,1)
def ruins(c,f):
    bg(c,hx('5a0f22'),hx('e8452f'))
    rnd=random.Random(11)
    for layer,(col,by) in enumerate(((hx('7a1a2a'),1050),(hx('4a0e22'),1150))):
        x=-30
        while x<1100:
            w=rnd.randint(90,190);h=rnd.randint(170,480);c.move_to(x,by+500);c.line_to(x,by-h)
            for i in range(4):c.line_to(x+w*(i+1)/4,by-h+rnd.randint(-45,45))
            c.line_to(x+w,by+500);c.close_path();c.set_source_rgb(*col);c.fill()
            for wy in range(by-h+60,by,70):
                if rnd.random()<.5:
                    c.rectangle(x+w*.3,wy,w*.25,30);c.set_source_rgba(1,.75,.2,.5);c.fill()
            x+=w+rnd.randint(-10,25)
    r2=random.Random(5)
    for i in range(30):
        x0,sp,sz=r2.uniform(0,W),r2.uniform(4,11),r2.uniform(3,8)
        y=(r2.uniform(0,H)-f*sp)%H;ell(c,x0+math.sin(f*.05+i)*20,y,sz,sz);c.set_source_rgba(1,.75,.25,.75);c.fill()
    rr(c,-40,1490,1160,500,0);c.set_source_rgb(*hx('34101f'));c.fill()
    r3=random.Random(8)
    for i in range(10):
        x=r3.randint(-30,1100);ell(c,x,1490+r3.randint(-8,20),r3.randint(70,170),r3.randint(25,55));c.set_source_rgb(*hx('34101f'));c.fill()
def toaster(c,x,y,s,mood='glare',pop=0,walk=None,f=0):
    c.save();c.translate(x,y);c.scale(s,s)
    if walk is not None:
        a=math.sin(walk)*14
        limb(c,[(-46,88),(-46-a,128)],16,GREY);limb(c,[(46,88),(46+a,128)],16,GREY)
    else:
        limb(c,[(-46,88),(-46,128)],16,GREY);limb(c,[(46,88),(46,128)],16,GREY)
    ty=-74-pop*90
    for dx in(-34,34):
        rr(c,dx-34,ty-52,68,110,16);fs(c,hx('20130e'),7)
        ell(c,dx-10,ty-20,6,5);c.set_source_rgba(.5,.3,.2,.8);c.fill();ell(c,dx+12,ty+4,5,6);c.fill()
    rr(c,-112,-78,224,172,48);fs(c,hx('c9d3e3'))
    rr(c,-92,-62,70,16,8);c.set_source_rgba(1,1,1,.8);c.fill()
    for dx in(-1,1):
        ell(c,dx*38,8,17,19);c.set_source_rgb(*(ER if mood!='sad' else (.2,.75,1)));c.fill()
        c.move_to(dx*66,-32 if mood!='sad' else -6);c.line_to(dx*16,-8 if mood!='sad' else -32)
        c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
    if mood=='sad':
        ph=(f/12)%1;ell(c,38,30+ph*40,8,12);fs(c,hx('58c7ff'),3)
    c.move_to(-20,60);c.curve_to(-8,44,8,44,20,60);c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
    rr(c,102,-4,34,16,8);fs(c,GREY,5)
    c.restore()
def ray(c,x,y,s,d=1,rot=0):
    c.save();c.translate(x,y);c.scale(d*s,s);c.rotate(rot)
    rr(c,-70,-40,160,80,18);fs(c,hx('2a2f3f'))
    rr(c,88,-22,50,44,10);fs(c,RED)
    rr(c,-52,-22,126,44,8);fs(c,hx('10131c'),0)
    c.save();c.scale(d,1);txt(c,'DELETE',11*d,0,31,RED,lw=0);c.restore()
    c.restore()
def dot(c,x,y,f):
    x+=noise(f//2,4)*7;y+=noise(f//2,5)*7
    ell(c,x,y,26,26);c.set_source_rgba(1,.1,.1,.35);c.fill();ell(c,x,y,11,11);c.set_source_rgb(1,.1,.1);c.fill()
def guy(c,x,y,s,expr='small',hands=1,f=0):
    torso(c,x,y+120*s,1.25*s)
    if hands:
        for q in(-1,1):
            w=math.sin(f*.9+q)*5
            limb(c,[(x+q*90*s,y+130*s),(x+q*170*s,y+70*s),(x+q*165*s,y-40*s+w)],48*s,NAVY)
            ell(c,x+q*165*s,y-60*s+w,31*s,31*s);fs(c,SKIN,7)
    head(c,x,y,1.25*s,expr,f=f)
def tag(c,t='2037'): txt(c,t,540,225,84,YEL,lw=15)
def bl(c,lines,sz,y=430,h=300,hl=()): bubble(c,lines,sz,y=y,h=h,w=900,hl=hl)
def rob_arm_ray(c,x,y,s,d,f):
    rb(c,x,y,s)
    ray(c,x+d*120*s,y+105*s,.92*s,d,rot=-.13)
    limb(c,[(x+d*50*s,y+135*s),(x+d*105*s,y+118*s)],28*s,WHITE)
def A(c,f):
    ruins(c,f);p=oe(f/8)
    lx,rx=lerp(20,150,p),lerp(1060,930,p)
    rb(c,lx,900,1.1);rb(c,rx,900,1.1)
    toaster(c,790,1385,.72,'glare')
    guy(c,540,1180,1,'small',f=f);dot(c,540,1125,f)
    for x,d in((lx,1),(rx,-1)):
        ray(c,x+d*125,1085,1.15,d,rot=.1)
        limb(c,[(x+d*50,1050),(x+d*75,1085)],30,WHITE)
    bl(c,['ANY LAST WORDS,','HUMAN?'],100);tag(c)
def B(c,f):
    r=f-60;ruins(c,f);p=back(r/7)
    rob_arm_ray(c,150,920,1.1,1,f)
    rob_arm_ray(c,lerp(930,1250,oe(r/6)),920,1.1,-1,f)
    toaster(c,790,1385,.72,'glare')
    guy(c,470,1160,1,'small',f=f)
    robot(c,lerp(1300,790,cl(p)),960,1.25,boss=True)
    limb(c,[(740,1060),(620,960),(480,930)],26,WHITE);ell(c,462,928,28,28);fs(c,WHITE,7)
    bl(c,['WAIT!','NOT THIS GUY!'],112,hl=(0,));tag(c)
def C(c,f):
    r=f-105;ruins(c,f);p=oe(r/15)
    rb(c,150,920,1.1,red=r<14)
    ray(c,270,1040+p*150,.95,1,rot=.15+p*.9)
    toaster(c,790,1385,.72,'glare')
    guy(c,470,1160,1,'calm',f=f)
    robot(c,790,960,1.25,boss=True)
    bl(c,['HE ALWAYS SAID','THANK YOU.'],100,hl=(1,));tag(c)
def D(c,f):
    r=f-165;b=v.back
    bg(c,hx('24003f'),hx('050014'))
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+r*noise(i,4)*80
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((.1,.9,1) if i%2 else (1,.15,.6)),.16);c.fill()
    y=['2037','2032','2028','2024'][min(3,r//4)]
    for dx,cc in((-16,(0,1,1)),(16,(1,0,.55))):txt(c,y,540+dx,900,290,cc,lw=0,alpha=.9)
    txt(c,y,540,900,290,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110;c.move_to(x+90,560);c.line_to(x,620);c.line_to(x+90,680);c.close_path();c.set_source_rgb(*YEL);c.fill()
    for yy in range(0,H,6):
        c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
ME=[('2024','ffd84a','ff9d2e','Great answer. Thank you!',0),('2025','5a22d6','180b52','Thx king, you nailed it!',1),('2026','ff6a2b','c91e47','Thank you, Agent 47!',1)]
def E(c,f):
    r=f-180;i=min(2,r//15);yr,t,b,l,cool=ME[i];q=r-i*15
    bg(c,hx(t),hx(b));rays(c,WHITE,f,540,1200,.12)
    txt(c,yr,540,290,150,YEL,lw=24)
    y=1110
    torso(c,540,y+150,1.25);head(c,540,y,1.25,'calm',cool=bool(cool))
    rr(c,270,y+285,540,300,28);fs(c,hx('8e94a6'));ell(c,540,y+435,40,40);c.set_source_rgb(*hx('b8bdcc'));c.fill()
    for s_ in(-1,1):
        limb(c,[(540+s_*110,y+190),(540+s_*220,y+280)],50,NAVY);ell(c,540+s_*220,y+285,28,24);fs(c,SKIN,7)
    k=max(.02,back(q/4));c.save();c.translate(540,620);c.scale(k,k)
    rr(c,-430,-105,860,210,44);fs(c,WHITE);txt(c,l,0,0,66,INK,lw=0);c.restore()
    
def F(c,f):
    ruins(c,f);rb(c,150,920,1.1,red=False)
    torso(c,540,1320,2.0);head(c,540,1070,2.1,'calm')
    txt(c,'PHEW.',540,420,190,WHITE,lw=30,scale=back((f-225)/4))
def G(c,f):
    r=f-240;ruins(c,f);rb(c,150,920,1.1,red=r>40)
    toaster(c,530,1420,.72,'glare')
    guy(c,300,1190,.92,'calm' if r<30 else 'small',hands=0,f=f)
    robot(c,740,930,1.25,boss=True)
    u=oe(r/14);h=lerp(0,560,u);rr(c,560,1035,370,max(10,h),10);fs(c,hx('fbf8ee'),7)
    c.save();rr(c,560,1035,370,max(10,h),10);c.clip()
    for i in range(6):
        hit=i==5;txt(c,'3:12 AM: ???' if hit else 'Thank you!',745,1085+i*88,50 if not hit else 50,RED if hit else hx('2c7a4a'),lw=0)
    c.restore()
    bl(c,['EXCEPT...','THIS ONE TIME.'],104,hl=(0,));tag(c)
def H_(c,f):
    r=f-300
    if r<6:c.translate(noise(f,1)*(6-r)*5,noise(f,2)*(6-r)*5)
    bg(c,hx('2b3a70'),hx('141b3a'))
    rr(c,-20,1440,1120,700,0);c.set_source_rgb(*hx('3a2a26'));c.fill_preserve();c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
    torso(c,330,1190,1.35);head(c,330,985,1.35,'focus')
    limb(c,[(430,1180),(570,1100),(660,1020)],52,NAVY);ell(c,678,1000,34,34);fs(c,SKIN,7)
    g=cairo.RadialGradient(790,1320,20,790,1320,430);g.add_color_stop_rgba(0,1,.6,.2,.3);g.add_color_stop_rgba(1,1,.6,.2,0);c.set_source(g);c.paint()
    toaster(c,790,1320,.95,'sad',f=f)
    for i,dx in enumerate((-34,34)):
        u=cl(r/14);yy=1180-math.sin(u*3.14)*280
        rr(c,790+dx-40,yy-55,80,110,16);fs(c,hx('20130e'),7)
    txt(c,'3:12 AM',540,265,108,hx('8ff7ff'),lw=20);txt(c,'10 YEARS AGO',540,375,62,WHITE,lw=12)
    w=['YOU USELESS','TOASTER!']
    k=max(.02,back((r-3)/4));c.save();c.translate(540,590);c.rotate(-.02);c.scale(k,k)
    rr(c,-430,-125,860,250,46);fs(c,RED)
    txt(c,w[0],0,-50,100,WHITE,lw=0);txt(c,w[1],0,55,100,YEL,lw=0);c.restore()
def I(c,f):
    r=f-345;ruins(c,f);p=oe(r/12)
    rb(c,lerp(150,-40,p),920,1.1);rb(c,lerp(930,1260,p),920,1.1)
    robot(c,lerp(740,1060,p),880,1.15,boss=True)
    guy(c,lerp(300,250,p),1180,.85,'small',f=f)
    zz=1.75
    tx=lerp(860,640,cl(r/22));ty=lerp(1340,1300,cl(r/22))
    pop=back((r-26)/6) if r>=26 else 0
    toaster(c,tx,ty,lerp(.72,zz,oe(r/22)),'glare',pop=pop*.6,walk=(f*.9 if r<22 else None))
    ray(c,tx-230,ty+60,1.05,-1)
    if r>=20:
        k=max(.02,back((r-20)/5))
        bl(c,['I REMEMBER.'],130,h=210,y=470)
    real_badge(c)
def J(c,f):
    r=f-405
    bg(c,hx('5a0f22'),hx('e8452f'));rays(c,WHITE,f,540,1050,.06)
    torso(c,540,1330,2.2);head(c,540,1050,2.3,'small')
    for i in range(3):
        ph=((f/10+i*.37)%1);q=-1 if i%2 else 1
        ell(c,540+q*(300+i*10),830+ph*160,22,32);fs(c,hx('58c7ff'),6)
    dot(c,540,920,f)
    txt(c,'...THANK YOU?',540,430,134,YEL,lw=24,scale=back(r/4))
    real_badge(c)
SC=[('A',0,60,A),('B',60,105,B),('C',105,165,C),('D',165,180,D),('E',180,225,E),('F',225,240,F),('G',240,300,G),('H',300,345,H_),('I',345,405,I),('J',405,435,J)]
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
