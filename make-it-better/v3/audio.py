import numpy as np,wave,subprocess,sys
sr=44100;D=15.0;N=int(sr*D);m=np.zeros(N);fx=np.zeros(N);vo=np.zeros(N);rng=np.random.default_rng(3)
def add(buf,t,x,g=1):
    idx=(int(t*sr)+np.arange(len(x)))%N;np.add.at(buf,idx,x*g)
T=lambda d:np.arange(int(d*sr))/sr
def kick(g=1):
    t=T(.22);return np.sin(2*np.pi*(48*t+(110/30)*(1-np.exp(-30*t))))*np.exp(-t*14)*g
def noise(d,dec):
    t=T(d);return rng.standard_normal(len(t))*np.exp(-t*dec)
hp=lambda x:np.diff(x,prepend=0)
def sq(fr,d,dec=4,duty=.5):
    t=T(d);return np.where((t*fr)%1<duty,1,-1)*np.exp(-t*dec)
midi=lambda n:440*2**((n-69)/12)
def sweep(a,b,d,dec=0,kind='sq'):
    t=T(d);fr=np.linspace(a,b,len(t));ph=np.cumsum(fr)/sr*2*np.pi
    return (np.sign(np.sin(ph)) if kind=='sq' else np.sin(ph))*np.exp(-t*dec)
SEC=[(0,2.2,33,[0,3,7,12]),(3.2,4,36,[0,4,7,12]),(4,4.8,34,[0,4,7,11]),(4.8,5.6,31,[0,3,7,10]),(5.6,7,29,[0,3,7,10]),(8.9,10.4,33,[0,3,7,12])]
for a,b,r,ar in SEC:
    t=a;k=0
    while t<b-1e-6:
        if k%2==0:add(m,t,kick(),.9)
        if k%4==2:add(m,t,hp(noise(.14,24)),.28)
        add(m,t,hp(hp(noise(.04,120))),.07)
        add(m,t,sq(midi(r+(12 if k%8 in(3,6) else 0)),.23,6),.17)
        add(m,t,sq(midi(r+24+ar[k%4]),.2,10,.25),.075)
        t+=.25;k+=1
add(fx,0,kick(1.2));add(fx,0,noise(.25,10),.2)
cr0=noise(1.3,1);add(fx,0,np.convolve(cr0,np.ones(30)/30,'same'),1.0)  # roar
add(fx,2.2,hp(noise(.3,9)),.45);add(fx,2.2,sweep(1200,150,.22,4),.14)  # record scratch
r=sweep(1400,90,.4);add(fx,2.8,r*np.linspace(.4,.9,len(r)),.18);n=noise(.4,0);add(fx,2.8,hp(n)*np.linspace(.3,.7,len(n)),.2)
for t in(3.2,4,4.8,5.6):add(fx,t,sweep(300,1000,.09,8,'sine'),.2)
for t in(7.1,7.3,7.5):add(fx,t,sq(1400,.04,40),.1)
add(fx,7.6,kick(.8));add(fx,7.6,noise(.09,30),.3)
rn=noise(2.5,0);rn=np.convolve(rn,np.ones(9)/9,'same');add(fx,7.9,rn*np.minimum(1,np.linspace(2,0,len(rn))),.55)
cr=noise(1.6,1.4);add(fx,9.4,np.convolve(cr,np.ones(30)/30,'same'),1.2)
add(fx,10.8,sweep(300,900,.12,8,'sine'),.2);add(fx,10.8,noise(.08,50),.2)
add(fx,12.6,sweep(600,1000,.12,8,'sine'),.2)
rt=np.convolve(noise(2.4,0),np.ones(60)/60,'same');add(fx,10.5,rt*np.minimum(1,np.minimum(np.linspace(0,8,len(rt)),np.linspace(8,0,len(rt)))),.09)
# the union's sign: the beat used to be 2.1 s of near-silence, which reads as a fault
mur=np.convolve(noise(2.3,0),np.ones(90)/90,'same')
mur*=(1+.5*np.sin(2*np.pi*1.7*T(2.3))+.3*np.sin(2*np.pi*.6*T(2.3)))
add(fx,10.4,mur*np.minimum(1,np.minimum(np.linspace(0,6,len(mur)),np.linspace(6,0,len(mur)))),.55)
crk=sweep(220,150,.5,2.5,'sine')*np.sin(np.pi*np.linspace(0,1,int(.5*sr)))**.5
add(fx,10.9,crk*(1+.4*np.sign(np.sin(2*np.pi*11*T(.5)))),.10)    # the sign creaks as it goes up
add(fx,11.9,sq(70,.3,5),.05)
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
for n,t in(('ask',1.2),('pop',3.34),('pro',4.14),('less',4.94),('first',5.74),('end',12.92)):
    x=load(f'vo/v_{n}.wav');add(vo,t,x/np.abs(x).max(),.85)
ch=load('vo/v_chantf.wav');ch=ch/np.abs(ch).max()
for at in(0.02,8.9):
    for dt,g in((0,.42),(.018,.34),(.04,.3),(.07,.24)):add(vo,at+dt,ch,g)
# duck music and fx by voice envelope
w=int(.03*sr);e=np.convolve(np.abs(vo),np.ones(w)/w,'same');e=np.clip(e*14,0,1)
a=np.exp(-1/(.012*sr));rl=np.exp(-1/(.2*sr));s=np.zeros(N);p=0
for i in range(N):
    p=max(e[i],p*rl) if e[i]>p else p*rl;s[i]=p
out=(m*(1-.72*s)+fx*(1-.35*s))*1.0+vo*1.25
out=np.tanh(out)/np.abs(np.tanh(out)).max()*.9
f=wave.open('mix.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
