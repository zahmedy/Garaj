"""create lead table

Revision ID: a1b2c3d4e5f6
Revises: 84d1654a1402
Create Date: 2026-03-07 13:40:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "84d1654a1402"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "lead" in inspector.get_table_names():
        return

    op.create_table(
        "lead",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("car_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("buyer_user_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("phone_e164", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=True),
        sa.Column("channel", sa.String(), nullable=False, server_default="form"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["car_id"], ["carlisting.id"], name=op.f("lead_car_id_fkey")),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"], name=op.f("lead_owner_id_fkey")),
        sa.ForeignKeyConstraint(["buyer_user_id"], ["user.id"], name=op.f("lead_buyer_user_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("lead_pkey")),
    )
    op.create_index(op.f("ix_lead_car_id"), "lead", ["car_id"], unique=False)
    op.create_index(op.f("ix_lead_owner_id"), "lead", ["owner_id"], unique=False)
    op.create_index(op.f("ix_lead_buyer_user_id"), "lead", ["buyer_user_id"], unique=False)
    op.create_index(op.f("ix_lead_phone_e164"), "lead", ["phone_e164"], unique=False)
    op.create_index(op.f("ix_lead_channel"), "lead", ["channel"], unique=False)
    op.create_index(op.f("ix_lead_created_at"), "lead", ["created_at"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "lead" not in inspector.get_table_names():
        return

    op.drop_index(op.f("ix_lead_created_at"), table_name="lead")
    op.drop_index(op.f("ix_lead_channel"), table_name="lead")
    op.drop_index(op.f("ix_lead_phone_e164"), table_name="lead")
    op.drop_index(op.f("ix_lead_buyer_user_id"), table_name="lead")
    op.drop_index(op.f("ix_lead_owner_id"), table_name="lead")
    op.drop_index(op.f("ix_lead_car_id"), table_name="lead")
    op.drop_table("lead")
