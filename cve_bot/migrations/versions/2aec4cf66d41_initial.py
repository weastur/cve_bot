"""Initial

Revision ID: 2aec4cf66d41
Revises:
Create Date: 2021-03-29 15:40:33.103343

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2aec4cf66d41"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "cve",
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("scope", sa.String(length=64), nullable=False),
        sa.Column("debianbug", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "packages", sa.Column("name", sa.String(length=64), nullable=False), sa.PrimaryKeyConstraint("name")
    )
    op.create_table(
        "package_cve",
        sa.Column("package_name", sa.String(), nullable=False),
        sa.Column("cve_name", sa.String(), nullable=False),
        sa.Column("sid_status", sa.String(length=32), nullable=False),
        sa.Column("sid_urgency", sa.String(length=64), nullable=False),
        sa.Column("sid_fixed_version", sa.String(length=64), nullable=False),
        sa.Column("bullseye_status", sa.String(length=32), nullable=False),
        sa.Column("bullseye_urgency", sa.String(length=64), nullable=False),
        sa.Column("bullseye_fixed_version", sa.String(length=64), nullable=False),
        sa.Column("buster_status", sa.String(length=32), nullable=False),
        sa.Column("buster_urgency", sa.String(length=64), nullable=False),
        sa.Column("buster_fixed_version", sa.String(length=64), nullable=False),
        sa.Column("stretch_status", sa.String(length=32), nullable=False),
        sa.Column("stretch_urgency", sa.String(length=64), nullable=False),
        sa.Column("stretch_fixed_version", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["cve_name"], ["cve.name"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["package_name"], ["packages.name"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("package_name", "cve_name"),
    )


def downgrade():
    op.drop_table("package_cve")
    op.drop_table("packages")
    op.drop_table("cve")
