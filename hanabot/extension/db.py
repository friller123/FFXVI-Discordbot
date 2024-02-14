# this is just simple delcaration of the database structure for peewee

from peewee import *

db = SqliteDatabase("./data/sqlite.db")

class serverdata(Model):
    ID = IntegerField(unique=True,primary_key=True)
    ServerID = IntegerField(null=True)
    ChannelID = IntegerField(null=True)
    MessageID = IntegerField(null=True)
    Entries = IntegerField(null=True)
    class Meta:
        database = db

class botdata(Model):
    ID = IntegerField(unique=True,primary_key=True)
    ServerID = IntegerField(null=True,unique=True)
    Hours = IntegerField(null=True)
    Minutes = IntegerField(null=True)
    Seconds = IntegerField(null=True)
    class Meta:
        database = db