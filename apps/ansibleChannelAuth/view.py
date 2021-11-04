from flask import Blueprint
from flask import request, Response
from apps.ansibleChannelAuth.models import db
from apps.ansibleChannelAuth.models import channel,ipwhilt
channelUrl = Blueprint('channel', __name__)
from libs.decorators import require_permission

@require_permission('system_channel_uuid_view')
@channelUrl.route('/uuid/v1', methods=['GET'])
def channelMain():
    return anisbleSelectUuidChanne()


@require_permission('system_channel_uuid_add')
@channelUrl.route('/uuid/v1', methods=['POST'])
def channelRun(isUpdate=False):
    import json
    Data = request.get_json()
    channeldesc = Data.get('desc', None)
    channelOwner = Data.get('owner', None)
    channelUse = Data.get('uuid_use', None)
    print(Data)
    if channeldesc and channelOwner and channelUse:
        try:
            if isUpdate:
                id = Data.get("id")
                data = anisbleAddUuidChannel(channeldesc, channelOwner, channelUse,id)
            else:
                data = anisbleAddUuidChannel(channeldesc, channelOwner, channelUse)
        except Exception as e:
            print(e)
            data = {"code": 500, "data": "必传参数不能为空", "message": "","status":str(e)}
    else:
        data = {"code": 1, "data": "必传参数不能为空", "message": "","status":"failure"}
    return Response(json.dumps(data), mimetype='application/json')


@require_permission('system_channel_uuid_edit')
@channelUrl.route('/uuid/v1', methods=['PUT'])
def systemChannelUuidEdit():
    import json
    Data = request.get_json()
    channeldesc = Data.get('desc', None)
    channelOwner = Data.get('owner', None)
    channelUse = Data.get('uuid_use', None)
    print(Data)
    if channeldesc and channelOwner and channelUse:
        id = Data.get("id")
        data = anisbleEditUuidChannel(channeldesc, channelOwner, channelUse,id)
    return Response(json.dumps(data), mimetype='application/json')


@require_permission('system_channel_uuid_del')
@channelUrl.route('/uuid/v1', methods=['DELETE'])
def systemChannelUuidDel():
    import json
    Data = request.get_json()
    channelId = Data.get('id', None)
    data = anisbleDeleteUuidChanne(channelId)
    return Response(json.dumps(data), mimetype='application/json')


def anisbleAddUuidChannel(desc, owner, uuid_use, id=None):
    import uuid
    uuid = str(uuid.uuid1())
    try:
        if id:
           channel.query.filter_by(id=id).update({"desc": desc, "owner": owner, "uuid_use": uuid_use})
        else:
            channelDataInsert = channel(desc=desc, owner=owner, uuid=uuid, uuid_use=uuid_use)
            db.session.add(channelDataInsert)
        data = """你申请{},认证ID: {}""".format(uuid_use, uuid)
        db.session.commit()
        msg = "Update Success"
        return {"code": 0, "data": data, "message": "","status":msg}
    except Exception as e:
        print(e)
        return {"code": 1, "data": None, "message": "","status":str(e)}


def anisbleEditUuidChannel(desc, owner, uuid_use, id=None):
    import uuid
    uuid = str(uuid.uuid1())
    try:
        if id:
            channel.query.filter_by(id=id).update({"desc": desc, "owner": owner, "uuid_use": uuid_use})
        else:
            channelDataInsert = channel(desc=desc, owner=owner, uuid=uuid, uuid_use=uuid_use)
            db.session.add(channelDataInsert)
        data = """你申请{},认证ID: {}""".format(uuid_use, uuid)
        db.session.commit()
        msg = "Update Success"
        return {"code": 0, "data": data, "message":"" ,"status":msg}
    except Exception as e:
        print(e)
        return {"code": 1, "data": None, "message":"", "status":str(e)}


def anisbleSelectUuidChanne():
    import json
    from config import ChanneUuidHeader,WhilteUuidField
    if "opsAdminForm" in request.args:
        return Response(json.dumps({"code": 0, "data":WhilteUuidField}), mimetype="application/json")
    else:
        try:
            pagesize = request.args.get('page_size', 5, type=int)
            page = request.args.get('page', 1, type=int)
            queryData = channel.query.all()
            if page and pagesize:
               pagination = channel.query.order_by(channel.create_time.desc()).paginate(page, per_page=pagesize,
                                                                                          error_out=False)
               channelData = pagination.items
            else:
                parameterInfo = "参数不足或错误,请检查"
                return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')

            return Response(json.dumps(
                {"code": 0, "data": [i.to_dict() for i in channelData], "columns": ChanneUuidHeader, "message": "","total":len(queryData)}),
                mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({"code": 1, "data": str(e), "message": ""}), mimetype='application/json')




def anisbleDeleteUuidChanne(ID):
    try:
        deleteData = channel.query.get(ID)
        db.session.delete(deleteData)
        db.session.commit()
        data = "删除成功"
    except Exception as e:
        data = {"code": 500, "data": "删除uuid失败", "message": "","status":str(e)}


    return {"code": 0, "data": data, "message": "","status":"delete success"}


@require_permission('system_channel_ipwhilt_del')
@channelUrl.route('/ip/v1', methods=['DELETE'])
def channeIpDelete():
    import json
    Data = request.get_json()
    channelId = Data.get('id', None)
    data = anisbleDeleteChanneIp(channelId)
    return Response(json.dumps(data), mimetype='application/json')


@require_permission('system_channel_ipwhilt_add')
@channelUrl.route('/ip/v1', methods=["POST"])
def systemChannelIpwhiltEadd():
    return channelIpRun()

@require_permission('system_channel_ipwhilt_edit')
@channelUrl.route('/ip/v1', methods=["PUT"])
def systemChannelIpwhiltEdit():
    return channelIpRun(True)


def channelIpRun(isUpdate=False):
    import json
    Data = request.get_json()
    channelIp = Data.get('ip', None)
    channeIpDesc = Data.get('desc', None)
    channelIPowner = Data.get('owner', None)

    if channelIp and channeIpDesc and channelIPowner:
        try:
            if isUpdate:
                id = Data.get("id")
                data = anisbleAddIpChannel(channelIp, channeIpDesc, channelIPowner, id)
            else:
                data = anisbleAddIpChannel(channelIp, channeIpDesc, channelIPowner)
        except Exception as e:
            print(e)
            data = {"code": 500, "data": "必传参数不能为空", "message":"","status":str(e)}
    else:
        data = {"code": 1, "data": "必传参数不能为空", "message": "","status":"failure"}
    return Response(json.dumps(data), mimetype='application/json')


def anisbleAddIpChannel(ipadress, desc, owner, id=None):
    try:
        if id:
            ipwhilt.query.filter_by(id=id).update({"desc":desc, "owner": owner, "ip": ipadress})
            msg = "Update Success"
        else:
            channelIpDataInsert = ipwhilt(desc=desc, owner=owner, ip=ipadress)
            db.session.add(channelIpDataInsert)
            msg = "Insert Success"
        data = """申请人{},授权IP地址: {}""".format(owner, ipadress)
        db.session.commit()
        return {"code": 0, "data": data, "message": "","status":msg}
    except Exception as e:
        print(e)
        return {"code": 1, "data": None, "message": "","status":str(e)}

@require_permission('system_channel_ipwhilt_view')
@channelUrl.route('/ip/v1', methods=["GET"])
def ansibleSelectChannelIpRun():
    import json
    from config import ChanneIpHeader, WhilteIpField
    pagesize = request.args.get('page_size', 5, type=int)
    page = request.args.get('page', 1, type=int)
    if "opsAdminForm" in request.args:
        return Response(json.dumps({"code": 0, "data": WhilteIpField}), mimetype="application/json")
    else:
        try:
            queryData = ipwhilt.query.all()
            if page and pagesize:
               pagination = ipwhilt.query.order_by(ipwhilt.create_time.desc()).paginate(page, per_page=pagesize,
                                                                                          error_out=False)
               ipwhiltData = pagination.items
            else:
               parameterInfo = "参数不足或错误,请检查"
               return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
            return Response(json.dumps(
                {"code": 0,  "data": [i.to_dict() for i in ipwhiltData], "total":len(queryData), "columns": ChanneIpHeader, "message": ""}),
                mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({"code": 1, "data": str(e), "message": ""}), mimetype='application/json')






def anisbleDeleteChanneIp(IPID):
    try:
        deleteData = ipwhilt.query.get(IPID)
        db.session.delete(deleteData)
        db.session.commit()
        data = "删除成功"
    except Exception as e:
        data = {"code": 500, "data": "删除授权IP失败", "message": str(e)}
    return {"code": 0, "data": data, "message": "","status":"success"}
from flask import Blueprint
from flask import request, Response
from apps.ansibleChannelAuth.models import db
from apps.ansibleChannelAuth.models import channel,ipwhilt
channelUrl = Blueprint('channel', __name__)
from libs.decorators import require_permission

@require_permission('system_channel_uuid_view')
@channelUrl.route('/uuid/v1', methods=['GET'])
def channelMain():
    return anisbleSelectUuidChanne()


@require_permission('system_channel_uuid_add')
@channelUrl.route('/uuid/v1', methods=['POST'])
def channelRun(isUpdate=False):
    import json
    Data = request.get_json()
    channeldesc = Data.get('desc', None)
    channelOwner = Data.get('owner', None)
    channelUse = Data.get('uuid_use', None)
    print(Data)
    if channeldesc and channelOwner and channelUse:
        try:
            if isUpdate:
                id = Data.get("id")
                data = anisbleAddUuidChannel(channeldesc, channelOwner, channelUse,id)
            else:
                data = anisbleAddUuidChannel(channeldesc, channelOwner, channelUse)
        except Exception as e:
            print(e)
            data = {"code": 500, "data": "必传参数不能为空", "message": "","status":str(e)}
    else:
        data = {"code": 1, "data": "必传参数不能为空", "message": "","status":"failure"}
    return Response(json.dumps(data), mimetype='application/json')


@require_permission('system_channel_uuid_edit')
@channelUrl.route('/uuid/v1', methods=['PUT'])
def systemChannelUuidEdit():
    import json
    Data = request.get_json()
    channeldesc = Data.get('desc', None)
    channelOwner = Data.get('owner', None)
    channelUse = Data.get('uuid_use', None)
    print(Data)
    if channeldesc and channelOwner and channelUse:
        id = Data.get("id")
        data = anisbleEditUuidChannel(channeldesc, channelOwner, channelUse,id)
    return Response(json.dumps(data), mimetype='application/json')


@require_permission('system_channel_uuid_del')
@channelUrl.route('/uuid/v1', methods=['DELETE'])
def systemChannelUuidDel():
    import json
    Data = request.get_json()
    channelId = Data.get('id', None)
    data = anisbleDeleteUuidChanne(channelId)
    return Response(json.dumps(data), mimetype='application/json')


def anisbleAddUuidChannel(desc, owner, uuid_use, id=None):
    import uuid
    uuid = str(uuid.uuid1())
    try:
        if id:
           channel.query.filter_by(id=id).update({"desc": desc, "owner": owner, "uuid_use": uuid_use})
        else:
            channelDataInsert = channel(desc=desc, owner=owner, uuid=uuid, uuid_use=uuid_use)
            db.session.add(channelDataInsert)
        data = """你申请{},认证ID: {}""".format(uuid_use, uuid)
        db.session.commit()
        msg = "Update Success"
        return {"code": 0, "data": data, "message": "","status":msg}
    except Exception as e:
        print(e)
        return {"code": 1, "data": None, "message": "","status":str(e)}


def anisbleEditUuidChannel(desc, owner, uuid_use, id=None):
    import uuid
    uuid = str(uuid.uuid1())
    try:
        if id:
            channel.query.filter_by(id=id).update({"desc": desc, "owner": owner, "uuid_use": uuid_use})
        else:
            channelDataInsert = channel(desc=desc, owner=owner, uuid=uuid, uuid_use=uuid_use)
            db.session.add(channelDataInsert)
        data = """你申请{},认证ID: {}""".format(uuid_use, uuid)
        db.session.commit()
        msg = "Update Success"
        return {"code": 0, "data": data, "message":"" ,"status":msg}
    except Exception as e:
        print(e)
        return {"code": 1, "data": None, "message":"", "status":str(e)}


def anisbleSelectUuidChanne():
    import json
    from config import ChanneUuidHeader,WhilteUuidField
    if "opsAdminForm" in request.args:
        return Response(json.dumps({"code": 0, "data":WhilteUuidField}), mimetype="application/json")
    else:
        try:
            pagesize = request.args.get('page_size', 5, type=int)
            page = request.args.get('page', 1, type=int)
            queryData = channel.query.all()
            if page and pagesize:
               pagination = channel.query.order_by(channel.create_time.desc()).paginate(page, per_page=pagesize,
                                                                                          error_out=False)
               channelData = pagination.items
            else:
                parameterInfo = "参数不足或错误,请检查"
                return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')

            return Response(json.dumps(
                {"code": 0, "data": [i.to_dict() for i in channelData], "columns": ChanneUuidHeader, "message": "","total":len(queryData)}),
                mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({"code": 1, "data": str(e), "message": ""}), mimetype='application/json')




def anisbleDeleteUuidChanne(ID):
    try:
        deleteData = channel.query.get(ID)
        db.session.delete(deleteData)
        db.session.commit()
        data = "删除成功"
    except Exception as e:
        data = {"code": 500, "data": "删除uuid失败", "message": "","status":str(e)}


    return {"code": 0, "data": data, "message": "","status":"delete success"}


@require_permission('system_channel_ipwhilt_del')
@channelUrl.route('/ip/v1', methods=['DELETE'])
def channeIpDelete():
    import json
    Data = request.get_json()
    channelId = Data.get('id', None)
    data = anisbleDeleteChanneIp(channelId)
    return Response(json.dumps(data), mimetype='application/json')


@require_permission('system_channel_ipwhilt_add')
@channelUrl.route('/ip/v1', methods=["POST"])
def systemChannelIpwhiltEadd():
    return channelIpRun()

@require_permission('system_channel_ipwhilt_edit')
@channelUrl.route('/ip/v1', methods=["PUT"])
def systemChannelIpwhiltEdit():
    return channelIpRun(True)


def channelIpRun(isUpdate=False):
    import json
    Data = request.get_json()
    channelIp = Data.get('ip', None)
    channeIpDesc = Data.get('desc', None)
    channelIPowner = Data.get('owner', None)

    if channelIp and channeIpDesc and channelIPowner:
        try:
            if isUpdate:
                id = Data.get("id")
                data = anisbleAddIpChannel(channelIp, channeIpDesc, channelIPowner, id)
            else:
                data = anisbleAddIpChannel(channelIp, channeIpDesc, channelIPowner)
        except Exception as e:
            print(e)
            data = {"code": 500, "data": "必传参数不能为空", "message":"","status":str(e)}
    else:
        data = {"code": 1, "data": "必传参数不能为空", "message": "","status":"failure"}
    return Response(json.dumps(data), mimetype='application/json')


def anisbleAddIpChannel(ipadress, desc, owner, id=None):
    try:
        if id:
            ipwhilt.query.filter_by(id=id).update({"desc":desc, "owner": owner, "ip": ipadress})
            msg = "Update Success"
        else:
            channelIpDataInsert = ipwhilt(desc=desc, owner=owner, ip=ipadress)
            db.session.add(channelIpDataInsert)
            msg = "Insert Success"
        data = """申请人{},授权IP地址: {}""".format(owner, ipadress)
        db.session.commit()
        return {"code": 0, "data": data, "message": "","status":msg}
    except Exception as e:
        print(e)
        return {"code": 1, "data": None, "message":"", "status":str(e)}

@require_permission('system_channel_ipwhilt_view')
@channelUrl.route('/ip/v1', methods=["GET"])
def ansibleSelectChannelIpRun():
    import json
    from config import ChanneIpHeader, WhilteIpField
    pagesize = request.args.get('page_size', 5, type=int)
    page = request.args.get('page', 1, type=int)
    if "opsAdminForm" in request.args:
        return Response(json.dumps({"code": 0, "data": WhilteIpField}), mimetype="application/json")
    else:
        try:
            queryData = ipwhilt.query.all()
            if page and pagesize:
               pagination = ipwhilt.query.order_by(ipwhilt.create_time.desc()).paginate(page, per_page=pagesize,
                                                                                          error_out=False)
               ipwhiltData = pagination.items
            else:
               parameterInfo = "参数不足或错误,请检查"
               return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
            return Response(json.dumps(
                {"code": 0,  "data": [i.to_dict() for i in ipwhiltData], "total":len(queryData), "columns": ChanneIpHeader, "message": ""}),
                mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({"code": 1, "data": str(e), "message": ""}), mimetype='application/json')






def anisbleDeleteChanneIp(IPID):
    try:
        deleteData = ipwhilt.query.get(IPID)
        db.session.delete(deleteData)
        db.session.commit()
        data = "删除成功"
    except Exception as e:
        data = {"code": 500, "data": "删除授权IP失败", "message": str(e)}
    return {"code": 0, "data": data, "message": "","status":"success"}
