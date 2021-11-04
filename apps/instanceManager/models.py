import datetime
from public import db

class Instancemg(db.Model):  # 从表
    __tablename__ = "deploy_instance"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instancename = db.Column(db.String(256), nullable=False)
    appname = db.Column(db.String(2048), nullable=False)
    domain = db.Column(db.String(2048), nullable=False)
    ip = db.Column(db.String(256), nullable=False)
    env = db.Column(db.String(64), nullable=False)
    createtime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())
    def to_dict(self):
        return {"id": self.id,"appname": self.appname, "instancename": self.instancename,"domain":self.domain,"ip": self.ip, "env": self.env,
                "createtime": str(self.createtime)}
    def to_appname(self):
        return {"appname": self.appname}


