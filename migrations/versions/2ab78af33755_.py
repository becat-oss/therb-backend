"""empty message

Revision ID: 2ab78af33755
Revises: 
Create Date: 2022-09-11 10:32:56.256926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ab78af33755'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('construction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('thickness', sa.String(length=255), nullable=False),
    sa.Column('categories', sa.String(length=255), nullable=False),
    sa.Column('uvalue', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('dailySch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hvac', sa.String(length=255), nullable=False),
    sa.Column('cooling', sa.String(length=255), nullable=False),
    sa.Column('heating', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('envelope',
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
    sa.Column('classification', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('construction_material',
    sa.Column('constructionId', sa.Integer(), nullable=True),
    sa.Column('materialId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['constructionId'], ['construction.id'], ),
    sa.ForeignKeyConstraint(['materialId'], ['material.id'], )
    )
    op.create_table('exWallIdentifier',
    sa.Column('envelopeId', sa.Integer(), nullable=True),
    sa.Column('exWallId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envelopeId'], ['envelope.id'], ),
    sa.ForeignKeyConstraint(['exWallId'], ['construction.id'], )
    )
    op.create_table('floorCeilingIdentifier',
    sa.Column('envelopeId', sa.Integer(), nullable=True),
    sa.Column('floorCeilingId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envelopeId'], ['envelope.id'], ),
    sa.ForeignKeyConstraint(['floorCeilingId'], ['construction.id'], )
    )
    op.create_table('groundFloorIdentifier',
    sa.Column('envelopeId', sa.Integer(), nullable=True),
    sa.Column('groundFloorId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envelopeId'], ['envelope.id'], ),
    sa.ForeignKeyConstraint(['groundFloorId'], ['construction.id'], )
    )
    op.create_table('inWallIdentifier',
    sa.Column('envelopeId', sa.Integer(), nullable=True),
    sa.Column('inWallId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envelopeId'], ['envelope.id'], ),
    sa.ForeignKeyConstraint(['inWallId'], ['construction.id'], )
    )
    op.create_table('monthlySch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scheduleId', sa.Integer(), nullable=True),
    sa.Column('hvac', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['scheduleId'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roofIdentifier',
    sa.Column('envelopeId', sa.Integer(), nullable=True),
    sa.Column('roofId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envelopeId'], ['envelope.id'], ),
    sa.ForeignKeyConstraint(['roofId'], ['construction.id'], )
    )
    op.create_table('schedule_dailySch',
    sa.Column('scheduleId', sa.Integer(), nullable=True),
    sa.Column('dailyId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dailyId'], ['dailySch.id'], ),
    sa.ForeignKeyConstraint(['scheduleId'], ['schedule.id'], )
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('constructionId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['constructionId'], ['construction.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('weeklySch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scheduleId', sa.Integer(), nullable=True),
    sa.Column('hvac', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['scheduleId'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('windowIdentifier',
    sa.Column('envelopeId', sa.Integer(), nullable=True),
    sa.Column('windowId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envelopeId'], ['envelope.id'], ),
    sa.ForeignKeyConstraint(['windowId'], ['construction.id'], )
    )
    op.create_table('construction_tag',
    sa.Column('constructionId', sa.Integer(), nullable=True),
    sa.Column('tagId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['constructionId'], ['construction.id'], ),
    sa.ForeignKeyConstraint(['tagId'], ['tag.id'], )
    )
    op.create_table('schedule_tag',
    sa.Column('scheduleId', sa.Integer(), nullable=True),
    sa.Column('tagId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['scheduleId'], ['schedule.id'], ),
    sa.ForeignKeyConstraint(['tagId'], ['tag.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule_tag')
    op.drop_table('construction_tag')
    op.drop_table('windowIdentifier')
    op.drop_table('weeklySch')
    op.drop_table('tag')
    op.drop_table('schedule_dailySch')
    op.drop_table('roofIdentifier')
    op.drop_table('monthlySch')
    op.drop_table('inWallIdentifier')
    op.drop_table('groundFloorIdentifier')
    op.drop_table('floorCeilingIdentifier')
    op.drop_table('exWallIdentifier')
    op.drop_table('construction_material')
    op.drop_table('schedule')
    op.drop_table('material')
    op.drop_table('envelope')
    op.drop_table('dailySch')
    op.drop_table('construction')
    # ### end Alembic commands ###
