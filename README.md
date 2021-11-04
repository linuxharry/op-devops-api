# op-devops-api
1.本项目采用Python Flask框架开发提供(应用管理,实例管理,Ansible管理,LDAP管理等相关功能) 后端项目配套前端项目为:op-devops-ui



# jenkinsManager
一.插件python-jenkins bug修复

(1).插件版本 python-jenkins==1.5.0
               
二.接口文档;

1.基础环境介绍;

   软件版本信息  |系统/内核信息 |项目目录功能介绍
  -|-|-
  Python 3.6.8     |Centos 7.2 | tools jekins jobs相关xml配置
  Flask1.0.2    |3.10.0-862.6.3.el7.x86_64  |boot.py flask 程序启动入口文件
  python-jekins1.5.0   |           | python jenkins sdk 插件


2.项目系统依赖包安装;  
   (1).centos 7x系统安装支持包;  
   yum -y install python36 mysql-devel libxml2* mysql initscripts python36-devel python36-pip python36-setuptools mysql-devel libxml2*      mysql initscripts psmisc  
 
   (2).安装项目依赖包pip3方式;  
   /usr/local/bin/pip3.6 install --upgrade pip  
   /usr/local/bin/pip3.6 install --upgrade setuptools  
   /usr/local/bin/pip3.6 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

3.修改项目配置文件 (MYSQL文件)
  cat config.py #新建数据库并且授权应用程序访问 (如下:op-cicd-api-v2)
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.1.101:3306/op-cicd-api-v2'
  
4.初始化数据库表结构设置授权管理员账号权限 操作流程:初始化数据库表---> 创建管理员账户---> 输入账号密码
$ python3.7 manage.py  
usage: manage.py <command>
command:
    	init_db
		-- 初始化数据库
	create_admin
		-- 创建管理员账户
	enable_admin
		-- 启用管理员账户，用于登录失败次数过多账户被禁用时使用

5.登录获取应用token参数如下:
 **token-api 接口文档：** 

- 输入用户密码登录获取token

**请求URL：** 
- ` http://devops-bmc-api.com/account/users/login/ `
  
**请求方式：**
- POST  

**格式：**  
- JSON  

**参数：** 

|参数   |必填   |类型   |说明   |
| ------------  | ------------ | ------------ | ------------ |
| username    |是   |str   |系统授权用户名
| password    |是   |str    |系统授权用户名
| type        |是   |str    |类型分为: standard 系统设置用户 ldap 用户

 **请求示例**
 ```
 http://devops-bmc-api.com/account/users/login/
 {
"username":"admin",
"password":"admin@123",
"type":"standard"
}
 ```
**返回参数**
```
http://devops-bmc-api.com/account/users/login/
{
    "data": {
        "is_supper": true,
        "nickname": "管理员",
        "permissions": [],
        "token": "3df9a449d44f4183a45ba9a43cc61fbc"  #Token 有过期时间每一次请求需要带token
    },
    "message": ""
}
```




