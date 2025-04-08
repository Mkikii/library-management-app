"""initial migration

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2023-10-15 10:00:00.000000

"""
from alembic import op


def upgrade():
    # Create tables with proper indexes
    op.create_index('idx_member_email', 'member', ['email'])
    op.create_index('idx_transaction_dates_combined', 'transaction',
                    ['issue_date', 'return_date', 'member_id'])


def downgrade():
    op.drop_index('idx_member_email')
    op.drop_index('idx_transaction_dates_combined')
