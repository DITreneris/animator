# Readability layer: bigger title bar with a year pill, and subtitles on a dark backing.
import math,v9
from v import *
BAR_Y,BAR_H=222,138
def topbar(c,f):
    if 60<=f<75:return
    cur=[y for y in v9.YEARS if y[0]<=f][-1];d=f-cur[0]
    c.rectangle(0,BAR_Y,W,BAR_H);c.set_source_rgba(.04,.05,.09,.92);c.fill()
    c.rectangle(0,BAR_Y+BAR_H-6,W,6);c.set_source_rgb(*YEL);c.fill()
    cy=BAR_Y+BAR_H/2-2
    txt(c,'ME + MY AI',560,cy,86,WHITE,lw=0,align='r')
    k=abs(math.cos(min(1,d/6)*math.pi)) if d<6 and cur[0]>0 else 1
    c.save();c.translate(760,cy);c.scale(1,max(.06,k))
    rr(c,-150,-52,300,104,26);c.set_source_rgb(*YEL);c.fill()
    txt(c,cur[1],0,0,90,INK,lw=0);c.restore()
SUB_Y=1640
def sub(c,f,a,b,t,size=92):
    if not a<=f<b:return
    k=max(.02,back((f-a)/4))
    c.save();c.translate(540,SUB_Y);c.scale(k,k)
    c.select_font_face('Lilita One');c.set_font_size(size);w=c.text_extents(t).width
    rr(c,-w/2-40,-size*.72,w+80,size*1.44,size*.4);c.set_source_rgba(.04,.05,.09,.72);c.fill()
    txt(c,t,0,0,size,WHITE,lw=size*.12);c.restore()
def badge(c):
    c.select_font_face('Lilita One');c.set_font_size(44);w=c.text_extents('promptanatomy.app').width+56
    rr(c,1040-w,BAR_Y+BAR_H+22,w,70,35);c.set_source_rgba(.04,.05,.09,.82);c.fill()
    txt(c,'promptanatomy.app',1040-w/2,BAR_Y+BAR_H+57,44,WHITE,lw=0)
def install():
    v9.topbar=topbar;v9.sub=sub;v9.badge=badge
