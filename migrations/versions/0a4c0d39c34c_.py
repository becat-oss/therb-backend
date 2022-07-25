"""empty message

Revision ID: 0a4c0d39c34c
Revises: 0c2a0a34cb95
Create Date: 2022-07-25 16:22:33.811480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a4c0d39c34c'
down_revision = '0c2a0a34cb95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('material', sa.Column('constructionId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'material', 'construction', ['constructionId'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'material', type_='foreignkey')
    op.drop_column('material', 'constructionId')
    # ### end Alembic commands ###
