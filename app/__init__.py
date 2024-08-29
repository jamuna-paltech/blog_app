import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

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

from app import routes,models