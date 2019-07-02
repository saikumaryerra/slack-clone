import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL') or 'postgresql://postgres:test123@localhost/slack_clone'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    
    CELERY_BROKER_URL='redis://localhost:6379/0'
    CELERY_BACKEND_URL='redis://localhost:6379/0'