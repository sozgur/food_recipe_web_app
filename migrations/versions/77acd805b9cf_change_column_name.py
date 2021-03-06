"""change column name

Revision ID: 77acd805b9cf
Revises: e4ca7221d608
Create Date: 2021-11-05 01:55:35.315673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77acd805b9cf'
down_revision = 'e4ca7221d608'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipes', sa.Column('directions', sa.Text(), nullable=False))
    op.drop_column('recipes', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipes', sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('recipes', 'directions')
    # ### end Alembic commands ###
