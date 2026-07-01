from datetime import datetime

import peewee as orm

import uuid

db = orm.SqliteDatabase("banco.db")

class Model(orm.Model):
    criado_em = orm.DateTimeField(default=datetime.now)
    uuid      = orm.UUIDField(default=uuid.uuid4, primary_key=True)

    class Meta:
        database = db
