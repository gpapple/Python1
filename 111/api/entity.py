# coding:utf-8
import math


class Point(object):
    point = None
    lines = []

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
        # if rotation > 180:
        #     rotation -= 180
        #     self.start_point = (x2,y2)
        #     self.end_point = (x1,y1)
        # else:
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
