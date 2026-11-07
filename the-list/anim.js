const T=(s,x,y,sz,col=INK,al='left',st=0)=>{c.font=sz+'px Marker';c.textAlign=al;c.textBaseline='middle';if(st){c.lineJoin='round';c.lineWidth=st;c.strokeStyle=INK;c.strokeText(s,x,y)}c.fillStyle=col;c.fillText(s,x,y)};
const at=(x,y,s,f)=>{c.save();c.translate(x,y);c.scale(s,s);f();c.restore()};
const B=a=>a.flatMap(q=>[q,q]);HAIR.splice(Math.floor(HAIR.length*.75));
const R=[395,585,775,1000],X=235,G='#179c58',RED='#e8263f';
let N=0;const slam=(f,x,y,fn)=>{if(N<f)return;const s=N==f?1.34:N==f+1?1.1:1;c.save();c.translate(x,y);c.scale(s,s);c.translate(-x,-y);fn();c.restore()};
function bill(x,y,r,s){c.save();c.translate(x,y);c.rotate(r);c.scale(s,s);shape(B([[-110,-54],[110,-54],[110,54],[-110,54]]),{fill:'#39c172',w:10,off:[0,0],two:false});shape(oval(0,0,34,30,9),{fill:'#c9f5d6',w:6,off:[0,0],two:false});c.restore()}
function empF(){at(120,R[0],.2,()=>{c.translate(-540,-700);shape([[280,360],[800,360],[830,860],[770,1030],[310,1030],[250,860]],{fill:'#d99a6c',w:30});shape([[272,420],[300,320],[780,310],[820,420],[800,470],[300,470]],{fill:'#4a4650',w:20});for(const x of[410,670]){shape(oval(x,650,74,74,11),{fill:'#fffdf5',w:18,off:[0,0]});c.fillStyle=INK;c.beginPath();c.arc(x,682,22,0,7);c.fill();shape([[x-80,650],[x,650],[x+80,650],[x+74,574],[x,566],[x-74,574]],{fill:'#bf8a60',w:14,off:[0,0],two:false})}line([[450,890],[540,896],[630,886]],24)})}
function freeF(h){at(120,R[1]+(h?10:0),h?.18:.2,()=>{c.translate(-540,-740);shape(oval(540,430,100,86,12),{fill:'#a2472b',w:22});shape([[260,760],[340,520],[540,450],[760,520],[820,760],[760,1010],[540,1100],[320,1010]],{fill:'#f7c7a6',w:28});shape([[258,740],[290,510],[540,430],[790,510],[822,740],[720,590],[540,550],[360,590]],{fill:'#b5532f',w:20});for(const x of[420,660]){shape(oval(x,720,70,76,11),{fill:'#fffdf5',w:16,off:[0,0]});c.fillStyle=INK;c.beginPath();c.arc(x+4,690,22,0,7);c.fill()}shape([[370,880],[450,900],[630,900],[710,875],[680,950],[620,980],[460,980],[400,950]],{fill:'#fffdf5',w:18,off:[0,0]})})}
function foundF(v,hit){at(120,R[2]-14+(hit?12:0),hit?.15:.18,()=>{c.translate(-540,-720);shape([[230,560],[340,420],[740,420],[850,560],[870,840],[760,1070],[320,1070],[210,840]],{fill:'#efb48c',w:28});shape([[214,560],[300,350],[780,330],[870,560],[740,460],[340,470]],{fill:'#d9a441',w:20});for(const x of[390,690]){shape([[x-70,690],[x,640],[x+70,690],[x,716]],{fill:'#fffdf5',w:14,off:[0,0]});if(v>0){const L=90+v*360,Wd=20+v*30;shape([[x-Wd,710],[x+Wd,710],[x+Wd+10,710+L],[x,750+L],[x-Wd-10,710+L]],{fill:'#7ed4ff',w:16,off:[0,0]})}}shape([[420,840],[540,780],[660,840],[640,960],[540,1000],[440,960]],{fill:'#6d1f35',w:16,off:[0,0]})})}
function codF(){at(120,R[3]+6,.22,()=>{c.translate(-548,-760);shape([[352,620],[432,450],[640,446],[744,610],[748,850],[666,1046],[430,1052],[346,860]],{fill:SKIN,w:26});c.save();c.translate(548,440);for(const h of HAIR)ink(wob(smooth(h.pts,false),1.6),h.w*2,h.col);c.restore();for(const[x,y]of[[446,700],[644,684]]){shape(oval(x,y,66,74,12),{fill:'#fffdf5',w:18,off:[0,0]});c.fillStyle=INK;c.beginPath();c.arc(x-22,y,24,0,7);c.fill()}shape([[388,842],[470,866],[620,862],[706,830],[688,958],[620,1012],[468,1014],[408,958]],{fill:'#6d1f35',w:18,off:[0,0]});shape([[394,848],[470,870],[620,866],[700,836],[690,884],[620,906],[470,908],[404,890]],{fill:'#fffdf5',w:10,off:[0,0],two:false})})}
function truck(x,y,s){at(x,y,s,()=>{c.translate(-500,-1100);shape(B([[-60,1540],[-60,620],[660,620],[660,1540]]),{fill:'#2f9e60',w:28,off:[0,0]});shape(B([[660,760],[880,760],[1060,1130],[1060,1540],[660,1540]]),{fill:'#f2c21b',w:28});for(const q of[170,860])shape(oval(q,1560,142,146,14),{fill:'#23242e',w:24,off:[0,0]});c.font='380px Marker';c.textAlign='center';c.textBaseline='middle';c.fillStyle='#ffe066';c.fillText('$',300,1080)})}
function quake(){let a=0;for(const[f,k]of[[22,12],[46,10],[52,10],[96,50],[138,6],[146,16],[149,22],[152,50],[186,10]])if(N>=f&&N<f+5)a+=k*(1-(N-f)/5);return[a*(N%2?1:-1),a*(N%2?-.7:.8)]}
window.vframe=n=>{N=n;S=7000+(n>>1)*131;const[sx,sy]=quake();c.setTransform(1,0,0,1,sx,sy);c.drawImage(PAPER,0,0,W,1600,-60,-60,W+120,H+120);
 T('WHO GETS PAID?',540,250,92,'#fff','center',24);
 // Employee row
 slam(18,200,R[0],()=>{empF();T('Employee',X,R[0]-48,66)});slam(22,X+120,R[0]+38,()=>T('+$3k',X,R[0]+38,122,G));
 if(n>=18&&n<34){const y=n<22?-170+(n-18)*140:R[0]+(n==22?18:n==23?-10:0);at(800,y,.3,()=>{c.translate(-540,-1400);shape([[430,1250],[370,1450],[470,1610],[620,1610],[730,1450],[650,1250]],{fill:'#d9b06e',w:18});shape([[468,1150],[612,1150],[650,1250],[430,1250]],{fill:'#c49a5c',w:15});c.font='190px Marker';c.textAlign='center';c.textBaseline='middle';c.fillStyle=INK;c.fillText('$',540,1440)})}
 if(n>=26&&n<36)T('mm.',620,R[0]-48,76,INK);
 // Freelancer row
 const fh=(n>=46&&n<49)||(n>=52&&n<55);slam(42,200,R[1],()=>{freeF(fh);T('Freelancer',X,R[1]-48,66)});slam(46,X+150,R[1]+38,()=>T('+$900',X,R[1]+38,122,G));
 for(const[f,dx]of[[46,50],[52,-40]]){const u=n-f;if(u>=-3&&u<7){const x=u<0?120+dx*.3:120+dx*(1+u*.8),y=u<0?R[1]-90+u*80:R[1]-90-u*44+u*u*16;shape(oval(x,y,28,u%3==1?10:28,10),{fill:'#ffc914',w:8,off:[0,0]})}}
 if(n>=46&&n<58)T('OW',n<52?640:790,R[1]-48,n<52?76:100,RED,'left',18);if(n>=58)shape(oval(185,R[1]-68,26,26,10),{fill:'#ffc914',w:8,off:[0,0]});
 // Founder row
 const k=(n>=68)+(n>=74)+(n>=80),hit=n>=96&&n<100;if(n>=66){slam(66,200,R[2],()=>{foundF(n>=96?0:k/3,hit);T('Founder',X,R[2]-48,66)})}
 [[235,68],[350,74],[465,80]].forEach(([x,f])=>slam(f,x+40,R[2]+40,()=>T('$0',x,R[2]+40,68,'#8d8d98')));
 for(const[a,b,f]of[[318,344,74],[433,459,80],[548,590,96]])if(n>=f){line([[a,R[2]+40],[b,R[2]+40]],8,'#6f6f7a');line([[b-14,R[2]+27],[b,R[2]+40],[b-14,R[2]+53]],8,'#6f6f7a')}
 slam(96,760,R[2]+36,()=>T('+$600k',606,R[2]+36,90,G));
 if(n>=90&&n<110){const tx=n<96?1400-(n-90)*95:n<100?830:830+(n-100)*140;truck(tx,R[2]-30,.15)}
 if(n>=96&&n<112){const u=n-96;for(let i=0;i<14;i++){const a=i*.45+.3,x=700+Math.cos(a*2)*(90+u*26),y=R[2]+Math.sin(a*2)*(40+u*16)+u*u*2;bill(x,y,a*2+u*.3,.42)}}
 if(n>=100&&n<112)T("I'm okay",630,R[2]-50,70,INK);
 // Divider + Vibe coder
 if(n>=108){const w=Math.min(1,(n-108)/3);line([[60,R[3]-122],[60+960*w,R[3]-128+6*(1-w)]],11)}
 slam(110,200,R[3],()=>{codF();T('Vibe coder',X,R[3]-46,66)});
 [[235,112],[425,116],[615,120],[805,124]].forEach(([x,f])=>slam(f,x+80,R[3]+22,()=>T('-$200',x,R[3]+22,54,RED)));
 if(n>=128)T('on AI tools',X,R[3]+88,54,RED);
 // Big coder, happy then shocked
 const up=n>=130,o={eyeL:66,eyeR:66,px:-.2,py:.3,pup:21,mouth:'grin',brow:18};
 if(up){o.px=0;o.py=-.7;o.mouth='frozen'}if(n>=136){o.eyeL=92;o.eyeR=92;o.pup=18;o.brow=38}if(n>=139){o.eyeL=118;o.eyeR=124;o.pup=13;o.brow=72;o.crack=1;o.gRot=.04;o.sweat=true}if(n>=142)o.mouth='flat';
 if(n>=146){o.mouth='jaw';o.jaw=110;o.gRot=.07;o.gDrop=10}if(n>=149){o.jaw=240;o.gRot=.11;o.gDrop=22}if(n>=152){o.jaw=n==152?400:n==153?360:380;o.gRot=.17;o.gDrop=36;o.brow=92;o.eyeL=128;o.eyeR=136}
 if(n>=156&&n<186)o.jaw=380+(n%3==0?-9:n%3==1?6:0);
 if(n>=186){o.mouth='grin';delete o.jaw;o.eyeL=66;o.eyeR=66;o.px=-.2;o.py=.3;o.pup=21;o.brow=20;o.crack=1;o.sweat=false;o.gRot=.17;o.gDrop=36}
 const bob=(n<130||n>=188)&&n%4>=2?-12:0;
 const K=[[0,.96,385],[15,.87,570],[39,.75,770],[63,.63,950],[105,.55,1225],[156,.5,1410]];let sc=K[0][1],tp=K[0][2];for(let i=1;i<K.length;i++){const[f,a,b]=K[i];if(n>=f){const d=i==5?2:3,u=Math.min(1,(n-f+1)/d),e=1-(1-u)**3;sc=K[i-1][1]+(a-K[i-1][1])*e;tp=K[i-1][2]+(b-K[i-1][2])*e}}
 at(540-sc*545,tp-sc*240+bob,sc,()=>coder(o));
 const ls=.6+(sc-.5)*.8;at(850-ls*900,1800-ls*1582,ls,()=>laptop(n));
 const pt=(s,x,y,col)=>{c.font='96px Marker';c.textAlign='left';c.textBaseline='middle';c.lineJoin='round';c.lineWidth=24;c.strokeStyle=INK;c.strokeText(s,x,y);c.fillStyle=col;c.fillText(s,x,y)};
 if(n>=156&&n<186){c.font='96px Marker';const L1=c.measureText('WAIT, YOU GUYS').width,A1=c.measureText('WAIT, ').width,L2=c.measureText('ARE GETTING PAID?').width,A2=c.measureText('ARE GETTING ').width,x1=540-L1/2,x2=540-L2/2;pt('WAIT,',x1,1190,'#fff');if(n>=164)pt('YOU GUYS',x1+A1,1190,'#fff');if(n>=170)pt('ARE GETTING',x2,1302,'#fff');if(n>=175)pt('PAID?',x2+A2,1302,'#ffc914')}
 if(n>=186){const a=n==186?1.25:1;at(800,1230,a,()=>{shape(B([[-190,-80],[190,-90],[200,90],[-20,90],[-100,170],[-90,90],[-200,90]]),{fill:'#fffdf4',w:11,off:[0,0]});c.fillStyle=INK;c.font='88px Marker';c.textAlign='center';c.textBaseline='middle';c.fillText('Thanks!',0,0)});T('promptanatomy.app',70,1240,40,'#5f6470')}
 return cv.toDataURL('image/jpeg',.94)};
