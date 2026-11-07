import numpy as np,wave,subprocess
sr=44100;D=6.9;N=int(sr*D);rng=np.random.default_rng(3)
def add(buf,t,x,g=1):
    i=int(t*sr);x=x[:max(0,N-i)];buf[i:i+len(x)]+=x*g
T=lambda d:np.arange(int(d*sr))/sr
def kick(g=1):
    t=T(.22);return np.sin(2*np.pi*(48*t+(110/30)*(1-np.exp(-30*t))))*np.exp(-t*14)*g
def noise(d,dec):
    t=T(d);return rng.standard_normal(len(t))*np.exp(-t*dec)
hp=lambda x:np.diff(x,prepend=0)
lp=lambda x,n:np.convolve(x,np.ones(n)/n,'same')
def sq(fr,d,dec=4,duty=.5):
    t=T(d);return np.where((t*fr)%1<duty,1,-1)*np.exp(-t*dec)
midi=lambda n:440*2**((n-69)/12)
def sweep(a,b,d,dec=0,kind='sine'):
    t=T(d);fr=np.linspace(a,b,len(t));ph=np.cumsum(fr)/sr*2*np.pi
    return (np.sign(np.sin(ph)) if kind=='sq' else np.sin(ph))*np.exp(-t*dec)
def load(p):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
    return x/np.abs(x).max()
def build(line):
    m=np.zeros(N);fx=np.zeros(N);vo=np.zeros(N)
    t=0;k=0
    while t<1.5:
        if k%2==0:add(m,t,kick(),.9)
        if k%4==2:add(m,t,hp(noise(.14,24)),.28)
        add(m,t,hp(hp(noise(.04,120))),.07)
        add(m,t,sq(midi(33+(12 if k%8 in(3,6) else 0)),.23,6),.17)
        t+=.25;k+=1
    add(fx,1.22,sweep(300,1000,.18,5),.2)   # flip
    add(fx,1.5,sweep(900,700,.25,6),.12)    # doodle sting
    add(fx,2.5,hp(lp(noise(.1,20),6)),.7);add(fx,2.68,hp(lp(noise(.1,24),6)),.5)   # cough
    # tape peel: crackle that rises
    p=hp(noise(.65,0))*np.linspace(.4,1,int(.65*sr));g=np.where(np.sin(2*np.pi*43*T(.65))>0,1,.25);add(fx,3.1,p*g,.34)
    add(fx,3.75,sweep(1500,900,.09,10),.15)
    # creak during wobble
    t_=T(.75);cr=np.sin(2*np.pi*(95*t_+8*np.sin(2*np.pi*3*t_)))*np.exp(-t_*1.2);add(fx,3.8,cr,.22)
    add(fx,4.3,sweep(1800,1700,.04,30),.2)
    # collapse at 4.6
    add(fx,4.6,kick(1.8));add(fx,4.6,lp(noise(1.2,2.6),8),1.0);add(fx,4.6,sweep(120,35,.8,3),.7)
    for dt,f_ in((.18,70),(.36,55),(.55,48)):add(fx,4.6+dt,kick(1.1));add(fx,4.6+dt,noise(.1,25),.25)
    add(fx,5.42,sweep(1300,1250,.5,7),.14)   # last clang
    add(fx,5.42,sweep(2100,2050,.3,10),.09)
    add(vo,.1,load('vo/v_garbage.wav'),.85);add(vo,5.65,load(f'vo/v_{line}.wav'),.85)
    w=int(.03*sr);e=np.clip(np.convolve(np.abs(vo),np.ones(w)/w,'same')*14,0,1)
    out=m*(1-.72*e)+fx+vo*1.25
    out=np.tanh(out);out=out/np.abs(out).max()*.9
    f=wave.open(f'mix_{line}.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
build('back');build('passed')
