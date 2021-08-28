"""subs

Revision ID: 432792f39072
Revises: a2a7ce8c0800
Create Date: 2021-08-19 00:18:20.969735

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "432792f39072"
down_revision = "a2a7ce8c0800"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password", sa.String(length=32), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("is_banned", sa.String(length=8), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
