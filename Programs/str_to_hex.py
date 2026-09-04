# -*- coding: utf-8 -*-

import sys

help_text = r"""用法：str_to_hex.py [<要转换的字符串>]
    如果要转换的字符串未指定，则会提示你输入要转换的字符串。

在注册表中，字符串是以 UTF-16 小端序存储的，并且会在导出时导出为 UTF-16 小端序编码格式，以 ,（英文半角逗号）分割，例如：
    qwerty -> 71,00,77,00,65,00,72,00,74,00,79,00
    注册表文件 -> e8,6c,8c,51,68,88,87,65,f6,4e
"""

def str_to_hex(data: str):
    """用于把字符串按照 UTF-16 小端序的编码格式输出，以 , 分割字节串，例如 '注册表文件' -> e8,6c,8c,51,68,88,87,65,f6,4e。"""
    print(data.encode("utf-16-le").hex(","))

if __name__ == '__main__':
    try:
        data = sys.argv[1]
    except:
        print(help_text)
        data = input("请输入要转换的字符串：")
    if data:
        str_to_hex(data)
    else:
        print("你没有输入要转换的字符串。")
