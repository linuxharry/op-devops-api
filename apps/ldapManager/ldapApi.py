import uuid
import random
import smtplib
import json
from email.mime.text import MIMEText
from ldap3 import Server, Connection,HASHED_SHA
from ldap3.utils.hashed import hashed
from ldap3 import ALL_ATTRIBUTES
class MyLdap(object):
    def __init__(self, ldap_host='ldap://op-ldap.mumway.com',
                 ldap_port='389',
                 ldap_name='cn=admin,dc=xiavan,dc=com',
                 ldap_passwd='Ldap#xiavan2021'):
        self.ldap_host = ldap_host
        self.ldap_port = ldap_port
        self.ldap_name = ldap_name
        self.ldap_passwd = ldap_passwd
        self.ldap_obj = None
        self.ldap_connect(ldap_host, ldap_port, ldap_name, ldap_passwd)

    def ldap_connect(self, ldap_host, ldap_port, ldap_name, ldap_passwd):
        ldap_url = "{}:{}".format(ldap_host, ldap_port)
        server = Server(ldap_url, get_info='ALL')
        conn = Connection(server, ldap_name, ldap_passwd)
        conn.bind()
        self.ldap_obj = conn
    def ldap_rendom_password(self):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(16):
            sa.append(random.choice(seed))
        password = ''.join(sa)
        return password
    def ldap_add(self, username, name, mail=None):
        if mail is None:
            mail = '{}@xiavan.com'.format(username)
        passwd = self.ldap_rendom_password()
        hashed_password = hashed(HASHED_SHA, passwd)
        hashed_password = hashed_password.replace('sha', 'SHA')  # 将sha 替换为 SHA
        dn = 'cn={},ou=user,dc=xiavan,dc=com'.format(username)
        uid = uuid.uuid1().int
        obj_class = ['top', 'shadowAccount', 'posixAccount', 'inetOrgPerson']
        data = {'cn': username,
                'uid': username,
                'uidNumber': uid,
                'gidNumber': 0,
                'givenName': name,
                'homeDirectory': '/home/{}'.format(username),
                'loginShell': username,
                'sn': username,
                'mail': mail,
                'shadowExpire': 99999,
                'shadowFlag': 0,
                'shadowInactive': 99999,
                'shadowLastChange': 12011,
                'shadowMax': 99999,
                'shadowMin': 0,
                'shadowWarning': 0,
                'userPassword': hashed_password}
        ret = self.ldap_obj.add(dn, obj_class, data)
        # self.ldap_mail(mail, username, passwd)
        # return username, passwd
        if ret:
            print(username, passwd)
            self.ldap_mail(mail, username, passwd)
            return {"code": 0, "loginname":username,"passwd":passwd,"mail":mail }
        return {"code": 1, "username":username,"passwd":"账号已存在","mail":mail }

    def ldap_search(self, user='*'):

        search_parameters = {'search_base': 'ou=user,dc=xiavan,dc=com',
                             'search_filter': '(cn={})'.format(user)}
        self.ldap_obj.search(**search_parameters, attributes=ALL_ATTRIBUTES)
        search_list = self.ldap_obj.response
        user_list = []
        for i in search_list:
            user_map = {}
            username_tmp = i['raw_dn'].decode()
            tmp_user = i['raw_attributes']
            user_map["username"] = username_tmp.split(",")[0].split('=')[1]
            user_map["password"] = tmp_user['userPassword'][0].decode()
            user_map["name"] = tmp_user['givenName'][0].decode()
            user_map["mail"] = tmp_user["mail"][0].decode()
            user_list.append(user_map)

        if not user_list:
            user_list = "用户不存在"
        return user_list


    def ldap_del(self, username):
        dn = "cn={},ou=user,dc=xiavan,dc=com".format(username)
        ret = self.ldap_obj.delete(dn)
        if ret:
           return {"code": 0, "msg":"success","username":username }
        else:
           return {"code": 1, "msg":"failure","username":username }

    def ldap_mail(self, receivers, username, password):
        print(receivers, username, password)
        mail_host = "smtp.exmail.qq.com"  # SMTP服务器
        mail_user = "developer@mumway.com"  # 用户名
        mail_pass = "Hymm2020!@#$"  # 密码(这里的密码不是登录邮箱密码，而是授权码)

        mail_sender = 'developer@mumway.com'  # 发件人邮箱
        mail_receivers = [receivers]  # 接收人邮箱

        content = '账号：{}  密码：{}'.format(username, password)
        title = '运维系统统一登录账号'  # 邮件主题
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(mail_sender)
        message['To'] = ",".join(mail_receivers)
        message['Subject'] = title

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(mail_user, mail_pass)  # 登录验证
            smtpObj.sendmail(mail_sender, mail_receivers, message.as_string())  # 发送
            print("账号: {} 密码: {}".format(username, password))
        except smtplib.SMTPException:
            print("发送邮件失败")

    def ldap_reload_json(self, filename):
        with open(filename, 'r', encoding="utf-8") as f:
            data = f.read()
        return json.loads(data)

    def ldap_get_values(self, data, tmp_list):
        for i in data.values():
            if isinstance(i, list):
                for j in i:
                    if isinstance(j, dict):
                        name = j.get("name")
                        email = j.get("email")
                        if name and email:
                            tmp_list.append((name, email))
                        else:
                            self.ldap_get_values(j, tmp_list)

