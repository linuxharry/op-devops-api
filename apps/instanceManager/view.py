from flask import Blueprint
from flask import request, Response, current_app
from flask_paginate import Pagination, get_page_parameter
from apps.instanceManager.models import Instancemg
from apps.instanceManager.models import db

instanceMgUrl = Blueprint('instance', __name__)
from config import instanceMgHeader
from libs.decorators import require_permission
import json


@require_permission('assets_instance_view')
@instanceMgUrl.route('/api/v1', methods=['GET'])
def appmgRun():
    """
    1.查询instance实例默认一页5条数据
    2.创建instance实例,判断是否存在该应用存在直接返回,不存在进行创建，
    3.修改instance实例信息,
    4.删除instance实例
    :return:
    """
    return qeuryApp()


def qeuryApp():
    """
    1.查询有目前有哪些应用
        :return:
    """
    import json
    queryData = Instancemg.query.all()
    pagesize = request.args.get('page_size', 5, type=int)
    page = request.args.get('page', 1, type=int)
    appname = request.args.get('appname', None)
    env = request.args.get('env', None)
    domain = request.args.get('domain', None)
    ip = request.args.get('ip', None)

    if appname or env or domain or ip:
        return queryInstanManyLike(appname, domain, env, ip)
    else:
        if page and pagesize:
            pagination = Instancemg.query.order_by(Instancemg.createtime.desc()).paginate(page, per_page=pagesize,
                                                                                          error_out=False)
            appData = pagination.items
        else:
            parameterInfo = "参数不足或错误,请检查"
            return Response(json.dumps({"code": 1,"message":"", "data": parameterInfo}), mimetype='application/json')
        return Response(
            json.dumps({"code": 0, "total": len(queryData), "message":"","data": [i.to_dict() for i in appData], "columns": instanceMgHeader}),
            mimetype='application/json')


@require_permission('assets_instance_add')
@instanceMgUrl.route('/api/v1', methods=['POST'])
def assetsInstanceAdd():
    from sqlalchemy import or_, and_
    Data = request.get_json()
    instname = Data.get('instancename', None)
    appname = Data.get('appname', None)
    domain = Data.get('domain', None)
    ip = Data.get('ip', None)
    env = Data.get('env', None)
    print(Data)
    if appname and instname and ip and env:
        queryInInfo = Instancemg.query.filter(and_(Instancemg.appname.like(appname)), (Instancemg.env.like(env))).all()
        print(queryInInfo)
        if queryInInfo:
            msg = "appname {app} existing".format(app=appname)
            return Response(json.dumps({"code": 1, "data": msg}), mimetype='application/json')
        else:
            reults = appDataAdd(instname, appname, domain, ip, env)
            data = {"code": 0, "data": reults, "message": "", "status":"insert success","appname": appname}
            return Response(json.dumps(data), mimetype='application/json')
    else:
        parameterInfo = "无效参数或者参数缺少,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


@instanceMgUrl.route('/query/api/v1', methods=['GET'])
def appmgInstanInfoRun():
    """
    1.查询instance实例默认一页5条数据
    2.创建instance实例,判断是否存在该应用存在直接返回,不存在进行创建，
    :return:
    """
    import json
    if request.method == "GET":
        return qeuryInstanceInfo()

    parameterInfo = "方法不支持,或者参数缺少,请检查"
    return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


def qeuryInstanceInfo():
    """
    1.查询有目前有哪些应用
        :return:
    """
    import json
    queryData = Instancemg.query.all()
    pagesize = request.args.get('page_size', 5, type=int)
    page = request.args.get('page', 1, type=int)
    appname = request.args.get('appname', None)
    env = request.args.get('env', None)
    if appname and env:
        return queryLike(appname, env)
    else:
        if page and pagesize:
            pagination = Instancemg.query.order_by(Instancemg.createtime.desc()).paginate(page, per_page=pagesize,
                                                                                          error_out=False)
            appData = pagination.items
        else:
            parameterInfo = "参数不足或错误,请检查"
            return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
        return Response(
            json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in appData], "columns": instanceMgHeader}),
            mimetype='application/json')


@require_permission('assets_instance_edit')
@instanceMgUrl.route('/api/v1', methods=['PUT'])
def assetsInstanceEdit():
    Data = request.get_json()
    id = Data.get("id")
    print(Data)
    instname = Data.get('instancename', None)
    appname = Data.get('appname', None)
    domain = Data.get('domain', None)
    ip = Data.get('ip', None)
    env = Data.get('env', None)
    try:
        if instname and appname and domain and ip and env and id:
            reults = editAppdata(instname, appname, domain, ip, env, id)
            return Response(json.dumps(reults), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"msg:": str(e)}), mimetype='application/json')


def editAppdata(instancename, appname, domain, ip, env, id):
    """
    1.id 更新应用信息,修改数据
    """
    try:
        Instancemg.query.filter_by(id=id).update(
            {"instancename": instancename, "appname": appname, "domain": domain, "ip": ip, "env": env})
        msg = ""
        db.session.commit()
        return {"code": 0, "data": True, "message": msg, "appname": appname}

    except Exception as e:
        print(e)
        current_app.logger.warning("update appname info failure" + str(e))
        return {"code": 1, "data": None, "message": str(e)}


def appDataAdd(instancename, appname, domain, ip, env):
    """
      1.实例应用信息录入
      :param instancename:
      :param appname:
      :param ip:
      :param env:
      :return:
      """
    try:
        InstanDataInsert = Instancemg(instancename=instancename, appname=appname, domain=domain, ip=ip, env=env)
        db.session.add(InstanDataInsert)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        current_app.logger.warning("app data add failure  Exception" + str(e))
        return False


@require_permission('assets_instance_del')
@instanceMgUrl.route('/api/v1', methods=['DELETE'])
def deletapp():
    import json
    try:
        Data = request.get_json()
        Id = Data.get('id', None)
        deleteData = Instancemg.query.get(Id)
        if deleteData:
            db.session.delete(deleteData)
            db.session.commit()
            data = {"code": 0, "date": True, "message": "","status":"delete Success"}
            current_app.logger.warning("delele data suceess")
        else:
            current_app.logger.warning("match data failure")
            data = {"code": 0, "date": False, "message": ""}
        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        current_app.logger.warning("args Parameters of the abnormal")
        data = {"code": 500, "data": "delete appname faild", "message": str(e)}
        return Response(json.dumps(data), mimetype='application/json')


def queryLike(appname, env):
    import json
    try:
        if appname and env:
            Data = Instancemg.query.filter_by(appname=appname, env=env).all()
            return dataResult(Data)
        else:
            return Response(json.dumps({"code": 1, "data": "输入条件有问题,请检查"}), mimetype='application/json')
    except Exception as e:
        print(e)
        parameterInfo = "查询数据库出现问题,请进行检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


def queryInstanManyLike(appname, domain, env, ip):
    """
    1.按照单个条件进行模糊查询 统一返回数据格式
    :param appname:
    :param domain:
    :param env:
    :param ip:
    :return:
    """
    import json
    try:
        if appname:
            Data = Instancemg.query.filter(
                Instancemg.appname.like("%" + appname + "%") if appname is not None else ""
            ).all()

        if domain:
            Data = Instancemg.domain.filter(
                Instancemg.domain.like("%" + domain + "%") if domain is not None else ""
            ).all()

        if env:
            Data = Instancemg.query.filter(
                Instancemg.env.like("%" + env + "%") if env is not None else ""
            ).all()

        if ip:
            Data = Instancemg.query.filter(
                Instancemg.ip.like("%" + ip + "%") if ip is not None else ""
            ).all()
        return dataResult(Data)

    except Exception as e:
        print(e)
        parameterInfo = "查询数据库出现问题,请进行检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


def dataResult(Data):
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
    return Response(json.dumps({"code": 0, "total": len(data_list), "data": data_list, "msg": msg, "columns": instanceMgHeader}),
                    mimetype='application/json')
