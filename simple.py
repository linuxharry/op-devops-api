#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdksts.request.v20150401.AssumeRoleRequest import AssumeRoleRequest

#构建一个阿里云客户端，用于发起请求。
#构建阿里云客户端时需要设置AccessKey ID和AccessKey Secret。
client = AcsClient('LTAI5tNH9MPKV8AcULHfTynA', 'sasVkPJvSXT57Yn2P5O7D2Z84458Vx', 'cn-zhangjiakou')

#构建请求。
request = AssumeRoleRequest()
request.set_accept_format('json')

#设置参数。
request.set_RoleArn("acs:ram::1059332678590504:role/smartdevice-ram")
request.set_RoleSessionName("smartdevice")

#发起请求，并得到响应。
response = client.do_action_with_exception(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))
