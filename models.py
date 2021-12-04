from peewee import *
import datetime 
from flask_login import UserMixin
#sqlite adaptor lets us connect to sqlite

DATABASE = SqliteDatabase('jv.sqlite')

class Jv(Model):
    name = CharField(null=True)
    ownership = CharField(null=True)
    sales = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE # use the db defined above as DATABASE


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE # use the db defined above as DATABASE

def initialize(): 
    DATABASE.connect() 
    DATABASE.create_tables([User, Jv], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    DATABASE.close()