# coding:utf8
import base64
import urllib.parse
import urllib.request
import json
if __name__ == '__main__':
    file = open('.\\test3.js','rb')
    file_data = file.read()
    file.close()
    print(file_data)
    data = {'json': file_data}
    data = urllib.parse.urlencode(data).encode('utf-8')
    # req = urllib2.Request(url='http://113.108.240.178:8080/api',
    #                       data=data)
    req = urllib.request.Request(url='http://localhost:8080/convert',
                                    data=data)
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result.decode('utf-8'))
    # data = urllib.parse.urlencode(data).encode('utf-8')
    # req = urllib.request.Request(url='http://113.108.240.178:8080/apartments', data=data)
    # response = urllib.request.urlopen(req)
    # result = response.read()
    # print(str(result))