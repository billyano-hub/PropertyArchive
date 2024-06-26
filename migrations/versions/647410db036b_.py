"""empty message

Revision ID: 647410db036b
Revises: 
Create Date: 2024-03-01 11:45:20.998560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '647410db036b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_username', sa.String(length=20), nullable=True),
    sa.Column('admin_pwd', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('agent',
    sa.Column('agent_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('agent_fullname', sa.String(length=100), nullable=False),
    sa.Column('agent_email', sa.String(length=120), nullable=True),
    sa.Column('agent_pwd', sa.String(length=120), nullable=True),
    sa.Column('agent_pix', sa.String(length=120), nullable=True),
    sa.Column('agent_datereg', sa.DateTime(), nullable=True),
    sa.Column('agent_phoneno', sa.String(length=120), nullable=True),
    sa.Column('agent_no', sa.String(length=120), nullable=True),
    sa.Column('agent_location', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('agent_id')
    )
    op.create_table('category',
    sa.Column('cat_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cat_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('cat_id')
    )
    op.create_table('state',
    sa.Column('state_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('state_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('state_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_fullname', sa.String(length=100), nullable=False),
    sa.Column('user_email', sa.String(length=120), nullable=True),
    sa.Column('user_pwd', sa.String(length=120), nullable=True),
    sa.Column('user_pix', sa.String(length=120), nullable=True),
    sa.Column('user_datereg', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('lga',
    sa.Column('lga_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('lga_name', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['state.state_id'], ),
    sa.PrimaryKeyConstraint('lga_id')
    )
    op.create_table('property',
    sa.Column('property_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('property_title', sa.Text(), nullable=False),
    sa.Column('property_desc', sa.Text(), nullable=True),
    sa.Column('property_cover', sa.String(length=100), nullable=True),
    sa.Column('property_publication', sa.Date(), nullable=True),
    sa.Column('property_catid', sa.Integer(), nullable=False),
    sa.Column('property_status', sa.Enum('1', '0'), server_default='0', nullable=False),
    sa.Column('property_type', sa.Text(), nullable=False),
    sa.Column('property_beds', sa.String(length=10), nullable=True),
    sa.Column('property_baths', sa.String(length=10), nullable=True),
    sa.Column('property_garage', sa.String(length=10), nullable=True),
    sa.Column('property_location', sa.Text(), nullable=True),
    sa.Column('property_price', sa.String(length=120), nullable=True),
    sa.Column('property_agentid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['property_agentid'], ['agent.agent_id'], ),
    sa.ForeignKeyConstraint(['property_catid'], ['category.cat_id'], ),
    sa.PrimaryKeyConstraint('property_id')
    )
    op.create_table('reviews',
    sa.Column('rev_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rev_title', sa.String(length=255), nullable=False),
    sa.Column('rev_text', sa.String(length=255), nullable=False),
    sa.Column('rev_date', sa.DateTime(), nullable=True),
    sa.Column('rev_userid', sa.Integer(), nullable=True),
    sa.Column('rev_agentid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['rev_agentid'], ['agent.agent_id'], ),
    sa.ForeignKeyConstraint(['rev_userid'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('rev_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('property')
    op.drop_table('lga')
    op.drop_table('user')
    op.drop_table('state')
    op.drop_table('category')
    op.drop_table('agent')
    op.drop_table('admin')
    # ### end Alembic commands ###
