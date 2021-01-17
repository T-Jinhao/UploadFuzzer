#!/usr/bin/python
# -*- encoding:utf8 -*-
import platform
from colorama import Fore,init

# 前景色彩色表
Red = '\033[1;31m'  # 红色
Green = '\033[1;32m'  # 绿色
Yellow = '\033[1;33m'  # 黄色
Blue = '\033[1;34m'  # 蓝色
Fuchsia = '\033[1;35m'  # 紫红色
Cyan = '\033[1;36m'  # 青蓝色
White = '\033[1;37m'  # 白色
Reset = '\033[0m'  # 终端默认颜色

def red(s):
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(Red, str(s), Reset)

def green(s):
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(Green, str(s), Reset)

def yellow(s):
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(Yellow, str(s), Reset)

def blue(s):
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(Blue, str(s), Reset)

def fuchsia(s):
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(Fuchsia, str(s), Reset)

def cyan(s):
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(Cyan, str(s), Reset)

def white(s):
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(White, str(s), Reset)

def interval():
    if platform.system() == 'Windows':
        init(autoreset=True)
    return "{0}{1}{2}".format(Red, ' | ', Reset)