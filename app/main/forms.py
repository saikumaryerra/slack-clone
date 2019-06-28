from app.models import Channel
from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField
from wtforms.validators import ValidationError,DataRequired
from flask import request


class ChannelForm(FlaskForm):
    channelname = StringField('ChannelName',validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_channelname(self,channelname):
        channel = Channel.query.filter_by(channelname=channelname.data).first()
        if channel is not None:
            raise ValidationError('choose another channel name')
class ChatForm(FlaskForm):
    message = StringField('Message',validators=[DataRequired()])
    submit = SubmitField('send')

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)