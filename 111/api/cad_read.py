#coding: utf-8
import sys
import dxfgrabber
from dxfgrabber.dxfentities import Line, LWPolyline
from PIL import Image, ImageDraw
from shapely.ops import polygonize_full, linemerge
import math

total_points = {}
total_lines = []

class LineFormula(object):
    start_point = None
    end_point = None
    length = 0
    formula = None
    index = 0

    def __str__(self):
        return '%s to %s' % (self.start_point, self.end_point)

    def __unicode__(self):
        return '%s to %s' % (self.start_point, self.end_point)

    def __init__(self, x1, y1, x2, y2):
        if math.fabs(x2 - x1) < 0.001:
            a = 1
            b = 0
            c = -x2
        elif math.fabs(y2 - y1) < 0.001:
            a = 0
            b = 1
            c = -y2
        else:
            a = (y1 - y2) / (x2 - x1)
            b = 1
            c = (y2 - y1) / (x2 - x1) * x1 - y1
        if math.fabs(a) < 0.00001:
            a = 0
        if math.fabs(b) < 0.00001:
            b = 0
        if a < 0:
            a = -a
            b = -b
            c = -c
        rotation = int((math.atan2(y2 - y1,
                                   x2 - x1) / math.pi * 180 + 360) % 360)
        if rotation >= 180:
            rotation -= 180
            self.start_point = (x2,y2)
            self.end_point = (x1,y1)
        else:
            self.start_point = (x1, y1)
            self.end_point = (x2, y2)
        self.length = math.sqrt(
            (self.end_point[1] - self.start_point[1]) * (self.end_point[1] - self.start_point[1]) + (
            self.end_point[0] - self.start_point[0]) * (self.end_point[0] - self.start_point[0]))
        self.formula = Formula(a, b, c, rotation)

    def overlap(self, line):
        width = self.formula.distance(line.formula)
        overlap_start_point = (self.start_point[0] + width * math.sin(self.formula.rotation / 180 * math.pi),
                               self.start_point[1] - width * math.cos(self.formula.rotation / 180 * math.pi))
        overlap_end_point = (self.end_point[0] + width * math.sin(self.formula.rotation / 180 * math.pi),
                             self.end_point[1] - width * math.cos(self.formula.rotation / 180 * math.pi))
        # 判断 overlap_start_point在line上
        overlap_start_point_flag = int((overlap_start_point[0] - line.start_point[0]) * (line.end_point[1] - line.start_point[1]) - (
                overlap_start_point[1] - line.start_point[1]) * (line.end_point[0] - line.start_point[0])) == 0 and \
                                   (min(line.start_point[0], line.end_point[0]) <= overlap_start_point[0] <= max(
                                       line.start_point[0], line.end_point[0]) and
                                     min(line.start_point[1], line.end_point[1]) <= overlap_start_point[1] <= max(
                                         line.start_point[1], line.end_point[1]))
        # 判断 overlap_end_point在line上
        overlap_end_point_flag = int((overlap_end_point[0] - line.start_point[0]) * (line.end_point[1] - line.start_point[1]) - (
                overlap_end_point[1] - line.start_point[1]) * (line.end_point[0] - line.start_point[0])) == 0 and \
                                    (min(line.start_point[0], line.end_point[0]) <= overlap_end_point[0] <= max(
                                        line.start_point[0], line.end_point[0]) and
                                     min(line.start_point[1], line.end_point[1]) <= overlap_end_point[1] <= max(
                                         line.start_point[1], line.end_point[1]))
        # 判断 line.start 在overlap上
        line_start_point_flag = int(
            (line.start_point[0] - overlap_start_point[0]) * (overlap_end_point[1] - overlap_start_point[1]) - (
                line.start_point[1] - overlap_start_point[1]) * (overlap_end_point[0] - overlap_start_point[0])) == 0 and \
                                 (min(overlap_start_point[0], overlap_end_point[0]) <= line.start_point[0] <= max(
                                     overlap_start_point[0], overlap_end_point[0]) and
                                  min(overlap_start_point[1], overlap_end_point[1]) <= line.start_point[1] <= max(
                                      overlap_start_point[1], overlap_end_point[1]))
        # 判断 line.end 在overlap上
        line_end_point_flag = int(
            (line.end_point[0] - overlap_start_point[0]) * (overlap_end_point[1] - overlap_start_point[1]) - (
                line.end_point[1] - overlap_start_point[1]) * (overlap_end_point[0] - overlap_start_point[0])) == 0 and \
                                (min(overlap_start_point[0], overlap_end_point[0]) <= line.end_point[0] <= max(
                                    overlap_start_point[0], overlap_end_point[0]) and
                                 min(overlap_start_point[1], overlap_end_point[1]) <= line.end_point[1] <= max(
                                     overlap_start_point[1], overlap_end_point[1]))
        if overlap_start_point_flag or overlap_end_point_flag or line_start_point_flag or line_end_point_flag:
            return True
        else:
            return False


class Formula(object):
    a = 0
    b = 0
    c = 0
    rotation = 0

    def __init__(self, a, b, c, rotation):
        self.a = a
        self.b = b
        self.c = c
        self.rotation = rotation

    def intersection(self, formula):
        if math.fabs(formula.a * self.b - self.a * formula.b) <= 0.001 or math.fabs(
                                formula.b * self.a - self.b * formula.a) < 0.001:
            return float('inf')
        x = (self.c * formula.b - formula.c * self.b) / (formula.a * self.b - self.a * formula.b)
        y = (self.c * formula.a - formula.c * self.a) / (formula.b * self.a - self.b * formula.a)
        return (x, y)

    def distance(self, formula):
        return abs(self.c - formula.c) / math.sqrt(self.a * self.a + self.b * self.b)

class CustomPoint(object):
    x = 0
    y = 0
    lines = []

    def __init__(self, x, y):
        self.x = x
        self.y = y

class CustomLine(object):
    points = []
    line_formula = None


def read_cad(file_name):
    dxf = dxfgrabber.readfile(file_name)
    lines = []
    x_list = []
    y_list = []
    polygon_lines = []
    line_index = 0
    origin_lines = []
    for entity in dxf.entities:
        if type(entity) == Line:
            # start_point_key = '%.5f%.5f' % (entity.start[0], entity.start[1])
            # end_point_key = '%.5f%.5f' % (entity.end[0], entity.end[1])
            # line = CustomLine()
            # if total_points.get(start_point_key):
            #     start_point = total_points.get(start_point_key)
            # else:
            #     start_point = CustomPoint(entity.start[0], entity.start[1])
            #     total_points.update({start_point_key: start_point})
            # start_point.lines.append(line)
            # line.points.append(start_point)
            # if total_points.get(end_point_key):
            #     end_point = total_points.get(end_point_key)
            # else:
            #     end_point = CustomPoint(entity.end[0], entity.end[1])
            #     total_points.update({end_point_key: end_point})
            # end_point.lines.append(line)
            # line.points.append(end_point)
            # total_lines.append(line)
            origin_lines.append((entity.start, entity.end))
    # print(len(origin_lines))
    # print(len(linemerge(origin_lines)))
    # for entity in linemerge(origin_lines):
    #     line = LineFormula(entity.coords[0][0], entity.coords[0][1], entity.coords[1][0], entity.coords[1][1])
            line = LineFormula(entity.start[0], entity.start[1], entity.end[0], entity.end[1])
            line.index = line_index
            # x_list.append(entity.coords[0][0])
            # x_list.append(entity.coords[1][0])
            # y_list.append(entity.coords[0][1])
            # y_list.append(entity.coords[1][1])
            x_list.append(entity.start[0])
            x_list.append(entity.end[0])
            y_list.append(entity.start[1])
            y_list.append(entity.end[1])
            lines.append(line)
            line_index += 1
        elif type(entity) == LWPolyline:
            pass
    rotation_dict = {}
    for line in lines:
        key = str(line.formula.rotation)
        if key in rotation_dict.keys():
            rotation_dict[key].append(line)
        else:
            rotation_dict.update({key: [line]})
    # 合并同一条直线上的所有线段
    for key, lines in rotation_dict.items():
        c_dict = {}
        for line in lines:
            if '%s' % line.formula.c in c_dict:
                c_dict['%s' % line.formula.c].append(line)
            else:
                c_dict['%s' % line.formula.c] = [line]
        for c in c_dict:
            old_lines = c_dict[c][:]
            new_lines = []
            tmp_line = old_lines[0]

    effective_lines = {}
    print(rotation_dict)
    for key,value in rotation_dict.items():
        if len(value) >= 2:
            effective_lines.update({key:value})
    wall_lines = {}
    for key,value in effective_lines.items():
        walls = []
        for formula1 in value:
            for formula2 in value:
                # 两条线之间的距离在50 到 300之间，并且互相有投影，则认为这是一面有效的墙
                if 50 < formula1.formula.distance(formula2.formula) < 300 and formula1.overlap(formula2):
                    polygon_lines.append(origin_lines[formula1.index])
                    polygon_lines.append(origin_lines[formula2.index])
                    walls.append([formula1,formula2])
        if len(walls) > 0:
            wall_lines.update({key:walls})
    img_width = int(max(x_list) - min(x_list))
    img_height = int(max(y_list) - min(y_list))
    image = Image.new('RGB', (img_width,img_height), (255,255,255))
    draw = ImageDraw.Draw(image)
    middle_lines = []
    for key,walls in wall_lines.items():
        for wall_line in walls:
            middle = middle_line(wall_line[0], wall_line[1])
            middle_formula = LineFormula(middle[0][0], middle[0][1], middle[1][0], middle[1][1])
            middle_lines.append(middle_formula)
            #draw.line((middle[0][0] - min(x_list), img_height - middle[0][1] + min(y_list), middle[1][0] - min(x_list), img_height - middle[1][1] + min(y_list)), (0, 0, 0), 3)
            draw.line((wall_line[0].start_point[0] - min(x_list), img_height - wall_line[0].start_point[1] + min(y_list), wall_line[0].end_point[0] - min(x_list), img_height - wall_line[0].end_point[1] + min(y_list)), (0,0,0), 3)
            draw.line((wall_line[1].start_point[0] - min(x_list), img_height - wall_line[1].start_point[1] + min(y_list), wall_line[1].end_point[0] - min(x_list),
                       img_height - wall_line[1].end_point[1] + min(y_list)), (0, 0, 0), 3)
            total_lines.append(wall_line[0])
            total_lines.append(wall_line[1])
    print(len(total_lines))
    exclude_single_line = []


    # result, dangles, cuts, invalids = polygonize_full(list(set(polygon_lines)))
    # max_area = 0
    # max_polygon = []
    # for polygon in result.geoms:
    #     coords = polygon.exterior.coords
    #     sum = 0
    #     for index,vertex in enumerate(coords):
    #         next_vertex = coords[(index+1)%len(coords)]
    #         sum += (vertex[0] * next_vertex[1] - next_vertex[0] * vertex[1]) / 2
    #     if abs(sum) > abs(max_area):
    #         max_polygon = coords
    # print(max_polygon)
    # for index,vertex in enumerate(max_polygon):
    #     next_vertex = coords[(index + 1) % len(coords)]
    #     draw.line((vertex[0] - min(x_list), img_height - vertex[1] + min(y_list),
    #                next_vertex[0] - min(x_list), img_height - next_vertex[1] + min(y_list)),
    #               (0, 0, 0), 3)
    # for line in dangles.geoms:
    #     draw.line((line.coords[0][0] - min(x_list), img_height - line.coords[0][1] + min(y_list),
    #                line.coords[1][0] - min(x_list), img_height - line.coords[1][1] + min(y_list)),
    #               (0, 0, 0), 3)
    # for line in cuts.geoms:
    #     draw.line((line.coords[0][0] - min(x_list), img_height - line.coords[0][1] + min(y_list),
    #                line.coords[1][0] - min(x_list), img_height - line.coords[1][1] + min(y_list)),
    #               (0, 0, 0), 3)
    # for line in linemerge(polygon_lines):
    #     draw.line((line.coords[0][0] - min(x_list), img_height - line.coords[0][1] + min(y_list),
    #                line.coords[1][0] - min(x_list), img_height - line.coords[1][1] + min(y_list)),
    #               (0, 0, 0), 3)
    image.save('test.png')


def middle_line(line1,line2):
    return (((min(line1.start_point[0],line1.end_point[0])+min(line2.start_point[0],line2.end_point[0]))/2,
          (min(line1.start_point[1],line1.end_point[1])+min(line2.start_point[1],line2.end_point[1]))/2),
          ((max(line1.start_point[0], line1.end_point[0]) + max(line2.start_point[0], line2.end_point[0])) / 2,
           (max(line1.start_point[1], line1.end_point[1]) + max(line2.start_point[1], line2.end_point[1])) / 2))

if __name__ == '__main__':
    read_cad(sys.argv[1])
