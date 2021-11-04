# -*- coding: utf-8 -*-
import datetime
from public import db

class Cicdmg(db.Model):
    __tablename__ = "deploy_cicdmg"
    id = db.Column(db.Integer, primary_key=True)
    env = db.Column(db.String(1024), nullable=False)
    appname = db.Column(db.String(1024), nullable=False)
    appversion = db.Column(db.String(1024), nullable=False)
    branch = db.Column(db.String(1024), nullable=False)
    instance_ip = db.Column(db.Text, nullable=False)
    giturl = db.Column(db.Text, nullable=False)
    language_type = db.Column(db.String(1024), nullable=False)
    release_type = db.Column(db.String(1024), nullable=False)
    release_reason = db.Column(db.Text, nullable=False)
    jenkins_callback = db.Column(db.Text, nullable=False)
    releasetime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "env": self.env, "appname": self.appname, "appversion": self.appversion,
                "branch": self.branch, "instance_ip": self.instance_ip,
                "giturl": self.giturl, "language_type": self.language_type, "release_type": self.release_type,
                "release_reason": self.release_reason, "callback": self.jenkins_callback, "releasetime": str(self.releasetime)}
