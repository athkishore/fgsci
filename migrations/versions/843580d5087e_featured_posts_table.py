"""featured posts table

Revision ID: 843580d5087e
Revises: ad106249fbf4
Create Date: 2021-03-18 06:16:30.837091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843580d5087e'
down_revision = 'ad106249fbf4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('featured',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_featured_type'), 'featured', ['type'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_featured_type'), table_name='featured')
    op.drop_table('featured')
    # ### end Alembic commands ###
