#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/9 10:21 PM
# @Author  : w8ay
# @File    : auto_build_chunked.py

# 根据payload内容自动生成分块，自动分割关键字
# chunk_size控制到1-9之内,遇到关键词自动切割
import string
import random

def chunk_data(data, keywords: list):
    dl = len(data)
    ret = ""
    index = 0
    while index < dl:
        chunk_size = random.randint(1, 9)
        if index + chunk_size >= dl:
            chunk_size = dl - index
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        while 1:
            tmp_chunk = data[index:index + chunk_size]
            tmp_bool = True
            for k in keywords:
                if k in tmp_chunk:
                    chunk_size -= 1
                    tmp_bool = False
                    break
            if tmp_bool:
                break
        index += chunk_size
        ret += "{0};{1}\r\n".format(hex(chunk_size)[2:], salt)
        ret += "{0}\r\n".format(tmp_chunk)

    ret += "0\r\n\r\n"
    return ret

def gen_body():
    pass

# hack = HackRequests.hackRequests()
#
# r = hack.httpraw(raw)
# print(raw)
#
# print(r.text())
# print(r.log)