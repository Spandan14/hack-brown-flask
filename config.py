import os
from dotenv import load_dotenv, find_dotenv

# this looks for a .env file in the directory and loads it up
load_dotenv(find_dotenv())

# this loads up the base directory of our project
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False