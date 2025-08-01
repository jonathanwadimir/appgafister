"""Agregar tecnico_id a tickets

Revision ID: 542f75ae97b5
Revises: 
Create Date: 2025-07-10 03:56:38.864089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '542f75ae97b5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clientes_id'), table_name='clientes')
    op.drop_index(op.f('ix_clientes_rut'), table_name='clientes')
    op.drop_table('clientes')
    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')
    op.drop_index(op.f('ix_tecnicos_id'), table_name='tecnicos')
    op.drop_index(op.f('ix_tecnicos_rut'), table_name='tecnicos')
    op.drop_table('tecnicos')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tecnicos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('rut', sa.VARCHAR(), nullable=True),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('zona', sa.VARCHAR(), nullable=True),
    sa.Column('certificado_sec', sa.BOOLEAN(), nullable=True),
    sa.Column('emision', sa.VARCHAR(), nullable=True),
    sa.Column('foto_perfil', sa.VARCHAR(), nullable=True),
    sa.Column('acepto_terminos', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tecnicos_rut'), 'tecnicos', ['rut'], unique=1)
    op.create_index(op.f('ix_tecnicos_id'), 'tecnicos', ['id'], unique=False)
    op.create_table('tickets',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cliente_id', sa.INTEGER(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.Column('emergencia', sa.BOOLEAN(), nullable=True),
    sa.Column('multimedia', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=False)
    op.create_table('clientes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('rut', sa.VARCHAR(), nullable=True),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clientes_rut'), 'clientes', ['rut'], unique=1)
    op.create_index(op.f('ix_clientes_id'), 'clientes', ['id'], unique=False)
    # ### end Alembic commands ###
