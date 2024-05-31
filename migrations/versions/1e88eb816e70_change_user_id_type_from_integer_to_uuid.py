"""Change user_id type from Integer to UUID

Revision ID: 1e88eb816e70
Revises: 
Create Date: 2024-05-27 16:13:35.428250

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1e88eb816e70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Ensure the UUID extension is available
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Add new UUID column for user_id
    op.add_column('campaign', sa.Column('new_user_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()'), nullable=False))

    # Migrate data from old column to new column
    op.execute('UPDATE campaign SET new_user_id = uuid_generate_v4()')

    # Drop the old column
    op.drop_column('campaign', 'user_id')

    # Rename the new column to the old column name
    op.alter_column('campaign', 'new_user_id', new_column_name='user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaign',
    sa.Column('cam_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('cam_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('completed_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('launch_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('send_data', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('page_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('temp_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('smtp_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('cam_id', name='campaign_pkey')
    )
    op.create_table('role_permission',
    sa.Column('roleid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('permid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['permid'], ['permission.perm_id'], name='role_permission_permid_fkey'),
    sa.ForeignKeyConstraint(['roleid'], ['role.role_id'], name='role_permission_roleid_fkey')
    )
    op.create_table('groups',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('groups_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('groupname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('camp_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('modified_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='groups_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('grouptarget',
    sa.Column('groupid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('targetid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['groupid'], ['groups.id'], name='grouptarget_groupid_fkey'),
    sa.ForeignKeyConstraint(['targetid'], ['target.id'], name='grouptarget_targetid_fkey')
    )
    op.create_table('role',
    sa.Column('role_id', sa.INTEGER(), server_default=sa.text("nextval('role_role_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('role_desc', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('role_id', name='role_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=170), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('modified_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], name='users_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_table('page',
    sa.Column('page_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('path', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('modified_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('page_id', name='page_pkey')
    )
    op.create_table('permission',
    sa.Column('perm_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('perm_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('perm_desc', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('perm_id', name='permission_pkey')
    )
    op.create_table('target',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('hostname', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('ip_addr', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('sess_id', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('recv_data', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='target_pkey')
    )
    op.create_table('result',
    sa.Column('rid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('modified_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('cam_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('rid', name='result_pkey')
    )
    op.create_table('template',
    sa.Column('temp_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('temp_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('temp_subject', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('temp_text', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('temp_html', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('modified_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('temp_id', name='template_pkey')
    )
    op.create_table('smtp',
    sa.Column('smtp_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('host', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('from_address', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('ignore_cert_errors', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('modified_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('smtp_id', name='smtp_pkey')
    )
    # ### end Alembic commands ###
