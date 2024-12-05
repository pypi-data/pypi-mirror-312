from lanstudio.app.models.preview_background_file import PreviewBackgroundFile
from lanstudio.app.services.exception import ArgumentsException
from lanstudio.app.services import files_service, deletion_service

from lanstudio.app.blueprints.crud.base import BaseModelResource, BaseModelsResource


class PreviewBackgroundFilesResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, PreviewBackgroundFile)

    def check_read_permissions(self):
        return True

    def update_data(self, data):
        name = data.get("name", None)
        preview_background_file = PreviewBackgroundFile.get_by(name=name)
        if preview_background_file is not None:
            raise ArgumentsException(
                "A preview background file with similar name already exists"
            )
        return data

    def post_creation(self, instance):
        if instance.is_default:
            files_service.reset_default_preview_background_files(instance.id)
        files_service.clear_preview_background_file_cache(str(instance.id))
        return instance.serialize()


class PreviewBackgroundFileResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, PreviewBackgroundFile)

    def check_read_permissions(self, instance):
        return True

    def update_data(self, data, instance_id):
        name = data.get("name", None)
        if name is not None:
            preview_background_file = PreviewBackgroundFile.get_by(name=name)
            if preview_background_file is not None and instance_id != str(
                preview_background_file.id
            ):
                raise ArgumentsException(
                    "A preview background file with similar name already exists"
                )
        return data

    def post_update(self, instance_dict):
        if instance_dict["is_default"]:
            files_service.reset_default_preview_background_files(
                instance_dict["id"]
            )
        files_service.clear_preview_background_file_cache(instance_dict["id"])
        return instance_dict

    def post_delete(self, instance_dict):
        deletion_service.clear_preview_background_files(instance_dict["id"])
        files_service.clear_preview_background_file_cache(instance_dict["id"])
        return instance_dict
