"""add surveys

Revision ID: 985a21799199
Revises: 38b971a6e41f
Create Date: 2025-03-25 10:49:15.899311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '985a21799199'
down_revision: Union[str, None] = '38b971a6e41f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('surveys',
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('slug', sa.String(length=50), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('questions',
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('survey_results',
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('min_point', sa.Integer(), nullable=False),
    sa.Column('max_point', sa.Integer(), nullable=False),
    sa.Column('text_result', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_points',
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('options',
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('bot_commands', 'in_main_menu')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bot_commands', sa.Column('in_main_menu', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_table('options')
    op.drop_table('user_points')
    op.drop_table('survey_results')
    op.drop_table('questions')
    op.drop_table('surveys')
    # ### end Alembic commands ###
