import datetime
import bcrypt

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *


# from sqlalchemy import Column, Integer, Text, TypeDecorator
# from sqlalchemy.dialects.postgresql import JSON
# from sqlalchemy.orm import validates

# from app import db

psql_db = PostgresqlDatabase('snaketron',
                             user='snaketron',password='snaketron')

class User(UserMixin, Model):
    username=CharField(unique=True,max_length=25)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email=CharField(unique=True, max_length=255)
    password=CharField(unique=True)
    company_employee=BooleanField(default=False)
    company_manager = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = psql_db

        @classmethod
        def create_user(cls,
                        username,first_name,last_name,email,password,company_employee=False,
                        company_manager=False)
            try:
                cls.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=generate_password_hash(password),
                    company_employee=company_employee,
                    company_manager=company_manager
                )
            except IntegrityError:
                raise ValueError("User already exists!")



class Idea(Model):
    title = CharField(max_length=50)
    description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    author_id = ForeignKeyField(rel_model=User,related_name='ideas')

    class Meta:
        database = psql_db

class IdeaComment(Model):
    idea_id = ForeignKeyField(rel=Idea,related_name='idea_comments')
    author_id = ForeignKeyField(rel=User, related_name='idea_comment_author')
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

def initialize():
    psql_db.connect()
    psql_db.create_tables([User,Idea,IdeaComment],safe=True)
    psql_db.close()


