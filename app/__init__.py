from config import Config
from flask import Flask,current_app
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from elasticsearch import Elasticsearch
from celery import Celery
from flask_bootstrap import Bootstrap

db =SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message='login required'
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL,backend=Config.CELERY_BACKEND_URL)

def create_app(config_class=Config):
    chat_app=Flask(__name__)
    chat_app.config.from_object(Config)

    celery.conf.update(chat_app.config)

    db.init_app(chat_app)
    migrate.init_app(chat_app,db)
    login.init_app(chat_app,db)
    # bootstrap = Bootstrap(chat_app)   

    chat_app.elasticsearch = Elasticsearch([chat_app.config['ELASTICSEARCH_URL']]) \
        if chat_app.config['ELASTICSEARCH_URL'] else None

    from app.errors import bp as errors_bp
    chat_app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    chat_app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    chat_app.register_blueprint(main_bp)

    return chat_app
from app import models