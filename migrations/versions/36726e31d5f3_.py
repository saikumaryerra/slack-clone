"""empty message

Revision ID: 36726e31d5f3
Revises: ccb12e3023ff
Create Date: 2019-07-05 09:52:04.831009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36726e31d5f3'
down_revision = 'ccb12e3023ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('channel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channelname', sa.String(length=64), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channel_channelname'), 'channel', ['channelname'], unique=True)
    op.create_table('channel_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channel_messages_timestamp'), 'channel_messages', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_channel_messages_timestamp'), table_name='channel_messages')
    op.drop_table('channel_messages')
    op.drop_index(op.f('ix_channel_channelname'), table_name='channel')
    op.drop_table('channel')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
