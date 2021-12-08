from peewee import *
import datetime 
from flask_login import UserMixin
#sqlite adaptor lets us connect to sqlite

DATABASE = SqliteDatabase('jv.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE # use the db defined above as DATABASE


class Jv(Model):
    preparer = ForeignKeyField(User, backref='jv')
    name = CharField()
    logo = CharField()
    location = CharField()
    ownership = IntegerField()
    sales = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE # use the db defined above as DATABASE



def initialize(): 
    DATABASE.connect() 
    DATABASE.create_tables([User, Jv], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    DATABASE.close()