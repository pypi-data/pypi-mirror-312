from sqlalchemy_utils import UUIDType

from lanstudio.app import db
from lanstudio.app.models.serializer import SerializerMixin
from lanstudio.app.models.base import BaseMixin


class SearchFilter(db.Model, BaseMixin, SerializerMixin):
    """
    Filters allow to store quick search on a list: asset list, shot list,
    sequence list, todo-list...
    """

    list_type = db.Column(db.String(80), nullable=False, index=True)
    entity_type = db.Column(db.String(80))
    name = db.Column(db.String(200), nullable=False, default="")
    search_query = db.Column(db.String(500), nullable=False, default="")

    search_filter_group_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("search_filter_group.id"),
        nullable=True,
    )
    person_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("person.id"), index=True
    )
    project_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("project.id"), index=True
    )
