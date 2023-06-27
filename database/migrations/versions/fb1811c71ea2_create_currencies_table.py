"""create_currencies_table

Revision ID: fb1811c71ea2
Revises: 9c5a3e031784
Create Date: 2023-06-25 21:52:27.803304

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fb1811c71ea2'
down_revision = '9c5a3e031784'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'currencies',
        sa.Column('currency_idx', sa.UUID(), nullable=False, server_default=sa.sql.expression.func.gen_random_uuid()),
        sa.Column('ticker', sa.String(length=8), nullable=False, unique=True),
        sa.Column('index_price_name', sa.String(length=32), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('currency_idx')
    )
    op.add_column('pricestamps', sa.Column('currency_idx', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'pricestamps', 'currencies', ['currency_idx'], ['currency_idx'], ondelete='CASCADE')
    op.drop_column('pricestamps', 'ticker')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'pricestamps',
        sa.Column(
            'ticker',
            sa.String(length=8),
            autoincrement=False,
            nullable=False,
            server_default='DEF'
        )
    )
    # op.drop_constraint(None, 'pricestamps', type_='foreignkey')
    op.drop_column('pricestamps', 'currency_idx')
    op.drop_table('currencies')
    # ### end Alembic commands ###
