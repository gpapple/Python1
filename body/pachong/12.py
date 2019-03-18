import requests
from urllib import parse
# 负责处理json格式的模块
import json

'''
大致流程是：
1. 利用data构造内容，然后urlopen打开
2. 返回一个json格式的结果
3. 结果就应该是girl的释义
'''

baseurl = 'https://fanyi.baidu.com/sug'


# 存放用来模拟form的数据一定是dict格式
data = {
    # girl是翻译输入的英文内容，应该是由用户输入，此处使用硬编码
    'kw': 'length'
}

#  我们需要构造一个请求头，请求头部应该至少包含传入的数据的长度
# request要求传入的请求头是一个dict格式

headers = {
    # 因为使用post，至少应该包含content-length 字段
    'Content-Length':str(len(data))
}


# 有了headers，data，url，就可以尝试发出请求了
rsp = requests.post(baseurl, data=data,  headers=headers)

# print(rsp.text)
# print(rsp.json())
for i in rsp.json()['data']:
    print(i['k'], "-->",i['v'])