from flask import Blueprint
from flask import request, Response, current_app
from flask_paginate import Pagination, get_page_parameter
from apps.JenkinsManager.jenkinsApi.jenkinsApi import JeninsDeploy
from libs.decorators import require_permission
from apps.appManager.models import Appmg
from apps.appManager.models import db
import json

appMgUrl = Blueprint('app', __name__)
from config import appMgHeader


@require_permission('apps_appname_view')
@appMgUrl.route('/api/v1', methods=['GET'])
def appmgRun():
    """
    1.查询app项目默认一页5条数据
    2.创建app项目,判断是否存在该应用存在直接返回,不存在进行创建，
    3.修改app项目信息,
    4.删除app项目
    :return:
    """
    return qeuryApp()


def qeuryApp():
    """
    1.查询有目前有哪些应用
        :return:
    """
    import json
    queryData = Appmg.query.all()
    pagesize = request.args.get('page_size', 5, type=int)
    page = request.args.get('page', 1, type=int)
    appname = request.args.get('appname', None)
    group = request.args.get('group', None)
    level = request.args.get('level', None)
    port = request.args.get('port', None)
    owner = request.args.get('owner', None)
    giturl = request.args.get('giturl', None)
    apptype = request.args.get("apptype", None)
    if appname or apptype or giturl or port or owner or level or group:
        return queryAppLike(appname, apptype, giturl, port, owner, level, group)
    else:
        if page and pagesize:
            pagination = Appmg.query.order_by(Appmg.createtime.desc()).paginate(page, per_page=pagesize,
                                                                                error_out=False)
            appData = pagination.items
        else:
            parameterInfo = "参数不足或错误,请检查"
            return Response(json.dumps({"code": 1, "message":"","data": parameterInfo}), mimetype='application/json')
        return Response(json.dumps(
            {"code": 0, "total": len(queryData), "message":"","data": [i.to_dict() for i in appData], "columns": appMgHeader}),
            mimetype='application/json')


@require_permission('apps_appname_edit')
@appMgUrl.route('/api/v1', methods=['PUT'])
def appsAppnameEdit():
    Data = request.get_json()
    id = Data.get("id")
    appname = Data.get('appname', None).strip()
    group = Data.get('group', None).strip()
    level = Data.get('level', None)
    business = Data.get('business', None)
    port = Data.get('port', None)
    giturl = Data.get('giturl', None).strip()
    apptype = Data.get("apptype", None).strip()
    owner = Data.get("owner", None).strip()
    used = Data.get("used", None)
    if appname and giturl and apptype and level and business and port and used and id:
        reults = editAppdata(business, group, appname, apptype, giturl, port, level, owner, used, id)
        return Response(json.dumps(reults), mimetype='application/json')


def editAppdata(business, group, appname, apptype, giturl, port, level, owner, used, id):
    """
    1.id 更新应用信息,修改数据
    """
    try:
        Appmg.query.filter_by(id=id).update(
            {"business": business, "group": group, "appname": appname, "apptype": apptype, "giturl": giturl, "port": port,
             "level": level, "owner": owner, "used": used})
        msg = "Update Success"
        db.session.commit()
        return {"code": 0, "data": True, "message":"", "status":"msg", "appname": appname}

    except Exception as e:
        print(e)
        current_app.logger.warning("update appname info failure" + str(e))
        return {"code": 1, "data": None, "message":"","status":str(e)}


@require_permission('apps_appname_add')
@appMgUrl.route('/api/v1', methods=['POST'])
def appsAppnameAdd():
    Data = request.get_json()
    appname = Data.get('appname', None)
    group = Data.get('group', None)
    level = Data.get('level', None)
    business = Data.get('business', None)
    port = Data.get('port', None)
    giturl = Data.get('giturl', None)
    apptype = Data.get("apptype", None)
    owner = Data.get("owner", None)
    used = Data.get("used", None)
    if appname and group and giturl and apptype and level and business and port and owner and used:
        queryAppname = Appmg.query.filter(Appmg.appname == appname).all()
        if queryAppname:
            msg = "appname {app} existing".format(app=appname)
            return Response(json.dumps({"code": 1, "data": msg}), mimetype='application/json')
        else:
            job = JeninsDeploy()
            jenkins_callback = job.jenkinsCreateJob(appname)
            print(jenkins_callback)
            reults = appDataAdd(business, group, appname, apptype, giturl, port, level, owner, used)
            data = {"code": 0, "data": reults, "message": "","status":"data insert success", "appname": appname}
            return Response(json.dumps(data), mimetype='application/json')
    else:
        parameterInfo = "无效参数,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


def appDataAdd(business, group, appname, apptype, giturl, port, level, owner, used):
    """
      1.app应用信息录入
      :param env:
      :param upname:
      :param giturl:
      :param apptype:
      :param used:
      :return:
      """
    try:
        appDataInsert = Appmg(business=business, group=group, appname=appname, apptype=apptype, giturl=giturl, port=port,
                              level=level, owner=owner, used=used)
        db.session.add(appDataInsert)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        current_app.logger.warning("app data add failure  Exception" + str(e))
        return False


@require_permission('apps_appname_del')
@appMgUrl.route('/api/v1', methods=['DELETE'])
def deletapp():
    import json
    try:
        Data = request.get_json()
        Id = Data.get('id', None)
        deleteData = Appmg.query.get(Id)
        if deleteData:
            db.session.delete(deleteData)
            db.session.commit()
            data = {"code": 0, "date": True, "message": " ","status":"delete success"}
            current_app.logger.warning("delele data suceess")
        else:
            current_app.logger.warning("match data failure")
            data = {"code": 0, "date": False, "message": "","status":"match data failure"}
        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        current_app.logger.warning("args Parameters of the abnormal")
        data = {"code": 500, "data": "delete appname faild", "message":"" ,"status":str(e)}
        data = {"code": 500, "data": "delete appname faild", "message":"", "status":str(e)}
        return Response(json.dumps(data), mimetype='application/json')


# 环境关系路由视图
class DeployParameter(object):
    def releaseList(self):
        import json
        from config import releaseListkey, releaseListDisplay_name
        Data = dict(zip(releaseListkey, releaseListDisplay_name))
        return json.dumps({"code": 0,"message":"", "data": [{"key": x, "display_name": Data[x]} for x in Data]})

    def appListEnv(self):
        from config import envListkey, envListdisplay_name
        import json
        Data = dict(zip(envListkey, envListdisplay_name))
        return json.dumps({"code": 0, "data": [{"key": x, "display_name": Data[x]} for x in Data]})

    def languageListEnv(self):
        from config import languageType, languageTypedisplay_name
        import json
        Data = dict(zip(languageType, languageTypedisplay_name))
        return json.dumps({"code": 0, "message":"","data": [{"key": x, "display_name": Data[x]} for x in Data]})


@appMgUrl.route('/envlist/v1', methods=['GET', 'POST', 'DELETE', 'PUT'])
def envListRun():
    import json
    if request.method == "GET":
        instanceListEev = DeployParameter()
        data = instanceListEev.appListEnv()
        return Response(data, mimetype='application/json')
    else:
        return json.dumps({"code": 0, "data": "不支持其他方法方法,get方法支持"})


@appMgUrl.route('/release/v1', methods=['GET', 'POST', 'DELETE', 'PUT'])
def releaseListRun():
    import json
    if request.method == "GET":
        instanceListEev = DeployParameter()
        data = instanceListEev.releaseList()
        return Response(data, mimetype='application/json')
    else:
        return json.dumps({"code": 0, "data": "不支持其他方法方法,get方法支持"})


@appMgUrl.route('/langlist/v1', methods=['GET', 'POST', 'DELETE', 'PUT'])
def languageListRun():
    import json
    if request.method == "GET":
        instanceListEev = DeployParameter()
        data = instanceListEev.languageListEnv()
        return Response(data, mimetype='application/json')
    else:
        return json.dumps({"code": 0, "message":"", "data": "不支持其他方法方法,get方法支持"})


"""
1.搜索发固定目录软件包版本
"""


@appMgUrl.route('/searchpack/v1', methods=['GET', 'POST', 'DELETE', 'PUT'])
def searchPackListRun():
    from config import searchPackPath
    import json
    if request.method == "POST":
        Data = request.get_json()
        servename = Data.get('appname', None)
        branch = Data.get('branch', None)
        print("vuepost获取版本请求")
        print(Data)
        if servename and branch:
            searchdata = searchServicesdir(searchPackPath, servename, branch)
            print(searchdata)
            return Response(searchdata, mimetype='application/json')
        else:
            return Response(json.dumps({"code": 0, "data": "未传递固定参数,无法使用"}), mimetype='application/json')
    else:
        return json.dumps({"code": 0, "data": "不支持其他方法方法,GET方法支持"})


def searchServicesdir(path, server, branch):
    import json, os
    server_dict = dict()
    try:
        path = "{}/{}/{}".format(path, server, branch)
        temp_dir = os.listdir(path)
        server_dict[server] = temp_dir
        Data = dict(zip(server, server_dict))
        return json.dumps(
            {"code": 0, "data": [{"key": server, "display_name": server_dict[x]} for x in server_dict], "status": "true"})
    except:
        server_dict[server] = "no data"
        return json.dumps(
            {"code": 1, "data": [{"key": server, "display_name": server_dict[x]} for x in server_dict], "status": "false"})



def queryAppLike(appname, apptype, giturl, port, owner, level, group):
    """
    1.按照单个条件进行模糊查询 统一返回数据格式
    :param appname:
    :param apptype:
    :param giturl:
    :param port:
    :param owner:
    :param level:
    :param group:
    :return:
    """
    import json
    try:
        if appname:
            Data = Appmg.query.filter(
                Appmg.appname.like("%" + appname + "%") if appname is not None else ""
            ).all()

        if apptype:
            Data = Appmg.query.filter(
                Appmg.apptype.like("%" + apptype + "%") if appname is not None else ""
            ).all()

        if giturl:
            Data = Appmg.query.filter(
                Appmg.giturl.like("%" + giturl + "%") if giturl is not None else ""
            ).all()

        if port:
            Data = Appmg.query.filter(
                Appmg.port.like("%" + port + "%") if port is not None else ""
            ).all()
        if owner:
            Data = Appmg.query.filter(
                Appmg.owner.like("%" + owner + "%") if owner is not None else ""
            ).all()

        if level:
            Data = Appmg.query.filter(
                Appmg.level.like("%" + level + "%") if level is not None else ""
            ).all()

        if group:
            Data = Appmg.query.filter(
                Appmg.group.like("%" + group + "%") if group is not None else ""
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
    return Response(json.dumps({"code": 0, "total": len(data_list), "data": data_list, "msg": msg, "columns": appMgHeader}),
                    mimetype='application/json')
