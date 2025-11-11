"""add_unique_constraint_author_name

Revision ID: c29f02399724
Revises: a7e8d67af3c8
Create Date: 2025-11-02 17:52:22.130570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c29f02399724'
down_revision: Union[str, Sequence[str], None] = 'a7e8d67af3c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("uq_books_author_name", "books", ["author", "name"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_books_author_name", "books", type_="unique")
