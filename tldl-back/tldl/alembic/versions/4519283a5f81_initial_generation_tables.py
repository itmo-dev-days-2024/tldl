"""initial generation tables

Revision ID: 4519283a5f81
Revises: 
Create Date: 2024-11-06 13:43:44.542197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4519283a5f81'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video_processing',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('created', 'cleaned', 'notified', name='videostatus'), nullable=False),
    sa.Column('chat_id', sa.String(), nullable=False),
    sa.Column('msg_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('finished_at', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
    sa.Column('raw_file_path', sa.String(), nullable=False),
    sa.Column('ready_file_path', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video_processing')
    # ### end Alembic commands ###
