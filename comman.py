#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
from color_output import *

content_type = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'json': 'application/json',
    'plain': 'text/plain',
}

def upload(url, files, data={}, headers={}):
    # 构造请求体
    try:
        r = requests.post(
            url,
            files=files,
            data=data,
            headers=headers,
            timeout=5
        )
        print(blue('[ result ]') + fuchsia('状态码:') + green(r.status_code))
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(yellow('[ Warn ]') + e)
    return

def setContentType(ext=''):
    # 设置content-type
    if ext != '':
        try:
            ct = content_type[ext]
        except:
            ct = content_type['plain']
    else:
        ct = content_type['plain']
    return ct