#!/usr/bin/python3
# coding:utf-8
import os
import sys
import getopt
try:
    from PIL import Image, ImageDraw, ImageMath
except ImportError:
    os.system('pip install Pillow')
    from PIL import Image, ImageDraw, ImageMath


def convert_size(input_file, size):
    '''
    转换比例：400mm:256pix
    :param input_file: 输入图片的路径
    :param size: 图片的尺寸，(宽,高)
    :return:
    '''
    try:
        print(os.path.splitext(input_file))
        image_file = Image.open(input_file)
        if not -0.1<size[1]/size[0]-min(image_file.width,image_file.height)/max(image_file.width,image_file.height)<0.1:
            print("输入图片的纵横比不正确")
            sys.exit(2)
        out_file = image_file.copy()
        image_file.close()
        if not os.path.exists('%sbak%s' % (os.path.splitext(input_file)[0],os.path.splitext(input_file)[1])):
            os.rename(input_file, '%sbak%s' % (os.path.splitext(input_file)[0],os.path.splitext(input_file)[1]))
        width = out_file.width
        height = out_file.height
        # 如果宽小于高，旋转90度
        if width<height:
            out_file = out_file.rotate(90, expand=True)
        width = int(size[0]*256/400)
        height = int(size[1]*256/400)
        # height = int(width*out_file.height/out_file.width)
        out_file = out_file.resize((width,height), resample=Image.LANCZOS)
        if not out_file.mode == 'RGB':
            out_file = out_file.convert('RGB')
        new_file = Image.new('L', out_file.size, 10)
        image_r, image_g, image_b = out_file.split()
        image_r = ImageMath.eval("convert(max(a, b), 'L')", a=image_r, b=new_file)
        image_g = ImageMath.eval("convert(max(a, b), 'L')", a=image_g, b=new_file)
        image_b = ImageMath.eval("convert(max(a, b), 'L')", a=image_b, b=new_file)
        out_file = Image.merge('RGB', (image_r, image_g, image_b))
        out_file = out_file.convert(image_file.mode)
        out_file.save(input_file,image_file.format)
        out_file.close()
        print('图片%s转化成功' % input_file)
    except Exception:
        print('图片格式不正确')
        if os.path.exists('%sbak%s' % (os.path.splitext(input_file)[0],os.path.splitext(input_file)[1])):
            if os.path.exists(input_file):
                os.remove(input_file)
            os.rename('%sbak%s' % (os.path.splitext(input_file)[0],os.path.splitext(input_file)[1]), input_file)


def usage():
    print("Usage: %s -i image -s length,width" % os.path.basename(sys.argv[0]))
    print("image: 输入的图片的完整路径")
    print("length: 图片的宽       height：图片的高")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hbi:i:s:",
                                   ["help", "input=",
                                    "size="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    input_file = ''
    size = (0, 0)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-i', '--input'):
            input_file = a
        elif o in ('-s', '--size'):
            if len(a.split(',')) == 2:
                try:
                    size = tuple([int(c) for c in a.split(',')])
                except Exception:
                    pass
    if input_file == "" or size == (0, 0):
        usage()
        sys.exit(2)
    if not os.path.exists(input_file):
        print('文件%s不存在。' % input_file)
        usage()
        sys.exit(2)
    if size[0] <= 0 or size[1] <= 0:
        print('输入尺寸不正确。')
        usage()
        sys.exit(2)
    if size[0]<size[1]:
        size = (size[1], size[0])
    if size[0] > 1600:
        size_0 = 1600
        size_1 = size[1] * 1600/size[0]
        size = (size_0, size_1)
    # elif size[0] < 157:
    #     size_0 = 157
    #     size_1 = size[1] * 157/size[0]
    #     size = (size_0, size_1)
    convert_size(input_file, size)
