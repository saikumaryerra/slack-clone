import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.flaskenv'))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.environ.get('POSTGRES_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # or 'http://localhost:9200'
    CELERY_BROKER_URL='redis://localhost:6379/0'
    CELERY_BACKEND_URL='redis://localhost:6379/0'
    # CELERY_BROKER_URL=os.environ.get('CELERY_BROKER_URL')
    # CELERY_BACKEND_URL=os.environ.get('CELERY_BACKEND_URL')
    MESSAGES_PER_PAGE=os.environ.get('MESSAGES_PER_PAGE')
