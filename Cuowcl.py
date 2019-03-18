# try:
#     print('try...')
#     r = 10 / 0
#     print('result:',r)
# except ZeroDivisionError as e:
#     print('except:',e)
# finally:
#     print('finally..')
# print('End')

# def division(x,y):
#     if y == 0:
#         raise ZeroDivisionError('zero is not allow')
#     return (x/y)
# try:
#     division(8,0)
# except BaseException as msg:
#     print(msg)
def bad_append(new_item, a_list=[]):
    a_list.append(new_item)

    return a_list
print (bad_append('one'))
print(id(bad_append('one')))
print (bad_append('one'))
print(id(bad_append('one')))
print (bad_append('one'))
print(id(bad_append('one')))
print (bad_append('one'))
print (bad_append('one'))

