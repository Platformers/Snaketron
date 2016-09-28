import datetime
import bcrypt

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import validates

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean, default=False)
    company_employee = db.Column(db.Boolean, default=False)
    company_manager = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.email = kwargs['email']
        self.password = generate_password_hash(kwargs['password'])
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']

    def is_active(self):
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's Requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported at the moment."""
        return False


class Idea(db.Model):
    __tablename__ = 'idea'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, author):
        self.title = title
        self.description = description
        self.author_id = author

class IdeaComment(db.Model):
    __tablename__ = 'idea_comment'

    id = db.Column(db.Integer, primary_key=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(500))

