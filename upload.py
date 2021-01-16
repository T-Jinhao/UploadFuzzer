#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import argparse
import sys

class UPLOAD:
    def __init__(self, args):
        self.args = args
        self.cookies = self.getCookie()

    def run(self):
        if self.args.attach != '':
            self.suffix = self.getSuffix(self.args.attach)
            # 占坑，未完成
        if self.args.bypass:
            pass
        elif self.args.bypass_ignore:
            pass
        else:    # 正常上传
            F = self.getFileContent(self.args.f)
            files = {self.args.param: F}
            self.upload(files)


    def getSuffix(self, filename):
        # 获取文件名后缀
        try:
            ext = filename.split('.')[-1]
            return ext
        except:
            print('获取文件后缀名失败')
            sys.exit()

    def getFileContent(self, file):
        # 获取文件内容
        try:
            F = open(file, 'rb')
            return F
        except:
            print('读取文件失败')
            sys.exit()

    def getCookie(self):
        # 解析document.cookie
        cookie = self.args.c
        if cookie == None:
            return None
        cookies = {}  # 初始化cookies字典变量
        try:
            for x in cookie.split(';'):  # 按照字符：进行划分读取
                name, value = x.strip().split('=', 1)
                cookies[name] = value  # 为字典cookies添加内容
        except:
            print('cookie格式错误')
            sys.exit()
        return cookies

    def upload(self, files, data={}, headers={}):
        # 构造请求体
        try:
            r = requests.post(
                self.args.u,
                files=files,
                data=data,
                headers=headers,
                timeout=5
            )
            print('状态码:', r.status_code)
            print(r.text)
            print()
            if r.status_code == 200:
                return True
        except:
            pass
        return False


def terminal_parser():
    if len(sys.argv)==1 :
        sys.argv.append('-h')
    parser = argparse.ArgumentParser(description='动态文件上传', add_help=True)
    parser.add_argument('-u', help='文件接收URL路径')
    parser.add_argument('-c', help='document.cookie，选填', default=None)
    parser.add_argument('-f', help='上传文件')
    parser.add_argument('--param', help='上传参数名')
    parser.add_argument('--attach', help='webshell文件，附加时将尝试附加在正常文件内', default='')
    parser.add_argument('--bypass', help='尝试绕过WAF，成功即停', action='store_true')
    parser.add_argument('--bypass_ignore', help='尝试绕过WAF，尝试全部payload', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = terminal_parser()
    x = UPLOAD(args)
    x.run()