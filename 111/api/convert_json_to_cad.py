#coding utf-8
import sys, json
import ezdxf
from entity import LineFormula
import math

def convert_json_to_cad(json_data):
    dxf = ezdxf.new('AC1015')
    model_space = dxf.modelspace()
    room_datas = json_data['inRoomData']
    out_lines = json_data['outLines']
    labels = json_data['labels']
    draw_room_data(model_space, room_datas, out_lines, labels)
    dxf.saveas('out.dxf')

def draw_room_data(model_space, room_datas, out_lines, labels):
    for out_room in out_lines:
        for index,point in enumerate(out_room):
            model_space.add_line((-point['y']*100,point['x']*100), (-out_room[(index+1)%len(out_room)]['y']*100,out_room[(index+1)%len(out_room)]['x']*100))
    for label in labels:
        draw_dimension(model_space, (-label['start']['y']*100, label['start']['x']*100), (-label['end']['y']*100, label['end']['x']*100), 200, 200)
    for room_data in room_datas:
        inner_point_list = room_data['pointList']
        middle_point_list = room_data['middlePoints']
        furns = room_data['furnList']
        for index,point in enumerate(inner_point_list):
            model_space.add_line((-point['y'] * 100, point['x'] * 100), (
            -inner_point_list[(index + 1) % len(inner_point_list)]['y'] * 100, inner_point_list[(index + 1) % len(inner_point_list)]['x'] * 100))
        for index,point in enumerate(middle_point_list):
            model_space.add_line((-point['y'] * 100, point['x'] * 100), (
            -middle_point_list[(index + 1) % len(middle_point_list)]['y'] * 100, middle_point_list[(index + 1) % len(middle_point_list)]['x'] * 100))
        for furn in furns:
            if not furn.get('box'):
                continue
            a = furn['box'][0]*100
            b = furn['box'][1]*100
            position = (-furn['position']['z']*100, furn['position']['x']*100)
            scale = (furn['scale']['z'], furn['scale']['x'])
            angle = furn['rotation']['y']
            vector_a = point_rotation((0, 0), (b / 2, a / 2), -angle)
            vector_b = point_rotation((0, 0), (b / 2, -a / 2), -angle)
            vector_c = point_rotation((0, 0), (-b / 2, -a / 2), -angle)
            vector_d = point_rotation((0, 0), (-b / 2, a / 2), -angle)
            print(position, vector_a, vector_b, vector_c, vector_d)
            model_space.add_line((position[0] + vector_a[0], position[1] + vector_a[1]),(position[0] + vector_b[0], position[1] + vector_b[1]))
            model_space.add_line((position[0] + vector_b[0], position[1] + vector_b[1]),(position[0] + vector_c[0], position[1] + vector_c[1]))
            model_space.add_line((position[0] + vector_c[0], position[1] + vector_c[1]),(position[0] + vector_d[0], position[1] + vector_d[1]))
            model_space.add_line((position[0] + vector_d[0], position[1] + vector_d[1]),(position[0] + vector_a[0], position[1] + vector_a[1]))


def draw_dimension(model_space, start_point, end_point, offset, height):
    line = LineFormula(start_point[0], start_point[1], end_point[0], end_point[1])
    if line.length <= 300:
        return
    start1,end1 = line.move(offset)
    start2,end2 = line.move(-offset)
    model_space.add_line(start_point, end_point)
    model_space.add_line(start1, start2)
    model_space.add_line(end1, end2)
    attribs = {
        'height': height,
        'insert': ((start_point[0]+end_point[0])/2,(start_point[1]+end_point[1])/2),
    }
    model_space.add_text('%d' % line.length, attribs)


def point_rotation(point, target, angle):
    return (point[0] + target[0]*math.cos(angle) - target[1]*math.sin(angle),
            point[1] + target[0]*math.sin(angle) + target[1]*math.cos(angle))


if __name__=='__main__':
    file_name = sys.argv[1]
    json_data = ''
    with open(file_name, 'rb') as file:
        for line in file.readlines():
            json_data += line.decode('utf-8')
    json_data = json.loads(json_data)
    convert_json_to_cad(json_data)