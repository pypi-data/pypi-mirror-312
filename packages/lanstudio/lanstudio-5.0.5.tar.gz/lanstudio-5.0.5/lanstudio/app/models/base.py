import datetime

from sqlalchemy_utils import UUIDType
from sqlalchemy import func
from lanstudio.app import db
from lanstudio.app.utils import fields


class BaseMixin(object):
    id = db.Column(
        UUIDType(binary=False), primary_key=True, default=fields.gen_uuid
    )

    # Audit fields
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    def __repr__(self):
        """
        String representation based on type and name by default.
        """
        return "<%s %s>" % (type(self).__name__, self.name)

    @classmethod
    def query(cls):
        """
        Shorthand to access session query object.
        """
        return db.session.query(cls)

    @classmethod
    def get(cls, id):
        """
        Shorthand to retrieve data by id.
        """
        return db.session.get(cls, id)

    @classmethod
    def get_by(cls, **kw):
        """
        Shorthand to retrieve data by using filters. It returns the first
        element of the returned data.
        """
        return cls.query.filter_by(**kw).first()

    @classmethod
    def get_by_case_insensitive(cls, **kw):
        """
        Shorthand to retrieve data by using filters. It returns the first
        element of the returned data without checking case for any String type value.
        """
        filters = []
        for key, value in kw.items():
            column = getattr(cls, key)
            if isinstance(column.type, db.String):
                filters.append(func.lower(column) == func.lower(value))
            else:
                filters.append(column == value)

        return cls.query.filter(*filters).first()

    @classmethod
    def get_all(cls):
        """
        Shorthand to retrieve all data for a model.
        """
        return cls.query.all()

    @classmethod
    def get_all_by(cls, **kw):
        """
        Shorthand to retrieve data by using filters.
        """
        return cls.query.filter_by(**kw).all()

    @classmethod
    def create(cls, **kw):
        """
        Shorthand to create an entry via the database session.
        """
        instance = cls(**kw)
        try:
            db.session.add(instance)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            db.session.remove()
            raise
        return instance

    @classmethod
    def create_no_commit(cls, **kw):
        """
        Shorthand to create an entry via the database session without commiting
        the request.
        """
        instance = cls(**kw)
        db.session.add(instance)
        return instance

    @classmethod
    def delete_all_by(cls, **kw):
        """
        Shorthand to delete data by using filters.
        """
        result = cls.query.filter_by(**kw).delete()
        db.session.commit()
        return result

    @classmethod
    def get_id_map(cls, field="shotgun_id"):
        """
        Build a map to easily match a field value with an id. It's useful during
        mass import to build foreign keys.
        """
        entry_map = {}
        entries = cls.query.all()
        for entry in entries:
            entry_map[getattr(entry, field)] = entry.id
        return entry_map

    @classmethod
    def create_from_import(cls, data):
        """
        Create a new instance of the model based on data that comes from the lanstudio
        API.
        """
        if "type" in data:
            del data["type"]
        previous_data = cls.get(data["id"])
        if previous_data is None:
            return cls.create(**data)
        else:
            previous_data.update(data)
            return previous_data

    @classmethod
    def create_from_import_list(cls, data_list):
        """
        Create a list of instances of the model based on data that comes from
        the lanstudio API.
        """
        if "data" in data_list:
            data_list = data_list["data"]
        for data in data_list:
            cls.create_from_import(data)

    @classmethod
    def delete_from_import(cls, instance_id):
        """
        Delete an entry and its related base on the entry id.
        """
        instance = cls.get(instance_id)
        if instance is not None:
            instance.delete()
        return instance_id

    @classmethod
    def commit(cls):
        db.session.commit()

    def save(self):
        """
        Shorthand to create an entry via the database session based on current
        instance fields.
        """
        try:
            self.updated_at = datetime.datetime.utcnow()
            db.session.add(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            db.session.remove()
            raise

    def delete(self):
        """
        Shorthand to delete an entry via the database session based on current
        instance id.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            db.session.remove()
            raise

    def delete_no_commit(self):
        """
        Shorthand to delete an entry via the database session based on current
        instance id. The change is not commited.
        """
        db.session.delete(self)
        return True

    def update(self, data):
        """
        Shorthand to update an entry via the database session based on current
        instance fields.
        """
        try:
            self.updated_at = datetime.datetime.utcnow()
            for key, value in data.items():
                setattr(self, key, value)
            db.session.add(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            db.session.remove()
            raise

    def update_no_commit(self, data):
        """
        Shorthand to update an entry via the database session based on current
        instance fields. It doesn't generate a commit.
        """
        self.updated_at = datetime.datetime.utcnow()
        for key, value in data.items():
            setattr(self, key, value)
        db.session.add(self)

    def set_links(self, ids, LinkTable, field_left, field_right):
        for id in ids:
            link = LinkTable.query.filter_by(
                **{field_left: self.id, field_right: id}
            ).first()
            if link is None:
                link = LinkTable(**{field_left: self.id, field_right: id})
                db.session.add(link)
        db.session.commit()
