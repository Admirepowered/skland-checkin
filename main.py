import tools
import request
import json
import pusher

def main():
    config=tools.load_config()
    num =int(config["account_num"])
    data=""
    if num>0:
        for i in range(0,num):
            if config["account"+'{}'.format(i+1)].get('cred') is None or config["account"+'{}'.format(i+1)]["cred"]=="" or config["account"+'{}'.format(i+1)].get('t_token') is None:
                try:
                    if config["account"+'{}'.format(i+1)].get('token') is None:
                        break
                    get_cred_and_token(config,i)
                except:
                    print("error")
            tools.save_config(config)
            status,msg= singin(config["account"+'{}'.format(i+1)]["uid"],config["account"+'{}'.format(i+1)]["cred"],config["account"+'{}'.format(i+1)]["t_token"])
            if status!=0:
                get_cred_and_token(config,i)
                tools.save_config(config)
                data+=" Status:" +'{}\n'.format(status)+" mssage:"+msg+"\n"#ReTry
                status,msg= singin(config["account"+'{}'.format(i+1)]["uid"],config["account"+'{}'.format(i+1)]["cred"],config["account"+'{}'.format(i+1)]["t_token"])
            data+=" Status:" +'{}\n'.format(status)+" mssage:"+msg+"\n"
        
        print(data)
        if config["pusher"]!="":
            pusher.push(0,data)
def get_cred_and_token(config,i):
    cred,t_token=tools.get_cred_by_token(config["account"+'{}'.format(i+1)]["token"])
    config["account"+'{}'.format(i+1)]["cred"]=cred
    config["account"+'{}'.format(i+1)]["t_token"]=t_token

def do_get(session,url,token):
    sign,ts=tools.get_sign_header(url,"",token)
    session.headers["sign"]=sign
    session.headers["timestamp"]=ts
    return session.get(url)
def do_post(session,url,token,postdata):
    sign,ts=tools.get_sign_header(url,json.dumps(postdata),token)
    session.headers["sign"]=sign
    session.headers["timestamp"]=ts
    return session.post(url,json=postdata)

def singin(uid,cred,token):
    session=request.get_new_session()
    tools.set_header(session)

    session.headers["cred"]=cred
    data=do_get(session,"https://zonai.skland.com/api/v1/game/player/binding",token)

    ret = data.text
    js=json.loads(ret)
    if js["code"]!=0:
        return js["code"],js["message"]
    list=js["data"]["list"][0]['bindingList']
    print(list)
    code=0
    msg=''

    for i in range(0,len(list)):
        uid=list[i]["uid"]
        data=do_post(session,"https://zonai.skland.com/api/v1/game/attendance",token,postdata={
        "uid":uid,
        "gameId":list[i]['channelMasterId']
        })
        ret = data.text
        js=json.loads(ret)
        message=js["message"]
        if js["code"]!=10001 and js["code"]!=0:
            code=js["code"]
            
        msg+=f'uid: {uid} 状态:{message}\n'

    #uid=js["data"]["list"][0]["defaultUid"]
    return code,msg

if __name__=="__main__":
    main()
