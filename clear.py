# __author__ = 'gxj'
#-*-coding:utf-8-*-
import re


def clear(file, newfile):
    f = open(file, 'r')
    n = open(newfile, 'a')
    line = f.readlines()
    print '***', line
    for i in line:
        # d = list(set(list(i)))
        # print d
        if i.split('\n')[0].isspace() or i=='\n':
            print '===========',i
            pass
        else:
            print '++++++++++',i,len(i)
            n.write(i)
    f.close()
    n.close()
    return 'the new file :', n


print clear('/home/gxj/old_demo.txt', '/home/gxj/dump1.txt')

