from public import db
from libs.model import ModelMixin


class Environment(db.Model, ModelMixin):
    __tablename__ = 'configuration_environments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    identify = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    priority = db.Column(db.Integer, default=100)

    def __repr__(self):
        return '<Environment %r>' % self.name

    class Meta:
        ordering = ('-id',)
