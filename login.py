import request
import tools
import sys
import tools
import json
def login(phone,password):
    
    session=request.get_new_session()
    session.headers["USER_AGENT"] = tools.get_useragent()
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


if __name__=="__main__":
    #print(len(sys.argv))
    if( len(sys.argv)<3):
        print("useage: python login.py yourphone yourpassword or python login.py yourphone code")
        exit(0)
    phone =sys.argv[1]
    password=sys.argv[2]
    if password=="code":
        print("还没写")
        exit(0)
    login(phone,password)

    #js=json.loads(ret)
    #return js["code"],js["message"]
    #https://as.hypergryph.com/user/auth/v1/token_by_phone_password
