import numpy as np,wave
sr=44100;D=17.0;N=int(sr*D);out=np.zeros(N);rng=np.random.default_rng(3)
def add(t,x,g=1):
    i=int(t*sr)%N
    idx=(i+np.arange(len(x)))%N   # wraps tails over the loop point
    np.add.at(out,idx,x*g)
T=lambda d:np.arange(int(d*sr))/sr
def kick(g=1):
    t=T(.22);return np.sin(2*np.pi*(48*t+ (110/30)*(1-np.exp(-30*t))))*np.exp(-t*14)*g
def noise(d,dec):
    t=T(d);return rng.standard_normal(len(t))*np.exp(-t*dec)
def hp(x):return np.diff(x,prepend=0)
def sq(fr,d,dec=4,duty=.5,):
    t=T(d);return np.where((t*fr)%1<duty,1,-1)*np.exp(-t*dec)
def midi(m):return 440*2**((m-69)/12)
def sweep(a,b,d,dec=0,kind='sq'):
    t=T(d);fr=np.linspace(a,b,len(t));ph=np.cumsum(fr)/sr*2*np.pi
    x=np.sign(np.sin(ph)) if kind=='sq' else np.sin(ph)
    return x*np.exp(-t*dec)
B=.5
# root per section (start,end,root,arp)
SEC=[(0,3,33,[0,3,7,12]),(4,6.5,36,[0,4,7,12]),(6.5,9,41,[0,4,7,11]),(9,12.5,38,[0,3,7,10]),(12.5,15,33,[0,3,7,12]),(15,16,36,[0,4,7,12]),(16,17,33,[0,3,7,12])]
for a,b,r,ar in SEC:
    t=a;k=0
    while t<b-1e-6:
        q=k%8
        if k%2==0: add(t,kick(),.9)
        if k%4==2: add(t,hp(noise(.14,24)),.28)
        add(t+0,hp(hp(noise(.04,120))),.07)
        add(t,sq(midi(r+(12 if q in(3,6) else 0)),.23,6,.5),.17)
        if a>=4 or t>=1.5:
            add(t,sq(midi(r+24+ar[k%4]),.2,10,.25),.075)
        t+=B/2;k+=1
# hook stinger + robot "speech"
add(0,kick(1.2));
vo=[.08,.3,.5,.75,.98,1.2,1.4,1.65,1.9]
for i,t in enumerate(vo):add(t,sq(330+[0,60,-30,40,0,-40,50,120,220][i],.15,8,.3),.13)
for t in(1.6,1.75,1.9,2.05):add(t,sweep(700,1000,.07,8),.05)
# rewind 3-4
r=sweep(1100,70,1.0,0);r=r*np.linspace(.35,.8,len(r));add(3,r,.17)
n=noise(1.0,0)*np.linspace(.2,.6,int(sr));add(3,hp(n),.18)
# 2024 typing + pops
t=4.0;rr=np.random.default_rng(5)
while t<6.45:
    add(t,hp(noise(.025,160)),.2);t+=rr.uniform(.05,.11)
for t in(4.4,5.23,5.73,6.23):add(t,sweep(500,1000,.07,10),.14)
add(6.23,sweep(1300,700,.25,3),.13)
# 2025 errors
for t in(7,7.5,8,8.23,8.5):add(t,sq(165,.18,6,.5),.17);add(t+.08,sq(120,.16,8,.5),.17)
# 2026 stomps, yoink
for k in range(7):add(9+k*.5,hp(noise(.08,40)),.25)
add(10.0,sweep(600,1500,.3,2,'sine'),.06)
add(10.8,sweep(500,2300,.2,0,'sine'),.22);add(11.0,sweep(2300,350,.35,3,'sine'),.24)  # the yoink
# hired
add(12.5,noise(.35,10),.14)
add(13,kick(1.7));add(13,noise(.35,16),.45);add(13,sweep(120,40,.5,5,'sine'),.65)
for i,m in enumerate((62,61,60,59)):
    t0=13.5+i*.25;d=.25 if i<3 else .7;t=T(d);v=1+.02*np.sin(2*np.pi*6*t)
    x=np.sign(np.sin(2*np.pi*midi(m)*v*t))*np.minimum(1,(d-t)*12);add(t0,x,.11)
# thanks sniffle
for t in(15.05,15.5):add(t,sweep(900,1250,.18,3,'sine'),.13)
# one more thing
for i,t in enumerate((16.05,16.22,16.4,16.56,16.72)):add(t,sq(260+i*25,.13,8,.3),.13)
out=np.tanh(out*1.25);out=out/np.abs(out).max()*.89
w=wave.open('music.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype('<i2').tobytes());w.close()
