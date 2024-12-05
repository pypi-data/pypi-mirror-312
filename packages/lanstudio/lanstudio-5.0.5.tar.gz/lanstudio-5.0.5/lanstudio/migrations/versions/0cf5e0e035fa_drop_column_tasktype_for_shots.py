"""drop column TaskType.for_shots

Revision ID: 0cf5e0e035fa
Revises: f874ad5e898a
Create Date: 2022-06-10 13:34:48.830690

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declarative_base
from lanstudio.migrations.utils.base import BaseMixin


# revision identifiers, used by Alembic.
revision = "0cf5e0e035fa"
down_revision = "f874ad5e898a"
branch_labels = None
depends_on = None


class TaskType(declarative_base(), BaseMixin):
    """
    Categorize tasks in domain areas: modeling, animation, etc.
    """

    __tablename__ = "task_type"
    name = sa.Column(sa.String(40), nullable=False)
    short_name = sa.Column(sa.String(20))
    color = sa.Column(sa.String(7), default="#FFFFFF")
    priority = sa.Column(sa.Integer, default=1)
    for_entity = sa.Column(sa.String(30), default="Asset")
    allow_timelog = sa.Column(sa.Boolean, default=True)
    shotgun_id = sa.Column(sa.Integer, index=True)
    for_shots = sa.Column(sa.Boolean, default=False)
    department_id = sa.Column(
        UUIDType(binary=False), sa.ForeignKey("department.id")
    )

    __table_args__ = (
        sa.UniqueConstraint(
            "name", "for_entity", "department_id", name="task_type_uc"
        ),
    )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    task_types = session.query(TaskType).all()
    for task_type in task_types:
        if task_type.for_shots and task_type.for_entity != "Shot":
            task_type.for_entity = "Shot"
    session.commit()
    op.drop_column("task_type", "for_shots")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "task_type",
        sa.Column(
            "for_shots", sa.BOOLEAN(), autoincrement=False, nullable=True
        ),
    )
    # ### end Alembic commands ###
