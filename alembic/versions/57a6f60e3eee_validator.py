"""Validator

Revision ID: 57a6f60e3eee
Revises: 6e73bc897016
Create Date: 2020-12-01 15:49:10.814900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57a6f60e3eee'
down_revision = '6e73bc897016'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('validators',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indice', sa.String(length=16), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_validators_indice'), 'validators', ['indice'], unique=False)
    op.create_index(op.f('ix_validators_user_id'), 'validators', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_validators_user_id'), table_name='validators')
    op.drop_index(op.f('ix_validators_indice'), table_name='validators')
    op.drop_table('validators')
    # ### end Alembic commands ###