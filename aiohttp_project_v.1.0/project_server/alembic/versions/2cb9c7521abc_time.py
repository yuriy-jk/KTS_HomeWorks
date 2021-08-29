"""time

Revision ID: 2cb9c7521abc
Revises: d8c2036ee771
Create Date: 2021-08-26 19:19:31.476229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2cb9c7521abc"
down_revision = "d8c2036ee771"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("subscriptions", sa.Column("schedule", sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("subscriptions", "schedule")
    # ### end Alembic commands ###