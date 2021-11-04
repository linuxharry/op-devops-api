#!/usr/bin/env python36
"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
from flask import request, Response
import requests
import os
HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "tools")

def getHostInventoryData(url):
    import json
    gethostdata = requests.get(url)
    getdata = gethostdata.json()["data"]
    data = dict()
    l=[]
    for i in getdata:
        l.append(i["group"])
    groups = set(l)
    gdata=str(groups)
    data["all"] = {"children": gdata}
    data["_meta"] = {"hostvars": {}}
    for group in groups:
        data[group] = dict()
        data[group]["hosts"] = list()
        for x in getdata:
            if x["group"] == group:
               data[group]["hosts"].append(x["instanceip"])
    return json.dumps(data, indent=5)

def HostApi():
    getInventoryUrl = "https://op-apis.breaklinux.com/op-ansible-api/ansible/host/v1"
    import json
    import configparser
    data = json.loads(getHostInventoryData(getInventoryUrl))

    config = configparser.ConfigParser(allow_no_value=True)
    for i in data:
        if i != "all" and i != "_meta":
            config.add_section(i)
            for h in data[i]["hosts"]:
                config.set(i, h)
            config.write(open("%s/inventory_static_hosts"%script_path, "w"))
    return True



if __name__ == "__main__":
    from optparse import OptionParser
    getInventoryUrl = "https://op-apis.breaklinux.com/op-ansible-api/ansible/host/v1"  ###获取动态主机接口###
    parse = OptionParser()
    parse.add_option("-l", "--list", action="store_true", dest="list", default=False)
    (option, arges) = parse.parse_args()
    if option.list:
        print(getHostInventoryData(getInventoryUrl))
    else:
        import json
        print(json.loads(getHostInventoryData(getInventoryUrl)))
