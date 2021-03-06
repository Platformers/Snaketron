"""empty message

Revision ID: 1fff491841c6
Revises: 830f0a68df9d
Create Date: 2016-09-28 09:46:49.038098

"""

# revision identifiers, used by Alembic.
revision = '1fff491841c6'
down_revision = '830f0a68df9d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('idea_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idea_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['idea_id'], ['idea.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('first_name', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_table('idea_comment')
    ### end Alembic commands ###
