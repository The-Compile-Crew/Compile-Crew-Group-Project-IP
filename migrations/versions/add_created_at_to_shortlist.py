"""
Revision ID: add_created_at_to_shortlist
Revises: 
Create Date: 2025-12-04

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('shortlist', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))

def downgrade():
    op.drop_column('shortlist', 'created_at')
