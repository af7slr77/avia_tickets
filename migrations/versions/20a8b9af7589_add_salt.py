"""add 'salt'

Revision ID: 20a8b9af7589
Revises: 296a5464eed2
Create Date: 2023-12-21 20:23:45.602429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20a8b9af7589'
down_revision: Union[str, None] = '296a5464eed2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('salt', sa.String(length=29), nullable=False))
    op.drop_constraint('user_password_key', 'user', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_password_key', 'user', ['password'])
    op.drop_column('user', 'salt')
    # ### end Alembic commands ###
