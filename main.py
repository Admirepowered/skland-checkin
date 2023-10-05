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
            #print(config["account"+'{}'.format(i+1)]["uid"],config["account"+'{}'.format(i+1)]["cred"])
            if config["account"+'{}'.format(i+1)].get('cred') is None or config["account"+'{}'.format(i+1)]["cred"]=="":
                try:
                    if config["account"+'{}'.format(i+1)].get('token') is None:
                        break
                    cred,uid=tools.get_cred_by_token(config["account"+'{}'.format(i+1)]["token"])
                
                    config["account"+'{}'.format(i+1)]["cred"]=cred
                    config["account"+'{}'.format(i+1)]["uid"]=uid
                except:
                    print("error")
            tools.save_config(config)
            status,msg= singin(config["account"+'{}'.format(i+1)]["uid"],config["account"+'{}'.format(i+1)]["cred"])
            if status!=0:
                cred,uid=tools.get_cred_by_token(config["account"+'{}'.format(i+1)]["token"])
            data+="uid:"+config["account"+'{}'.format(i+1)]["uid"]+" Status:" +'{}'.format(status)+" mssage:"+msg+"\n"
        
        print(data)
        if config["pusher"]!="":
            pusher.push(0,data)


    
def singin(uid,cred):
    session=request.get_new_session()
    session.headers["USER_AGENT"] = tools.get_useragent()
    session.headers["vCode"] = "100001014"
    session.headers["vName"] = '1.0.1'
    session.headers["dId"] = 'de9759a5afaa634f'
    session.headers["platform"] =  '1'
    session.headers["cred"]=cred
    session.headers["Content-Type"]="application/json"
    data= session.post("https://zonai.skland.com/api/v1/game/attendance",json={
    "uid":uid,
    "gameId":1
    })
   
    ret = data.text
    js=json.loads(ret)
    return js["code"],js["message"]
if __name__=="__main__":
    main()
