import os
import yaml
import request
import json
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
    session.headers["USER_AGENT"] = get_useragent()
    session.headers["Content-Type"]="application/json"
    data= session.post("https://as.hypergryph.com/user/oauth2/v2/grant",json={
    "token":token,
    "appCode":"4ca99fa6b56cc2ba",
    "type":0
    })

    ret = data.text
    js=json.loads(ret)
    if js["status"]!=0:
        print("Login Failed"+js["msg"])
        return "",""
    print(ret)
    code=js["data"]["code"]
    #uid=js["data"]["uid"]
    data= session.post("https://zonai.skland.com/api/v1/user/auth/generate_cred_by_code",json={
    "kind":1,
    "code":code
    })
    ret = data.text
    js=json.loads(ret)
    if js["code"]!=0:
        print(js["message"])
        return "",""
    cred=js["data"]["cred"]
    session.headers["cred"] = cred
    data= session.get("https://zonai.skland.com/api/v1/game/player/binding")
    ret = data.text
    js=json.loads(ret)
    uid=js["data"]["list"][0]["defaultUid"]
    return cred,uid
    
