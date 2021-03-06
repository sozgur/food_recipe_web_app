"""update column on user

Revision ID: 877c28f2f2ed
Revises: ce5ecd91638c
Create Date: 2021-11-11 23:52:56.842132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '877c28f2f2ed'
down_revision = 'ce5ecd91638c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipebookentities')
    op.drop_table('recipebooks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipebooks',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('recipebooks_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='recipebooks_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='recipebooks_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('recipebookentities',
    sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['recipebooks.id'], name='recipebookentities_book_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], name='recipebookentities_recipe_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('book_id', 'recipe_id', name='recipebookentities_pkey')
    )
    # ### end Alembic commands ###
