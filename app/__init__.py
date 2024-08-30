import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, session
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import identity.web
from config import Config
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
auth = identity.web.Auth(
    session=session,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/blog_app.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

# def get_posts():
#     SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
#     json_url = os.path.join(SITE_ROOT, "static/data", "posts.json")
#     data = json.load(open(json_url))
#     return data

# users = [
#     {
#         "id": 1,
#         "username": "lisa",
#         "password": "lisa",
#         "email": "lisa@test.com",
#         "avatar": "/static/default.jpg",
#         "about_me": "I am lisa",
#         "last_seen": "2024-08-16 02:28:30"
#     },
#     {
#         "id": 2,
#         "username": "frank",
#         "password": "frank",
#         "email": "frank@test.com",
#         "avatar": "/static/default.jpg",
#         "about_me": "I am frank",
#         "last_seen": "2024-08-16 02:28:30"
#     },
#     {
#         "id": 3,
#         "username": "raj",
#         "password": "raj",
#         "email": "raj@test.com",
#         "avatar": "/static/default.jpg",
#         "about_me": "I am raj",
#         "last_seen": "2024-08-22 02:28:30"
#     },
#     {
#         "id": 4,
#         "username": "pri",
#         "password": "pri",
#         "email": "pri@test.com",
#         "avatar": "/static/default.jpg",
#         "about_me": "I am pri",
#         "last_seen": "2024-08-23 02:28:30"
#     }
# ]
# posts = get_posts()

from app import routes,models,errors