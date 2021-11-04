# -*- coding: utf-8 -*-
import datetime
from public import db
class ldapmg(db.Model):  #ldap用户表
    __tablename__ = "system-ldap"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(2048), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    mail = db.Column(db.String(64), nullable=False)
    createtime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id,"username": self.username, "password": self.password, "name": self.name, "mail": self.mail,
                "createtime": str(self.createtime)}

