"""Add subscriptions

Revision ID: 51049344216f
Revises: 2aec4cf66d41
Create Date: 2021-03-30 17:52:00.172399

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "51049344216f"
down_revision = "2aec4cf66d41"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_cve",
        sa.Column("cve_name", sa.Integer(), nullable=False),
        sa.Column("subscription_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cve_name"],
            ["cve.name"],
        ),
        sa.ForeignKeyConstraint(
            ["subscription_id"],
            ["subscriptions.id"],
        ),
        sa.PrimaryKeyConstraint("cve_name", "subscription_id"),
    )


def downgrade():
    op.drop_table("subscription_cve")
    op.drop_table("subscriptions")
