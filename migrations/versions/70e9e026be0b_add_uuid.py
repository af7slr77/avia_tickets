"""add 'uuid'

Revision ID: 70e9e026be0b
Revises: 20a8b9af7589
Create Date: 2023-12-22 14:21:22.955246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70e9e026be0b'
down_revision: Union[str, None] = '20a8b9af7589'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
