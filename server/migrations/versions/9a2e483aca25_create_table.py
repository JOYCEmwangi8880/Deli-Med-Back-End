"""Create table

Revision ID: 9a2e483aca25
Revises: 
Create Date: 2024-01-23 12:46:38.835961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a2e483aca25'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Illnesses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Medicines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('blood_type', sa.String(length=3), nullable=True),
    sa.Column('previous_illnesses', sa.String(length=750), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=True),
    sa.Column('delivery_address', sa.String(length=200), nullable=True),
    sa.Column('medicine_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['medicine_id'], ['Medicines.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('illness_medicine',
    sa.Column('illness_id', sa.Integer(), nullable=True),
    sa.Column('medicine_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['illness_id'], ['Illnesses.id'], ),
    sa.ForeignKeyConstraint(['medicine_id'], ['Medicines.id'], )
    )
    op.create_table('user_illness',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('illness_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['illness_id'], ['Illnesses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_illness')
    op.drop_table('illness_medicine')
    op.drop_table('Orders')
    op.drop_table('Users')
    op.drop_table('Medicines')
    op.drop_table('Illnesses')
    # ### end Alembic commands ###
