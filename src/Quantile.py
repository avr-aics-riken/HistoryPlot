#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:
# Author:      Ernesto P. Adorio
# Created:
# Copyright:
# Licence:
#-------------------------------------------------------------------------------

import numpy as np
import sys

#-----------------------------------------------------------------------------
"""
箱ひげ図（はこひげず、箱髭図、box plot）

                            +-----+-+
  *           o     |-------|   + | |---|
                            +-----+-+

+---+---+---+---+---+---+---+---+---+---+   number line
0   1   2   3   4   5   6   7   8   9  10

このデータセット（値は図から読み取れる概略値とする）から、次のことが分かる:
    最小値（min） = 5。
    第1四分位点（Q1） = 7。
    中央値（第2四分位点、Med） = 8.5。
    第3四分位点（Q3） = 9。
    最大値（max） = 10。
    平均値 = 8。
    IQR(interquartile range) = Q3-Q1 = 2
    3.5という値は"軽度の"外れ値、つまりQ1よりも 1.5×IQR から 3×IQR だけ下にある。
    0.5という値は"極端な"外れ値、つまりQ1よりも 3×IQR 以上下にある。
    外れ値以外の最小値は5。
    データは左に歪んでいる（負の歪度）。
"""
# 箱ひげ図(BoxPlot）をプロットするため、データをソートしています。
# ソートする候補のデータは、この配列に格納しています。
g_Values = [0.0,   0.0,   0.0,   0,0, 0.0,   0.0,   0.0,   0,0]

MED_VAL = 0
MIN_VAL = 1
MAX_VAL = 2
DIF_VAL = 3
Q1_VAL  = 4
Q3_VAL  = 5
AVG_VAL = 6
IQR_VAL = 7

g_ValueName = ['', '', '', '', '', '', '', '']
g_ValueName[MED_VAL] = u'中央値(Q2)'         #median (Q2)
g_ValueName[MIN_VAL] = u'最小値'             #minimum
g_ValueName[MAX_VAL] = u'最大値'             #maximum
g_ValueName[DIF_VAL] = u'最大最小差値'       #range
g_ValueName[Q1_VAL]  = u'第1四分位数(Q1)'    #first quartile (Q1)
g_ValueName[Q3_VAL]  = u'第3四分位数(Q3)'    #third quartile (Q3)
g_ValueName[AVG_VAL] = u'平均値'             #average
g_ValueName[IQR_VAL] = u'四分位数範囲(IQR)'  #Interquartile range (IQR)

# 配列データの分位数ルゴリズム
#g_qtype = 1 # inverse empirical distrib.function., R type 1
#g_qtype = 2 # similar to type 1, averaged, R type 2
#g_qtype = 3 # nearest order statistic,(SAS) R type 3
#g_qtype = 4 # California linear interpolation, R type 4
#g_qtype = 5 # hydrologists method, R type 5
#g_qtype = 6 # mean-based estimate(Weibull method), (SPSS,Minitab), type 6
g_qtype = 7 # mode-based method,(S, S-Plus), R type 7
#g_qtype = 8 # median-unbiased ,  R type 8
#g_qtype = 9 # normal-unbiased, R type 9.

def calculate_Median_Q1_Q3( array):
  g_Values[MED_VAL]=quantile(array, 0.50, g_qtype)   #median
  g_Values[Q1_VAL ]=quantile(array, 0.25, g_qtype)   #first quartile (Q1)
  g_Values[Q3_VAL ]=quantile(array, 0.75, g_qtype)   #third quartile (Q3)
  g_Values[IQR_VAL]=g_Values[Q3_VAL]-g_Values[Q1_VAL]#Interquartile range (IQR)
  g_Values[MIN_VAL]=np.amin(array)                   #minmum
  g_Values[MAX_VAL]=np.amax(array)                   #maxmum
  g_Values[AVG_VAL]=np.average(array)                #average
  g_Values[DIF_VAL]=g_Values[MAX_VAL]-g_Values[MIN_VAL] #range

#-----------------------------------------------------------------------------

"""
File	quantile.py
Desc	computes sample quantiles
Author  Ernesto P. Adorio, PhD.	 UPDEPP (U.P. at Clarkfield)
Version 0.0.1 August 7. 2009
"""
from math import modf, floor
def quantile(x, q,  qtype = 7, issorted = False):
	"""
	Args:
	   x - input data
	   q - quantile
	   qtype - algorithm
	   issorted- True if x already sorted.
	Compute quantiles from input array x given q.For median,
	specify q=0.5.
	References:
	   http://reference.wolfram.com/mathematica/ref/Quantile.html
	   http://wiki.r-project.org/rwiki/doku.php?id=rdoc:stats:quantile
	Author:
	Ernesto P.Adorio Ph.D.
	UP Extension Program in Pampanga, Clark Field.
	"""
	if not issorted:
		y = sorted(x)
	else:
		y = x
	if not (1 <= qtype <= 9):
	   return None  # error!
	# Parameters for the Hyndman and Fan algorithm
	abcd = [(0,   0, 1, 0), # inverse empirical distrib.function., R type 1
		(0.5, 0, 1, 0), # similar to type 1, averaged, R type 2
		(0.5, 0, 0, 0), # nearest order statistic,(SAS) R type 3
		(0,   0, 0, 1), # California linear interpolation, R type 4
		(0.5, 0, 0, 1), # hydrologists method, R type 5
		(0,   1, 0, 1), # mean-based estimate(Weibull method), (SPSS,Minitab), type 6
		(1,  -1, 0, 1), # mode-based method,(S, S-Plus), R type 7
		(1.0/3, 1.0/3, 0, 1), # median-unbiased ,  R type 8
		(3/8.0, 0.25, 0, 1)   # normal-unbiased, R type 9.
	       ]
	a, b, c, d = abcd[qtype-1]
	n = len(x)
	g, j = modf( a + (n+b) * q -1)
	if j < 0:
		return y[0]
	elif j >= n:
		return y[n-1]   # oct. 8, 2010 y[n]???!! uncaught  off by 1 error!!!
	j = int(floor(j))
	if g ==  0:
	   return y[j]
	else:
	   return y[j] + (y[j+1]- y[j])* (c + d * g)
def Test():
	x = [11.4, 17.3, 21.3, 25.9, 40.1, 50.5, 60.0, 70.0, 75]
	for qtype in range(1,10):
		print qtype, quantile(x, 0.35, qtype)
if __name__ == "__main__":
	Test()
"""
When the test code runs, it outputs
    1 25.9
    2 25.9
    3 21.3
    4 21.99
    5 24.29
    6 23.6
    7 24.98
    8 24.06
    9 24.1175
This matches the output of the following R code:
x <- c(11.4, 17.3, 21.3, 25.9, 40.1, 50.5, 60.0, 70.0, 75)
for (i in seq(1,9)) { print(c( i, quantile(x, 0.35, type=i))) }
"""

