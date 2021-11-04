from flask import request,Response
from apps.ansibleChannelAuth.models import channel,ipwhilt
def Check(fun):
    def checkAuth(*args, **kwargs):
        import json
        if request.method != "GET":
            Data = request.get_json()
            uuid = Data.get("channelID", None)
            print("myid" + uuid)
            realIp=request.headers['X-Real-IP']
            print("ip" + realIp)
            UUID = channel.query.filter_by(uuid=uuid).all()
            Ipwhilt=ipwhilt.query.filter_by(ip=realIp).all()
            if UUID and Ipwhilt:
                return fun(*args, **kwargs)
            elif not UUID:
                data = {"code": 403, "message": "channelID No Find"}
            else:
                data = {"code": 403, "message": "ip {realIp} 没权限,请申请授权".format(realIp=realIp)}
        else:
            return fun(*args, **kwargs)
        return Response(json.dumps(data), mimetype='application/json')
    return checkAuth
