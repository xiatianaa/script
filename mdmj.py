"""
cron: 10 10 * * * mdmj.py
new Env('美的美居');
updatetime:2022/10/22
"""


import requests
from config import global_config
from qywx_push import send

cookie = global_config.get('mdmj', 'cookie')

def qiandao():
    url = 'https://mvip.midea.cn/act/taobao/api/sign?channel=mj'
    headers = {
        'User-Agent': 'Mi 10(Android/12) WXApp-meiju(/8.11.0) Weex/0.28.0.61 1080x2206',
        'Accept-Encoding': 'gzip',
        'Host': 'mvip.midea.cn',
        'cookie': cookie

    }
    res = requests.post(url=url, headers=headers, timeout=30).json()
    print(res)
    send(content=res)

def main():
    qiandao()

if __name__ == '__main__':
    main()


