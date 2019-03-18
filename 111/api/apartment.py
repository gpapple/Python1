# coding:utf-8
import math
# import cv2
# import numpy as np
import sys, json, os


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


def convert_json(json_data, file_name=None):
    in_rooms = json_data.get('InRooms')
    out_walls = json_data.get('OutWall')
    out_wall_points = out_walls.get('WallPoints')
    doors = json_data.get('DoorList')
    windows = json_data.get('WindowList')
    x_list = []
    y_list = []
    for point in out_wall_points:
        x_list.append(point['X'])
        y_list.append(point['Y'])
    mean_x = (max(x_list) + min(x_list)) / 2
    mean_y = (max(y_list) + min(y_list)) / 2
    door_list = []
    for door in doors:
        length1 = math.sqrt((door['Side_One'][0]['X'] - door['Side_One'][1]['X']) * (
            door['Side_One'][0]['X'] - door['Side_One'][1]['X']) + (
                                door['Side_One'][0]['Y'] - door['Side_One'][1]['Y']) * (
                                door['Side_One'][0]['Y'] - door['Side_One'][1]['Y']))
        length2 = math.sqrt((door['Side_One'][0]['X'] - door['Side_Two'][0]['X']) * (
            door['Side_One'][0]['X'] - door['Side_Two'][0]['X']) + (
                                door['Side_One'][0]['Y'] - door['Side_Two'][0]['Y']) * (
                                door['Side_One'][0]['Y'] - door['Side_Two'][0]['Y']))
        door_point_x = sum([door['Side_One'][0]['X'], door['Side_One'][1]['X'], door['Side_Two'][0]['X'],
                            door['Side_Two'][1]['X']]) / 4
        door_point_y = sum([door['Side_One'][0]['Y'], door['Side_One'][1]['Y'], door['Side_Two'][0]['Y'],
                            door['Side_Two'][1]['Y']]) / 4
        door_info = {
            'x': (door_point_x - mean_x) / 100,
            'y': (door_point_y - mean_y) / 100,
            'length': max(length1, length2) / 100,
            'width': min(length1, length2) / 100
        }
        door_list.append(door_info)
    window_list = []
    for window in windows:
        length1 = math.sqrt((window['Side_One'][0]['X'] - window['Side_One'][1]['X']) * (
            window['Side_One'][0]['X'] - window['Side_One'][1]['X']) + (
                                window['Side_One'][0]['Y'] - window['Side_One'][1]['Y']) * (
                                window['Side_One'][0]['Y'] - window['Side_One'][1]['Y']))
        length2 = math.sqrt((window['Side_One'][0]['X'] - window['Side_Two'][0]['X']) * (
            window['Side_One'][0]['X'] - window['Side_Two'][0]['X']) + (
                                window['Side_One'][0]['Y'] - window['Side_Two'][0]['Y']) * (
                                window['Side_One'][0]['Y'] - window['Side_Two'][0]['Y']))
        window_point_x = sum([window['Side_One'][0]['X'], window['Side_One'][1]['X'], window['Side_Two'][0]['X'],
                              window['Side_Two'][1]['X']]) / 4
        window_point_y = sum([window['Side_One'][0]['Y'], window['Side_One'][1]['Y'], window['Side_Two'][0]['Y'],
                              window['Side_Two'][1]['Y']]) / 4
        window_info = {
            'x': (window_point_x - mean_x) / 100,
            'y': (window_point_y - mean_y) / 100,
            'length': max(length1, length2) / 100,
            'width': min(length1, length2) / 100
        }
        window_list.append(window_info)
    output_data = []
    for room_data in in_rooms:
        # print(room_data)
        output_room = {}
        room_name = room_data['Index']
        print('房间%s' % room_name)
        output_room.update({'index': room_name})
        formulas = []
        wall_widths = []
        tmp_line = None
        for index, in_wall in enumerate(room_data['InWalls']):
            start_point = in_wall['EndPoint']
            end_point = in_wall['StartPoint']
            width = in_wall['Thickness']
            formula = LineFormula(start_point['X'], start_point['Y'], end_point['X'], end_point['Y'])
            if math.fabs(formula.length) < 0.0001:
                continue
            if not tmp_line:
                tmp_line = {'start_point': start_point, 'end_point': end_point, 'width': width}
                continue
            tmp_formula = LineFormula(tmp_line['start_point']['X'], tmp_line['start_point']['Y'],
                                      tmp_line['end_point']['X'], tmp_line['end_point']['Y'])
            if tmp_formula.formula.rotation == formula.formula.rotation and math.sqrt(
                                    (tmp_line['end_point']['X'] - start_point['X']) * (
                                        tmp_line['end_point']['X'] - start_point['X']) + (
                                tmp_line['end_point']['Y'] - start_point['Y']) * (
                                tmp_line['end_point']['Y'] - start_point['Y'])) < 0.001 and (
                            width == tmp_line['width'] or width - tmp_line['width'] > 1000):
                tmp_line['end_point'] = end_point
                continue
            else:
                formulas.append(
                    LineFormula(tmp_line['start_point']['X'] - mean_x, tmp_line['start_point']['Y'] - mean_y,
                                tmp_line['end_point']['X'] - mean_x, tmp_line['end_point']['Y'] - mean_y))
                wall_widths.append(tmp_line['width'])
                tmp_line = {'start_point': start_point, 'end_point': end_point, 'width': width}
        if tmp_line:
            tmp_formula = LineFormula(tmp_line['start_point']['X'], tmp_line['start_point']['Y'],
                                      tmp_line['end_point']['X'], tmp_line['end_point']['Y'])
            # print(tmp_line['end_point'], room_data['InWalls'][0]['EndPoint'])
            if tmp_formula.formula.rotation == formulas[0].formula.rotation and math.sqrt(
                                    (tmp_line['end_point']['X'] - formulas[0].start_point[0] - mean_x) * (
                                            tmp_line['end_point']['X'] - formulas[0].start_point[0] - mean_x) + (
                                    tmp_line['end_point']['Y'] - formulas[0].start_point[1] - mean_y) * (
                                    tmp_line['end_point']['Y'] - formulas[0].start_point[1] - mean_y)) < 0.001 and (
                            width == tmp_line['width'] or width - tmp_line['width'] > 1000):
                formulas[0] = LineFormula(tmp_line['start_point']['X'] - mean_x, tmp_line['start_point']['Y'] - mean_y,
                                          formulas[0].start_point[0], formulas[0].start_point[1])
            else:
                formulas.append(
                    LineFormula(tmp_line['start_point']['X'] - mean_x, tmp_line['start_point']['Y'] - mean_y,
                                tmp_line['end_point']['X'] - mean_x, tmp_line['end_point']['Y'] - mean_y))
                wall_widths.append(tmp_line['width'])
        middle_wall_lines = []
        new_formulas = []
        for index, formula in enumerate(formulas):
            # 根据原线和宽度推导出中线公式
            new_formula = Formula(formula.formula.a, formula.formula.b, formula.formula.c + wall_widths[index] / 2 * formula.formula.a * math.sin(
                formula.formula.rotation / 180 * math.pi) - wall_widths[index] / 2 * formula.formula.b * math.cos(
                formula.formula.rotation / 180 * math.pi), formula.formula.rotation)
            new_formulas.append(new_formula)
        start_point = {}
        end_point = {}
        tmp_wall_lines = []
        for index, new_formula in enumerate(new_formulas):
            width = wall_widths[index]
            start_intersection = new_formula.intersection(
                new_formulas[(index - 1 + len(new_formulas)) % len(new_formulas)])
            end_intersection = new_formula.intersection(new_formulas[(index + 1) % len(new_formulas)])
            # print(start_intersection, end_intersection, wall_widths[index])
            if end_intersection and not start_intersection:
                start_intersection = {'x': formulas[index].start_point[0] + width / 2 * math.sin(
                    new_formulas[index].rotation / 180 * math.pi),
                                      'y': formulas[index].start_point[0] - width / 2 * math.cos(
                                          new_formulas[index].formula.rotation / 180 * math.pi)}
            if start_intersection and not end_intersection:
                end_intersection = {'x': formulas[index].end_point[0] + width / 2 * math.sin(
                    new_formulas[index].formula.rotation / 180 * math.pi),
                                    'y': formulas[index].end_point[0] - width / 2 * math.cos(
                                        new_formulas[index].formula.rotation / 180 * math.pi)}
            if start_intersection != float('inf'):
                start_point = {
                    'x': start_intersection[0] / 100,
                    'y': start_intersection[1] / 100
                }
            if end_intersection != float('inf'):
                end_point = {
                    'x': end_intersection[0] / 100,
                    'y': end_intersection[1] / 100
                }
            if start_point and end_point:
                line_info = {
                    'width': wall_widths[index] / 100,
                    'startPoint': start_point,
                    'endPoint': end_point
                }
                tmp_wall_lines.append(line_info)
        lonely_lines = []
        for index in range(len(tmp_wall_lines)):
            wall_line = tmp_wall_lines[index]
            # print(wall_line)
            length = math.sqrt((wall_line['startPoint']['x'] - wall_line['endPoint']['x']) * (
                wall_line['startPoint']['x'] - wall_line['endPoint']['x']) + (
                                   wall_line['startPoint']['y'] - wall_line['endPoint']['y']) * (
                                   wall_line['startPoint']['y'] - wall_line['endPoint']['y']))
            width = wall_line['width']
            if length < 0.01:
                if new_formulas[(index - 1 + len(new_formulas)) % len(new_formulas)].rotation != new_formulas[
                            (index + 1) % len(new_formulas)].rotation:
                    # print(wall_line)
                    start_point = wall_line['startPoint']
                    end_point = {
                        'x': start_point['x'] + width / 2 * math.sin(new_formulas[index].rotation / 180 * math.pi),
                        'y': start_point['y'] - width / 2 * math.cos(new_formulas[index].rotation / 180 * math.pi)}
                    lonely_line = {'startPoint': start_point, 'endPoint': end_point, 'width': width}
                    lonely_lines.append(lonely_line)
                    continue
                else:
                    continue
            if length < wall_line['width']/4 and abs(new_formulas[(index - 1 + len(new_formulas)) % len(new_formulas)].rotation-new_formulas[
                            (index + 1) % len(new_formulas)].rotation) <= 1:
                middle_wall_lines[-1]['endPoint'] = {
                    'x': middle_wall_lines[-1]['endPoint']['x'] + width / 2 * math.sin(new_formulas[index].rotation / 180 * math.pi),
                    'y': middle_wall_lines[-1]['endPoint']['y'] - width / 2 * math.cos(new_formulas[index].rotation / 180 * math.pi)
                }
                wall_line['startPoint'] = {
                    'x': wall_line['startPoint']['x'] + width / 2 * math.sin(new_formulas[index].rotation / 180 * math.pi),
                    'y': wall_line['startPoint']['y'] - width / 2 * math.cos(new_formulas[index].rotation / 180 * math.pi)
                }
                wall_line['endPoint'] = {
                    'x': wall_line['endPoint']['x'] + width / 2 * math.sin(
                        new_formulas[index].rotation / 180 * math.pi),
                    'y': wall_line['endPoint']['y'] - width / 2 * math.cos(
                        new_formulas[index].rotation / 180 * math.pi)
                }
                wall_line['width'] = 0
                tmp_wall_lines[(index+1)%len(tmp_wall_lines)]['startPoint'] = {
                    'x': tmp_wall_lines[(index+1)%len(tmp_wall_lines)]['startPoint']['x'] + width / 2 * math.sin(
                        new_formulas[index].rotation / 180 * math.pi),
                    'y': tmp_wall_lines[(index+1)%len(tmp_wall_lines)]['startPoint']['y'] - width / 2 * math.cos(
                        new_formulas[index].rotation / 180 * math.pi)
                }
            middle_wall_lines.append(wall_line)
        output_room.update({'wallLines': middle_wall_lines})
        output_room.update({'singleLines': lonely_lines})
        room_doors = []
        for door in room_data['DoorIndex']:
            room_doors.append(door_list[door])
        output_room.update({'doors': room_doors})
        room_windows = []
        for window in room_data['WindowIndex']:
            room_windows.append(window_list[window])
        output_room.update({'windows': room_windows})
        # print(output_room)
        # print(room_windows)
        output_data.append(output_room)
    # print(output_data)
    # if file_name:
    #     img = np.zeros((4096, 4096, 3), np.uint8)
    #     for index, out_wall_point in enumerate(out_wall_points):
    #         cv2.line(img, (
    #             int((out_wall_point['X'] - mean_x) / 10) + 2048, -int((out_wall_point['Y'] - mean_y) / 10) + 2048),
    #                  (int((out_wall_points[(index + 1) % len(out_wall_points)]['X'] - mean_x) / 10) + 2048,
    #                   -int((out_wall_points[(index + 1) % len(out_wall_points)]['Y'] - mean_y) / 10) + 2048),
    #                  (255, 255, 255))
    #     for room in json_data['InRooms']:
    #         for wall_line in room['InWalls']:
    #             cv2.line(img, (
    #                 int((wall_line['StartPoint']['X'] - mean_x) / 10) + 2048,
    #                 -int((wall_line['StartPoint']['Y'] - mean_y) / 10) + 2048),
    #                      (int((wall_line['EndPoint']['X'] - mean_x) / 10) + 2048,
    #                       -int((wall_line['EndPoint']['Y'] - mean_y) / 10) + 2048),
    #                      (255, 255, 255))
    #     for room in output_data:
    #         for line in room['wallLines']:
    #             cv2.line(img, (int(line['startPoint']['x'] * 10) + 2048, -int(line['startPoint']['y'] * 10) + 2048),
    #                      (int(line['endPoint']['x'] * 10) + 2048, -int(line['endPoint']['y'] * 10) + 2048), (255, 0, 0))
    #         for line in room['singleLines']:
    #             cv2.line(img, (int(line['startPoint']['x'] * 10) + 2048, -int(line['startPoint']['y'] * 10) + 2048),
    #                      (int(line['endPoint']['x'] * 10) + 2048, -int(line['endPoint']['y'] * 10) + 2048), (255, 0, 0))
    #     for door in doors:
    #         cv2.line(img, (int(door['Side_One'][0]['X'] - mean_x) // 10 + 2048,
    #                        -int(door['Side_One'][0]['Y'] - mean_y) // 10 + 2048),
    #                  (int(door['Side_One'][1]['X'] - mean_x) // 10 + 2048,
    #                   -int(door['Side_One'][1]['Y'] - mean_y) // 10 + 2048), (0, 255, 0))
    #         cv2.line(img, (int(door['Side_Two'][0]['X'] - mean_x) // 10 + 2048,
    #                        -int(door['Side_Two'][0]['Y'] - mean_y) // 10 + 2048),
    #                  (int(door['Side_Two'][1]['X'] - mean_x) // 10 + 2048,
    #                   -int(door['Side_Two'][1]['Y'] - mean_y) // 10 + 2048), (0, 255, 0))
    #         cv2.line(img, (int(door['Side_One'][0]['X'] - mean_x) // 10 + 2048,
    #                        -int(door['Side_One'][0]['Y'] - mean_y) // 10 + 2048),
    #                  (int(door['Side_Two'][0]['X'] - mean_x) // 10 + 2048,
    #                   -int(door['Side_Two'][0]['Y'] - mean_y) // 10 + 2048), (0, 255, 0))
    #         cv2.line(img, (int(door['Side_One'][1]['X'] - mean_x) // 10 + 2048,
    #                        -int(door['Side_One'][1]['Y'] - mean_y) // 10 + 2048),
    #                  (int(door['Side_Two'][1]['X'] - mean_x) // 10 + 2048,
    #                   -int(door['Side_Two'][1]['Y'] - mean_y) // 10 + 2048), (0, 255, 0))
    #     for window in windows:
    #         cv2.line(img, (int(window['Side_One'][0]['X'] - mean_x) // 10 + 2048,
    #                        -int(window['Side_One'][0]['Y'] - mean_y) // 10 + 2048),
    #                  (int(window['Side_One'][1]['X'] - mean_x) // 10 + 2048,
    #                   -int(window['Side_One'][1]['Y'] - mean_y) // 10 + 2048), (0, 0, 255))
    #         cv2.line(img, (int(window['Side_Two'][0]['X'] - mean_x) // 10 + 2048,
    #                        -int(window['Side_Two'][0]['Y'] - mean_y) // 10 + 2048),
    #                  (int(window['Side_Two'][1]['X'] - mean_x) // 10 + 2048,
    #                   -int(window['Side_Two'][1]['Y'] - mean_y) // 10 + 2048), (0, 0, 255))
    #         cv2.line(img, (int(window['Side_One'][0]['X'] - mean_x) // 10 + 2048,
    #                        -int(window['Side_One'][0]['Y'] - mean_y) // 10 + 2048),
    #                  (int(window['Side_Two'][0]['X'] - mean_x) // 10 + 2048,
    #                   -int(window['Side_Two'][0]['Y'] - mean_y) // 10 + 2048), (0, 0, 255))
    #         cv2.line(img, (int(window['Side_One'][1]['X'] - mean_x) // 10 + 2048,
    #                        -int(window['Side_One'][1]['Y'] - mean_y) // 10 + 2048),
    #                  (int(window['Side_Two'][1]['X'] - mean_x) // 10 + 2048,
    #                   -int(window['Side_Two'][1]['Y'] - mean_y) // 10 + 2048), (0, 0, 255))
    #     cv2.imwrite(file_name.replace('.json', '.png'), img)
    return output_data


if __name__ == '__main__':
    file_name = sys.argv[1]
    json_data = ''
    with open(file_name, 'r+') as file:
        for line in file.readlines():
            json_data += line
    json_data = json.loads(json_data)
    out_json = convert_json(json_data, file_name)
    print(os.path.splitext(file_name)[0])
    os.rename(file_name,'%sbak.json' % os.path.splitext(file_name)[0])
    with open(file_name, 'wb') as file:
        file.write(json.dumps(out_json).encode('utf-8'))
