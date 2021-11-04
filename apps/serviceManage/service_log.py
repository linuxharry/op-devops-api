def serviceLogInster(modelname,request,response):
    from models import db
    from models import serviceLog
    import json
    import datetime
    Data = request.get_json()
    runTime=datetime.datetime.now()
    from config import channelID
    sourceIp = request.headers['X-Real-IP']
    opsmethod = request.method
    if  Data and runTime and modelname:
        bcmLogDataInsert = serviceLog(descname=modelname,source=sourceIp,  channelID=channelID, username=getOwner(sourceIp),request=json.dumps(Data),response=json.dumps(response),opsmethod=opsmethod,run_time=runTime)
        db.session.add(bcmLogDataInsert)
        db.session.commit()
        return True
    else:
        return  False

def getOwner(IP):
    from config import getChannelIp
    import requests
    try:
        destData=getChannelIp + "ip=" + IP
        data=requests.get(destData,timeout=5)
        if data.json().get("msg") == "success":
            for result in data.json().get("data"):
                return result["owner"]
        else:
            msg = "{ipaddr},IP未进行授权白名单".format(ipaddr=IP)
            return msg
    except Exception as e:
        print(e)
