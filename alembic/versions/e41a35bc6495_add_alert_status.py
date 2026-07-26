"""add alert status

Revision ID: e41a35bc6495
Revises: 899a27747f51
Create Date: 2026-07-24 14:31:03.498418
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e41a35bc6495"
down_revision: Union[str, Sequence[str], None] = "899a27747f51"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add column with default value so existing rows are updated
    op.add_column(
        "alerts",
        sa.Column(
            "status",
            sa.String(),
            nullable=False,
            server_default="ACTIVE",
        ),
    )

    # Optional: remove server default if you want the application
    # to explicitly set status for future inserts.
    op.alter_column(
        "alerts",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("alerts", "status")