"""empty message

Revision ID: 45349613ddc5
Revises: 
Create Date: 2024-01-16 13:39:34.370166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45349613ddc5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Faculty_information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pan_no', sa.String(length=255), nullable=True),
    sa.Column('Names', sa.String(length=255), nullable=True),
    sa.Column('bank_account', sa.Integer(), nullable=True),
    sa.Column('ifsc_code', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Faculty_information', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Faculty_information_pan_no'), ['pan_no'], unique=False)

    op.create_table('Subject_information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_code', sa.String(length=255), nullable=True),
    sa.Column('subject_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Examination_bills',
    sa.Column('examination_id', sa.Integer(), nullable=False),
    sa.Column('pan_no', sa.String(length=255), nullable=True),
    sa.Column('name_of_the_staff', sa.String(length=255), nullable=True),
    sa.Column('bank_account_no', sa.Integer(), nullable=True),
    sa.Column('ifsc_code', sa.String(length=255), nullable=True),
    sa.Column('transaction_type', sa.String(length=255), nullable=True),
    sa.Column('no_of_scripts', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.Column('grand_total', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['pan_no'], ['Faculty_information.pan_no'], ),
    sa.PrimaryKeyConstraint('examination_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Examination_bills')
    op.drop_table('Subject_information')
    with op.batch_alter_table('Faculty_information', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Faculty_information_pan_no'))

    op.drop_table('Faculty_information')
    # ### end Alembic commands ###
