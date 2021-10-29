#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : elfin
# @Time     : 2021/10/27 9:31
# @File     : parser_ana.py
# @Project  : python-common-functions

import argparse

examples = """examples:
    # 初始化解析器
    parser = argparse.ArgumentParser(description=%(prog)s程序的简单介绍)
    # 添加参数
    parser.add_argument('--name', default='', help='Add parameter description')
"""

arg = argparse.ArgumentParser(
    description="命令行参数使用及其功能说明",
    epilog=examples,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
# # arg.add_argument("-n", "--name", default='firstelfin', help="所有者姓名")
# arg.add_argument("-n", "--name", default='firstelfin', dest="n", help="所有者姓名")
# arg.add_argument("-student-of-IBM", default='', help="学生名字")
# arg.add_argument("--city", nargs="?", const="chengdu", default="guangzhou", help="city name")
# arg.add_argument("home", nargs="*", default="guangzhou", help="city name")
# arg.add_argument("home", nargs="?", const="chengdu", default="guangzhou", help="city name")
# arg.add_argument("--subject1", nargs="+", dest="s1", metavar="e", default="mathematics", help="subject name")
# arg.add_argument("--subject2", nargs="+", dest="s2", default="mathematics", help="subject name")
# arg.add_argument("--anchor", type=list, required=True, metavar="锚框", help="anchor coordinate")
# arg.add_argument("--performance", action="count", help="performance")
# arg.add_argument("subject2", nargs="+", default="mathematics", help="subject name")
# arg.add_argument('-V', action='version', version='parser_ana V20211029')
# arg.add_argument("-p", action="SubParsers", help="performance")

arg.add_argument("--model", required=True, help="模型加载路径")
# 添加子解析器
subparsers = arg.add_subparsers(description="模型训练子解析器", dest="command", help="子解析器对象")
parser_train = subparsers.add_parser(name="train", help="训练一个模型")
parser_train.add_argument("--batchsize", default=64, help="Train batch size")
parser_train.add_argument("-lr", required=True, default="WarmUp", help="Learning rate of train")

parser_valid = subparsers.add_parser(name="valid", help="验证一个模型")
parser_valid.add_argument("--batchsize", default=64, help="Valid batch size")
parser_valid.add_argument("--out", type=str, required=True, help="Result output path")


args = arg.parse_args()

if __name__ == '__main__':
    # print(args.n)
    # print(args.student_of_IBM)
    # print(args.s)
    # print(args.city)
    # print(args.home)
    print(args.p)
