# QA fixes for v3.3: captions out of the app's caption area, right-side content clear of the action buttons,
# clean robot push-back arm, only two texts in the opening.
import os,chars,v9,titles,today
def install():
    titles.SUB_Y=1450
    from v import txt,RED
    _tb=titles.topbar
    def topbar(c,f):
        _tb(c,f)
        if f<60 or 285<=f<315:
            txt(c,'TODAY',985,titles.BAR_Y+titles.BAR_H/2,40,RED,lw=0) if os.environ.get('NOTAG')=='1' else txt(c,'TODAY',1012,titles.BAR_Y+titles.BAR_H/2,44,RED,lw=0)   # NOTAG: Y clear of the right edge
    v9.topbar=topbar
    _dog,_nb,_ball,_rarm=v9.dog,v9.neighbor,v9.ball,v9.rarm
    def dog(c,x,gy,s,*a,**k):
        if 540<=chars.CURF<720:x-=70
        return _dog(c,x,gy,s,*a,**k)
    def nb(c,x,gy,s,*a,**k):
        if 540<=chars.CURF<720:x-=40
        return _nb(c,x,gy,s,*a,**k)
    def ball(c,x,y,*a,**k):
        f=chars.CURF
        if (f<60 or 285<=f<315) and x>860:x-=130
        return _ball(c,x,y,*a,**k)
    def rarm(c,pts,w,*a):
        if pts[0]==(1100,1500):pts=[(1130,pts[-1][1]-18),pts[-1]]
        return _rarm(c,pts,w,*a)
    v9.dog,v9.neighbor,v9.ball,v9.rarm=dog,nb,ball,rarm
    _sub=titles.sub
    def sub(c,f,a,b,t,*x,**k):
        if f<60 or 285<=f<315:titles.SUB_Y=1300      # hook: above the dragged guy
        elif 75<=f<210:titles.SUB_Y=560              # 2024: in the open wall space
        elif 315<=f<540:titles.SUB_Y=1585            # office: on the desk front, under the button
        else:titles.SUB_Y=1450                       # 2027: between the robot's legs and the dog
        return _sub(c,f,a,b,t,*x,**k)
    v9.sub=sub
