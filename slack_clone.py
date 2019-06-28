from app import create_app,db
from app.models import User,Channel,ChannelMessages
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Channel':Channel,'ChannelMessages':ChannelMessages}