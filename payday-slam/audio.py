"""Synthesizes the Payday Slam soundtrack (music + SFX) from scratch. Writes audio.wav next to this file."""
import os
import numpy as np
from scipy.signal import butter,sosfilt
from scipy.io import wavfile
HERE=os.path.dirname(os.path.abspath(__file__))
SR=44100; T=17.0; N=int(SR*T); out=np.zeros(N); rng=np.random.default_rng(7)
fr=lambda f:int(f/30*SR)
def add(sig,f,g=1,buf=None):
    b=out if buf is None else buf
    i=fr(f); e=min(N,i+len(sig))
    if i<N: b[i:e]+=sig[:e-i]*g
def t(d): return np.arange(int(d*SR))/SR
def lp(x,c): return sosfilt(butter(2,c,'low',fs=SR,output='sos'),x)
def hp(x,c): return sosfilt(butter(2,c,'high',fs=SR,output='sos'),x)
def bp(x,a,b): return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
def kick():
    x=t(.35); return np.sin(2*np.pi*(45*x+ (150-45)*(1-np.exp(-x*28))/28))*np.exp(-x*9)+.25*np.exp(-x*300)*rng.normal(0,1,len(x))
def clap():
    x=t(.25); n=bp(rng.normal(0,1,len(x)),900,5000); e=np.exp(-x*22)
    for o in (.012,.024): e+=(x>o)*np.exp(-(x-o)*90)*.5
    return n*e
def hat(): x=t(.06); return hp(rng.normal(0,1,len(x)),8000)*np.exp(-x*90)
def saw(fq,x): return 2*((fq*x)%1)-1
def bass(fq,d=.22):
    x=t(d); y=saw(fq,x)+.5*np.sin(2*np.pi*fq*x); return np.tanh(2*lp(y,700))*np.minimum(1,(d-x)*60)*np.minimum(1,x*400)
def stab(fqs,d=.18):
    x=t(d); y=sum(saw(f,x)+saw(f*1.006,x) for f in fqs); return lp(y,3200)*np.exp(-x*9)/len(fqs)
def bell(fq,d=.5):
    x=t(d); return (np.sin(2*np.pi*fq*x)+.5*np.sin(2*np.pi*fq*2.76*x)+.25*np.sin(2*np.pi*fq*5.4*x))*np.exp(-x*7)
def chaching(g=1):
    return np.r_[bell(2093,.09)*.8,bell(2637,.55)]*g+ np.r_[hp(rng.normal(0,1,int(.05*SR)),5000)*.25,np.zeros(int(.59*SR))]
def groove(a,b,buf,g=1,fill=True):
    """frames a..b on 120bpm grid; bar patterns in C minor"""
    prog=[65.41,65.41,77.78,58.27]  # C C Eb Bb
    chords=[[261.6,311.1,392],[261.6,311.1,392],[311.1,392,466.2],[233.1,293.7,349.2]]
    for i in range(0,(b-a)//4+1):   # 16ths approx 3.75 frames
        f=a+i*3.75
        if f>=b: break
        st=i%16; bar=(i//16)%4
        if st%4==0: add(kick(),f,1.0*g,buf)
        if st in(4,12): add(clap(),f,.5*g,buf)
        if st%2==1: add(hat(),f,.16*g,buf)
        if st in(0,3,6,10,11,14): add(bass(prog[bar]*(2 if st in(6,14) else 1)),f,.42*g,buf)
        if st in(2,7,10): add(stab(chords[bar]),f,.2*g,buf)
mus=np.zeros(N); sfx=np.zeros(N)
groove(0,150,mus); groove(225,270,mus); groove(405,510,mus)
# hook hits
for f in(0,15,30,45): add(kick(),f,.9,sfx); add(clap(),f,.5,sfx)
# employee ka-ching
for f in(68,75,83,90): add(chaching(),f,.3,sfx)
for f,fq in zip((113,122,128,139),(1320,1760,988,2093)): add(bell(fq,.35),f,.4,sfx)
# row labels
for f in(60,105,150,285):
    x=t(.12); add(hp(rng.normal(0,1,len(x)),2500)*np.exp(-x*30),f,.18,sfx)
# founder zeros
for f in(165,180,195):
    x=t(.35); add(np.sin(2*np.pi*70*x)*np.exp(-x*12),f,.9,sfx); add(lp(rng.normal(0,1,len(x)),400)*np.exp(-x*25),f,.5,sfx)
# riser 195->225
d=1.0;x=t(d);rs=hp(rng.normal(0,1,len(x)),1500)*(x/d)**2.2
ph=2*np.pi*np.cumsum(200*2**(x/d*3))/SR; rs=rs*.4+np.sin(ph)*.35*(x/d)**1.6+saw(1,x)*0
add(rs,195,.7,sfx)
# impact
x=t(1.5); imp=np.sin(2*np.pi*(38*x+70*(1-np.exp(-x*20))/20))*np.exp(-x*3.2)+lp(rng.normal(0,1,len(x)),3000)*np.exp(-x*7)*.8
add(imp,225,1.0,sfx); add(chaching(),225,.55,sfx); add(chaching(),232,.35,sfx)
for k,fq in enumerate((1047,1319,1568,2093,2637,3136)): add(bell(fq,.4),225+k*3,.28,sfx)
# record scratch at 270
d=.32;x=t(d);sw=np.abs(np.sin(2*np.pi*x*5.5));nz=rng.normal(0,1,len(x))
sc=np.array(bp(nz,500,3500))*sw*np.exp(-x*3)
add(sc,270,1.0,sfx)
# sad trombone on -$200s
for f,fq,dd in zip((300,315,330,345),(233.1,220,207.65,196),(.45,.45,.45,1.05)):
    x=t(dd); vib=1+(.03*np.sin(2*np.pi*6*x)*(x>.4)) if dd>.5 else 1+0*x
    ph=np.cumsum(fq*vib*(1-.04*x))/SR; y=sum(np.sin(2*np.pi*ph*h)/h**.7 for h in range(1,9))
    wah=lp(y,1300)*(.65+.35*np.sin(np.pi*np.minimum(x/.45,1)))
    y=wah*np.minimum(1,x*25)*np.minimum(1,(dd-x)*14)
    add(y,f,.42,sfx); xx=t(.2); add(np.sin(2*np.pi*90*xx)*np.exp(-xx*18),f,.5,sfx)
# crickets 372->405 (awkward silence)
def cricket():
    x=t(.22); return np.sin(2*np.pi*4300*x)*(np.sin(2*np.pi*28*x)>0)*np.minimum(1,(.22-x)*30)
for f in(366,380,394): add(cricket(),f,.14,sfx)
# punch
for f in(378,390):
    x=t(.1); add(hp(rng.normal(0,1,len(x)),1800)*np.exp(-x*40),f,.14,sfx)
add(imp,405,.75,sfx)
add(np.r_[bell(1047,.1),bell(784,.45)],450,.4,sfx)
x=t(.25); add(np.sin(2*np.pi*70*x)*np.exp(-x*16),450,.8,sfx)
add(chaching(),468,.25,sfx)
# fade tail
mix=mus*.8+sfx*.9
fd=int(.4*SR); mix[-fd:]*=np.linspace(1,0,fd)
mix=np.tanh(mix*1.05)
st=np.stack([mix,mix],1)
# gentle stereo on hats/bells via short delay on one side
st[:,1]=np.r_[np.zeros(12),mix[:-12]]*.35+mix*.65
wavfile.write(os.path.join(HERE,'audio.wav'),SR,(st/np.max(np.abs(st))*.95*32767).astype('int16'))
