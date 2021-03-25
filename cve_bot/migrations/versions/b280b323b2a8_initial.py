"""Initial

Revision ID: b280b323b2a8
Revises:
Create Date: 2021-03-24 16:32:12.094803

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b280b323b2a8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "packages",
        sa.Column("name", sa.String(64), primary_key=True, nullable=False),
    )
    op.create_table(
        "cve",
        sa.Column("name", sa.String(32), primary_key=True, nullable=False),
        sa.Column("description", sa.Text, nullable=False, default=""),
        sa.Column("scope", sa.String(64), nullable=False, default=""),
        sa.Column("debianbug", sa.Integer, nullable=True),
    )
    op.create_table(
        "package_cve",
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True, nullable=False),
        sa.Column("package_name", sa.String, sa.ForeignKey("packages.name", ondelete="cascade"), nullable=False),
        sa.Column("cve_name", sa.String, sa.ForeignKey("cve.name", ondelete="cascade"), nullable=False),
        sa.Column("sid_status", sa.String(32), nullable=False, default=""),
        sa.Column("sid_urgency", sa.String(64), nullable=False, default=""),
        sa.Column("sid_fixed_version", sa.String(64), nullable=False, default=""),
        sa.Column("bullseye_status", sa.String(32), nullable=False, default=""),
        sa.Column("bullseye_urgency", sa.String(64), nullable=False, default=""),
        sa.Column("bullseye_fixed_version", sa.String(64), nullable=False, default=""),
        sa.Column("buster_status", sa.String(32), nullable=False, default=""),
        sa.Column("buster_urgency", sa.String(64), nullable=False, default=""),
        sa.Column("buster_fixed_version", sa.String(64), nullable=False, default=""),
        sa.Column("stretch_status", sa.String(32), nullable=False, default=""),
        sa.Column("stretch_urgency", sa.String(64), nullable=False, default=""),
        sa.Column("stretch_fixed_version", sa.String(64), nullable=False, default=""),
    )


def downgrade():
    op.drop_table("package_cve")
    op.drop_table("packages")
    op.drop_table("cve")
