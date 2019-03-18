import json
# 变量从内存中变成可存储或传输的过程称之为序列化 序列化之后，就可以把序列化后的内容写入磁盘，或者通过网络传输到别的机器上
# dumps 将Python中的字典转换成字符串
dict = {'name':'乔治','age':34,'gender':'male'}
str = json.dumps(dict,ensure_ascii=False)
print(str)

# loads 将字符串转换成Python字典
new_dict = json.loads(str)
print(new_dict)

# dump: 将数据写入json文件中
# with open('11.txt','w') as f:
#     json.dump(new_dict,f,ensure_ascii=False)

# load:把文件打开，并把字符串变换为数据类型
with open('21.txt','r') as f:
    print(json.load(f))