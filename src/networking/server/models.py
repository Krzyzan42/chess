from peewee import *

db = SqliteDatabase('database/db.sqlite3')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    username = TextField()
    password = TextField()

def init_db():
    db.connect()
    db.create_tables([User])