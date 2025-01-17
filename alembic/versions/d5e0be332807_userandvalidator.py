"""UserAndValidator

Revision ID: d5e0be332807
Revises: 
Create Date: 2020-12-06 09:45:30.829552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5e0be332807'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=123), nullable=False),
    sa.Column('password', sa.String(length=123), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('validators',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indice', sa.String(length=16), nullable=False),
    sa.Column('pubkey', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_validators_indice'), 'validators', ['indice'], unique=False)
    op.create_index(op.f('ix_validators_pubkey'), 'validators', ['pubkey'], unique=False)
    op.create_index(op.f('ix_validators_user_id'), 'validators', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_validators_user_id'), table_name='validators')
    op.drop_index(op.f('ix_validators_pubkey'), table_name='validators')
    op.drop_index(op.f('ix_validators_indice'), table_name='validators')
    op.drop_table('validators')
    op.drop_table('users')
    # ### end Alembic commands ###
