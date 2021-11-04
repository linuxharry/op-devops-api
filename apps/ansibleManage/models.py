import datetime
from public import db

class bmc_ansible(db.Model):
    __tablename__ = 'system_ansible'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键自增长
    run_ip = db.Column(db.String(1024), nullable=False)  ###不能为空
    command_name = db.Column(db.String(64), nullable=False)  ###不能为空
    run_agrs = db.Column(db.Text, nullable=False)  ###不能为空
    ansible_callback = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "run_ip": self.run_ip, "command_name": self.command_name, "run_agrs": self.run_agrs,
                "ansible_callback": self.ansible_callback}


class bmclog(db.Model):
    __tablename__ = 'system_ansible_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descname = db.Column(db.String(128), nullable=True)  #########模块名称###########
    source = db.Column(db.String(64), nullable=True)  ########ip源地址###########
    request = db.Column(db.Text, nullable=True)  #######请求参数##########
    response = db.Column(db.Text, nullable=True)  ########返回参数###########
    opsmethod = db.Column(db.String(64), nullable=True)  ########返回方法##########
    run_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "descname": self.descname, "source": self.source,
                "request": self.request, "response": self.response, "opsmethod": self.opsmethod, "run_time":
                    self.run_time}


class bmc_ansible_hosts(db.Model):
    __tablename__ = 'system_ansible_hosts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键自增长
    instanceip = db.Column(db.String(256), nullable=False)  ###不能为空
    username = db.Column(db.String(32), nullable=False)  ###不能为空
    password = db.Column(db.String(64), nullable=False)  ###不能为空
    port = db.Column(db.String(8), nullable=False)
    group = db.Column(db.String(24), nullable=False)
    createtime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "instanceip": self.instanceip, "username": self.username, "password": self.password,
                "port": self.port, "group": self.group,"createtime": str(self.createtime)}
    def __repr__(self):
        return '<Host %r>' % self.instanceip
