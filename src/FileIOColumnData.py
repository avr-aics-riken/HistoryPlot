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
        
#--------------------------------------------------------------
def replace_many_spaces_by_one(my_string):
        my_string = my_string.strip()
        while '  ' in my_string:
            my_string = my_string.replace('  ', ' ')
        return my_string

#--------------------------------------------------------------
def read_file(filename, data_block_name, column_names):

        data_dict = {}
        sequence_vec = []
        
        f = open(filename)
        if not f: return output

        # read lines until the one we want.
        line = f.readline()
        while not data_block_name in line:
                line = f.readline()
        print 'Found the Named Data Block: ', data_block_name

        #Note:  It is no allowed to have blank line between
        #       data_block_name and column name line
        
        #get column name line
        column_name_line = f.readline()
        if not column_name_line: return output
        
        #print 'before: column_name_line  :', column_name_line
        column_name_line = replace_many_spaces_by_one(column_name_line)
        #print 'after : column_name_line  :', column_name_line

        #put column names into a string array and a corresponding index array
        #then, we construct a dictionary for finding index by column name.
        column_names = column_name_line.strip().split(' ')
        #print 'column_names  :', column_names
        
        step=1
        while True:
                line = f.readline()
                if not line: break
                
                line = replace_many_spaces_by_one(line)

                values = line.strip().split(' ')
                #print 'values:', values

                sequence_vec.append(values)
                #print 'sequence_vec:', sequence_vec
                        
                data_dict[step] = np.array(sequence_vec)
                
                del sequence_vec[:]
                
                step = step+1
                
        f.close()

        return data_dict, column_names


#--------------------------------------------------------------
def load_data(filename, data_block_name, column_names):

        print u'入力ファイル名：', filename
        
        data_dict, column_names = read_file(filename, data_block_name, column_names)
        
        print u'Data Retained in Data Array. len = ', len(data_dict)

        '''
        for step in data_dict:
                sequence_vec = data_dict[step]

                print 'sequence_vec= ', sequence_vec

                #print ' ', len(sequence_vec)
                #for data in sequence_vec:
                #        print data
        '''

        return data_dict, column_names


