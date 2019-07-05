FLASK_APP=slack_clone.py
FLASK_DEBUG=True
ELASTICSEARCH_URL=http://localhost:9200
POSTGRES_URL=postgresql://postgres:test123@localhost/slack_clone
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_BACKEND_URL=redis://localhost:6379/0
SECRET_KEY = you-will-never-guess
MESSAGES_PER_PAGE=7