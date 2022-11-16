from flask import render_template, redirect, url_for, flash
# from flask_login import login_user, logout_user, current_user, login_required
from app import app
# from app.forms import SignUpForm, LogInForm, PostForm
# from app.models import User, Post

@app.route("/")
def index():
    return render_template('base.html')