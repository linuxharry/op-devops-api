from pytz import timezone
import os

#jenkins 账号信息
accUrl="http://192.168.11.13:8080/jenkins"
username="admin"
password="admin"
"""
2.jenkins视图列表默认dev,test,ontest,prod 环境;
"""
viewList = ["Dev", "Test", "Ontest", "Prod"]

DEBUG = True
TIME_ZONE = timezone('Asia/Shanghai')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.1.101:3306/op-cicd-api-v2'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

DOCKER_REGISTRY_SERVER = 'op-harbor.xxx.com'
DOCKER_REGISTRY_AUTH = {'username': 'xxx', 'password': 'xxx'}

LDAP_CONFIG = {
    'host': 'xxx',
    'port': 389,
    'is_openldap':  True,
    'base_dn': 'dc=xiavan,dc=com',
    'admin_dn': 'cn=admin,dc=xiavan,dc=com',
    'admin_password': 'xxx',
    'user_filter': 'cn',
}

appMgHeader=[
    {"name":"group","alias":"小组名称"},
    {"name":"appname","alias":"应用名称"},{"name":"level","alias":"应用级别"},
    {"name":"apptype","alias":"应用类型"},{"name":"business","alias":"业务线"},
    {"name":"giturl","alias":"git地址"}, {"name":"owner","alias":"应用负责人"},
    {"name":"port","alias":"服务端口"},{"name":"used","alias":"用途"},
    {"name":"createtime","alias":"创建时间"},
]
#{"name":"id","alias":"唯一标识"},

instanceMgHeader=[
    {"name":"appname","alias":"应用名称"},{"name":"domain","alias":"域名"},{"name":"instancename","alias":"实例名称"},
    {"name":"ip","alias":"实例ip地址"}, {"name":"env","alias":"环境"},
]


###环境关系标识定义####
envListkey = ["dev","test","test2","pre","pro","devops"]
envListdisplay_name=["开发环境","测试环境","测试环境2","预发布环境","生产环境","运维环境"]

##发布版本分支关系定义#####
releaseListkey = ["Release","master","hostfix"]
releaseListDisplay_name=["release","master","hostfix"]

#支持发布语言
languageType = ["java","php","vue","python","go"]
languageTypedisplay_name=["Java","PHP","VUE","Python","Go"]

#查询软件包路径地址
searchPackPath="/xwkj/data/update"

##发布表头
cicdMgHeader=[
    {"name": "id", "alias": "唯一标识"},{"name": "env", "alias": "发布环境"},
    {"name": "appname", "alias": "应用名称"},{"name": "appversion", "alias": "发布版本"},
    {"name": "instance_ip", "alias": "发布实例"},{"name": "giturl", "alias": "GIT地址"},
    {"name": "language_type", "alias": "语言类型"},{"name": "release_reason", "alias": "发布原因"},
    {"name": "jenkins_callback", "alias": "Jenkins返回"},{"name": "releasetime", "alias": "发布时间"},
]
#ldap表头
ldapHeader=[
    #{"name": "id", "alias": "唯一标识"},
    {"name": "username", "alias": "登录用户"},
    {"name": "password", "alias": "用户密码"},{"name": "name", "alias": "用户全名"},
    {"name": "mail", "alias": "邮箱地址"},{"name": "createtime", "alias": "创建时间"},
]

#服务启动配置文件
ansibleApiUrl="https://op-apis.mumway.com/op-ansible-api/ansible/api/v1"
channelID="c5655f1c-1cea-11ec-b4f2-00163e158a73"
getChannelIp="https://op-apis.mumway.com/op-ansible-api/channel/ip/v1?"

serviceMgHeader=[
    {"name":"source","alias":"来源ip地址"},{"name":"channelID","alias":"授权ID"},{"name":"username","alias":"使用用户"},
    {"name":"request","alias":"请求参数"},{"name":"response","alias":"响应结果"},{"name":"opsmethod","alias":"运行方法"},
    {"name": "run_time", "alias": "操作时间"},
]

##########Ansible 认证授权UUID表头模板###############
#ChanneUuidHeader=[{"name": "id", "alias":"唯一标识"},{"name": "uuid","alias":"授权uuid"},{"name":"desc","alias":"备注说明"},{"name":"owner","alias":"使用方"}, {"name":"uuid_use","alias":"用途"}]

ChanneUuidHeader=[{"name": "uuid","alias":"授权uuid"},{"name":"desc","alias":"备注说明"},{"name":"owner","alias":"使用方"}, {"name":"uuid_use","alias":"用途"}]



ChanneIpHeader=[{"name": "id", "alias":"唯一标识"},{"name": "ip","alias":"授权IP地址"},{"name":"desc","alias":"备注说明"},{"name":"owner","alias":"使用方"}]


WhilteIpField = [
    {"name": "ip", "label": "授权IP地址", "fieldType": "TextInput","disabled": False, "cols": 8},
    {"name": "owner", "label": "使用方", "fieldType": "TextInput","disabled": False, "cols": 8},
    {"name": "desc", "label": "备注说明", "fieldType": "TextInput","disabled": False, "cols": 8}
]


WhilteUuidField = [
    {"name": "owner", "label": "使用方", "fieldType": "TextInput","disabled": False, "cols": 8},
    {"name": "uuid_use", "label": "用途", "fieldType": "TextInput", "disabled": False, "cols": 8},
    {"name": "desc", "label": "备注说明", "fieldType": "TextInput","disabled": False, "cols": 8}
]

DynamicHostHeader=[
    {"name":"id","alias":"唯一标识"},{"name":"instanceip","alias":"主机IP"},
    {"name":"password","alias":"密码"},{"name":"username","alias":"用户"},
    {"name":"port","alias":"端口"},{"name":"group","alias":"主机组"},
    {"name":"createtime","alias":"创建时间"}]
