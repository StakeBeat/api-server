import os

from flask import Flask
from flask_cors import CORS

from app.services.jwt import authenticate, identity, JWT

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

JWT(app, authenticate, identity)
