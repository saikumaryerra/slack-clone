from app import db,login
from app.search import add_to_index, remove_from_index, query_index
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash,check_password_hash

class SearchableMixin(object):
    @classmethod
    def search (cls,expression,page,per_page):
        ids,total = query_index(cls.__tablename__,expression,page,per_page)
        if total==0:
            return cls.query.filter_by(id=0),0
        when = []
        for i in range(len(ids)):
            when.append((ids[i],i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when,value=cls.id)),total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique = True)
    email = db.Column(db.String(120),index=True)
    password_hash =  db.Column(db.String(128))
    last_seen=db.Column(db.DateTime,default=datetime.utcnow)
    channels = db.relationship('Channel',backref='admin',passive_deletes=True,lazy='dynamic')
    messages = db.relationship('ChannelMessages',backref='message_author',passive_deletes=True,lazy='dynamic')
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def avatar(self,size):
        digest=md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

    def __repr__(self):
        return '<user {}'.format(self.username)

class Channel(SearchableMixin,db.Model):
    __searchable__=['channelname']
    id=db.Column(db.Integer,primary_key=True)
    channelname=db.Column(db.String(64),index=True,unique = True)
    admin_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    channelmessages = db.relationship('ChannelMessages',passive_deletes=True,backref = 'channel',cascade="all, delete, delete-orphan",lazy='dynamic')

    def __repr__(self):
        return '<channel {}'.format(self.id)

class ChannelMessages(SearchableMixin,db.Model):
    __searchable__=['body']
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    channel_id = db.Column(db.Integer,db.ForeignKey('channel.id',ondelete='CASCADE'))
    sender_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))