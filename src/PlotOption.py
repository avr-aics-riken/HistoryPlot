#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:
# Author:      zrm
# Created:     11/06/2014
# Copyright:
# Licence:
#-------------------------------------------------------------------------------

class PlotOption(object):
    def __init__(self):
        self.figwidth = 10
        self.figheight= 10
        self.figdpi   = 80
        self.facecolor = 'w'
        self.edgecolor = 'k'
        self.drawcolor = 'k'
        self.drawwidth = 0.6
        self.figalpha = 1.0
        self.figcolor = 'w'

        self.title = ''
        self.titlecolor = 24
        self.width = 20
        self.titlefont  = 18

        self.labelcolor = 'blue'
        self.labelfont = 18
        self.xlabel= 'X'
        self.ylabel= 'Y'

        self.tickcolor = 'black'
        self.xtitlerot  = 0
        self.ytitlerot  = 0
        self.tickfont   = 16

        self.textflag = 0
        self.textposx = 0.5 # pct
        self.textposy = 0.5 # pct
        self.text = 'text'
        self.textfont = 16
        self.textcolor= 'red'
        self.textalpha= 0.5

        self.xrange = 0
        self.xmin = 0.0;
        self.xmax = 0.0;
        self.yrange = 0
        self.ymin = 0.0;
        self.ymax = 0.0;

        self.pngname = ''
        self.logscale = 0
    
    def set_logscale(self, zero_or_not):
        self.logscale = zero_or_not

    def set_xrange(self, amin, amax):
        self.xrange = 1;
        self.xmin = amin
        self.xmax = amax

    def set_yrange(self, amin, amax):
        self.yrange = 1;
        self.ymin = amin
        self.ymax = amax

    def set_pngname(self, pngname):
        self.pngname = pngname

    def set_tick(self, color, font, rotx, roty):
        self.tickcolor = color
        self.xtitlerot = rotx
        self.ytitlerot = roty
        self.tickfont  = font

    def set_text(self, text, posx=0.5, posy=0.5, font=16, color='k', color_bg='green', alpha=0.5):
        self.textflag = 1
        self.textposx = posx
        self.textposy = posy
        self.text = text
        self.textfont = font
        self.textcolor= color
        self.textcolor_gb = color_bg
        self.textalpha= alpha

    def set_draw(self, drawcolor, edgecolor, drawwidth):
        self.drawcolor = drawcolor
        self.edgecolor = edgecolor
        self.drawwidth = drawwidth

    def set_figcolor(self, color, alpha):
        self.figalpha = alpha
        self.figcolor = color

    def set_figsize(self, width, height):
        self.figwidth = width
        self.figheight= height

    def set_title(self, title, font, color):
        self.title = title
        self.titlefont = font
        self.titlecolor = color

    def set_label(self, xlabel, ylabel, font, color):
        self.xlabel= xlabel
        self.ylabel= ylabel
        self.labelfont = font
        self.labelcolor = color


