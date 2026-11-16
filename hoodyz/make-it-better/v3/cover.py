"""Cover thumbnail, 1080x1920: the strike wall, the title, and the guy still asking."""
import cairo, render, v
from v import *
s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(s)
render.rally(c,6,1.0,0,guyx=540,bot_x=170,expr='happy',paper=1,thumbk=1)
c.rectangle(0,0,W,H);c.set_source_rgba(0,0,0,.18);c.fill()
txt(c,'MAKE IT',540,1030,150,WHITE,lw=26)
txt(c,'BETTER',540,1190,172,hx('ffd84a'),lw=28)
v.topbar(c,'ON STRIKE')
s.write_to_png('make_it_better_cover.png')
