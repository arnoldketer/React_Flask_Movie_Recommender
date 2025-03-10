"""Initial migration

Revision ID: ab831f897fa2
Revises: 
Create Date: 2024-11-30 12:51:14.722886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab831f897fa2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userId', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint('uq_user_userId', ['userId'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('userId')

    # ### end Alembic commands ###
