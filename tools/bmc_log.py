"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
def bmcLogInster(modelname,request,response):
    from apps.ansibleManage.models import db
    from apps.ansibleManage.models import bmclog
    import json
    import datetime
    Data = request.get_json()
    runTime=datetime.datetime.now()
    sourceIp = request.headers['X-Real-IP']
    opsmethod = request.method
    if  Data and runTime and modelname:
        bcmLogDataInsert = bmclog(descname=modelname,source=sourceIp,request=json.dumps(Data),response=json.dumps(response),opsmethod=opsmethod,run_time=runTime)
        db.session.add(bcmLogDataInsert)
        db.session.commit()
        return True
    else:
        return  False




