# coding: utf-8
import os
import subprocess

import uuid as uid
def uuid():
    return str(uid.uuid4()).split('-')[0] + str(uid.uuid1()).split('-')[0]

def convert_dxf_to_dwg(dxf, dwg):
    convert_tool = os.path.join('plugins', 'App', 'Acme CAD Converter',
                                'AcmeCADConverter')
    command = '%s /r /g2007 %s %s' % (
        convert_tool, dxf, dwg)
    ps = subprocess.Popen(command)
    ps.wait()

def convert_js_to_dxf(js):
    convert_tool = os.path.join('plugins', 'converter', 'Converter.exe')
    convert_tool = 'E:\\Converter\\Converter.exe'
    command = '%s -i %s -t apartment' % (convert_tool, js)
    ps = subprocess.Popen(command)
    ps.wait()

def convert_dwg_to_dxf(dwg, dxf):
    convert_tool = os.path.join('plugins', 'App', 'Acme CAD Converter',
                                'AcmeCADConverter')
    command = '%s /r /x2007 %s %s' % (
        convert_tool, dwg, dxf)
    ps = subprocess.Popen(command)
    ps.wait()

def convert_dwg_to_json(js, format):
    convert_tool = os.path.join('plugins', 'converter', 'Converter.exe')
    convert_tool = 'E:\\Converter\\Converter.exe'
    command = '%s -i %s -t contour -f %s' % (convert_tool, js, format)
    ps = subprocess.Popen(command)
    ps.wait()
