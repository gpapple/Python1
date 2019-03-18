# coding:utf-8
import sys
import cv2
import os
import subprocess
from PIL import Image
import json
import numpy as np
import math
import re
import binascii

pixel_pad = ['FE0000','FF9900','FFFF01','FF00FF','7A7A7A','14AF2F','00FF01','663001','01FFFF','0000FE','000000','FFFFFF']
pixel_rgb_pad = [(254, 0, 0), (255, 153, 0), (255, 255, 1), (255, 0, 255), (122, 122, 122), (255, 255, 255), (20, 175, 47), (0, 255, 1), (102, 48, 1), (1, 255, 255), (0, 0, 254), (0, 0, 0)]
pixel_offset = 16

def find_contour(file_name):
    output_json = os.path.splitext(file_name)[0] + '.json'
    output_file = open(output_json, 'w+')
    cad_flag = False
    if file_name.upper().endswith('DWG'):
        convert_tool = os.path.join('plugins', 'App', 'Acme CAD Converter',
                     'AcmeCADConverter')
        converted_file_name = '%s.png' % os.path.splitext(file_name)[0]
        command_png = '%s /r /w %s /h %s /b 1 /f 6 /ad A4 %s %s' % (
            convert_tool, 2048, 2048, file_name, converted_file_name)
        ps = subprocess.Popen(command_png)
        ps.wait()
        file_name = converted_file_name
        cad_flag = True
    pixel_error = False
    try:
        image = Image.open(file_name)
        width, height = image.size
        if height > width:
            image = image.rotate(90, expand=True)
            image.save(file_name,image.format)
        if not image.mode == 'RGB':
            image = image.convert('RGB')
        if not cad_flag:
            if len(list(filter(lambda x:x in pixel_pad,list(set([convert_pixel_to_hex(index[1]) for index in
                      filter(lambda x: x[0] > 5000,
                             image.getcolors(maxcolors=256 * 256 * 256))]))))) <2:
                pixel_error = True
        pixels = list(set([convert_pixel_to_hex(index[1]) for index in
                  filter(lambda x: x[0] > 1000,
                         image.getcolors(maxcolors=256 * 256 * 256))]))
        image.close()
    except Exception as e:
        print(e)
        output_file.write(json.dumps({"code": -5, "info": "上传的文件不是图片"}))
        output_file.flush()
        output_file.close()
        return
    im_origin = cv2.imread(file_name, cv2.IMREAD_COLOR)
    height, width = im_origin.shape[:2]
    if cad_flag:
        im_origin = cv2.copyMakeBorder(im_origin, 3, 3, 3, 3,
                                   cv2.BORDER_CONSTANT,
                                   value=[0, 0, 255])
    if not cad_flag:
        if width < 2048:
            output_file.write(json.dumps({"code": -1, "info": "图片尺寸太小"}))
            output_file.flush()
            output_file.close()
            return
        elif width > 4096:
            output_file.write(json.dumps({"code": -2, "info": "图片尺寸太大"}))
            output_file.flush()
            output_file.close()
            return
    if pixel_error:
        output_file.write(json.dumps({"code": -6, "info": "图片颜色不正确，请参照\"拼花样式图片制作规范\""}))
        return
    colors = []
    ratio = float(height) / float(width)
    if not cad_flag:
        kernel = np.ones((1, 1), np.uint8)
        im_origin = cv2.dilate(im_origin, kernel, iterations=1)
    x_list = []
    y_list = []
    max_contour = []
    for pixel in pixels:
        if pixel == 'FFFFFF':
            continue
        im_constant = cv2.copyMakeBorder(im_origin, 10, 10, 10, 10,
                                             cv2.BORDER_CONSTANT,
                                             value=[255, 255, 255])
        cv2.imwrite(file_name+"constant.png", im_constant)
        if not cad_flag:
            kernel = np.ones((1, 1), np.uint8)
            im_constant = cv2.erode(im_constant, kernel, iterations=1)
        pixel_changed = False
        if not pixel in pixel_pad:
            print('change color %s to 000000' % pixel)
            pixel = '000000'
            pixel_changed = True
            continue
        pixel = convert_hex_to_pixel(pixel)
        mask = cv2.inRange(im_constant, np.array(
            [pixel[2] - pixel_offset, pixel[1] - pixel_offset,
             pixel[0] - pixel_offset]),
                           np.array([pixel[2] + pixel_offset,
                                     pixel[1] + pixel_offset,
                                     pixel[0] + pixel_offset]))
        # if cad_flag:
        #     ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        # else:
        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite(file_name + convert_pixel_to_hex(pixel) + '.png', thresh)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                                      cv2.CHAIN_APPROX_NONE)
        for index, contour in enumerate(contours):
            leftmost = tuple(contour[contour[:, :, 0].argmin()][0])
            rightmost = tuple(contour[contour[:, :, 0].argmax()][0])
            topmost = tuple(contour[contour[:, :, 1].argmin()][0])
            bottommost = tuple(contour[contour[:, :, 1].argmax()][0])
            xs = [leftmost[1], rightmost[1], topmost[1], bottommost[1]]
            ys = [leftmost[0], rightmost[0], topmost[0], bottommost[0]]
            # print convert_pixel_to_hex(pixel), constant_height, xs, constant_width, ys
            if min(xs) ==0 and min(ys) ==0:
                continue
            # if (not pixel_changed) and pixel != (0,0,0) and min(xs) <10 and min(ys) <10:
            #     continue
            contour_tree = 0
            tree_index = index
            while (hierarchy[0][tree_index][3]) > 0:
                contour_tree += 1
                tree_index = hierarchy[0][tree_index][3]
            if contour_tree % 2 == 1:
                continue
            sub_contours = []
            if hierarchy[0][index][2] != -1:
                previous_tree_index = hierarchy[0][hierarchy[0][index][2]][0]
                next_tree_index = hierarchy[0][hierarchy[0][index][2]][1]
                sub_contour = contours[hierarchy[0][index][2]]
                sub_contours.append(sub_contour)
                while previous_tree_index != -1:
                    sub_contour = contours[previous_tree_index]
                    sub_contours.append(sub_contour)
                    previous_tree_index = hierarchy[0][previous_tree_index][0]
                while next_tree_index != -1:
                    sub_contour = contours[next_tree_index]
                    sub_contours.append(sub_contour)
                    next_tree_index = hierarchy[0][previous_tree_index][1]
            area = cv2.contourArea(contour)
            if cad_flag and area/width/height>0.999:
                continue
            if area/width/height<0.001:
                continue
            if area <= 25:
                continue
            if sub_contours:
                for sub_contour in sub_contours:
                    area -= cv2.contourArea(sub_contour)
                if area <= 25:
                    continue
            if not cad_flag and (max(xs) - min(xs) > width / 2 or max(ys) - min(
                        ys) > height / 2) and area / width / height < 0.005:
                continue
            if contour_tree == 2:
                max_contour.append(contour)
            x_list.append(tuple(contour[contour[:, :, 0].argmin()][0])[0])
            x_list.append(tuple(contour[contour[:, :, 0].argmax()][0])[0])
            y_list.append(tuple(contour[contour[:, :, 1].argmin()][0])[1])
            y_list.append(tuple(contour[contour[:, :, 1].argmax()][0])[1])
            img = np.zeros((height+20, width+20, 3), np.uint8)
            if pixel != '000000':
                cv2.drawContours(img, contour, -1, (pixel[2], pixel[1], pixel[0]), 2)
            else:
                cv2.drawContours(img, contour, -1, (255,255,255),
                                 2)
            for sub_contour in sub_contours:
                if pixel != '000000':
                    cv2.drawContours(img, sub_contour, -1,
                                     (pixel[2], pixel[1], pixel[0]),
                                     2)
                else:
                    cv2.drawContours(img, sub_contour, -1,
                                     (255, 255, 255),
                                     2)
            cv2.imwrite('%s-%s-%s.%s' % (
            os.path.splitext(file_name)[0], convert_pixel_to_hex(pixel), index,
            os.path.splitext(file_name)[1]), img)
            if cad_flag:
                colors.append(
                    {'color': '000000',
                     'contour': simple(list(map(
                         lambda x: {'x': x[0][0] - 10, 'y': x[0][1] - 11},
                         contour))),
                     'sub_contour': list(filter(lambda x:len(x)>0,[simple(list(map(
                         lambda x: {'x': x[0][0] - 10, 'y': x[0][1] - 11},
                         sub_contour))) for sub_contour in sub_contours])),
                     'tree_index': contour_tree})
            else:
                colors.append({'color': convert_pixel_to_hex(pixel),
                               'contour': simple(list(map(
                                   lambda x: {'x': x[0][0]-11,
                                              'y': x[0][1]-11},
                                   contour))),
                               'sub_contour': list(filter(lambda x:len(x)>0,[simple(list(map(
                                   lambda x: {'x': x[0][0]-11,
                                              'y': x[0][1]-11},
                                   sub_contour))) for sub_contour in
                                               sub_contours])),
                               'tree_index': contour_tree})
    if cad_flag:
        if len(x_list) == 0:
            x_list = [0, width]
        if len(y_list) == 0:
            y_list = [0, height]
        colors.append({
            'color': '000000',
            'contour': [
                {'x': min(x_list) - 11, 'y': min(y_list) - 11},
                {'x': min(x_list) - 11, 'y': max(y_list) - 9},
                {'x': max(x_list) - 9, 'y': max(y_list) - 9},
                {'x': max(x_list) - 9, 'y': min(y_list) - 11},
            ],
            'sub_contour': [simple(list(map(
                                       lambda x: {'x': x[0][0]-11,
                                                  'y': x[0][1]-11},
                                       sub_contour))) for sub_contour in
                                                   max_contour],
            'tree_index':0
        })
        max_x = max(x_list)
        min_x = min(x_list)
        max_y = max(y_list)
        min_y = min(y_list)
        print(max_x,min_x,max_y,min_y)
        width = max_x-min_x
        height = max_y-min_y
        ratio = float(height) / float(width)
        for color in colors:
            for contour in color['contour']:
                contour['x'] = contour['x'] - (min_x-11)
                contour['y'] = contour['y'] - (min_y-11)
            for sub_contours in color['sub_contour']:
                for sub_contour in sub_contours:
                    sub_contour['x'] = sub_contour['x'] - (min_x - 11)
                    sub_contour['y'] = sub_contour['y'] - (min_y - 11)
    output_file.write(json.dumps({'code': 1, 'data': {'width': width, 'height': height,
                                         'ratio': '%.3f' % ratio,
                                         'units': colors}}, cls=NumpyEncoder))
    output_file.flush()
    output_file.close()
    return

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)

def convert_pixel_to_hex(pixel):
    for index, pixel_rgb in enumerate(pixel_rgb_pad):
        if pixel_rgb[0] - pixel_offset <= pixel[0] <= pixel_rgb[
            0] + pixel_offset and pixel_rgb[1] - pixel_offset <= pixel[1] <= \
                        pixel_rgb[1] + pixel_offset and pixel_rgb[
            2] - pixel_offset <= pixel[2] <= pixel_rgb[2] + pixel_offset:
            return ''.join(["%02X" % x for x in pixel_rgb]).strip().upper()
    return ''.join(["%02X" % x for x in pixel]).strip().upper()


def convert_hex_to_pixel(hex):
    pixel = list(binascii.unhexlify(hex))
    for pixel_rgb in pixel_rgb_pad:
        if pixel_rgb[0] - pixel_offset <= pixel[0] <= pixel_rgb[
            0] + pixel_offset and pixel_rgb[1] - pixel_offset <= pixel[1] <= \
                        pixel_rgb[1] + pixel_offset and pixel_rgb[
            2] - pixel_offset <= pixel[2] <= pixel_rgb[2] + pixel_offset:
            return (pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
    return (pixel[0], pixel[1], pixel[2])


def simple(contour):
    new_contour = []
    last_index = -1
    tol = 10
    for index, point in enumerate(contour):
        last_index = last_index > -1 and last_index or (index - 1)
        last_point = contour[last_index]
        next_point = contour[(index+1)%len(contour)]
        if math.sqrt((last_point['y'] - point['y']) * (
                    last_point['y'] - point['y']) + (
                    last_point['x'] - point['x']) * (
                    last_point['x'] - point['x'])) < tol and \
            math.sqrt((next_point['y'] - point['y']) * (
                next_point['y'] - point['y']) + (
                next_point['x'] - point['x']) * (
                next_point['x'] - point['x'])) < tol and \
            abs(math.atan2(next_point['y']-point['y'],next_point['x']-point['x'])/math.pi*180-math.atan2(point['y']-last_point['y'],point['x']-last_point['x'])/math.pi*180)<5:
            continue
        new_contour.append(point)
        last_index = index
    return new_contour

if __name__ == '__main__':
    file_name = ''
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    find_contour(file_name)