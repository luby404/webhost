import uuid

from flask_login import UserMixin

from .ext.database import orm, Model, db


class Usuario(Model, UserMixin):
    email = orm.CharField(max_length=256, unique=True)

class Evento(Model):
    usuario = orm.ForeignKeyField(Usuario, backref="eventos")
    nome    = orm.CharField(max_length=256)
    pub_id  = orm.UUIDField(default=uuid.uuid4)
    data    = orm.TextField(null=True)


def init_models():
    db.connect()
    db.create_tables([Usuario, Evento])
