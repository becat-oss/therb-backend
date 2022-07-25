"""empty message

Revision ID: c81afc09c4a5
Revises: 0a4c0d39c34c
Create Date: 2022-07-25 16:25:12.570579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c81afc09c4a5'
down_revision = '0a4c0d39c34c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'material', 'construction', ['constructionId'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'material', type_='foreignkey')
    # ### end Alembic commands ###
