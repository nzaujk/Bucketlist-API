from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['parent'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)






