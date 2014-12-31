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

# PyScripterを使用している際に、ファイルを shift_jis で保存して下さい

# If you are using PyScripter, and your file contains
# japanease font, please save file using Shift-JIS format.

import sys

from PlotOption import *

import optparse

import ParamDef                 as param
import FileIOColumnData         as io
import PlotMatplotlib           as my_plt
import matplotlib.pyplot        as plt

from Quantile import *

g_colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']

#--------------------------------------------------------------
def verify_filename(filename):
        s = filename
        s = s.replace("/", "_")
        s = s.replace("|", "_")
        s = s.replace(".", "_")
        s = s.replace("*", "_")
        s = s.replace(":", "_")
        return s

#--------------------------------------------------------
def config_parser() :
        parser = optparse.OptionParser()

        #値を入力するための引数
        parser.add_option('-f', '--file',
                          dest="input_file",
                          help="input file name",
                          default="",
                          )  #文字列
        parser.add_option('-x', '--xindex',
                          dest="x_index",
                          help="column index used as X data",
                          default="0",
                          action="store",
                          type="int"
                          )  #整数
        parser.add_option('-y', '--yindex',
                          dest="y_index",
                          help="column index(indices) used as Y data, e.g. 1 2 3-8",
                          default="",
                          )  #文字列
        parser.add_option('-t', '--title',
                          dest="title",
                          help="title of the plot, by default, it is input file name",
                          default="",
                          )  #文字列
        parser.add_option('-l', '--ylabel',
                          dest="y_label",
                          help="label of Y axis",
                          default="",
                          )  #文字列

        '''
        parser.add_option('-b',
                          dest="b",
                          action="store",
                          type="float")  #浮点小数
        parser.add_option('-c',
                          dest="c",
                          action="store",
                          type="int")  #整数
        '''
        
        #スイッチ類の引数
        parser.add_option('--log', '--logy',
                          dest="log_yscale",
                          help="switch for logarithmic y-scale",
                          action="store_true",
                          default=False)
        '''
        parser.add_option('--logx',
                          dest="log_xscale",
                          help="switch for logarithmic x-scale",
                          action="store_true",
                          default=False)

        parser.add_option('-a',
                          dest="a",
                          action="store_true", 
                          default=False)
        '''
        return parser

#------- main() -----------------------------------------
if __name__ == '__main__':

        parser = config_parser()
        
        options, remainder = parser.parse_args()

        print '---------------[ optparse ]-------------------------'
        print 'INPUT_FILE : -f or --file  \t', options.input_file
        print 'PLOT_TITLE : -t or --title \t', options.title
        print 'X_INDEX    : -x or --xindex\t', options.x_index
        print 'Y_INDEX    : -y or --yindex\t', options.y_index
        print 'Y_LABEL    : -l or --ylabel\t', options.y_label
        print 'LOG_YSCALE : --log or --logy\t', options.log_yscale
        print 'LOG_XSCALE : --logx        \t', options.log_xscale
        
        #print '-a bool  :', options.a
        #print '-b float :', options.b
        #print '-c int   :', options.c
        print '----------------------------------------------------'

        if options.y_index == '' :
                print u'\nエラー: Y データのカラム index を入力して下さい。例：-y 3 5-7\n'
        if options.input_file == '' :
                print u'\nエラー: 入力ファイル名を指定して下さい。例：-f history_force.txt\n'
        
        y_index_dict = {}

        value_s = options.y_index.strip().split(' ')
        for str_s in value_s :
                if str_s.find('-') > -1:
                        sub_str_s = str_s.strip().split('-')
                        a = (int)(sub_str_s[0])
                        b = (int)(sub_str_s[1])
                        for c in range(a, b+1) :
                                y_index_dict[c] = 0
                                #print 'value=', c
                else:
                        y_index_dict[int(str_s)] = 0
                        #print 'value=', str_s
        print 'specified y_index = ', y_index_dict        

        #Examples: 
        #PlotColumnData.py -f history_force.txt --yindex "2 3 4-5" --log 1
        #PlotColumnData.py -f history_force.txt -y"2 3 4-5"
        #PlotColumnData.py -f history_force.txt -y "2 3 4-5" -l
        #PlotColumnData.py -f history_force.txt -y "2 3 4-5" --log 1
        #PlotColumnData.py -f history_force.txt -y "2 3 4-5" -l -x 1 -b 1.2 -c 3
        #PlotColumnData.py --file history_force.txt -y "2 3 4-5" -l -x 1 -b 1.
        #PlotColumnData.py --file history_force.txt -y "2 3 4-5" -x 1 -b 1.2 -c 3 --log
        #PlotColumnData.py --file history_force.txt -y "2 3 6-11 16" -x 1 -b 1.2 -c 3 --log
        #PlotColumnData.py --file history_force.txt -y "2 3 6-11 8-16" -x 1 -b 1.2 -c 3 --log
        
        print u'\n'

        ########### Default Setting ################
        filename        = options.input_file
        graph_title     = options.title
        y_label         = options.y_label
        x_index         = options.x_index
        
        if options.log_yscale == True:
                y_log=1
        else:
                y_log=0
        ############################################

        if graph_title == '' : graph_title = filename
        if y_label == '' : y_label = 'Value[--]'

        ############### Load Data ##################
        column_names = []
        data_dict, column_names = io.load_data(filename, 'Column_Data_00', column_names)
        ############################################

        n_names = len(column_names)
        print 'column_names=', column_names, 'n=', n_names

        """
        To be here, we have a dictionary containing all data

        step      time[sec]       Fx[04]        Fy[04]        Fz[04]
        1   1.666667e-01   6.3148e-02   -3.0289e-10    0.0000e+00
        2   3.333333e-01   1.1352e-02   -5.7448e-09    0.0000e+00
        3   5.000000e-01   3.2546e-03   -1.9197e-08    0.0000e+00
        ... ... ...
        """

        x_label = column_names[x_index]

        ############ 作図仕様 ##########################
        #----------------------------------------------
        #出力PNG画像ファイル名中に使えない文字を '_' に置換
        png_name = 'image_plot' + graph_title
        png_name = verify_filename(png_name)
        png_name = png_name + '.png'
        
        # 作図仕様を指定する
        opt2 = PlotOption()
        opt2.set_figsize( 10, 7 )
        opt2.set_title( graph_title, 20, 'green' )
        opt2.set_label( x_label, y_label, 18, 'blue' )
        #opt2.set_xrange( 0, n_max )
        #opt2.set_yrange( 0, 0.025 )
        #opt2.set_draw( 'b', 'k', 0.6 )
        #opt2.set_text( graph_title, 0.80, 0.90, 16, 'red', 0.3 )
        #opt2.set_figcolor( 'lightgoldenrodyellow', 0.2 )
        #opt2.set_tick( 'red', 16, 0, 0 )
        opt2.set_pngname(png_name)
        opt2.set_logscale(y_log)
        # ------------------------------------------------

        mute = 0     #if 1, 図が表示されません、画像が出力されます。     
        finalize = 0 #複数の Column データを同じ図に入れますので、0のままにする。
        
        ############ データ配列の準備、作図 #################
        legend_text = []
        for the_y_index in y_index_dict:
                if the_y_index < n_names :
                        column_name = column_names[the_y_index];
                        print 'plot: ', column_name, 'the_y_index=', the_y_index

                        legend_text.append(column_name)
                        
                        x_data = []
                        y_data = []
                        for step in data_dict:
                                sequence_vec = data_dict[step]

                                xx = float(sequence_vec[0, x_index])
                                x_data.append(xx)

                                yy = float(sequence_vec[0, the_y_index])
                                y_data.append(yy)

                        Min = np.amin(y_data)                   #minmum
                        Max = np.amax(y_data)                   #maxmum
                        Avg = np.average(y_data)                #average
                        #print 'Max=', Max, 'Min=', Min, 'Avg=', Avg
                        
                        Q1 = quantile(y_data, 0.25, g_qtype)   #first  quartile (Q1)
                        Mid= quantile(y_data, 0.50, g_qtype)   #middle quartile (Mid)
                        Q3 = quantile(y_data, 0.75, g_qtype)   #third  quartile (Q3)
                        #print 'Q3=', Q3, 'Mid=', Mid, 'Q1=', Q1

                        #opt2.set_yrange( -0.007, 0.007 )

                        #線の太さは 1.6 固定、色は８色巡回
                        opt2.set_draw( g_colors[the_y_index % 8], 'k', 1.6 )

                        my_plt.draw_barplot(x_data, y_data, opt2, 'xy', finalize, mute)

                        x_data[:] = []
                        y_data[:] = []

        print 'Draw legend, Save Png, Show Graph'
        
        #凡例を表示し、画像を出力します。
        plt.legend(legend_text)
        plt.savefig(opt2.pngname, bbox_inches="tight", pad_inches=0.15)

        #図を表示します。（mute=1の場合、何も表示しません）
        if mute==0: plt.show()

