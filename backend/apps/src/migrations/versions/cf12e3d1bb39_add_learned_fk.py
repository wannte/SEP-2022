"""add learned fk

Revision ID: cf12e3d1bb39
Revises: b95dacb2669e
Create Date: 2022-05-13 10:32:22.576171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf12e3d1bb39'
down_revision = 'b95dacb2669e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('learneds')
    op.create_table('learneds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('lecture_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lectures.id']),
    sa.ForeignKeyConstraint(['student_id'], ['users.id']),
    sa.Column('custom_lecture_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learneds_id'), 'learneds', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'learneds', type_='foreignkey')
    op.drop_constraint(None, 'learneds', type_='foreignkey')
    op.drop_index(op.f('ix_learneds_id'), table_name='learneds')
    op.drop_table('learneds')
    op.create_table('learneds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('lecture_id', sa.Integer(), nullable=True),
    sa.Column('custom_lecture_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learneds_id'), 'learneds', ['id'], unique=False)
    # ### end Alembic commands ###
