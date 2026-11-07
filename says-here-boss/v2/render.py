import sys,os,subprocess,math,cairo
import v
from v import *
real_badge=v.badge; v.badge=lambda c:None
v.ERR=[(205,'847 BUGS',270,775,.1,74),(225,'PROD IS DOWN',800,960,.09,54),(245,'WHO DELETED THE DB?',540,650,-.03,62)]
TAG=lambda c:txt(c,'2027',540,282,92,YEL,lw=17)
B2=(y:=545,340)
def hook(c,f):
    pk=oe(f/12) if f<62 else 1-oe((f-62)/8)
    z=lerp(1.3,1.22,f/75)
    office(c,f,1,z,peek=pk)
    bubble(c,v.BL,98,y=545,h=340,hl=(2,));TAG(c)
    if f>=45:
        txt(c,'hehe',135,760,56,WHITE,lw=10,rot=-.15,scale=back((f-45)/5));txt(c,'hehe',945,760,56,WHITE,lw=10,rot=.15,scale=back((f-49)/5))
def closeup(c,f,bgt,bgb,expr,word,col,drops=0):
    bg(c,hx(bgt),hx(bgb));rays(c,WHITE,f,540,1050,.09)
    torso(c,540,1300,2.2);head(c,540,1030+noise(f,8)*5,2.3,expr,f=f)
    for i in range(drops):
        ph=((f/12+i*.37)%1);q=-1 if i%2 else 1
        ell(c,540+q*(290+i*12),810+ph*140,22,32);fs(c,hx('58c7ff'),6)
    return
def react(c,f):
    closeup(c,f,'1a3a5c','0d2236','small','',YEL,3)
    txt(c,'...YES?',540,420,170,YEL,lw=28,scale=back((f-75)/4))
def rew(c,f): v.s_rew(c,90+(f-90)*2)
def y24(c,f): v.s_24(c,120+round((f-105)*75/45))
def y25(c,f): v.s_25(c,195+round((f-150)*75/45))
def y26(c,f):
    r=f-195
    k=oe((r-20)/8)*(1-oe((r-48)/8))
    hy=845
    z=lerp(1,1.85,k);c.translate(540,950);c.scale(z,z);c.translate(-540-(0*k),-lerp(950,870,k)); c.translate(lerp(0,-70,k),0)
    bg(c,hx('ff6a2b'),hx('c91e47'));rays(c,hx('ffd84a'),f,540,1000,.14)
    if k<.02: v.caption(c,'2026','AI AGENT BOSS',WHITE,f,195)
    y=1000
    rr(c,350,y+215,380,180,14);fs(c,hx('a9713f'))
    limb(c,[(505,y+100),(505,y+210)],52,hx('14151e'));limb(c,[(590,y+100),(590,y+210)],52,hx('14151e'))
    for x_ in(490,600): ell(c,x_,y+215,48,24);fs(c,WHITE)
    torso(c,545,y-30,1.1)
    arm=math.sin(r*math.pi/7.5)*12*(1-k)
    limb(c,[(460,y),(310,y-70+arm),(205,y-90+arm)],46,NAVY);ell(c,195,y-95+arm,30,30);fs(c,SKIN,7)
    limb(c,[(630,y-10),(680,y+70),(640,y+95)],46,NAVY)
    head(c,545,hy,1.1,cool=r<28,expr='calm',f=f)
    tx=lerp(1120,770,oe((r-6)/14));ty=hy+10-abs(math.sin(f*.8))*10*(r<20)
    if r>=46:
        u=(r-46)/14;tx=lerp(770,1200,u);ty=hy+10+u*300-abs(math.sin(f*.8))*18
    robot(c,tx,ty-60,.62,walk=f*.8,boss=r>=36)
    if 28<=r<36:
        q=oe((r-28)/8);shades(c,lerp(545,tx,q),lerp(hy+9,ty-60-7,q),lerp(1.1,.63,q))
    if 28<=r<46: txt(c,'YOINK!',780,690,62,YEL,lw=12,rot=.08,scale=back((r-28)/5))
    for i in range(5):
        x=(1400-r*12+i*300)%1500-200;w=r*.9+i
        robot(c,x,1385-abs(math.sin(w))*14,.78,walk=w)
    if 2<=r<20: txt(c,'FASTER!',205,700,74,YEL,lw=14,rot=-.1,scale=back((r-2)/5))
def offer(c,f):
    r=f-255
    v.s_hire(c,375+r*2 if r<15 else 405+(r-15))
def thx(c,f): v.s_thx(c,450+(f-330)*2)
def nice(c,f):
    r=f-345
    office(c,f,1,1.18,tap=1)
    bubble(c,['NICE SHADES,','BY THE WAY.'],112,y=545,h=340);TAG(c)
    if r>=8:
        q=abs(math.sin(r*.35));c.save();c.translate(640,790);c.scale(q,q);c.rotate(r*.05)
        for i in range(4):
            c.rotate(math.pi/2);c.move_to(0,-60);c.line_to(10,-10);c.line_to(-10,-10);c.close_path()
        c.set_source_rgb(*YEL);c.fill();c.restore()
def real(c,f):
    r=f-390;z=lerp(1.12,1.0,oe(r/4))
    if r<6:c.translate(noise(f,1)*(6-r)*5,noise(f,2)*(6-r)*5)
    bg(c,hx('c91e47'),hx('5b0d2a'));rays(c,WHITE,f,540,1030,.08)
    c.save();c.translate(540,1030);c.scale(z,z);c.translate(-540,-1030)
    torso(c,540,1300,2.2);head(c,540,1030,2.3,'small')
    for q in(-1,1):
        limb(c,[(540+q*240,1340),(540+q*340,1200),(540+q*215,1050)],64,NAVY);ell(c,540+q*195,1040,42,36);fs(c,SKIN,8)
    c.restore()
    txt(c,'MY SHADES?!',540,420,132,YEL,lw=24,scale=back(r/4))
    real_badge(c)
def about(c,f):
    t=(f-405)/45;z=lerp(1.18,1.3,oe(t))
    office(c,f,1,z)
    bubble(c,['ABOUT YOUR','EXPERIENCE...'],112,y=545,h=340);TAG(c)
    real_badge(c)
SC=[('A',0,75,hook),('B',75,90,react),('C',90,105,rew),('D',105,150,y24),('E',150,195,y25),('F',195,255,y26),('G',255,330,offer),('H',330,345,thx),('I',345,390,nice),('J',390,405,real),('K',405,450,about)]
def draw(f):
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(s)
    for n,a,b,fn in SC:
        if a<=f<b: fn(c,f);break
    return s
if __name__=='__main__':
    if sys.argv[1]=='frames':
        for f in map(int,sys.argv[2:]):draw(f).write_to_png(f'chk_{f:03d}.png')
        from PIL import Image
        fs=list(map(int,sys.argv[2:]));S=Image.new('RGB',(5*360,((len(fs)+4)//5)*640))
        for i,f in enumerate(fs):S.paste(Image.open(f'chk_{f:03d}.png').convert('RGB').resize((360,640)),((i%5)*360,(i//5)*640))
        S.save('sheet.png')
    else:
        for n,a,b,fn in SC:
            if len(sys.argv)>2 and n not in sys.argv[2:]:continue
            p=subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 17 -preset veryfast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -video_track_timescale 15360 tmp_{n}.mp4'.split(),stdin=subprocess.PIPE)
            for f in range(a,b):p.stdin.write(bytes(draw(f).get_data()))
            p.stdin.close();assert p.wait()==0;os.rename(f'tmp_{n}.mp4',f'{n}.mp4');print(n,flush=True)
