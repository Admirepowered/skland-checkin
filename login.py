import request
import tools
import sys
import tools
import json
def login(phone,password):
    
    session=request.get_new_session()
    session.headers["user-agent"] = tools.get_useragent()
    session.headers["Content-Type"]="application/json"
    data= session.post("https://as.hypergryph.com/user/auth/v1/token_by_phone_password",json={
    "phone":phone,
    "password":password
    })
   
    ret = data.text
    js=json.loads(ret)
    if js["status"]!=0:
        print(js["msg"])
        return 
    token=js["data"]["token"]
    
    config=tools.load_config()
    num =int(config["account_num"])+1
    config["account_num"]=num
    config["account"+'{}'.format(num)]["token"]=token
    tools.save_config(config)
    
    #print(ret)
def login_bysms(phone):
    session=request.get_new_session()
    session.headers["user-agent"] = tools.get_useragent()
    session.headers["Content-Type"]="application/json"
    data= session.post("https://as.hypergryph.com/general/v1/send_phone_code",json={
    "phone":phone,
    "type":2
    })
    ret = data.text
    js=json.loads(ret)
    if js.get("status") != 0:
        raise Exception(f"发送手机验证码出现错误：{js['msg']}")
    code = input("请输入手机验证码：")
    data = session.post('https://as.hypergryph.com/user/auth/v2/token_by_phone_code', json={"phone": phone, "code": code})
    ret = data.text
    js=json.loads(ret)
    if js["status"]!=0:
        print(js["msg"])
        return 
    token=js["data"]["token"]
    
    config=tools.load_config()
    num =int(config["account_num"])+1
    config["account_num"]=num
    config["account"+'{}'.format(num)]["token"]=token
    tools.save_config(config)

if __name__=="__main__":
    #print(len(sys.argv))
    if (len(sys.argv)==2):
        login_bysms(sys.argv[1])
        exit(0)
    if (len(sys.argv)<3):
        print("useage: python login.py yourphone yourpassword or python login.py yourphone")
        exit(0)
    phone =sys.argv[1]
    password=sys.argv[2]
    #if password=="code":
    #    print("还没写")
    #    exit(0)
    login(phone,password)

    #js=json.loads(ret)
    #return js["code"],js["message"]
    #https://as.hypergryph.com/user/auth/v1/token_by_phone_password
