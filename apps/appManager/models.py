# -*- coding: utf-8 -*-
import datetime
from public import db
class Appmg(db.Model):
    __tablename__ = "deploy_appname"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business = db.Column(db.String(256), nullable=False)
    group = db.Column(db.String(1024), nullable=False)
    appname = db.Column(db.String(2048), nullable=False)
    apptype = db.Column(db.String(1024), nullable=False)
    giturl = db.Column(db.Text, nullable=False)
    port = db.Column(db.String(16), nullable=False)
    level = db.Column(db.String(64), nullable=False)
    owner = db.Column(db.String(256), nullable=False)
    used = db.Column(db.Text, nullable=False)
    createtime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())
    def __repr__(self):
        return '<App %r>' % self.name

    def to_dict(self):
        return {"id": self.id, "business": self.business, "group": self.group, "appname": self.appname, "apptype": self.apptype,
                "giturl": self.giturl, "owner": self.owner, "port": self.port, "level": self.level,
                "used": self.used, "createtime": str(self.createtime)}

    def to_appNameList(self):
        return {"env": self.appname}
