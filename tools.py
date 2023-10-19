import os
import yaml
import request
import json
import hashlib
import time
import hmac
from urllib import parse


def load_config():
    path = os.path.dirname(os.path.realpath(__file__)) + "/config.yaml"
    #print(path)
    with open(path, "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
def save_config(config):
    path = os.path.dirname(os.path.realpath(__file__)) + "/config.yaml"
    with open(path, "w+") as f:
        try:
            f.seek(0)
            f.truncate()
            f.write(yaml.dump(config, Dumper=yaml.Dumper, sort_keys=False))
            f.flush()
        except OSError:
            serverless = True
            print("Config保存失败")
            exit(-1)
        else:
            print("Config保存完毕")
def get_useragent():
    return "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 30; ) Okhttp/4.11.0"
def get_cred_by_token(token):
    session=request.get_new_session()
    session.headers["user-agent"] = get_useragent()
    session.headers["Content-Type"]="application/json"
    data= session.post("https://as.hypergryph.com/user/oauth2/v2/grant",json={
    "token":token,
    "appCode":"4ca99fa6b56cc2ba",
    "type":0
    })

    ret = data.text
    print(ret)
    js=json.loads(ret)
    if js["status"]!=0:
        print("Login Failed"+js["msg"])
        return ""
    code=js["data"]["code"]
    #uid=js["data"]["uid"]
    data= session.post("https://zonai.skland.com/api/v1/user/auth/generate_cred_by_code",json={
    "kind":1,
    "code":code
    })
    ret = data.text
    print(ret)
    js=json.loads(ret)
    if js["code"]!=0:
        print(js["message"])
        return ""
    cred=js["data"]["cred"]
    session.headers["cred"] = cred
    t_token=js["data"]["token"]
    #data= session.get("https://zonai.skland.com/api/v1/game/player/binding")
    #ret = data.text
    #print(session.headers)
    #print(ret)

    #js=json.loads(ret)
    #uid=js["data"]["list"][0]["defaultUid"]
    return cred,t_token
    #,uid

def get_sign_header(url: str,query,sign_token,platform='',did='',vName=''):
    p = parse.urlparse(url)

    header_for_sign = {
    'platform': platform,
    'timestamp': '',
    'dId': did,
    'vName': vName
    }
    sign,header_ca = generate_signature(sign_token, p.path, query,header_for_sign)
    ts=header_ca['timestamp']
    #print(header_ca)
    return sign,ts
    #h = json.loads(json.dumps(old_header))
    #p = parse.urlparse(url)
    #if method.lower() == 'get':
    #    h['sign'], header_ca = generate_signature(sign_token, p.path, p.query)
    #else:
    #    h['sign'], header_ca = generate_signature(sign_token, p.path, json.dumps(body))
    #for i in header_ca:
    #    h[i] = header_ca[i]
    #return h

def generate_signature(token: str, path, body_or_query,header_for_sign):
    """//ref https://gitee.com/FancyCabbage/skyland-auto-sign/blob/master/skyland.py
    获得签名头
    接口地址+方法为Get请求？用query否则用body+时间戳+ 请求头的四个重要参数（dId，platform，timestamp，vName）.toJSON()
    将此字符串做HMAC加密，算法为SHA-256，密钥token为请求cred接口会返回的一个token值
    再将加密后的字符串做MD5即得到sign
    :param token: 拿cred时候的token
    :param path: 请求路径（不包括网址）
    :param body_or_query: 如果是GET，则是它的query。POST则为它的body
    :return: 计算完毕的sign
    """
    # 总是说请勿修改设备时间，怕不是yj你的服务器有问题吧，所以这里特地-2
    t = str(int(time.time()) - 2)
    token = token.encode('utf-8')
    header_ca = json.loads(json.dumps(header_for_sign))
    header_ca['timestamp'] = t
    header_ca_str = json.dumps(header_ca, separators=(',', ':'))
    s = path + body_or_query + t + header_ca_str
    hex_s = hmac.new(token, s.encode('utf-8'), hashlib.sha256).hexdigest()
    md5 = hashlib.md5(hex_s.encode('utf-8')).hexdigest().encode('utf-8').decode('utf-8')
    #print(f'算出签名: {md5}')
    return md5, header_ca
