"""post relationships

Revision ID: d4bc0e5fdbbd
Revises: f14b23b84d19
Create Date: 2021-03-02 06:19:06.459560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4bc0e5fdbbd'
down_revision = 'f14b23b84d19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_rel',
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('child_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['post.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_rel')
    # ### end Alembic commands ###
