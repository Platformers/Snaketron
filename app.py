import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_user, logout_user, login_required,
                         current_user)

import models
import forms


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    """Given a userid, return the associated User object.

    :param unicode userid: userid (email) user to retrieve
    """
    return User.query.get(userid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)

        flask.flash('Logged in successfully')

        return redirect( url_for('home'))
    else:
        flash("Your email or password were incorrect please try again!",
              "error")
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!")
    return redirect( url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')
