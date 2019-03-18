from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
import os, sys, math, subprocess, json
import datetime
from django.conf import settings
# Create your views here.
from .tools import convert_dxf_to_dwg, convert_dwg_to_dxf, convert_js_to_dxf, convert_dwg_to_json

host = 'https://apartment.gezlife.com'

@api_view(['POST'])
def api(request):
    type = request.data['type']
    file = request.data['img']
    file_content = base64.b64decode(file.split(',')[1])
    width = 2048
    height = 2048
    # if type.upper() == 'DWG':
    #     file = request.form['img']
    #     data = {'img': file}
    #     data = urllib.parse.urlencode(data).encode('utf-8')
    #     req = urllib.request.Request.Request(url='http://localhost:8000/api/Size',
    #                           data=data)
    #     try:
    #         response = urllib.request.Request.urlopen(req)
    #         result = json.loads(response.read())
    #         width = result['width']
    #         height = result['height']
    #         height = int(width*1.0/2048*height)
    #         width = 2048
    #         # if width < 2048:
    #         #     return jsonify({"code": -2, "info": "图片尺寸太小"})
    #         # elif width > 4096:
    #         #     return jsonify({"code": -2, "info": "图片尺寸太大"})
    #     except Exception as e:
    #         print(e.message)
    #         return jsonify({'code': -1, 'info': "转换失败"})
    if len(file_content) > 3*1024 * 1024:
        return Response({"code": -4, "info": "上传的文件大于1024KB"})
    if not (type.upper().endswith('DWG') or type.upper().endswith('PNG')):
        return Response({"code": -5, "info": "上传的文件格式不对"})
    file_path = os.path.join(settings.BASE_DIR, 'media',
                             datetime.datetime.now().strftime('%Y%m%d'))
    file_name = datetime.datetime.now().strftime(
        '%H%M%S%f') + '.' + type.lower()
    print(file_name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = os.path.join(file_path, file_name)
    print(file_name)
    with open(file_name, 'wb') as f:
        f.write(base64.b64decode(file.split(',')[1]))
    # if type.upper()=='DWG':
    #     ps = subprocess.Popen('python %s %s' % (os.path.join('api', 'find_contour.py'),file_name))
    #     ps.communicate()
    #     ps.wait()
    # else:
    convert_dwg_to_json(file_name, "parquet")
    output_file = os.path.splitext(file_name)[0] + '.json'
    try:
        result = ''
        with open(output_file, 'r+') as output_json:
            for line in output_json.readlines():
                result += line.strip()
        result = json.loads(result)
        return Response(result)
    except Exception as e:
        return Response({'code': -1})


@api_view(['POST'])
def brick(request):
    type = request.data['type']
    file = request.data['img']
    file_content = base64.b64decode(file.split(',')[1])
    # if type.upper() == 'DWG':
    #     file = request.form['img']
    #     data = {'img': file}
    #     data = urllib.parse.urlencode(data).encode('utf-8')
    #     req = urllib.request.Request.Request(url='http://localhost:8000/api/Size',
    #                           data=data)
    #     try:
    #         response = urllib.request.Request.urlopen(req)
    #         result = json.loads(response.read())
    #         width = result['width']
    #         height = result['height']
    #         height = int(width*1.0/2048*height)
    #         width = 2048
    #         # if width < 2048:
    #         #     return jsonify({"code": -2, "info": "图片尺寸太小"})
    #         # elif width > 4096:
    #         #     return jsonify({"code": -2, "info": "图片尺寸太大"})
    #     except Exception as e:
    #         print(e.message)
    #         return jsonify({'code': -1, 'info': "转换失败"})
    if len(file_content) > 5 * 1024 * 1024:
        return Response({"code": -4, "info": "上传的文件大于1024KB"})
    if not (type.upper().endswith('DWG') or type.upper().endswith('PNG')):
        return Response({"code": -5, "info": "上传的文件格式不对"})
    file_path = os.path.join(settings.BASE_DIR, 'media',
                             datetime.datetime.now().strftime('%Y%m%d'))
    file_name = datetime.datetime.now().strftime(
        '%H%M%S%f') + '.' + type.lower()
    print(file_name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = os.path.join(file_path, file_name)
    print(file_name)
    with open(file_name, 'wb') as f:
        f.write(base64.b64decode(file.split(',')[1]))
    # command = 'python %s %s' % (os.path.join('api', 'find_contour2.py'),file_name)
    # ps = subprocess.Popen(command)
    # ps.communicate()
    # ps.wait()
    convert_dwg_to_json(file_name, "brick")
    output_file = os.path.splitext(file_name)[0] + '.json'
    try:
        result = ''
        with open(output_file, 'r+') as output_json:
            for line in output_json.readlines():
                result += line.strip()
        result = json.loads(result)
        return Response(result)
    except Exception as e:
        return Response({'code': -1})


@api_view(['POST'])
def convert(request):
    json_str = request.data['json']
    # print(json_str)
    try:
        file_path = os.path.join(settings.BASE_DIR, 'media',
                                 datetime.datetime.now().strftime('%Y%m%d'))
        time = datetime.datetime.now().strftime(
            '%H%M%S%f')
        js_name = time + '.js'
        file_name = time + '.dxf'
        dwg_file_name = time + '.dwg'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        js_name = os.path.join(file_path, js_name)
        file_name = os.path.join(file_path, file_name)
        dwg_file_name = os.path.join(file_path, dwg_file_name)
        with open(js_name, 'wb') as file:
            file.write(json_str.encode('utf-8'))
        convert_js_to_dxf(js_name)
        convert_dxf_to_dwg(file_name, dwg_file_name)
        if os.path.exists(dwg_file_name):
        # return send_file(file_name, mimetype='application/octet-stream', as_attachment=True)
            return Response({'code': 1,
                        'data': host + dwg_file_name.replace(settings.BASE_DIR, '').replace(
                            '\\', '/')})
        else:
            return Response({'code': -1, 'info': '转换失败'})
    except Exception as e:
        print(e)
        return Response({'code': -1, 'info': "转换失败: "})


@api_view(['POST'])
def apartments(request):
    type = request.data['type']
    file = request.data['cad_data']
    file_content = base64.b64decode(file.split(',')[1])
    if type == 'dwg' and len(file_content) > 5*1024*1024:
        return Response({'status': 0,
                         'info': 'DWG文件最大支持5MB'})
    elif type == 'dxf' and len(file_content) > 10*1024*1024:
        return Response({'status': 0,
                         'info': 'DXF文件最大支持10MB'})
    file_path = os.path.join(settings.BASE_DIR, 'media',
                             datetime.datetime.now().strftime('%y%m%d'))
    file_name = datetime.datetime.now().strftime(
        '%H%M%S%f')
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = os.path.join(file_path, file_name)
    return Response({'status': 1,
                     'info': '',
                     'data': []})
