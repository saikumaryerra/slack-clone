#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

#install python3
sudo apt-get install python3

#pip
sudo apt-get install python3-pip python3-setuptools
sudo apt-get install libpq-dev python-dev
sudo apt-get install python3-venv

#postgres
sudo apt install postgresql postgresql-contrib

#db creation...note :set password manually
sudo -u postgres psql -c "create database slack_clone;"

#creating  and activating venv vating
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
flask db init
flask db migrate
flask db upgrade

# install redis ans start server
sudo apt-get install redis
redis-server

# create slack.service
sudo touch /etc/systemd/system/slack.service
sudo bash -c 'cat > /etc/systemd/system/slack.service <<EOF
[Unit]
Description=starting slack service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn slack_clone:app -b 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
EOF'

#create celery worker
sudo touch /etc/systemd/system/celery-worker.service
sudo bash -c 'cat > /etc/systemd/system/celery-worker.service <<EOF
[Unit]
Description=celery instance to serve slack
After=network.target

[Service]
User=ubuntu
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/celery -A app.main.tasks worker --loglevel=info

[Install]
WantedBy=multi-user.target
EOF'

sudo apt install nginx
# create nginx conf
sudo touch /etc/nginx/sites-available/slack.conf
sudo bash -c 'cat>/etc/nginx/sites-available/slack.conf <<EOF
server {
    listen 80;

    location / {
        include proxy_params;
        proxy_pass http://localhost:8000;
    }
}

EOF'
sudo systemctl daemon-reload

sudo systemctl restart redis-server.service

sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/slack.conf /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/slack.conf /etc/nginx/sites-enabled/

sudo systemctl enable slack.service 
sudo systemctl restart slack.service

sudo systemctl enable celery-worker.service
sudo systemctl restart celery-worker.service

sudo systemctl enable nginx
sudo systemctl restart nginx
