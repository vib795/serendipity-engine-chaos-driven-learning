"""initial schema

Revision ID: 001_initial
Revises:
Create Date: 2025-12-25 16:56:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create topics table
    op.create_table('topics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('source_id', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('full_content', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('source_url', sa.Text(), nullable=True),
        sa.Column('keywords', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_topics_created_at', 'topics', ['created_at'], unique=False)
    op.create_index('idx_topics_source', 'topics', ['source'], unique=False)
    op.create_index('idx_topics_source_id', 'topics', ['source', 'source_id'], unique=True)

    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('connections_generated', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('favorites_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create connections table
    op.create_table('connections',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('topic_a_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('topic_b_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('connection_title', sa.String(length=500), nullable=False),
        sa.Column('connection_summary', sa.Text(), nullable=False),
        sa.Column('connection_detailed', sa.Text(), nullable=False),
        sa.Column('connection_type', sa.String(length=50), nullable=True),
        sa.Column('bridge_concepts', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('creativity_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('plausibility_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('favorite_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('share_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('model_used', sa.String(length=50), nullable=True),
        sa.Column('generation_time_ms', sa.Integer(), nullable=True),
        sa.Column('prompt_tokens', sa.Integer(), nullable=True),
        sa.Column('completion_tokens', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['topic_a_id'], ['topics.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['topic_b_id'], ['topics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_connections_created_at', 'connections', ['created_at'], unique=False)
    op.create_index('idx_connections_favorite_count', 'connections', ['favorite_count'], unique=False)
    op.create_index('idx_connections_topics', 'connections', ['topic_a_id', 'topic_b_id'], unique=True)

    # Create favorites table
    op.create_table('favorites',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('connection_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['connection_id'], ['connections.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_favorites_unique', 'favorites', ['user_id', 'connection_id'], unique=True)
    op.create_index('idx_favorites_user', 'favorites', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_favorites_user', table_name='favorites')
    op.drop_index('idx_favorites_unique', table_name='favorites')
    op.drop_table('favorites')

    op.drop_index('idx_connections_topics', table_name='connections')
    op.drop_index('idx_connections_favorite_count', table_name='connections')
    op.drop_index('idx_connections_created_at', table_name='connections')
    op.drop_table('connections')

    op.drop_table('users')

    op.drop_index('idx_topics_source_id', table_name='topics')
    op.drop_index('idx_topics_source', table_name='topics')
    op.drop_index('idx_topics_created_at', table_name='topics')
    op.drop_table('topics')
