import os

from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_user, logout_user, login_required,
                         current_user)


import modelsV
import forms


app = Flask(__name__)
app.secret_key = '3a5s1df6a3sd85a3se1f5aw23e1f3s813as8e565a951ef3a861wea1'
app.config.from_object(os.environ['APP_SETTINGS'])


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """ Close the database connection"""
    g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash('You have Successfully Registered!', 'success')
        models.User.create_user(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try: 
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your username or password do not match our records",
                  "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You have successfully logged in!')
                return redirect(url_for('home'))
            else:
                flash("Your username or password do not match our records")
    return render_template('login.html', form=form)

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

