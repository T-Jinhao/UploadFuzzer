#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import requests
import re
import os
import random
import string
from color_output import *
from urllib.parse import urljoin

content_type = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'json': 'application/json',
    'plain': 'text/plain',
}
class Comman:
    def __init__(self, initUrl):
        '''
        初始化
        :param initUrl: 初始请求url
        :param initUrls: 初始页面url集
        '''
        self.initUrl = initUrl

    def upload(self, url, files, data={}, headers={}):
        # 构造请求体
        try:
            r = requests.post(
                url,
                files=files,
                data=data,
                headers=headers,
                timeout=5
            )
            print(blue('[ upload ]') + fuchsia('状态码:') + green(r.status_code))
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(yellow('[ Warn ]') + e)
        return

    def setContentType(self, ext=''):
        # 设置content-type
        if ext != '':
            try:
                ct = content_type[ext]
            except:
                ct = content_type['plain']
        else:
            ct = content_type['plain']
        return ct

    def checkStatus(self, url):
        # 检测结果存活
        result = 0
        try:
            r = requests.get(
                url,
                timeout=5
            )
            if r.status_code != 404:
                print(green('[ match_status ]') + cyan(r.status_code))
                result = 1
            else:
                print(yellow('[ match_status ]') + cyan(r.status_code))
        except Exception as e:
            print(yellow('[ Warn ]') + e)
        return result

    def comparaUrls(self, initUrls, urls):
        # 对比页面url差别
        count = 0
        if urls == []:
            return count
        for u in urls:
            if u not in initUrls:
                print(green('[ match ]') + u)
                count += self.checkStatus(u)
        return count

    def checkResult(self, initUrls, res):
        # 检查结果
        if res != None:  # 通过与初始页面对比尝试找出上传路径
            urls = self.extractUrls(res)      # 提取URL
            result = self.comparaUrls(initUrls, urls)            # 结果对比
            if result > 0:
                return True
        print()
        return False

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
                    u = self.url_check(m)
                    if u not in resultUrls and u:
                        resultUrls.append(u)
        return resultUrls

    def url_check(self, u):
        # 检测url完整性，返回绝对地址
        err = ['', None, '/', '\n']
        if u in err:
            return
        if re.match("(http|https)://.*", u):  # 匹配绝对地址
            return u
        else:  # 拼凑相对地址，转换成绝对地址
            u = urljoin(self.initUrl, u)
            return u

    def getRandomStr(self, length=8):
        # 生成随机字符串
        ran_str = ''
        for _ in range(length):
            ran_str += random.choice(string.ascii_letters + string.digits)
        return ran_str


    def getFilename(self, file):
        # 获取文件名
        (path, filename) = os.path.split(file)
        return filename
