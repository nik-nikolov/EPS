from app import app, db
from app.models import User
from flask import request

user0 = User.query.filter_by(user=username).all()
user0