'''
大致流程是：
1. 利用data构造内容，然后urlopen打开
2. 返回一个json格式的结果
3. 结果就应该是girl的释义
'''
import requests
import json
word = input('please enter:')
url = 'https://fanyi.baidu.com/sug'
data = {
    'kw':word
}
headers = {
    'ContentLength':str(len(data))
}
rsp = requests.post(url,data=data,headers=headers)
# print(rsp.json())
for i in rsp.json()['data']:
    print(i['k'],'---',i['v'])

