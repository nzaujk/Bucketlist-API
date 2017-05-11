"""empty message

Revision ID: 50adba61c30e
Revises: 288f6574e3c0
Create Date: 2017-05-10 22:24:31.131597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50adba61c30e'
down_revision = '288f6574e3c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=128), nullable=True))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###