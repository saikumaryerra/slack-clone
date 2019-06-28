"""channel table

Revision ID: 6efc50572a1c
Revises: ee06412d8b86
Create Date: 2019-06-25 10:59:01.527530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6efc50572a1c'
down_revision = 'ee06412d8b86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channel_messages_timestamp'), 'channel_messages', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_channel_messages_timestamp'), table_name='channel_messages')
    op.drop_table('channel_messages')
    op.drop_table('channel_members')
    # ### end Alembic commands ###
