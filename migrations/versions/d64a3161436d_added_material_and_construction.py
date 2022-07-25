"""added material and construction

Revision ID: d64a3161436d
Revises: 8c63c7cd3247
Create Date: 2022-07-22 13:45:48.672249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd64a3161436d'
down_revision = '8c63c7cd3247'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('construction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('material',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('conductivity', sa.Float(), nullable=False),
    sa.Column('specificHeat', sa.Float(), nullable=False),
    sa.Column('density', sa.Float(), nullable=False),
    sa.Column('moistureConductivity', sa.Float(), nullable=False),
    sa.Column('moistureCapacity', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('material')
    op.drop_table('construction')
    # ### end Alembic commands ###
