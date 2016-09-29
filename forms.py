from flask_wtf import Form
from wtforms_sqlalchemy.orm import model_form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, Length, EqualTo,
                                ValidationError, Email)

from models import *
from app import db


def name_exists(form, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('A User with that username already exists.')

def email_exists(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('User with that email exists already.')

class RegistrationForm(Form):
    first_name = StringField(
        'First Name',
        validators = [DataRequired(), Length(max=50),]
    )
    last_name = StringField(
        'Last Name',
        validators = [DataRequired(), Length(max=100),]
    )
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers, and"
                         " underscores only.")
            ),
            name_exists,
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            Length(max=255),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired])

class IdeaForm(Form):
    title = StringField(
        'Title',
        validators = [
            DataRequired(),
            Length(min=20)
        ])
    content = TextAreaField(
        'Give more details on your idea',
        validators = [DataRequired()])
