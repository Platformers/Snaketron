import os

from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_user, logout_user, login_required,
                         current_user)


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

import models
import forms


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    """Given a userid, return the associated User object.

    :param unicode userid: userid (email) user to retrieve
    """
    return User.query.filter_by(username=userid)


@app.before_request
def before_request():
    g.user = current_user


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash('You have Successfully Registered!', 'success')
        data = {
            'username': form.username.data,
            'password': form.password.data,
            'email': form.email.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data
        }
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        user.authenticated = True
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
        except TypeError:
            pass
        else:
            if check_password_hash(user.password.decode('utf8'),
                                   form.password.data.encode('utf8')):
                user.authenticated=True
                login_user(user)
                flash("You have been logged in!", "success")
                return redirect(url_for('home'))
            else:
                flash("Your email or password are incorrect!", 'error')
    return render_template('login.html',form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!")
    return redirect( url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()

