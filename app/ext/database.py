from datetime import datetime
import peewee as orm

db = orm.SqliteDatabase("banco.db")

class Model(orm.Model):
    criado_em = orm.DateTimeField(default=datetime.now)
    class Meta:
        database = db
