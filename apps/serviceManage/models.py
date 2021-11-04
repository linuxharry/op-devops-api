# -*- coding: utf-8 -*-
import datetime
from public import db
##服务管理日志表记录
class serviceLog(db.Model):
    __tablename__ = 'deploy_servicelog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descname = db.Column(db.String(128), nullable=True)  #########模块名称###########
    source = db.Column(db.String(64), nullable=True)  ########ip源地址###########
    channelID = db.Column(db.String(128), nullable=True)  #######授权id#####
    username = db.Column(db.String(64), nullable=True)  ####谁调用#########
    request = db.Column(db.Text, nullable=True)  #######请求参数##########
    response = db.Column(db.Text, nullable=True)  ########返回参数###########
    opsmethod = db.Column(db.String(64), nullable=True)  ########返回方法##########
    run_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "descname": self.descname, "source": self.source, "channelID": self.channelID,
                "username": self.username,
                "request": self.request, "response": self.response, "opsmethod": self.opsmethod, "run_time":
                    str(self.run_time)}


