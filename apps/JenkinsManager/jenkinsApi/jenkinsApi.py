from flask import Response
import json
import jenkins
"""
https://python-jenkins.readthedocs.io/en/latest/examples.html#

"""


class JeninsDeploy(object):
    @property
    def jenkinsConfig(self):
        """
        1.jenkins 相关配置信息url,user，password
        2.return 返回连接信息
        """
        from config import accUrl, username, password
        jenKins = jenkins.Jenkins(accUrl, username=username, password=password,timeout=5)
        return jenKins

    @property
    def tempJenkinsXml(self):
        """
        1.读取xml 生成创建视图配置文件;
        2.读取pipline xml 替换视图内容;
        3 return 返回xml 配置信息;
        """
        from apps.JenkinsManager.conf.tempxml import tempconf
        from apps.JenkinsManager.conf.temppipeline import jenkinFileBody
        return tempconf.format(JenkinsPipelineTemp=jenkinFileBody.strip())


    def jenkinsCreateJob(self, appname):
        """
        1.获取所有joblist 返回list判断appname 是否存在 joblist 中,
        2.job存在执行更新job逻辑
        3.job 不存在执行创建job方法;
        4.return 返回创建job;
        """
        try:
            if [jobs["name"] for jobs in self.jenkinsConfig.get_jobs() if appname == jobs["name"]]:
                self.jenkinsConfig.reconfig_job(appname, self.tempJenkinsXml)
                msg = "create jenkins jobs success"
                return msg
            else:
                self.jenkinsConfig.create_job(appname, self.tempJenkinsXml)
                msg = "update jenkins jobs success"
                return msg
        except Exception as e:
            print(e)
            return Response(json.dumps({"code": 1, "msg": str(e)}), mimetype="application/json")

    def jenkinsBuildJob(self,env,appname, appversion, giturl, appbranch, language_type,appType, ipaddr):
        """
        1.构建参数job任务;
        :param appname:
        :param appversion:
        :param giturl:
        :param appbranch:
        :param appType:
        2.return 处理信息;
        """

        try:
            buildjob = self.jenkinsConfig.build_job(appname, {"runenv":env,"appname": appname, "version": appversion,
                                                              "giturl": giturl, "branch": appbranch, "language_type":language_type,"type": appType,
                                                              "instance_ip": ipaddr})
            return buildjob
        except Exception as e:
            print(e)
            return Response(json.dumps({"code": 0, "msg": str(e)}), mimetype="application/json")

    def jenKinsdeleteJob(self, appname):
        """
        1.删除job 传入jobname
        :param appname:
        :return:
        """

        try:
            self.jenkinsConfig.delete_job(appname)
            msg = "delete success"
            return Response(json.dumps({"code": 0, "msg": appname + ' ' + msg}), mimetype="application/json")
        except Exception as e:
            print(e)
            data = "delete failure"
            return Response(json.dumps({"code": 0, "data": data, "msg": appname + ' ' + str(e)}),
                            mimetype="application/json")

    def formatResultStr(self,data, appname):
        """
        1.url替换修改并完成字符串拼接
        2.拼接完成示例:http://192.168.58.125:8080/blue/organizations/jenkins/sec-service-web/detail/sec-service-web/4/pipeline
        :param data:
        :param appname:
        :return:
        """
        from urllib.parse import urlparse
        print("获取的值",data)
        if data:
            tempData = data.split('/', -2)
            nuber = tempData[-2]
            newuber=int(nuber) + 1
            o = urlparse(data)
            print("地址" + data)
            # resultJobInfo = o.scheme + "://" + o.hostname + ":" + str(
            #     o.port) + """/job/{appname}/detail/{appname}/{nuber}/pipeline""".format(appname=appname, nuber=str(newuber))
            resultJobInfo = "http://192.168.11.101" + """/job{appname}/detail/{appname}/{nuber}/pipeline""".format(appname=appname, nuber=str(newuber))
            newstr = resultJobInfo.replace("/job", "/jenkins/blue/organizations/jenkins/xiavan")
            print("修改后地址",newstr)
            return newstr
        else:
            #http://192.168.11.101/jenkins/blue/organizations/jenkins/xiavan%2Fop-ceshi-api/detail/op-ceshi-api/16/pipeline/
            return  '''http://192.168.11.101/jenkins/blue/organizations/jenkins/xiavan/{appName}/detail/{JobName}/1/pipeline'''.format(appName=appname,JobName=appname)
    def jenkinsCreateView(self):
        """
        1.创建jenkins 视图;
        2.目前支持dev,test,ontest.prod
        :return:
        """
        from apps.JenkinsManager.conf.tempview import viewConf
        from config import viewList
        try:
            for i in viewList:
                self.jenkinsConfig.create_view(i, viewConf)
        except Exception as e:
            msg = "failure" + str(e)
        return Response(json.dumps({"code": 1, "data": msg}), mimetype='application/json')

    def getAllJob(self):
        """
        1.获取全部job任务;
        :return:
        """
        # return self.jenkinsConfig.get_info()
        try:
            result = self.jenkinsConfig.get_jobs()
            return Response(json.dumps({"code": 0, "data": result}), mimetype='application/json')
        except Exception as e:
            print(e)
            msg = "get job failure" + ' ' + str(e)
        return Response(json.dumps({"code": 1, "data": msg}), mimetype='application/json')

    def getJobInfo(self, appname):
        try:
            last_build_number = self.jenkinsConfig.get_job_info(appname)['lastCompletedBuild']['number']
            build_info = self.jenkinsConfig.get_build_info(appname, last_build_number)
            url = build_info.get("url")
            print(url)
            return url
        except Exception as e:
            print(e)
