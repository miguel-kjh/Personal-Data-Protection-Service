"""new schema

Revision ID: 5d335c3f1af0
Revises: 
Create Date: 2019-12-21 18:33:26.406337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d335c3f1af0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fileLog',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('folder', sa.String(length=255), nullable=False),
    sa.Column('isDelete', sa.Boolean(), nullable=False),
    sa.Column('filetype', sa.String(length=255), nullable=False),
    sa.Column('publicId', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('publicId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fileLog')
    # ### end Alembic commands ###
