from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfkhksdfs35r49edfbjksfk32v3'

# Configuration for MySQL database
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'


# Initialize SQLAlchemy
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# Initialize Flask-Login's LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from magnus import routes
