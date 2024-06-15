from peewee import *
import datetime

db = SqliteDatabase('database/db.sqlite3')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    username = TextField()
    password = TextField()

class SavedGame(BaseModel):
    id = AutoField()
    host = ForeignKeyField(User)
    guest = ForeignKeyField(User)
    win = BooleanField(null=True)
    moves = TextField()
    date_played = DateTimeField(default = datetime.datetime.now)

def init_db():
    db.connect()
    db.create_tables([User, SavedGame])