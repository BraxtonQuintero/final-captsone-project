from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
# from app import models
from app.forms import MatchForm, SignUpForm, LogInForm, SearchForm
from app.models import User, Matches

@app.route("/")
def index():
    myUser = User.query.all()
    return render_template('index.html', myUser=myUser)

@app.route("/signup", methods= ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray our form submitted!')
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User(email=email, username=username, password=password)

        login_user(new_user)

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

@app.route("/account/user_id", methods= ["GET"])
@login_required
def account():
    email = User.email
    username = User.username

    account = User.query.filter_by(username=username, email=email)

    return render_template('account.html', account=account)

@app.route("/account/user_id", methods= ["GET"])
@login_required
def profile():
    email = User.email
    username = User.username

    profile = User.query.filter_by(username=username, email=email)

    return render_template('profile.html', profile=profile)

@app.route("/match", methods= ["GET", "POST"])
@login_required
def match():
    form = MatchForm()
    if form.validate_on_submit():
        maps = form.maps.data
        modes = form.modes.data

        new_match = Matches(maps=maps, modes=modes)

        print(new_match)
        return redirect(url_for('eights'))

    return render_template('match.html', form=form)

@app.route("/teamates", methods= ["GET"])
@login_required
def teamates():
    email = User.email
    username = User.username

    account = User.query.filter_by(username=username, email=email)

    return render_template('teamates.html', account=account)

@app.route("/eights", methods= ["GET", "POST"])
@login_required
def eights():
    maps = Matches.maps
    modes = Matches.modes

    match = Matches.query.filter_by(maps=maps, modes=modes)

    return render_template('eights.html', match=match)

@app.route('/search', methods=['POST'])
@login_required
def search():
  form = SearchForm()
  if not form.validate_on_submit():
    return redirect(url_for('teamates'))
  return redirect((url_for('search_results', query=form.search.data)))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
  results = User.query.whoosh_search(query).all()
  return render_template('search_results.html', query=query, results=results)