jenkinFileBody = """
#!groovy
import groovy.transform.Field
import groovy.json.JsonOutput
import groovy.json.JsonSlurperClassic
@Field CHANGE_HOST = 'http://192.168.54.12'
@Field CONSOLE_SCRIPT = "/chj/data/jenkins-data"
@Field SERVICE_TYPE = "ChangE"

try {
    node {
        parameters {
            string defaultValue: '1', description: '环境', name: 'runenv', trim: true
            string defaultValue: 'ordercenter', description: '服务名称', name: 'appname', trim: true
            string defaultValue: 'ordercenter_v1.0.90_20210622_002_release-APPLET-149.tar.gz', description: '软件包名称', name: 'appversion', trim: true
            string defaultValue: 'release-APPLET-149#v1.0.90_20210622_002', description: '分支名称', name: 'branch', trim: true
            string defaultValue: '127.0.0.1', description: '实例ip地址', name: 'instance_ip', trim: true
            string defaultValue: '6', description: '项目地址', name: 'giturl', trim: true
            string defaultValue: '7', description: '语言类型', name: 'language_type', trim: true
            string defaultValue: '8', description: '发布类型VM/k8', name: 'release_type', trim: true
            string(defaultValue: 'type', description: '构建应用类型 1.java 2.python 3.go 4.node.js', name: 'type')
            string(defaultValue: 'gitURL', description: 'git地址', name: 'gitURL')
        }
        stage('checkout') {
            try {
                checkout([$class: 'GitSCM', branches: [[name: '${branch}']], doGenerateSubmoduleConfigurations: false, userRemoteConfigs: [[credentialsId: 'cd_change_jenkins', url: '${giturl}']]])
            } catch (Exception e) {
                print(e)
            }
        }
        stage('Build') {
            //构建类型为1 属于java 类型应用
            //构建类型为2 属于python 类型应用
            //构建类型为3 属于go 类型应用
            //构建类型为4 属于node 类型应用
            try {
                if ("$type" == "1") {
                    sh "mvn clean package -U -DskipTests=true"
                } else if ("$type" == "2") {
                   sh "echo '不需要编译'"

                } else if ("$type" == "3") {
                    sh "go build"

                } else if ("$type" == "4") {
                    sh "rm -rf  dist"
                    sh "cnpm install"
                }
            }catch (Exception e) {
                print(e)
            }
    }
    }
    } catch (Exception e ) {
        print(e)
    }
"""
