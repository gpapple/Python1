# f = open('nice.txt','r')
# lines = f.readlines()
# print(lines)
# for line in lines:
#     print(line.split(',')[0])

# with open('21.csv','r') as f:
#         print(  f.read())

import csv
# f = csv.reader(open('21.csv','r'))
# print(f)
# for nice in f:
#     print(nice)
# a = ['hangzhou',34]
# b = ['shanghai',31]
#打开文件
# f = open('21.csv','w',newline = '')
#设定写入模式
# w = csv.writer(f,dialect='excel')
# w.writerow(a)
# w.writerow(b)
# print('over!')

# def hano(m,a,b,c):
#     if m ==1:
#         print(a,'-->',c)
#     else:
#         hano(m-1,a,c,b)
#         print(a,'-->',c)
#         hano(m-1,b,a,c)
# hano(3,'A','B','C')

import time
def wrap(f):
    def stu(*args,**kwargs):
        print('Time:',time.ctime())
        return f(*args,**kwargs)
    return stu
@wrap
def learn():
    print('hha')
learn()



