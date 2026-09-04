# -*- coding: utf-8 -*-

"""按照注册表编辑器对于注册表文件的解析逻辑解析注册表文件。"""

import sys

const_header = "Windows Registry Editor Version"

def check_and_parse(reg_file: str):
    with open(reg_file, "r", encoding = "utf-16-le") as file:
        """第一部分：文件头"""
        file.seek(2) # 跳过前两个 BOM 字符
        header = file.readline()
        header = header.strip('\n')
        if not header.startswith(const_header):
            print("指定的文件不是注册脚本。\n你在注册表编辑器中只能导入二进位注册文件。", file = sys.stderr)
            sys.exit(1)
        # 检查版本
        version_string = ""
        before_point = True # 用于判断是否在小数点前
        before_first_zero = True # 用于判断是否在第一个 '0' 字符前
        before_first_char = True # 用于判断是否在第一个有效的版本字符串前（即字符 '5' 前）
        # 从 const_header 之后的位置开始逐个检查字符，并尝试提取版本信息
        for char in header[len(const_header):]:
            if char.isdigit():
                if char == "0":
                    # '0' 字符需要在小数点后面才能添加
                    if not before_point:
                        version_string += char
                        before_first_zero = False
                    else: # 在小数点前面的任何 0 都会被忽略
                        pass
                elif char == "5":
                    # 如果 version_string 不为空，说明前面已经有一个 5 了，不允许再出现一个 5
                    # 这样会形成 5.5x 或者 5.x5 这样的版本从而判定版本非法（x 为任意数字字符）
                    if version_string:
                        print("指定的文件不能和该版本的 Windows 一起使用。", file = sys.stderr)
                        sys.exit(1)
                    else:
                        version_string += char
                        before_first_char = False
                else:
                    print("指定的文件不能和该版本的 Windows 一起使用。", file = sys.stderr)
                    sys.exit(1)
            elif char == ".":
                # 如果遇到了小数点，且 before_point 为真，则说明小数点还未被添加，添加小数点并将 before_point 设为假
                if before_point:
                    # 必须在字符 '5' 之后才能添加，因此 .5 是非法的
                    if before_first_char:
                        print("指定的文件不是注册表文件。只可导入注册表文件。", file = sys.stderr)
                        sys.exit(1)
                    else:
                        version_string += char
                        before_point = False
                elif before_first_zero: # 不允许在第一个 '0' 字符之前有更多的小数点，例如 5.00 是不允许的
                    print("指定的文件不是注册表文件。只可导入注册表文件。", file = sys.stderr)
                    sys.exit(1)
                else: # 会被系统忽略
                    pass
            else:
                if before_point: # 不允许在小数点前出现其他字符
                    print("指定的文件不是注册表文件。只可导入注册表文件。", file = sys.stderr)
                    sys.exit(1)
                else:
                    pass
            if version_string == "5.00":
                break
        if version_string != "5.00":
            print("指定的文件不是注册表文件。只可导入注册表文件。", file = sys.stderr)
            sys.exit(1)
        """第二部分：正文"""
        registry_item = "" # 存储有效的注册表项
        for line in file:
            line = line.strip('\n')
            if not line or line.startswith(" "): # 是空行或空格开头
                continue
            elif line.startswith(';'): # 是注释
                print(f'行 "{line}" 是注释，忽略')
            elif line.startswith('@'): # 给无名称键（(默认)）的字符
                # 如果是有效的注册表项，则检查其后面的注释
                if registry_item:
                    pass # 当前还不检查注释
                else:
                    print(f'忽略行 "{line}"，因为在第一条有效的注册表项前')
            elif line.startswith('"'):
                # 如果是有效的注册表项，则检查其后面的注释
                if registry_item:
                    pass # 当前还不检查注释
                else:
                    print(f'忽略行 "{line}"，因为在第一条有效的注册表项前')
            elif line.startswith('['): # 注册表项的开始
                has_closed = False # 方括号是否闭合
                temp_string = ""
                for char in line[1:]:
                    if char == ']':
                        has_closed = True
                        if len(line[line.index(char) + 1:]):
                            print(f'忽略 "{temp_string}" 后面的文本 "{line[line.index(char) + 1:]}"')
                        break # 不再检查后面的任何文本
                    else:
                        temp_string += char
                if has_closed:
                    registry_item = temp_string
                else:
                    print(f'忽略行 "{line}"，因为其方括号没有闭合（缺少右方括号）')
            else:
                print(f'忽略行 "{line}"')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法：checker.py <要检查的注册表文件路径>", file = sys.stderr)
        sys.exit(1)
    else:
        sys.exit(check_and_parse(sys.argv[1]))