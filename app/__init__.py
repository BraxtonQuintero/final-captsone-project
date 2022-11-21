from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from config import Config
from cod_api import API

app = Flask(__name__)

api = API()
api.login('MzEyNjA0MTUyNjM5ODQzOTk0OToxNjcwMjY3Njk1NzA2Ojc0Yjg2OTcwNzA4ZmRjMzA5ZWQ3MGRjMjkxN2M3NDJk')

app.config.from_object(Config)

db=SQLAlchemy(app)

migrate=Migrate(app,db)

login = LoginManager(app)

login.login_view = 'login'

from . import routes