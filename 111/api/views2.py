# coding:utf-8
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
import os, sys, math, subprocess, json
import datetime
from django.conf import settings
# Create your views here.
from PIL import Image
from django.core.cache import cache

host = 'http://119.23.117.136:8080'
host = 'http://192.168.3.32:8000'


import matlab.engine
sessions = matlab.engine.find_matlab()
eng = None
if len(sessions) > 0:
    eng = matlab.engine.connect_matlab(sessions[0])

@api_view(['POST'])
def apartments(request):
    id = request.data['id']
    file_data = cache.get(id)
    images = file_data['images']
    scale = file_data['scale']
    picture_scaling = file_data['picture_scaling']
    ratio = int(request.data.get('ratio', 0.2))
    data = []
    try:
        img = eng.MainWallRefine(images[ratio], scale[0], scale[1], picture_scaling, nargout=1)
        result = eng.JsonOutput(img, scale[0], scale[1], picture_scaling, nargout=1)
        print(result)
        data = json.loads(result.replace('\r\n', ''))
    except Exception as e:
        print(e)
    return Response({'code': 1,
                     'info': '',
                     'data': data})

from .tools import uuid
@api_view(['POST'])
def walls(request):
    file = request.data['img']
    scale = request.data['scale'].replace('mm','').replace('px','').split(':')
    print(scale)
    file_type, file_content = file.split(',')[0],base64.b64decode(file.split(',')[1])
    file_path = os.path.join(settings.BASE_DIR, 'media',
                             datetime.datetime.now().strftime('%Y%m%d'))
    file_name = '%s.%s' % (datetime.datetime.now().strftime(
        '%H%M%S%f'), file_type.split(';')[0].split(':')[-1].split('/')[-1])
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = os.path.join(file_path, file_name)
    with open(file_name, 'wb') as f:
        f.write(base64.b64decode(file.split(',')[1]))
    data = []
    try:
        time1 = datetime.datetime.now()
        result = eng.Unit_Extraction(file_name, float(scale[0]), float(scale[1]), nargout=1)
        # result = eng.Unit_Extraction( 'image023.jpg' , 4170.0 ,   349.0 , nargout=1)
        data = json.loads(result.replace('\r\n', ''))
        time2 = datetime.datetime.now()
        print(time2-time1)
    except Exception as e:
        print(e)
    if data==[]:
        return Response({'code': 0,
                     'info': '未能识别出户型',
                     'data': data})
    return Response({'code': 1,
                     'info': '',
                     'data': data})
