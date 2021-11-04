from flask import Blueprint
from flask import request, Response
from libs.decorators import require_permission

serviceUrl = Blueprint('service', __name__)


@require_permission("apps_service_view")
@serviceUrl.route('/api/v1', methods=['GET'])
def serviceRun():
    if request.method == "GET":
        return qeuryServiceHistrory()


def qeuryServiceHistrory():
    """
    1.查询有目前有哪些应用
        :return:
    """
    import json
    from apps.serviceManage.models import serviceLog
    from config import serviceMgHeader
    queryData = serviceLog.query.all()
    pagesize = request.args.get('page_size', 5, type=int)
    page = request.args.get('page', 1, type=int)
    source = request.args.get('source', None)
    username = request.args.get('username', None)
    channelID = request.args.get('channelID', None)
    if source and username and channelID:
        return queryAServiceLike(source, username, channelID)
    else:
        if page and pagesize:
            pagination = serviceLog.query.order_by(serviceLog.run_time.desc()).paginate(page, per_page=pagesize,
                                                                                        error_out=False)
            appData = pagination.items
        else:
            parameterInfo = "参数不足或错误,请检查"
            return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
        return Response(
            json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in appData], "columns": serviceMgHeader}),
            mimetype='application/json')


@require_permission("apps_service_add")
@serviceUrl.route('/api/v1', methods=['POST'])
def appsServiceAdd():
    import requests, json
    from config import ansibleApiUrl, channelID
    from service_log import serviceLogInster
    ops_oper = ["start", "stop", "restart", "status"]
    serviceEnvlistOld = ["test", "test2"]
    Data = request.get_json()
    service_ip = Data.get('app_ip', None)
    env = Data.get('env', None)
    service_name = Data.get('app_name', None)
    service_operation = Data.get('app_operation', None)
    if env in serviceEnvlistOld:
        if service_operation in ops_oper:
            serviceData = {
                "instance_ip": service_ip,
                "channelID": channelID,
                "command": "shell",
                "args": """/bin/bash /xwkj/app/service/{}/run/console {}""".format(service_name, service_operation),
                "user": "ops"
            }
            serviceResult = requests.post(ansibleApiUrl, data=json.dumps(serviceData),
                                          headers={"Content-Type": "application/json"})
            serviceLogInster("serviceRun", request, serviceResult.json())
            return Response(json.dumps({"code": 0, "data": serviceResult.json()}), mimetype='application/json')
        else:
            return Response(json.dumps({"code": 1, "data": ops_oper}), mimetype='application/json')
    else:
        if service_operation in ops_oper:
            serviceData = {
                "instance_ip": service_ip,
                "channelID": channelID,
                "command": "shell",
                "args": """/bin/bash /xwkj/app/{}/console {}""".format(service_name, service_operation),
                "user": "ops"
            }
            serviceResult = requests.post(ansibleApiUrl, data=json.dumps(serviceData),
                                          headers={"Content-Type": "application/json"})
            serviceLogInster("serviceRun", request, serviceResult.json())
            return Response(json.dumps({"code": 0, "data": serviceResult.json()}), mimetype='application/json')
        else:
            return Response(json.dumps({"code": 1, "data": ops_oper}), mimetype='application/json')


def queryAServiceLike(source, username, channelID):
    """
    1.按照单个条件进行模糊查询 统一返回数据格式
    :param source:
    :param username:
    :param channelID
    :return:
    """
    from apps.serviceManage.models import serviceLog
    import json
    try:
        if source:
            Data = serviceLog.query.filter(
                serviceLog.appname.like("%" + source + "%") if source is not None else ""
            ).all()

        if username:
            Data = serviceLog.query.filter(
                serviceLog.username.like("%" + username + "%") if username is not None else ""
            ).all()

        if channelID:
            Data = channelID.query.filter(
                serviceLog.channelID.like("%" + channelID + "%") if channelID is not None else ""
            ).all()
        return dataResult(Data)

    except Exception as e:
        print(e)
        parameterInfo = "查询数据库出现问题,请进行检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


def dataResult(Data):
    from config import serviceMgHeader
    import json
    """
    1.统一返回字段
    :param Data:
    :return:
    """
    data_list = list()
    if Data:
        for i in Data:
            dict_one = i.to_dict()
            data_list.append(dict_one)
        msg = "success"
    else:
        msg = "未查询到数据"
    return Response(json.dumps({"code": 0, "total": len(data_list), "data": data_list, "msg": msg, "columns": serviceMgHeader}),
                    mimetype='application/json')
