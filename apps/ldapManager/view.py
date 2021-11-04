from flask import Blueprint
from flask import request, Response, current_app

from apps.ldapManager.ldapApi import MyLdap
from config import ldapHeader
import json
ldapUrl = Blueprint('ldap', __name__)
from libs.decorators import require_permission

@require_permission("system_ldap_view")
@ldapUrl.route('/api/v1', methods=['GET'])
def ldapRun():
    """
    1.路由入口方法
    """
    import json
    if request.method == "GET":
        from apps.ldapManager.models import ldapmg
        queryData = ldapmg.query.all()
        pagesize = request.args.get('page_size', 5, type=int)
        page = request.args.get('page', 1, type=int)
        username = request.args.get("username", None)
        name = request.args.get('name', None)
        mail = request.args.get('mail', None)
        if username or name or mail:
            return queryLdapLike(username,name,mail)
        else:
            if page and pagesize:
               pagination = ldapmg.query.order_by(ldapmg.createtime.desc()).paginate(page, per_page=pagesize,error_out=False)
               ldapData = pagination.items
            else:
                parameterInfo = "参数不足或错误,请检查"
                return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
            return Response(json.dumps(
                {"code": 0, "total": len(queryData), "message":"", "data": [i.to_dict() for i in ldapData], "columns": ldapHeader}),
                mimetype='application/json')

def ldapQuery(username):
    """
    1.查询有目前有哪些应用
        :return:
    """
    import json
    if username or username == "*":
        m = MyLdap()
        return Response(json.dumps({"code": 0, "data": m.ldap_search(username),"columns":ldapHeader}), mimetype='application/json')
    else:
        parameterInfo = "参数不足或错误,查询所有请输入all"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')

@require_permission("system_ldap_add")
@ldapUrl.route('/api/v1', methods=['POST'])
def systemLdapView():
    from apps.ldapManager.models import ldapmg
    Data = request.get_json()
    username = Data.get('username', None)
    name = Data.get('name', None)
    mail = Data.get('mail', None)
    if username and name and mail:
        queryLdapname = ldapmg.query.filter(ldapmg.username == username).all()
        if queryLdapname:
            msg = "Ldap {app} existing".format(app=username)
            return Response(json.dumps({"code": 1, "message":"","data": msg}), mimetype='application/json')
        else:
            return ldapCrete(username, name, mail)
    else:
        parameterInfo = "参数不足或错误,查询所有请输入all"
        return Response(json.dumps({"code": 1, "message":"","data": parameterInfo}), mimetype='application/json')

def ldapCrete(loginname, username, mail):
    """
    1.ldap创建和查询用户和用户名称和邮箱
    """
    try:
        if loginname and username:
            m = MyLdap()
            addUser = m.ldap_add(loginname, username, mail)
            if addUser:
                return ldapAddData(addUser.get("loginname"), addUser.get("passwd"), username, addUser.get("mail"))
            else:
                parameterInfo = "ldap服务出现问题.请检查"
                return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
        else:
            parameterInfo = "参数不足或错误,请进行检查"
            return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"code": 1, "data": str(e)}), mimetype='application/json')


@require_permission("system_ldap_del")
@ldapUrl.route('/api/v1', methods=['DELETE'])
def systemLdapDel():
    from apps.ldapManager.models import ldapmg
    Data = request.get_json()
    print(Data)
    username = Data.get('username')
    try:
        queryLdapname = ldapmg.query.filter(ldapmg.username == username).all()
        if queryLdapname:
            dataList = queryLdapname[0]
            return delLdap(username, dataList.id)
        else:
            parameterInfo = "用户不存在,无需进行删除"
            return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
    except Exception as e:
        print(e)


def delLdap(username, id):
    """
    1.删除ldap功能和数据库信息id
    """
    try:
        if username:
            m = MyLdap()
            retData = m.ldap_del(username)
            if retData.get("code") == 0:
                return deletSQLLdap(id)
            else:
                return Response(json.dumps({"code": 1, "message:":"","data": "删除数据Ldap账号失败"}), mimetype='application/json')
        else:
            parameterInfo = "参数不足或错误,请进行检查"
            return Response(json.dumps({"code": 1,"message":"", "data": parameterInfo}), mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"code": 1, "message":"","data": str(e)}), mimetype='application/json')


def ldapAddData(username, password, name, mail):
    """
      1.ldap信息录入
      :param username:
      :param name:
      :param mail:
      :return:
      1.数据插入数据库
      2.统一返回查询信息通知
      """
    from apps.ldapManager.models import db
    from apps.ldapManager.models import ldapmg
    try:
        lodapDataInsert = ldapmg(username=username, password=password, name=name, mail=mail)
        db.session.add(lodapDataInsert)
        db.session.commit()
        return Response(json.dumps({"code": 1, "data": "创建用户完毕,数据写入成功"}), mimetype='application/json')
    except Exception as e:
        print(e)
        current_app.logger.warning("ldap  add user failure  Exception" + str(e))
        return Response(json.dumps({"code": 1, "data": str(e)}), mimetype='application/json')


def deletSQLLdap(id):
    """
    1.删除数据中存在的Id数据
    2.删除过程记录日志信息
    3.统一返回删除提示信息给用户
    """
    from apps.ldapManager.models import db
    from apps.ldapManager.models import ldapmg
    import json
    try:
        deleteData = ldapmg.query.get(id)
        if deleteData:
            db.session.delete(deleteData)
            db.session.commit()
            data = {"code": 0, "date": True, "message": "","status":"delete success"}
            current_app.logger.warning("delele ldap data suceess")
        else:
            current_app.logger.warning("match ldap  data failure")
            data = {"code": 0, "date": False, "message": "","status":"match data failure"}

        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        current_app.logger.warning("args Parameters of the abnormal")
        data = {"code": 500, "data": "delete ldap faild", "message":"","status":str(e)}
        return Response(json.dumps(data), mimetype='application/json')

def queryLdapLike(username,name,mail):
    """"
    1.ldap 模糊查询
    """
    from apps.ldapManager.models import ldapmg
    import json
    try:
        if username:
            Data = ldapmg.query.filter(
                ldapmg.username.like("%" + username + "%") if username is not None else ""
            ).all()

        if name:
            Data = ldapmg.query.filter(
                ldapmg.name.like("%" + name + "%") if name is not None else ""
            ).all()

        if mail:
            Data = ldapmg.query.filter(
                ldapmg.mail.like("%" + mail + "%") if mail is not None else ""
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
    return Response(json.dumps({"code": 0, "total": len(data_list),"data":data_list,"msg":msg,"columns":ldapHeader}),mimetype='application/json')

@require_permission("system_ldap_scrapes")
@ldapUrl.route('/scrapes/v1', methods=['GET'])
def scrapesLdapRun():
    if request.method == "GET":
        return scrapesLdap()
    else:
        parameterInfo = "方法不支持"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')

def scrapesLdap():
    from apps.ldapManager.models import ldapmg
    import json
    username="*"
    if username == "*":
       m = MyLdap()
       m.ldap_search(username)
       data=m.ldap_search(username)
       print(data)
       try:
           for ldapData in data:
               myname=ldapData["username"]
               queryLdapname = ldapmg.query.filter(ldapmg.username == myname).all()
               if queryLdapname:
                  continue
               else:
                   ldapAddData(ldapData["username"],ldapData["password"] ,ldapData["name"],ldapData["mail"])
           return  Response(json.dumps({"code": 1, "data": "数据抓取成功"}), mimetype='application/json')
       except Exception as e:
           print(e)
           return  Response(json.dumps({"code": 1, "data": str(e)}), mimetype='application/json')
