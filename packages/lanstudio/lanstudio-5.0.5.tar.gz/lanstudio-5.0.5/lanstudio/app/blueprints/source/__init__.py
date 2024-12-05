"""
This module is named source instead of import because import is a Python
keyword.
"""
from flask import Blueprint
from lanstudio.app.utils.api import configure_api_from_blueprint

from lanstudio.app.blueprints.source.shotgun.project import (
    ImportShotgunProjectsResource,
    ImportRemoveShotgunProjectResource,
)
from lanstudio.app.blueprints.source.shotgun.person import (
    ImportShotgunPersonsResource,
    ImportRemoveShotgunPersonResource,
)
from lanstudio.app.blueprints.source.shotgun.shot import (
    ImportShotgunShotsResource,
    ImportRemoveShotgunShotResource,
)
from lanstudio.app.blueprints.source.shotgun.scene import (
    ImportShotgunScenesResource,
    ImportRemoveShotgunSceneResource,
)
from lanstudio.app.blueprints.source.shotgun.sequence import (
    ImportShotgunSequencesResource,
    ImportRemoveShotgunSequenceResource,
)
from lanstudio.app.blueprints.source.shotgun.episode import (
    ImportShotgunEpisodesResource,
    ImportRemoveShotgunEpisodeResource,
)
from lanstudio.app.blueprints.source.shotgun.assets import (
    ImportShotgunAssetsResource,
    ImportRemoveShotgunAssetResource,
)
from lanstudio.app.blueprints.source.shotgun.steps import (
    ImportShotgunStepsResource,
    ImportRemoveShotgunStepResource,
)
from lanstudio.app.blueprints.source.shotgun.status import (
    ImportShotgunStatusResource,
    ImportRemoveShotgunStatusResource,
)
from lanstudio.app.blueprints.source.shotgun.tasks import (
    ImportShotgunTasksResource,
    ImportRemoveShotgunTaskResource,
)
from lanstudio.app.blueprints.source.shotgun.versions import (
    ImportShotgunVersionsResource,
    ImportRemoveShotgunVersionResource,
)
from lanstudio.app.blueprints.source.shotgun.import_errors import (
    ShotgunImportErrorsResource,
    ShotgunImportErrorResource,
)
from lanstudio.app.blueprints.source.shotgun.notes import (
    ImportShotgunNotesResource,
    ImportRemoveShotgunNoteResource,
)
from lanstudio.app.blueprints.source.shotgun.team import (
    ImportShotgunProjectConnectionsResource,
    ImportRemoveShotgunProjectConnectionResource,
)

from lanstudio.app.blueprints.source.csv.persons import PersonsCsvImportResource
from lanstudio.app.blueprints.source.csv.assets import AssetsCsvImportResource
from lanstudio.app.blueprints.source.csv.edits import EditsCsvImportResource
from lanstudio.app.blueprints.source.csv.shots import ShotsCsvImportResource
from lanstudio.app.blueprints.source.csv.casting import CastingCsvImportResource
from lanstudio.app.blueprints.source.csv.task_type_estimations import (
    TaskTypeEstimationsCsvImportResource,
    TaskTypeEstimationsEpisodeCsvImportResource,
)
from lanstudio.app.blueprints.source.kitsu import (
    ImportKitsuCommentsResource,
    ImportKitsuEntitiesResource,
    ImportKitsuEntityLinksResource,
    ImportKitsuProjectsResource,
    ImportKitsuTasksResource,
)

from lanstudio.app.blueprints.source.edl import (
    EDLImportResource,
    EDLImportEpisodeResource,
)

routes = [
    ("/import/shotgun/persons", ImportShotgunPersonsResource),
    ("/import/shotgun/projects", ImportShotgunProjectsResource),
    ("/import/shotgun/episodes", ImportShotgunEpisodesResource),
    ("/import/shotgun/sequences", ImportShotgunSequencesResource),
    ("/import/shotgun/shots", ImportShotgunShotsResource),
    ("/import/shotgun/scenes", ImportShotgunScenesResource),
    ("/import/shotgun/assets", ImportShotgunAssetsResource),
    ("/import/shotgun/steps", ImportShotgunStepsResource),
    ("/import/shotgun/status", ImportShotgunStatusResource),
    ("/import/shotgun/tasks", ImportShotgunTasksResource),
    ("/import/shotgun/versions", ImportShotgunVersionsResource),
    ("/import/shotgun/notes", ImportShotgunNotesResource),
    ("/import/shotgun/errors", ShotgunImportErrorsResource),
    (
        "/import/shotgun/projectconnections",
        ImportShotgunProjectConnectionsResource,
    ),
    ("/import/shotgun/errors/<error_id>", ShotgunImportErrorResource),
    ("/import/shotgun/remove/project", ImportRemoveShotgunProjectResource),
    ("/import/shotgun/remove/person", ImportRemoveShotgunPersonResource),
    ("/import/shotgun/remove/shot", ImportRemoveShotgunShotResource),
    ("/import/shotgun/remove/scene", ImportRemoveShotgunSceneResource),
    ("/import/shotgun/remove/episode", ImportRemoveShotgunEpisodeResource),
    ("/import/shotgun/remove/sequence", ImportRemoveShotgunSequenceResource),
    ("/import/shotgun/remove/asset", ImportRemoveShotgunAssetResource),
    (
        "/import/shotgun/remove/projectconnection",
        ImportRemoveShotgunProjectConnectionResource,
    ),
    ("/import/shotgun/remove/step", ImportRemoveShotgunStepResource),
    ("/import/shotgun/remove/status", ImportRemoveShotgunStatusResource),
    ("/import/shotgun/remove/task", ImportRemoveShotgunTaskResource),
    ("/import/shotgun/remove/note", ImportRemoveShotgunNoteResource),
    ("/import/shotgun/remove/version", ImportRemoveShotgunVersionResource),
    ("/import/csv/persons", PersonsCsvImportResource),
    ("/import/csv/projects/<project_id>/assets", AssetsCsvImportResource),
    ("/import/csv/projects/<project_id>/shots", ShotsCsvImportResource),
    ("/import/csv/projects/<project_id>/edits", EditsCsvImportResource),
    ("/import/csv/projects/<project_id>/casting", CastingCsvImportResource),
    (
        "/import/csv/projects/<project_id>/task-types/<task_type_id>/estimations",
        TaskTypeEstimationsCsvImportResource,
    ),
    (
        "/import/csv/projects/<project_id>/episodes/<episode_id>/task-types/<task_type_id>/estimations",
        TaskTypeEstimationsEpisodeCsvImportResource,
    ),
    ("/import/edl/projects/<project_id>", EDLImportResource),
    (
        "/import/edl/projects/<project_id>/episodes/<episode_id>",
        EDLImportEpisodeResource,
    ),
    ("/import/kitsu/comments", ImportKitsuCommentsResource),
    ("/import/kitsu/entities", ImportKitsuEntitiesResource),
    ("/import/kitsu/entity-links", ImportKitsuEntityLinksResource),
    ("/import/kitsu/projects", ImportKitsuProjectsResource),
    ("/import/kitsu/tasks", ImportKitsuTasksResource),
]

blueprint = Blueprint("/import", "import")
api = configure_api_from_blueprint(blueprint, routes)
