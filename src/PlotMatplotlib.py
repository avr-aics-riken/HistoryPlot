#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:
# Author:      zrm
# Created:     11/06/2014
# Copyright: AICS, RIKEN
# Licence: New BSD (2-caluse)
#-------------------------------------------------------------------------------

import ParamDef as param
#--------------------------------------------------------------
def utf(any_str):
        if param.G_DECODE_STR == 1 : new_str = any_str.decode('utf-8')
        else: new_str = any_str
        return new_str
#--------------------------------------------------------------

import matplotlib

#Please use 'Agg' If it issues following error
#"no display name and no $DISPLAY environment"
#
#Agg is a non-interactive backend, meaning it won't display
#on the screen, Show() does not work, it only save to files.

if param.G_USE_AGG == 1: matplotlib.use('Agg')

import matplotlib.font_manager as font_manager
import matplotlib.patches as patches
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt

import numpy as np
import sys

from matplotlib.patches import Polygon

from Quantile import *

# 日本語fontの設定
g_fontsize = 18

if   param.G_WINDOWS == 1:
        # for Windows
        #ttfフォントでない場合、pdf と eps 作成できません、'konatu.ttf'を使用します。
        #font_path = 'C:/WINDOWS/Fonts/meiryo.ttc' 
        font_path = 'konatu.ttf'
        #  -----------------------------------------------------------------
        # 『小夏』("Konatu") Copyright (C) 2002〜 桝田道也 All rights reserved.
        #  http://avoidnotes.org/urlmemo/cache/20050722191344.html#about
        # 『小夏』のライセンスはver.26（2010-01）までは CC-BY-SA 3.0 でしたが、
        #  ver.20121218 から The MIT License に変更しました。 
        #  -----------------------------------------------------------------
elif param.G_MACOSX == 1:
        # for Mac
        font_path = '/Library/Fonts/Osaka.ttf'
elif param.G_LINUX_K == 1 :
        # for Linux of K-Computer
        font_path = '/Please/Specify/ProperFont.ttf'
elif param.G_LINUX_FOCUS == 1 :
        # for Linux of FOCUS
        font_path = '/Please/Specify/ProperFont.ttf'
else:
        # for CentOS
        font_path = '/usr/share/fonts/ja/TrueType/kochi-gothic-subst.ttf'
        
g_font_prop = font_manager.FontProperties(fname=font_path)
g_font_prop.set_style('normal')
g_font_prop.set_weight('light')
g_font_prop.set_size(g_fontsize)

#--------------------------------------------------------------
def set_rect_color(rect, color, alpha):
        rect.set_facecolor(color)
        rect.set_alpha(alpha)

def set_tick_xlabel(ax, color, font, rot):
        for label in ax.get_xticklabels():
            label.set_color(color)
            label.set_rotation(rot)
            label.set_fontsize(font)

def set_tick_ylabel(ax, color, font, rot):
        for label in ax.get_yticklabels():
            label.set_color(color)
            label.set_rotation(rot)
            label.set_fontsize(font)
	
#--------------------------------------------------------------
def draw_barplot(x_data, y_data, opt, graph_type, finalize, mute):

        #　図の縦、横を定義する
        fig = plt.figure( num=0,                                \
                          figsize=(opt.figwidth, opt.figheight),\
                          dpi=opt.figdpi,                       \
                          facecolor=opt.facecolor,              \
                          edgecolor=opt.edgecolor,              \
                         )

        #　図を作成する
        handles = 0

        if graph_type == 'bar' :
                handles, = plt.bar(x_data, y_data,             \
                        facecolor=opt.drawcolor,    \
                        edgecolor=opt.edgecolor,    \
                        width=opt.drawwidth,        \
                        label='----',               \
                        align='center'              \
                        )
        else:
                handles, = plt.plot(x_data, y_data,
                         color=opt.drawcolor,
                         linewidth=opt.drawwidth,
                         linestyle='-'
                         )

        #　図の枠範囲の色と透明度を指定する
        set_rect_color( fig.patch, opt.figcolor, opt.figalpha )

        #　図のタイトルを設定する
        plt.title(  opt.title,
                    fontsize=opt.titlefont,
                    color=opt.titlecolor,
                    fontproperties=g_font_prop
                 )

        #　縦、横軸の範囲、ラベル、色、フォントサイズを設定する
        plt.xlabel(opt.xlabel, fontsize=opt.labelfont,
                   color=opt.labelcolor, fontproperties=g_font_prop)

        plt.ylabel(opt.ylabel, fontsize=opt.labelfont,
                   color=opt.labelcolor, fontproperties=g_font_prop)

        x_min = np.amin(x_data)
        x_max = np.amax(x_data)

        y_min = np.amin(y_data)
        y_max = np.amax(y_data) * 1.1 # make margin for showing text at top

        if opt.xrange > 0 :
            plt.xlim(xmin=opt.xmin)
            plt.xlim(xmax=opt.xmax)
            x_min = opt.xmin
            x_max = opt.xmax

        if opt.yrange > 0 :
            plt.ylim(ymin=opt.ymin)
            plt.ylim(ymax=opt.ymax)
            y_min = opt.ymin
            y_max = opt.ymax

        #　図の一部をハイライトする方法
        opacity = 0.001
        #縦ハイライト範囲
        plt.axvspan(x_max*0.25, x_max*0.75, color='red',  alpha=opacity)
        #横ハイライト範囲
        plt.axhspan(y_max*0.25, y_max*0.75, color='blue', alpha=opacity)

        #　図の範囲の色、軸の刻みのラベルの色、フォント、回転を指定する
        #ax = fig.add_subplot(111, axisbg='darkslategray')
        ax = fig.add_subplot(111)

        # 画像をグラフに入れる　テスト！
        #image_file = cbook.get_sample_data('C:\\_ZrmData\\ffv_ono_graph\\logo.png')
        #image = plt.imread(image_file)
        #im = ax.imshow(image)
        #patch = patches.Circle((260, 200), radius=200, transform=ax.transData)
        #im.set_clip_path(patch)

        set_rect_color( ax.patch, 'white', 1.0 )

        set_tick_xlabel(ax, opt.tickcolor, opt.tickfont, opt.xtitlerot)
        set_tick_ylabel(ax, opt.tickcolor, opt.tickfont, opt.ytitlerot)

        #handles, labels = ax.get_legend_handles_labels()
        #ax.legend(handles, labels)

        #ax.fill(x_data,y_data, 'b' )

        if opt.logscale > 0 :
                ax.set_yscale('log')

        #　文字箱を作成する
        if opt.textflag > 0 :
                g_font_prop.set_size(opt.textfont)
                ax.text( x_max*opt.textposx,                    \
                         y_max*opt.textposy,                    \
                         opt.text,                              \
                         style='italic',                        \
                         fontproperties=g_font_prop,            \
                         fontsize=opt.textfont,                 \
                         bbox={'facecolor':opt.textcolor,       \
                               'alpha':opt.textalpha,           \
                               'pad':opt.textfont}              \
                         )
                g_font_prop.set_size(g_fontsize)

        # savefig() must be called before show(), otherwise, blank image.
        if len(opt.pngname) >=8 : # The shortest pngname C:\a.png
                plt.savefig(opt.pngname, bbox_inches="tight", pad_inches=0.15)

        #plt.legend(loc='upper right')

        if finalize > 0 :
                if mute <= 0 :  plt.show()
                else :          plt.clf()

        return handles

#--------------------------------------------------------------
def draw_boxplot_a(list_of_data_array, xticks, xticklabels, rot, opt, mute):

        fig, ax1 = plt.subplots(figsize=(opt.figwidth, opt.figheight))

        fig.canvas.set_window_title(opt.title)

        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

        bp = plt.boxplot(list_of_data_array, notch=0, sym='+', vert=1, whis=1.5)

        plt.setp(bp['boxes'],    color='black') # 箱の輪郭
        plt.setp(bp['whiskers'], color='blue')  # 中央値の線
        plt.setp(bp['fliers'],   color='lightgrey', marker='+')# 異常値の点

        ax1.yaxis.grid(True, linestyle='-', which='major',
                       color='lightgrey', alpha=0.5)

        ax1.set_axisbelow(True) # グリッド線を図の下に置く

        ax1.set_title(opt.title, fontsize=opt.titlefont,
                      color=opt.titlecolor, fontproperties=g_font_prop)

        ax1.set_xlabel(opt.xlabel, fontsize=opt.labelfont,
                       color=opt.labelcolor, fontproperties=g_font_prop)

        ax1.set_ylabel(opt.ylabel, fontsize=opt.labelfont,
                       color=opt.labelcolor, fontproperties=g_font_prop)

        boxColors = ['darkkhaki','royalblue']
        numBoxes = len(list_of_data_array)
        medians = range(numBoxes)
        for i in range(numBoxes):
            box = bp['boxes'][i]

            boxX = []
            boxY = []
            for j in range(5):
                    boxX.append(box.get_xdata()[j])
                    boxY.append(box.get_ydata()[j])
                    boxCoords = zip(boxX,boxY)

            k = i % 2 # 二つの色を切り替える
            boxPolygon = Polygon(boxCoords, facecolor=boxColors[k], alpha=0.5)

            ax1.add_patch(boxPolygon)

        x_min = 0
        x_max = len(xticks)

        y_min = np.amin(list_of_data_array)
        y_max = np.amax(list_of_data_array)

        if opt.xrange > 0 :
            x_min = opt.xmin
            x_max = opt.xmax
            plt.xlim(xmin=opt.xmin)
            plt.xlim(xmax=opt.xmax)

        if opt.yrange > 0 :
            y_min = opt.ymin
            y_max = opt.ymax
            plt.ylim(ymin=opt.ymin)
            plt.ylim(ymax=opt.ymax)

        plt.xticks(xticks, xticklabels, rotation=75,
                   fontsize=opt.tickfont, color=opt.tickcolor)

        plt.yticks(fontsize=opt.tickfont, color=opt.tickcolor)

        # 中央値を計算し、図の上に中央値を表示する
        b_show_median = 1
        if b_show_median > 0 :
                ii=0
                for array in list_of_data_array:
                    medians[ii] = quantile(array, 0.5, g_qtype)
                    ii=ii+1

                top = y_max
                pos = np.arange(numBoxes)+1
                upperLabels = [str(np.round(s, 2)) for s in medians]
                weights = ['bold', 'semibold']
                for tick,label in zip(range(numBoxes),ax1.get_xticklabels()):
                   k = tick % 2
                   ax1.text(    pos[tick], top-(top*0.05),
                                upperLabels[tick],
                                horizontalalignment='center',
                                size='x-small',
                                weight=weights[k],
                                color=boxColors[k])

        if opt.textflag > 0 :
                g_font_prop.set_size(opt.textfont)
                plt.figtext(opt.textposx,
                            opt.textposy,
                            opt.text ,
                            fontproperties=g_font_prop,
                            backgroundcolor='lightgrey',
                            color=opt.textcolor,
                            weight='roman',
                            fontsize=opt.textfont,
                            bbox={'facecolor':opt.textcolor_gb,
                                  'alpha':opt.textalpha,
                                  'pad':opt.textfont}
                            )
                g_font_prop.set_size(g_fontsize)

        # savefig() must be called before show(), otherwise, blank image.
        if len(opt.pngname) >=8 : # The shortest pngname C:\a.png
                plt.savefig(opt.pngname, bbox_inches="tight", pad_inches=0.15)

        if mute <= 0 : plt.show()
        else :         plt.clf()

        return

def draw_boxplot(list_of_data_array, xticks, xticklabels, rot, opt, mute):

        draw_boxplot_a(list_of_data_array, xticks, xticklabels, rot, opt, mute)

        return

        #　図の縦、横を定義する
        fig = plt.figure( num=0,                                \
                          figsize=(opt.figwidth, opt.figheight),\
                          dpi=opt.figdpi,                       \
                          facecolor=opt.facecolor,              \
                          edgecolor=opt.edgecolor,              \
                         )

        plt.boxplot( list_of_data_array, 0, '' )

        #そうしないと、横軸のTickLabelがははみ出していまう。
        plt.tight_layout(pad=15)

        #　図の枠範囲の色と透明度を指定する
        set_rect_color( fig.patch, opt.figcolor, opt.figalpha )

        #　図のタイトルを設定する
        plt.title(opt.title, fontsize=opt.titlefont,
                  color=opt.titlecolor, fontproperties=g_font_prop)

        #　縦、横軸の範囲、ラベル、色、フォントサイズを設定する
        plt.xlabel(opt.xlabel, fontsize=opt.labelfont,
                   color=opt.labelcolor, fontproperties=g_font_prop)

        plt.ylabel(opt.ylabel, fontsize=opt.labelfont,
                   color=opt.labelcolor, fontproperties=g_font_prop)

        x_min = 0
        x_max = len(xticks)

        y_min = np.amin(list_of_data_array)
        y_max = np.amax(list_of_data_array)

        plt.xticks(xticks, xticklabels, rotation=75,
                   fontsize=opt.tickfont, color=opt.tickcolor)

        plt.yticks(fontsize=opt.tickfont, color=opt.tickcolor)

        if opt.xrange > 0 :
            x_min = opt.xmin
            x_max = opt.xmax
            plt.xlim(xmin=opt.xmin)
            plt.xlim(xmax=opt.xmax)

        if opt.yrange > 0 :
            y_min = opt.ymin
            y_max = opt.ymax
            plt.ylim(ymin=opt.ymin)
            plt.ylim(ymax=opt.ymax)

        #　図の範囲の色、軸の刻みのラベルの色、フォント、回転を指定する
        ax = fig.add_subplot(111)
        set_rect_color( ax.patch, 'white', 1.0 )

        #　文字箱を作成する
        if opt.textflag > 0 :
                g_font_prop.set_size(opt.textfont)
                ax.text( x_max*opt.textposx,                    \
                         y_max*opt.textposy,                    \
                         opt.text,                              \
                         style='italic',                        \
                         fontproperties=g_font_prop,            \
                         fontsize=opt.textfont,                 \
                         bbox={'facecolor':opt.textcolor,       \
                               'alpha':opt.textalpha,           \
                               'pad':opt.textfont}              \
                         )
                g_font_prop.set_size(g_fontsize)

        # マージンをセットする
        b_set_margin = 0
        if b_set_margin > 0 :
                plot_margin_x = x_max * 0.02
                plot_margin_y = y_max * 0.02
                x0, x1, y0, y1 = plt.axis()
                plt.axis((x0 - plot_margin_x,
                          x1 + plot_margin_x,
                          y0 - plot_margin_y,
                          y1 + plot_margin_y))

        # savefig() must be called before show(), otherwise, blank image.
        if len(opt.pngname) >=8 : # The shortest pngname C:\a.png
                plt.savefig(opt.pngname, bbox_inches="tight", pad_inches=0.15)

        if mute <= 0 : plt.show()
        else :          plt.clf()
