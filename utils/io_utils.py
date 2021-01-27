#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: io_utils.py
@time: 2021/1/27 17:34
@desc:
'''

import json


def write_json_file(file_path='', data=None):
    if not data:
        return
    with open(file_path, 'w') as outfile:
        j_data = json.dumps(data)
        outfile.write(j_data)


def load_json_file(filepath=''):
    with open(filepath) as infile:
        contents = infile.read()
        return json.loads(contents)