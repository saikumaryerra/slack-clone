from app import db
from app.main.forms import ChannelForm,ChatForm
from app.main import bp
from app.main.forms import SearchForm
from app.models import Channel,ChannelMessages
from datetime import datetime
from flask import current_app,flash,redirect,render_template,url_for,request, json,g
from flask_login import login_required,current_user
from werkzeug.urls import url_parse


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
    if form.validate_on_submit():
        message = ChannelMessages(body=form.message.data,message_author=current_user,channel_id=channelid)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('main.chat',channelid=channelid))
    messages = ChannelMessages.query.filter_by(channel_id=channelid).order_by(ChannelMessages.timestamp)
    return render_template('chat.html',messages=messages,form=form)

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