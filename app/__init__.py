import os
from flask import Flask, json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# login = LoginManager(app)

def get_posts():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "posts.json")
    data = json.load(open(json_url))
    return data

users = [
    {
        "id": 1,
        "username": "lisa",
        "password": "lisa",
        "email": "lisa@test.com"
    },
    {
        "id": 2,
        "username": "frank",
        "password": "frank",
        "email": "frank@test.com"
    },
    {
        "id": 3,
        "username": "raj",
        "password": "raj",
        "email": "raj@test.com"
    },
    {
        "id": 4,
        "username": "pri",
        "password": "pri",
        "email": "pri@test.com"
    }
]
posts = get_posts()

from app import routes