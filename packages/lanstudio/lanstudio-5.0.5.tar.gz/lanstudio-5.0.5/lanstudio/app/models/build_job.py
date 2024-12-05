import datetime

from sqlalchemy_utils import UUIDType, ChoiceType

from lanstudio.app import db
from lanstudio.app.models.serializer import SerializerMixin
from lanstudio.app.models.base import BaseMixin
from lanstudio.app.utils import fields

STATUSES = [
    ("running", "Running"),
    ("failed", "Failed"),
    ("succeeded", "Succeeded"),
]

TYPES = [("archive", "Archive"), ("movie", "Movie")]


class BuildJob(db.Model, BaseMixin, SerializerMixin):
    """
    A build job stores information about the state of the building
    of a given playlist.
    """

    status = db.Column(ChoiceType(STATUSES))
    job_type = db.Column(ChoiceType(TYPES))
    ended_at = db.Column(db.DateTime)

    playlist_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("playlist.id"),
        nullable=False,
        index=True,
    )

    def end(self, status):
        self.update({"status": status, "ended_at": datetime.datetime.utcnow()})

    def present(self):
        return fields.serialize_dict(
            {
                "id": self.id,
                "status": self.status,
                "created_at": self.created_at,
            }
        )
