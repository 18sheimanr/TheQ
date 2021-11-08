"""empty message

Revision ID: d9cae427537d
Revises: 25b0ade915bb
Create Date: 2020-12-09 22:42:13.651992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9cae427537d'
down_revision = '25b0ade915bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'meme', ['name'])
    op.add_column('user', sa.Column('joinDate', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'joinDate')
    op.drop_constraint(None, 'meme', type_='unique')
    # ### end Alembic commands ###