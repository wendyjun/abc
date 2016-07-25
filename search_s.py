# __author__ = 'gxj'
#-*-coding:utf-8-*-

import os
import sys


def search(word, path):
    files = os.listdir(path)
    for f in files:

        ff = path + '/' + f
        if os.path.isdir(ff):
            print "**This is dir:**", ff
            search(word, ff)
        else:
            file = open(ff, 'r').read()
            if word in file:
                print '++The word in filename :++ ', ff


search(sys.argv[2], sys.argv[1])
