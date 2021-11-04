# op-devops-api
1.本项目采用Python Flask框架开发提供(应用管理,实例管理,Ansible管理,LDAP管理等相关功能) 后端项目配套前端项目为:op-devops-ui



# jenkinsManager
一.插件python-jenkins bug修复

(1).插件版本 python-jenkins==1.5.0
(2).获取jobs 出现如下错误
>>> server.get_jobs() 
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/site-packages/jenkins/__init__.py", line 768, in get_info
    requests.Request('GET', self._build_url(url))
  File "/usr/local/lib/python3.6/site-packages/jenkins/__init__.py", line 556, in jenkins_open
    return self.jenkins_request(req, add_crumb, resolve_auth).text
  File "/usr/local/lib/python3.6/site-packages/jenkins/__init__.py", line 575, in jenkins_request
    self._request(req))
  File "/usr/local/lib/python3.6/site-packages/jenkins/__init__.py", line 535, in _response_handler
    response.raise_for_status()
  File "/usr/local/lib/python3.6/site-packages/requests/models.py", line 940, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 400 Client Error:  for url: http://172.21.206.227:8080/jenkins/api/json?tree=jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs[url,color,name,jobs]]]]]]]]]]

(3).处理办法；找到文件
vim /usr/local/lib/python3.6/site-packages/jenkins/__init__.py  +1020行 去掉 query=jobs_query 代码;

               
二.接口文档;

1.基础环境介绍;

   软件版本信息  |系统/内核信息 |项目目录功能介绍
  -|-|-
  Python 3.7.9     |Centos 7.2 | tools jekins jobs相关xml配置
  Flask1.0.2    |3.10.0-862.6.3.el7.x86_64  |boot.py flask 程序启动入口文件
  python-jekins1.5.0   |           | python jenkins sdk 插件


2.项目系统依赖包安装;  
  (1).centos 7x系统安装支持包;  
   yum -y install python36 mysql-devel libxml2* mysql initscripts python36-devel python36-pip python36-setuptools mysql-devel libxml2*      mysql initscripts psmisc  
   
   
   (2).安装项目依赖包pip方式;  
   
   /usr/local/bin/pip3.6 install --upgrade pip  
   /usr/local/bin/pip3.6 install --upgrade setuptools  
   /usr/local/bin/pip3.6 install requests  
   /usr/local/bin/pip3.6 install Jinja2==2.10  
   /usr/local/bin/pip3.6 install flask==1.0.2  
    /usr/local/bin/pip3.6 install request==1.0.2  
    /usr/local/bin/pip3.6 install Jinja2==2.10  
    /usr/local/bin/pip3.6 install Flask-Cors==3.0.6  
    /usr/local/bin/pip3.6 install flask-sqlalchemy  
    /usr/local/bin/pip3.6 install flask_restful  
    /usr/local/bin/pip3.6 install  python-jenkins==1.5.0
    
3.接口文档介绍;  
(1).jenkisn 构建job主机接口;  

**jenkinsManager-api 接口文档：** 

- 创建job 任务

**请求URL：** 
- ` http://devops-bmc-api.com/jenkins/api/v1 `
  
**请求方式：**
- POST  

**格式：**  
- JSON  

**参数：** 

|参数   |必填   |类型   |说明   |
| ------------  | ------------ | ------------ | ------------ |
| instance_ip    |是   |str   |执行端合法ip地址, 默认值:None,支持多个ip地址添加","隔开".
| appname       |是   |str    |应用名称，
| giturl        |是   |str    |代码仓库git地址
| branch        |是   |str    |代码仓库应用分支
| type          |是   |str    |应用类型1.java 2.python 3.go 4.node.js
| appversion    |是   |str    |应用当前的版本
 **请求示例**
```
{
 "instance_ip":"192.168.1.2,192.168.1.3",  	 
 "appname":"op-bmc-api-004",
 "giturl":"https://github.com/breaklinux/devops-bmc-api.git",
 "branch":"master",
 "type":"1",
 "appversion":"1.0.0.2"
}
```
 **返回参数**
```
{
    "code": 0,
    "data": {
        "appname": "op-bmc-api-003"
    },
    "msg": "job create success"
}
```

 **备注** 

- code状态码描述
  0 表示系统正常响应;
  1 表示系统内部出现问题;  
 
**删除 job 任务: **

**请求URL：** 
- `http://devops-bmc-api.com/jenkins/api/v1 `
  
**请求方式：**
- Delete 
 **请求示例**
 ```
{
 "appname":"op-bmc-api003"
 }
```
 **返回参数**
 ```
{
    "code": 0,
    "msg": "op-bmc-api-003 delete success"
}
```
