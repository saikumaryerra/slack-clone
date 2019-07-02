from app import db
from app.main.forms import ChannelForm,ChatForm
from app.main import bp,tasks
from app.main.forms import SearchForm
from app.models import Channel,ChannelMessages
from datetime import datetime
from flask import current_app,flash,redirect,render_template,url_for,request, json,g,jsonify,render_template_string,send_file
from flask_login import login_required,current_user
from werkzeug.urls import url_parse
from sqlalchemy import and_


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    # g.locale = str(get_locale())

@bp.route('/index',methods=['GET','POST'])
@bp.route('/',methods=['GET','POST'])
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form=ChannelForm()
    if form.validate_on_submit():
        channel=Channel(channelname=form.channelname.data,admin=current_user)
        db.session.add(channel)
        db.session.commit()
        flash('congratulations, channel created')
        return redirect(url_for('main.index'))
    channels=Channel.query.order_by(Channel.id)
   
    return render_template('index.html',title='index',form=form,channels=channels)

@bp.route('/profile/')
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('profile'))
    channels = Channel.query.filter_by(admin_id=current_user.id)
    return render_template('profile.html',title='profile',channels=channels)

# @bp.route('/delete-channel/<admin_id>/<channel_id>')
# @login_required
# def delete_channel(channel_id,admin_id):
#     print(current_user.id)
#     print(admin_id)
#     if not current_user.is_authenticated:
#         return redirect(url_for('auth.login'))
#     if current_user.id==admin_id:
#         flash('cannot delete channel')
#         return redirect(url_for('main.profile'))
#     d = ChannelMessages.query.filter_by(channel_id=channel_id)
#     db.session.delete(d)
#     db.session.commit()
#     return redirect(url_for('main.profile'))

@bp.route('/chat/<channelid>',methods=['GET','POST'])
@login_required
def chat(channelid):
    form=ChatForm()
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    c=Channel.query.filter_by(id=channelid).first_or_404()
    msg_body = request.get_json()
    if msg_body:
        message = ChannelMessages(body=msg_body['message'],message_author=current_user,channel_id=channelid)
        db.session.add(message)
        db.session.commit()  
        response = {
            'message':msg_body['message'],
        } 
        return jsonify(response)            
    return render_template('chat.html',form=form,channelid=channelid)

max_message_id=0
@bp.route("/_sendMessages/<channelid>",methods=['GET'])
@login_required
def sendMessagesList(channelid):
    messages=ChannelMessages.query.filter(and_(ChannelMessages.id > max_message_id,ChannelMessages.channel_id==channelid)  ).order_by(ChannelMessages.timestamp).all()
    renderedHtml=getHtml(messages)
    return renderedHtml

def getHtml(messages):
    text='''{% for message in messages%}
                    <p>{{ message.sender_id }}</p>
                    <p>{{message.body}}|{{message.timestamp}}</p>
                {% endfor %}
        '''
    return render_template_string(text, messages=messages)

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    channels, total = Channel.search(g.search_form.q.data,1,10)
    print(total)
    if total ==1:
        return redirect(url_for('main.chat',channelid=channels.first().id))
    elif total==0:
        return redirect(url_for('main.index'))
    return render_template('search.html',channels=channels,title='search')    

@bp.route('/download',methods=['GET','POST'])
@login_required
def download():

    task=tasks.download_background.apply_async((current_user.id,))
    return jsonify({}),{'url':url_for('main.task_check',task_id=task.id)}
    # download_data = { 
    #     'Name' : current_user.username,
    #     'Email' : current_user.email,
    # }
    # channels = current_user.channels.all()
    # channel = [channel.channelname for channel in channels]
    # download_data['channels'] = list(channel)
    # file = open('data.json','w') 
    # file.write(json.dumps(download_data)) 
    # file.close() 
    # return send_file('../data.json', attachment_filename='download.json',as_attachment=True)
@bp.route('/download_file')
def download_file():
    return send_file('../data.json', attachment_filename='download.json',as_attachment=True)

@bp.route('/download/check/<task_id>')
def task_check(task_id):
    task = tasks.download_background.AsyncResult(task_id)
    if task.state=='PENDING':
        response = {
            'current':0,
            'total':100,
            'state':task.state,
            'status':'task pending'
        }
    elif task.state=='FAILURE':
        response = {
            'current':0,
            'total':100,
            'state':task.state,
            'status':'task failed'
        }
    elif task.state == 'PROGRESS' :
        response = {
            'current':50,
            'total':100,
            'state':task.state,
            'status':'task running'
        }
    else :
        response = {
            'current':100,
            'total':100,
            'state':task.state,
            'status':'task done'
        }
    return jsonify(response)