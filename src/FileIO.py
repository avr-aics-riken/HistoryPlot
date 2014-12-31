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

import numpy as np
import sys

#----------------- HardCoded ------------------------------
#以下の定義は、入力ファイルのフォマットによって、HardCodedされます。
the_str_data_begin = 'Detail of Timing Statistics'

g_keys = ['call', 'accm[s]', 'accm[%]', 'waiting[s]',
          'accm/call[s]', 'flop|msg', 'speed']
g_vals = [0, 1, 2, 3, 4, 5, 6]
g_dict = dict(zip(g_keys, g_vals))

g_s = [7,  20, 34, 42, 56, 70, 82]
g_e = [20, 34, 42, 56, 70, 82, 91]

#--------------------------------------------------------------
def load_data(filename):

        my_dict = read_file(filename)

        print u'\n 入力ファイル名： \n', filename
        print u'\n Data Retained in Python Dictionary. len = ', len(my_dict), '\n\n'

        for func_name in my_dict:
                #print '\nfunction name =', func_name
                sequence_vec = my_dict[func_name]
                #print ' ', len(sequence_vec)
                #for data in sequence_vec:
                #        print data

        #Giving function name and value name, we can get array from my_dict
        #print '\ntry to get array by given function name and value name'

        n_funcs = len(sequence_vec)
        return my_dict

#--------------------------------------------------------------
def read_file(filename):
        my_dict = {}
        sequence_vec = []

        f = open(filename)
        if not f: return output

        line = f.readline()
        while not the_str_data_begin in line:
                line = f.readline()
        print '\nRead Data: ', the_str_data_begin

        line = f.readline() # get the empty line

        while True:
                func_name  = f.readline()
                if not func_name: break
                func_name = func_name.rstrip('\n')

                #print '\nfunction name = ', '[', func_name, ']\n',
                unicode(func_name).strip()
                func_name.strip()
                #print '\nfunction name = ', '[', func_name, ']\n',

                dummy_line = f.readline() # get the empty line "   call accm[s] accm[%]..."

                line = f.readline()
                if not line: break

                while '#' in line:
                        values = get_data_from_line(line)
                        #print 'line  :', line, 'return:', values
                        sequence_vec.append(values)

                        line = f.readline()
                        if not line: break

                my_dict[func_name] = np.array(sequence_vec)
                del sequence_vec[:]
        f.close()

        return my_dict


#--------------------------------------------------------------
def get_data_from_line(line):
        array = []

        #values = line.strip().split(' ')
        #for key in g_keys:
        #        array.append( values[ g_dict2[key] ] )

        #　g_□□　はプログラム先頭に定義されているグローバルリストや辞書などです
        ii = 0
        for key in g_keys:
                i = g_s[ii]
                j = g_e[ii]
                str = line[i:j]
                array.append( float(str) )
                ii = ii+1

	return array

###--------------------------------------------------------------
##def arrays_from_file(filename):
##	output = []
##	with open(filename, 'r') as infile:
##		for line in infile:
##			line = np.array(line.strip().split(' '), dtype=np.float)
##			output.append(line)
##	return output

