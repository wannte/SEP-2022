"""cascade

Revision ID: 9edd6354c302
Revises: cf12e3d1bb39
Create Date: 2022-05-20 10:24:18.615695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9edd6354c302'
down_revision = 'cf12e3d1bb39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('learneds')
    op.create_table('learneds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('lecture_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lectures.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
    sa.Column('custom_lecture_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learneds_id'), 'learneds', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
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
    # ### end Alembic commands ###
