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

ANY_VAL = 101

#日本語の文字化けを防止するために、これを１にして下さい。
#出力先がファイルで、エンコードエラーを起す時に、これを0にして下さい。
G_DECODE_STR    = 1

#プラットフォームによって、一つを１にして下さい。
G_WINDOWS       = 0
G_MACOSX        = 1
G_LINUX         = 0
G_LINUX_K       = 0
G_LINUX_FOCUS   = 0

#Please use 'Agg' If it issues following error:
#"no display name and no $DISPLAY environment"
#Agg is a non-interactive backend, it won't display
#on the screen, Show() does not work, it saves to files.

if G_LINUX_K == 1 : G_USE_AGG = 1
else:               G_USE_AGG = 0

#global ANY_VAL
#global G_WINDOWS
#global G_MACOSX
#global G_LINUX
#global G_LINUX_K
#global G_USE_AGG
