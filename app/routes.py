from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.forms import SignUpForm, LogInForm
from app.models import User

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup", methods= ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray our form submitted!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):

            login_user(user)
            flash(f"{user} is now logged in.", 'primary')
            return redirect(url_for('index'))

        else:

            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))