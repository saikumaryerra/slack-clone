from app import celery,db,create_app
from flask import json,jsonify,current_app
from app.models import User,Channel,ChannelMessages
import time
@celery.task(bind=True)
def download_background(self,current_id):
    app = create_app()
    db.create_all(app=create_app())
    with app.app_context():
        print('bg started')
        time.sleep(5)
        print('sleep done')
        user = User.query.filter_by(id=current_id).first()
        print(user.username)
        download_data = { 
            'Name' : user.username,
            'Email' : user.email,
        }
        print(download_data)
        channels = user.channels.all()
        channel = [channel.channelname for channel in channels]
        # print(list(channel))
        download_data['channels'] = list(channel)
        print(download_data)
        file = open('data.json','w') 
        file.write(json.dumps(download_data)) 
        file.close() 
        # return jsonify(download_data)
        return {'current':100,'total':100,'status':'task done'}
