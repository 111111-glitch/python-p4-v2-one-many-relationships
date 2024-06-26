"""add foreign key to onboarding

Revision ID: cf6f6b8a700f
Revises: ca4b907ee531
Create Date: 2024-04-07 16:48:06.069368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf6f6b8a700f'
down_revision = 'ca4b907ee531'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the foreign key constraint
    op.create_table('onboardings_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('orientation', sa.DateTime(), nullable=True),
        sa.Column('forms_complete', sa.Boolean(), nullable=True),
        sa.Column('employee_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name=op.f('fk_onboardings_employee_id_employees')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data from the old table to the new one
    op.execute('INSERT INTO onboardings_new (id, orientation, forms_complete) SELECT id, orientation, forms_complete FROM onboardings')
    
    # Drop the old table
    op.drop_table('onboardings')
    
    # Rename the new table to the original name
    op.rename_table('onboardings_new', 'onboardings')



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_reviews_employee_id_employees'), 'reviews', type_='foreignkey')
    op.drop_constraint(op.f('fk_onboardings_employee_id_employees'), 'onboardings', type_='foreignkey')
    op.drop_column('onboardings', 'employee_id')
    # ### end Alembic commands ###
