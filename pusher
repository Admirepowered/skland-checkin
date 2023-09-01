import time
import tools
from request import http


# telegram的推送
def telegram(send_title, push_message,cfg):
    http.post(
        url="https://{}/bot{}/sendMessage".format(cfg["api_url"], cfg["token"]),
        data={
            "chat_id": cfg.get('telegram', 'chat_id'),
            "text": send_title + "\r\n" + push_message
        }
    )


# server酱
def ftqq(send_title, push_message,cfg):
    http.post(
        url="https://sctapi.ftqq.com/{}.send".format(cfg["token"]),
        data={
            "title": send_title,
            "desp": push_message
        }
    )


# pushplus
def pushplus(send_title, push_message,cfg):
    http.post(
        url="https://www.pushplus.plus/send",
        data={
            "token": cfg["token"],
            "title": send_title,
            "content": push_message
        }
    )


# cq http协议的推送
def cqhttp(send_title, push_message,cfg):
    http.post(
        url=cfg["url"],
        json={
            "user_id": cfg["token"],
            "message": send_title + "\r\n" + push_message
        }
    )



def push(status, push_message):
    config = tools.load_config()
    #print(config["pusher"])
    func = globals().get(config["pusher"])
    if not func:
        print("未知推送")
        return 0
    try:
        func("Status:["+str(status)+"]",push_message,config)
    except Exception as r:
        print(f"error:{str(r)}")
        return 0
if __name__ == "__main__":
    push(0, f'推送验证{int(time.time())}')
