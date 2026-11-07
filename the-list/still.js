const T=(s,x,y,sz,col=INK,al='left',st=0)=>{c.font=sz+'px Marker';c.textAlign=al;c.textBaseline='middle';if(st){c.lineJoin='round';c.lineWidth=st;c.strokeStyle=INK;c.strokeText(s,x,y)}c.fillStyle=col;c.fillText(s,x,y)};
const at=(x,y,s,f)=>{c.save();c.translate(x,y);c.scale(s,s);f();c.restore()};
const B=a=>a.flatMap(q=>[q,q]);
const R=[395,585,775,1000];
window.draw=()=>{S=4242;HAIR.splice(Math.floor(HAIR.length*.75));c.setTransform(1,0,0,1,0,0);c.fillStyle='#f5efdf';c.fillRect(0,0,W,H);c.drawImage(PAPER,0,0,W,1640,0,0,W,1640);c.fillStyle='#f5efdf';c.fillRect(0,1630,W,300);
 T('WHO GETS PAID?',540,250,92,'#fff','center',24);
 // employee face
 at(120,R[0],.2,()=>{c.translate(-540,-700);shape([[280,360],[800,360],[830,860],[770,1030],[310,1030],[250,860]],{fill:'#d99a6c',w:30});shape([[272,420],[300,320],[780,310],[820,420],[800,470],[300,470]],{fill:'#4a4650',w:20});for(const x of[410,670]){shape(oval(x,650,74,74,11),{fill:'#fffdf5',w:18,off:[0,0]});c.fillStyle=INK;c.beginPath();c.arc(x,682,22,0,7);c.fill();shape([[x-80,650],[x,650],[x+80,650],[x+74,574],[x,566],[x-74,574]],{fill:'#bf8a60',w:14,off:[0,0],two:false})}line([[450,890],[540,896],[630,886]],24)});
 // freelancer face + coin
 at(120,R[1],.2,()=>{c.translate(-540,-740);shape(oval(540,430,100,86,12),{fill:'#a2472b',w:22});shape([[260,760],[340,520],[540,450],[760,520],[820,760],[760,1010],[540,1100],[320,1010]],{fill:'#f7c7a6',w:28});shape([[258,740],[290,510],[540,430],[790,510],[822,740],[720,590],[540,550],[360,590]],{fill:'#b5532f',w:20});for(const x of[420,660]){shape(oval(x,720,70,76,11),{fill:'#fffdf5',w:16,off:[0,0]});c.fillStyle=INK;c.beginPath();c.arc(x+4,690,22,0,7);c.fill()}shape([[370,880],[450,900],[630,900],[710,875],[680,950],[620,980],[460,980],[400,950]],{fill:'#fffdf5',w:18,off:[0,0]})});
 shape(oval(185,R[1]-68,26,26,10),{fill:'#ffc914',w:8,off:[0,0]});
 // founder face crying
 at(120,R[2]-14,.18,()=>{c.translate(-540,-720);shape([[230,560],[340,420],[740,420],[850,560],[870,840],[760,1070],[320,1070],[210,840]],{fill:'#efb48c',w:28});shape([[214,560],[300,350],[780,330],[870,560],[740,460],[340,470]],{fill:'#d9a441',w:20});for(const x of[390,690]){shape([[x-70,690],[x,640],[x+70,690],[x,716]],{fill:'#fffdf5',w:14,off:[0,0]});shape([[x-46,710],[x+46,710],[x+56,1120],[x,1170],[x-56,1120]],{fill:'#7ed4ff',w:16,off:[0,0]})}shape([[420,840],[540,780],[660,840],[640,960],[540,1000],[440,960]],{fill:'#6d1f35',w:16,off:[0,0]})});
 // coder face happy
 at(120,R[3]+6,.22,()=>{c.translate(-548,-760);shape([[352,620],[432,450],[640,446],[744,610],[748,850],[666,1046],[430,1052],[346,860]],{fill:SKIN,w:26});c.save();c.translate(548,440);for(const h of HAIR)ink(wob(smooth(h.pts,false),1.6),h.w*2,h.col);c.restore();for(const[x,y]of[[446,700],[644,684]]){shape(oval(x,y,66,74,12),{fill:'#fffdf5',w:18,off:[0,0]});c.fillStyle=INK;c.beginPath();c.arc(x-22,y,24,0,7);c.fill()}shape([[388,842],[470,866],[620,862],[706,830],[688,958],[620,1012],[468,1014],[408,958]],{fill:'#6d1f35',w:18,off:[0,0]});shape([[394,848],[470,870],[620,866],[700,836],[690,884],[620,906],[470,908],[404,890]],{fill:'#fffdf5',w:10,off:[0,0],two:false})});
 const X=235;
 T('Employee',X,R[0]-48,66);T('+$3k',X,R[0]+38,122,'#179c58');
 T('Freelancer',X,R[1]-48,66);T('+$900',X,R[1]+38,122,'#179c58');
 T('Founder',X,R[2]-46,66);for(const x of[235,350,465])T('$0',x,R[2]+40,68,'#8d8d98');for(const[a,b]of[[318,344],[433,459],[548,590]]){line([[a,R[2]+40],[b,R[2]+40]],8,'#6f6f7a');line([[b-14,R[2]+27],[b,R[2]+40],[b-14,R[2]+53]],8,'#6f6f7a')}T('+$600k',606,R[2]+36,90,'#179c58');
 line([[60,R[3]-122],[1020,R[3]-128]],11);
 T('Vibe coder',X,R[3]-46,66);T('-$200 -$200 -$200 -$200',X,R[3]+22,54,'#e8263f');T('on AI tools',X,R[3]+88,54,'#e8263f');
 // small props
 // punchline
 T('WAIT, YOU GUYS',540,1190,96,'#fff','center',24);T('ARE GETTING PAID?',540,1302,96,'#ffc914','center',24);
 at(540-.5*545,1430-.5*280,.5,()=>coder({eyeL:128,eyeR:136,px:0,py:-.6,pup:13,mouth:'jaw',jaw:380,brow:92,hairS:0,crack:1,gRot:.17,gDrop:36,sweat:true}));
 return cv.toDataURL('image/png')};
