import json
import time

import requests

from config import global_config

AgentId = global_config.get('wx_push', 'agentid')
corpid = global_config.get('wx_push', 'corpid')
secret = global_config.get('wx_push', 'secret')
expires_time = global_config.get('wx_push', 'expires_time')


def gettoken():
    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    res = requests.get(url=url, headers=headers).json()
    print('res:', res)

    if res['errcode'] == 0:
        return res
    else:
        print('错误码:', res['errmsg'])
        return -1

"""
图文消息
"""
def send_news(title: str, content: str, tourl: str, imgurl: str):
    update_token()
    if not content:
        print(f"推送内容为空！")
        return
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    t = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))

    body = {
        "touser": "@all",
        "toparty": "",
        "totag": "",
        "msgtype": "news",
        "agentid": AgentId,
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": f"{t}\n{content}",
                    "url": tourl,
                    "picurl": imgurl,
                    "appid": "",
                    "pagepath": "",
                }
            ]
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    access_token = global_config.get('wx_push', 'access_token')
    url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
    res = requests.post(url=url, headers=headers, data=json.dumps(body)).json()
    print(res)
    if res['errcode'] == 0:
        print('推送成功')
    else:
        print('推送失败')
        print('错误码:', res['errmsg'])
    return res


def send_text(content: str):
    update_token()
    if not content:
        print(f"推送内容为空！")
        return
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        "touser": "@all",
        "toparty": "q",
        "totag": "q",
        "msgtype": "text",
        "agentid": AgentId,
        "text": {
            "content": content
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    access_token = global_config.get('wx_push', 'access_token')
    url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
    res = requests.post(url=url, headers=headers, data=json.dumps(body)).json()
    print(res)
    if res['errcode'] == 0:
        print('推送成功')
    else:
        print('推送失败')
        print('错误码:', res['errmsg'])
    return res


"""
卡片消息
"""


def send_textcard(title: str, content: str, tourl: str):
    update_token()
    t = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
    if not content:
        print(f"{title} 推送内容为空！")
        return
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        "touser": "@all",
        "toparty": "",
        "totag": "",
        "msgtype": "textcard",
        "agentid": AgentId,
        "textcard": {
            "title": title,
            "description": f"<div class=\"gray\">{t}</div><div class=\"highlight\">{content}</div>",
            "url": tourl,
            "btntxt": "更多"
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    access_token = global_config.get('wx_push', 'access_token')
    url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
    res = requests.post(url=url, headers=headers, data=json.dumps(body)).json()
    print(res)
    return res


def update_token():
    if int(time.time()) < int(expires_time) - 5:
        pass
    else:
        print("update_token")
        time.sleep(5)
        res = gettoken()
        if res != -1:
            token = res['access_token']
            # global access_token
            # access_token = token
            expires_in = res['expires_in']
            global_config.set('wx_push', 'access_token', token)
            expires = int(time.time() + expires_in)
            global_config.set('wx_push', 'expires_time', str(expires))


def send(**kwargs):
    if len(kwargs) < 1:
        return -1
    update_token()
    if len(kwargs) == 1:
        print("推送文本消息")
        res = send_text(kwargs['content'])
    if len(kwargs) == 2:
        print("推送文本卡片消息")
        res = send_textcard(kwargs['title'], kwargs['content'])
    if len(kwargs) == 3:
        print("推送文本卡片消息")
        res = send_textcard(kwargs['title'], kwargs['content'], kwargs['tourl'])
    if len(kwargs) == 4:
        print("推送图文消息")
        res = send_news(kwargs['title'], kwargs['content'], kwargs['tourl'], kwargs['imgurl'])
    # if res['errcode'] == 0:
    #     print('推送成功')
    # else:
    #     print('推送失败')
    #     print('错误码:', res['errmsg'])


if __name__ == '__main__':
    # token = gettoken(corpid, Secret)
    # 先发送消息 如果token过期再更新token
    # gettoken()
    tourl = '<a href="myapp://jp.app/openwith?name=zhangsan&age=26">启动应用程序</a> '

    content = '啦啦啦\n <a href="alipays://platformapi/startapp?appId=60000002">唤醒浙江移动手机营业厅！</a>'

    send(content=content)
