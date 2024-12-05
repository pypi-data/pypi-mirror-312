from lanstudio.app.models.software import Software
from lanstudio.app.blueprints.crud.base import BaseModelResource, BaseModelsResource


class SoftwaresResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, Software)

    def check_read_permissions(self):
        return True


class SoftwareResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, Software)

    def check_read_permissions(self, instance):
        return True
