"""dynamic Read More text

Revision ID: 10a9db7d27fc
Revises: 843580d5087e
Create Date: 2021-03-20 06:15:52.712060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10a9db7d27fc'
down_revision = '843580d5087e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('read_more_text', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'read_more_text')
    # ### end Alembic commands ###
