"""Add notifications

Revision ID: f0c2178416d4
Revises: 51049344216f
Create Date: 2021-03-30 18:00:50.629887

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f0c2178416d4"
down_revision = "51049344216f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("subscription_id", sa.Integer(), nullable=True),
        sa.Column("information", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subscription_id"],
            ["subscriptions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("notifications")
