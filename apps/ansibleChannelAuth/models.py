import datetime
from public import db
class channel(db.Model):  ########认证code##########
    __tablename__ = 'bmc_channel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(64), nullable=True)
    desc = db.Column(db.String(128), nullable=True)  ########这个uuid 给谁用###########
    owner = db.Column(db.String(64), nullable=True)
    uuid_use = db.Column(db.String(64), nullable=True)  #######这个uuid 给那个系统使用(用途)
    create_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "uuid": self.uuid, "desc": self.desc, "uuid_use": self.uuid_use,
                "owner": self.owner}
class ipwhilt(db.Model):  #######ip 白名单########
    __tablename__ = 'bmc_ipwhilt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(24), nullable=True)
    desc = db.Column(db.String(128), nullable=True)
    owner = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "ip": self.ip, "desc": self.desc,
                "owner": self.owner}
