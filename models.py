import datetime
import os

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

psql_db = Proxy()


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = psql_db


class User(UserMixin, BaseModel):
    username = CharField(unique=True,max_length=25)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = CharField(unique=True, max_length=255)
    password = CharField(unique=True)
    company_employee = BooleanField(default=False)
    company_manager = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def create_user(cls,
                    username,first_name,last_name,email,password,company_employee=False,
                    company_manager=False):
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

    class Meta:
        db_table = 'users'


class Idea(BaseModel):
    title = CharField(max_length=50)
    description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    author_id = ForeignKeyField(rel_model=User,related_name='ideas')


class IdeaComment(BaseModel):
    idea_id = ForeignKeyField(rel_model=Idea,related_name='idea_comments')
    author_id = ForeignKeyField(rel_model=User, related_name='idea_comment_author')
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

def initialize():
    psql_db.connect()
    psql_db.create_tables([User,Idea,IdeaComment],safe=True)
    psql_db.close()

if 'HEROKU' in os.environ:
    import urlparse, pyscopg2
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    db = PostgresqlDatabase(database=url.path[1:],
                            user=url.username,password=url.password,host=url.hostname,
                            port=url.port)
    psql_db.initialize(db)
else:
    db = PostgresqlDatabase(database=os.environ['DATABASE'],
                                 user=os.environ['DATABASE_USERNAME'],
                                password=os.environ['DATABASE_PASSWORD'],host=os.environ['DB_HOST'],
                                port=os.environ['DB_PORT'])
    psql_db.initialize(db)

