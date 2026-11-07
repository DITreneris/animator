import numpy as np
from scipy.signal import butter,sosfilt
from scipy.io import wavfile
SR=44100;DUR=204/12;N=int(DUR*SR);rng=np.random.default_rng(6);vo=np.zeros(N);sx=np.zeros(N);mu=np.zeros(N);T=lambda d:np.arange(int(d*SR))/SR
P=lambda p:p/12
def add(b,x,t,g=1):
    i=int(t*SR);e=min(N,i+len(x))
    if i<N:b[i:e]+=x[:e-i]*g
lp=lambda x,f:sosfilt(butter(2,f,'low',fs=SR,output='sos'),x);hp=lambda x,f:sosfilt(butter(2,f,'high',fs=SR,output='sos'),x);bp=lambda x,a,b:sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
import os
VO=os.path.join(os.path.dirname(os.path.abspath(__file__)),'vo')
def clip(name,target,fade=.03):
    s,x=wavfile.read(os.path.join(VO,name+'.wav'));y=hp(x.astype(float)/32768,85);f=int(fade*s);y[:f]*=np.linspace(0,1,f);y[-f:]*=np.linspace(1,0,f)
    act=y[np.abs(y)>.003];y=y*10**((target-20*np.log10(np.sqrt((act**2).mean())))/20);return np.tanh(y*1.1)/1.1
# Your recorded voice lines, placed on the 12-poses-per-second grid (P = pose number)
add(vo,clip('employee_mm',-17),P(26))
add(vo,clip('freelancer_ow',-18),P(46))
add(vo,clip('founder_okay',-16),P(100))
add(vo,clip('coder_money',-16),P(110))
add(vo,clip('coder_wait',-15),P(156)-.04)
add(vo,clip('coder_thanks',-15),P(187))
def pluck(f,d=.3):
    x=T(d);return (np.sin(2*np.pi*f*x)+.4*np.sin(4*np.pi*f*x))*np.exp(-x*9)*np.minimum(1,x*800)
def tuba(f,d=.18):
    x=T(d);return sum(np.sin(2*np.pi*f*h*x)/h for h in(1,2,3))*np.minimum(1,x*60)*np.minimum(1,(d-x)*30)
mel=[523,659,784,659,587,698,784,988,880,784,659,784,587,659,523,0];bs=[131,196,165,196,147,196,131,196]
for i in range(55):
    p=i*2
    if mel[i%16]:add(mu,pluck(mel[i%16]),P(p),.3)
    if i%2==0:add(mu,tuba(bs[(i//2)%8]),P(p),.4)
for i,p in enumerate(range(186,204,2)):
    if mel[i%16]:add(mu,pluck(mel[i%16]),P(p),.28)
    if i%2==0:add(mu,tuba(bs[(i//2)%8]),P(p),.36)
def bell(f,d=.5):
    x=T(d);return (np.sin(2*np.pi*f*x)+.5*np.sin(2*np.pi*f*2.76*x))*np.exp(-x*7)
def thud(f=60):
    x=T(.32);return np.sin(2*np.pi*(f*x+f*(1-np.exp(-x*30))/30))*np.exp(-x*14)+lp(rng.normal(0,1,len(x)),700)*np.exp(-x*32)*.55
def bonk(f):
    x=T(.22);return np.sin(2*np.pi*(f*x+f*.5*(1-np.exp(-x*25))/25))*np.exp(-x*20)+.4*np.sin(2*np.pi*f*2.3*x)*np.exp(-x*35)
add(sx,thud(55),P(22),.85);add(sx,np.r_[bell(2093,.08)*.8,bell(2637,.45)],P(23),.2)
for p,f in((46,700),(52,560)):add(sx,bonk(f),P(p),.55)
for p,f,d in((68,587,.42),(74,523,.42),(80,440,.45)):
    x=T(d);ph=np.cumsum(f*(1+.012*np.sin(2*np.pi*6*x)))/SR;y=sum(np.sin(2*np.pi*ph*h)/h for h in range(1,7));add(sx,lp(y,2800)*np.minimum(1,x*20)*np.minimum(1,(d-x)*12),P(p),.16)
x=T(.3);add(sx,lp(np.sign(np.sin(2*np.pi*220*x))+np.sign(np.sin(2*np.pi*277*x)),2300)*np.minimum(1,(.3-x)*40),P(90),.14)
x=T(1.1);cr=np.sin(2*np.pi*(35*x+80*(1-np.exp(-x*22))/22))*np.exp(-x*4.5)+lp(rng.normal(0,1,len(x)),4500)*np.exp(-x*6)*.85
for f in(413,971,1687,2311):cr+=np.sin(2*np.pi*f*x)*np.exp(-x*9)*.17
add(sx,cr,P(96),.85);add(sx,np.r_[bell(2093,.08)*.8,bell(2637,.5)],P(97),.25)
for p,f in zip((112,116,120),(233.1,220,207.65)):
    x=T(.32);y=sum(np.sin(2*np.pi*f*h*x)/h**.7 for h in range(1,8));add(sx,lp(y,1300)*np.minimum(1,x*25)*np.minimum(1,(.32-x)*14),P(p),.17)
x=T(.8);ph=np.cumsum(196*(1+.03*np.sin(2*np.pi*6*x)))/SR;y=sum(np.sin(2*np.pi*ph*h)/h**.7 for h in range(1,8));add(sx,lp(y,1300)*np.minimum(1,x*25)*np.minimum(1,(.8-x)*10),P(124),.17)
def pop(f):
    x=T(.1);return np.sin(2*np.pi*(f*x+f*2*(1-np.exp(-x*40))/40))*np.exp(-x*40)
add(sx,pop(420),P(136),.55);add(sx,pop(620),P(139),.6);x=T(.1);add(sx,bp(rng.normal(0,1,len(x)),2500,7000)*np.exp(-x*50),P(139),.25)
add(sx,thud(170),P(146),.55);add(sx,thud(120),P(149),.7);x=T(1.0);im=np.sin(2*np.pi*(45*x+70*(1-np.exp(-x*25))/25))*np.exp(-x*6)+lp(rng.normal(0,1,len(x)),3500)*np.exp(-x*16)*.7
for f in(610,1190,1830,2750):im+=np.sin(2*np.pi*f*x)*np.exp(-x*7)*.13
add(sx,im,P(152),.9)
env=np.abs(vo);w=int(.08*SR);env=np.convolve(env,np.ones(w)/w,'same');duck=1-.55*np.clip(env/.03,0,1);m=mu*duck*.85+sx+vo
m=np.tanh(m*.85)*.85;s=np.stack([m,m],1);wavfile.write(os.path.join(os.path.dirname(os.path.abspath(__file__)),'audio.wav'),SR,(s*32767).astype('int16'))
