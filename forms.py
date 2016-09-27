from flask_wtf import Form
from wtforms_sqlalchemy.orm import model_form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, Length, EqualTo,
                                ValidationError, Email)

from models import *


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')

def email_exists(form, field):
    if db.sessionUser.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email exists already.')

class RegistrationForm(Form):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers, and"
                         " underscores only.")
            ),
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
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
    email = StringField('Email', validators=[DataRequired(), Email()])
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
