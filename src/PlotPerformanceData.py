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
from Quantile   import *

import ParamDef         as param
import FileIO           as io
import PlotMatplotlib   as my_plt
import Quantile         as q

#--------------------------------------------------------------
def verify_filename(filename):
        s = filename
        s = s.replace("/", "_")
        s = s.replace("|", "_")
        s = s.replace(".", "_")
        s = s.replace("*", "_")
        s = s.replace(":", "_")
        return s

#--------------------------------------------------------------
def get_value(my_dict, func_name, val_name, index):
        sequence_vec = my_dict[func_name]
        values = sequence_vec[index]
        i = io.g_dict[val_name]
        value = values[i]
        #print func_name, val_name, '\t value = ', value
        return value

#--------------------------------------------------------------
def get_array(my_dict, func_name, val_name):
        values = []
        sequence_vec = my_dict[func_name]
        num = len(sequence_vec)
        for i in range(0, num):
                value = get_value(my_dict, func_name, val_name, i)
                values.append(value)
        return values

# -------------------------------------------------------------------
#　箱ひげ図作図
def create_boxplot(my_dict, func_names, val_name, mute=0):

        print u'箱ひげ図作図', val_name

        ticks = []
        labels = []
        list_of_data_array = []
        array_dict = {} # for sorting

        # 分位数を計算するアルゴリズムを指定する「mode-based method,(S, S-Plus)」
        q.g_qtype = 7

        # -----------------------------------------------------------
        # 作図仕様を指定する(箱ひげ図)
        sortby = q.IQR_VAL  #ソートする値を指定する

        # 配列のデータと中央値をarray_dictに格納する。後で中央値でソートする。
        if len(func_names) > 0 :
                for func_name in func_names:
                        array = get_array( my_dict, func_name, val_name )
                        calculate_Median_Q1_Q3( array )
                        array_dict[func_name] = g_Values[sortby]
        else:
                for func_name in my_dict:
                        array = get_array( my_dict, func_name, val_name )
                        calculate_Median_Q1_Q3( array )
                        array_dict[func_name] = g_Values[sortby]

        # 中央値で array_dict をソート(降順)する
        print u'中央値で array_dict をソート(降順)する'

        # -----------------------------------------------------------
        # 作図仕様を指定する(箱ひげ図)
        n_max = 25 # n_max を任意に指定できます、負の場合、array_dictの全て

        ii = 1
        for func_name, median_val in sorted(array_dict.items(), key=lambda x:x[1], reverse=True):
            #print func_name, '\t\t', median_val
            array = get_array( my_dict, func_name, val_name )
            list_of_data_array.append(array)
            labels.append(func_name)
            ticks.append(ii)
            ii = ii + 1
            if ii == n_max : break

        if n_max > 0 :  n_data = n_max
        else :          n_data = len(ticks)

        #出力PNG画像ファイル名中に使えない文字を '_' に置換
        png_name = 'image_boxplot_' + val_name
        png_name = verify_filename(png_name)
        png_name = png_name + '.png'

        # -----------------------------------------------------------
        # 作図仕様を指定する(箱ひげ図)
        opt1 = PlotOption()
        opt1.set_figsize( 15, 7 )
        opt1.set_title( u'Detail of Timing Statistics', 24, 'k' )
        opt1.set_label( u'関数名', val_name, 18, 'red' )
        opt1.set_draw( 'c', 'k', 0.6 )
        #opt1.set_yrange(0.0, 10.0)
        opt1.set_tick( 'blue', 14, 0, 0 )
        opt1.set_text( '-  Sorted By ' + g_ValueName[sortby] + '  -', 0.70, 0.38, 12, 'k', 'green', 0.3 )
        opt1.set_pngname(png_name)
        # -----------------------------------------------------------

        my_plt.draw_boxplot( list_of_data_array, ticks, labels, 90, opt1, mute )

# -------------------------------------------------------------------
#　棒グラフ作図
def create_barplot(my_dict, func_name, val_name, is_bar=0, mute=0):

        print u'棒グラフ作図', u'関数名=', func_name, u'値=', val_name

        #　作図のデータ配列を取り出す
        array = get_array( my_dict, func_name, val_name )
        #print 'array_len = ', len(array)

        # -----------------------------------------------------------
        # 作図仕様を指定する(棒グラフ)
        n_max = -1 #配列の上位nn_max個を図に入れる。-1の場合、全部入れる

        #　作図用配列を生する
        x_data = []
        y_data = []
        for i in range(len(array)):
                x_data.append(i)
                y_data.append(array[i])
                if i == n_max : break

        if n_max < 0 : n_max = len(array)

        #出力PNG画像ファイル名中に使えない文字を '_' に置換
        png_name = 'image_bar_' + func_name + '_' + val_name
        png_name = verify_filename(png_name)
        png_name = png_name + '.png'

        # -----------------------------------------------------------
        # 作図仕様を指定する(棒グラフ)
        title_label = u'関数名:  ' + func_name
        opt2 = PlotOption()
        opt2.set_figsize( 20, 7 )
        opt2.set_title( u'Detail of Timing Statistics', 20, 'green' )
        opt2.set_label( u'プロセス', val_name, 18, 'blue' )
        opt2.set_xrange( 0, n_max )
        #opt2.set_yrange( 0, 0.025 )
        if is_bar == 1 : opt2.set_draw( 'c', 'k', 0.6 )
        else :           opt2.set_draw( 'b', 'k', 0.6 )
        opt2.set_text( title_label, 0.80, 0.90, 16, 'red', 0.3 )
        opt2.set_pngname(png_name)
        #opt2.set_figcolor( 'lightgoldenrodyellow', 0.2 )
        #opt2.set_tick( 'red', 16, 0, 0 )
        # -----------------------------------------------------------

        if is_bar == 1 : my_plt.draw_barplot(x_data, y_data, opt2, 'bar', mute)
        else :           my_plt.draw_barplot(x_data, y_data, opt2, 'xy',  mute)

#------- main() -----------------------------------------
if __name__ == '__main__':

    """
    実行引数の例：
        PlotPerformanceData.py
        PlotPerformanceData.py box
        PlotPerformanceData.py bar
        PlotPerformanceData.py xy
    """
    print u'\n'
    
    arguments = sys.argv
    for arg in arguments : print u'引数：' + arg

    my_dict = io.load_data('profiling.txt')

    b_barplot = 0
    b_boxplot = 0
    b_xyplot  = 0

    if len(arguments) > 1 :
            if 'box' in arguments[1] : b_boxplot = 1
            if 'bar' in arguments[1] : b_barplot = 1
            if 'xy'  in arguments[1] : b_xyplot  = 1
    else :
            b_barplot = 1
            b_boxplot = 1

    if b_xyplot == 1: b_barplot = 1

    print u'棒グラフ作図モード b_barplot = ', b_barplot
    print u'箱ひげ図作図モード b_boxplot = ', b_boxplot
    print u'散布図XY作図モード b_xyplot  = ', b_xyplot
    print u'\n'

    #　棒グラフ作図 --------------------------------------------------
    if b_barplot > 0 :

        """         0        1          2           3             4                5         6
        io.g_keys = ['call', 'accm[s]', 'accm[%]', 'waiting[s]', 'accm/call[s]', 'flop|msg', 'speed']
        """
        val_name = ''
        func_name = ''

        ####### ユーザ入力 ######　棒グラフ作図
        val_name  = io.g_keys[3]
        #-----------------------
        ####### ユーザ入力 ######　棒グラフ作図
        func_name = 'Initialization'
        #-----------------------

        # 図に入れる関数名を指定しないと、全ての関数の図が順次作成される

        print 'val_name =', val_name
        print 'func_name=', func_name

        if b_xyplot == 1 : is_bar = 0
        else :             is_bar = 1

        if len(val_name) > 0 :                  # val_name  指定あり
                if len(func_name) > 0 :         # func_name 指定あり
                        mute = 0
                        create_barplot(my_dict, func_name, val_name, is_bar, mute)
                else :                          # func_name  指定なし
                        mute = 1
                        for func_name in my_dict:
                            create_barplot(my_dict, func_name, val_name, is_bar, mute)

        else :                                  # val_name  指定なし
                val_names = ['accm[s]', 'accm[%]', 'waiting[s]', 'accm/call[s]']

                for val_name in val_names:
                    if len(func_name) > 0 : # func_name  指定あり
                      mute = 1
                      create_barplot(my_dict, func_name, val_name, is_bar, mute)

                    else :                  # func_name  指定なし
                      mute = 1
                      for the_func_name in my_dict:
                        create_barplot(my_dict, the_func_name, val_name, is_bar, mute)
                      print

    #　箱ひげ図作図 -----------------------------------------------------
    if b_boxplot > 0 :
        func_names = []

        """
        # 定義の例
        func_names = [   'Initialization'		\
                        ,'Search Vmax'			\
                        #,'Vmax A.R.'			\
                        #,'*Flow Sct.'			\
                        ,'*NS: F-Step Sct.'		\
                     ]

                        0        1          2           3             4                5         6
        io.g_keys = ['call', 'accm[s]', 'accm[%]', 'waiting[s]', 'accm/call[s]', 'flop|msg', 'speed']
        """

        ####### ユーザ入力 ######　箱ひげ図作図
        val_name  = io.g_keys[3]
        #---------------------

        print 'val_name=', val_name

        if len(val_name) > 0 :
            mute = 0
            create_boxplot(my_dict, func_names, val_name, mute)
        else :
            mute = 1
            val_names = ['accm[s]', 'accm[%]', 'waiting[s]', 'accm/call[s]']
            for val_name in val_names:
                    create_boxplot(my_dict, func_names, val_name, mute)




