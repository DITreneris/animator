import sys,os,subprocess,cairo
import chars,v9,v
from v import *
chars.install()
import titles;titles.install()
import today;today.install()
import qafix;qafix.install()
# NOTAG=1: no burned-in promptanatomy.app chip (TODAY is also moved inside the frame, see qafix.py)
if os.environ.get('NOTAG')=='1':
    import v8
    v9.badge=v.badge=v8.badge=titles.badge=lambda c:None
import polish34;polish34.install()
PRE=('v34' if os.environ.get('V34')=='1' else '')+('n' if os.environ.get('NOTAG')=='1' else '')   # render file prefix   # V34=1: v3.4 polish (picture only)
def draw(f):
    chars.CURF=f;return v9.draw(f)
def sheet():
    S=cairo.ImageSurface(cairo.FORMAT_RGB24,1080,1920);c=cairo.Context(S)
    bg(c,hx('f7f2ea'),hx('e9dfcf'))
    txt(c,'CHARACTER SHEET',540,90,70,INK,lw=0)
    names=['calm','adoring','happy','panic','shock','offended','deadpan','sheepish','sideeye','proud']
    chars.GUY=[(-1,0,'calm',0)]
    for i,n in enumerate(names):
        x=110+(i%5)*215;y=360+(i//5)*320
        chars.CURF=1000;row=(0,99999,n,-14 if n=='sideeye' else 0)
        chars.GUY=[row];v.HAIR=(.25,.13,.09) if i<5 else (.72,.72,.76);v.BEARD=i>=5
        chars.head2(c,x,y,.7)
        if n=='proud':v9.ball(c,x,y+62*.7+4,19)
        txt(c,n.upper(),x,y+128,32,INK,lw=0)
    v.HAIR=(.25,.13,.09);v.BEARD=False
    txt(c,'GUY: 10 EXPRESSIONS (TOP: 2024, BOTTOM: 2027)',540,170,34,hx('66707f'),lw=0)
    txt(c,'ROBOT SCREEN FACES',540,1000,40,hx('66707f'),lw=0)
    for i,e in enumerate(['eyes','happy','love','wide','nope']):
        chars.CURF=1000;chars.robot2(c,130+i*205,1150,.62,emote=e)
        txt(c,e.upper(),130+i*205,1300,34,INK,lw=0)
    txt(c,'CAST',540,1400,40,hx('66707f'),lw=0)
    chars.CURF=1000;chars.GUY=[(0,99999,'calm',0)]
    v9.guyfull(c,160,1850,.6,'calm',1)
    v9.bot(c,370,1850,.75)
    v9.neighbor(c,610,1850,.55,0,sip=.3)
    v9.dog(c,790,1850,.9,'sit')
    v6t=__import__('v6');v6t.tester(c,960,1720,.5)
    S.write_to_png('character_sheet.png')
if __name__=='__main__':
    if sys.argv[1]=='sheet':sheet()
    elif sys.argv[1]=='frames':
        fs_=list(map(int,sys.argv[2:]))
        for f in fs_:draw(f).write_to_png(f'chk_{f:03d}.png')
        from PIL import Image
        S=Image.new('RGB',(6*300,((len(fs_)+5)//6)*534))
        for i,f in enumerate(fs_):S.paste(Image.open(f'chk_{f:03d}.png').convert('RGB').resize((300,534)),((i%6)*300,(i//6)*534))
        S.save('sheet.png')
    else:
        for n,a,b,fn in v9.SC:
            if len(sys.argv)>2 and n not in sys.argv[2:]:continue
            p=subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 12 -preset veryfast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -video_track_timescale 15360 tmp_{PRE}{n}.mp4'.split(),stdin=subprocess.PIPE)
            for f in range(a,b):p.stdin.write(bytes(draw(f).get_data()))
            p.stdin.close();assert p.wait()==0;os.rename(f'tmp_{PRE}{n}.mp4',f'{PRE}{n}.mp4');print(PRE+n,flush=True)
