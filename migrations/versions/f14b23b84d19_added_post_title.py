"""added post title

Revision ID: f14b23b84d19
Revises: e386ff5d450d
Create Date: 2021-02-28 13:37:56.210729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f14b23b84d19'
down_revision = 'e386ff5d450d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('title', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_post_title'), 'post', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_title'), table_name='post')
    op.drop_column('post', 'title')
    # ### end Alembic commands ###