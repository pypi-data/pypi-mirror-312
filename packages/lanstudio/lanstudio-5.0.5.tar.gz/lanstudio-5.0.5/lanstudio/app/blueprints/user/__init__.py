from flask import Blueprint
from lanstudio.app.utils.api import configure_api_from_blueprint

from lanstudio.app.blueprints.user.resources import (
    AssetTasksResource,
    AssetTaskTypesResource,
    AssetTypeAssetsResource,
    ClearAvatarResource,
    ContextResource,
    DateTimeSpentsResource,
    DayOffResource,
    OpenProjectsResource,
    ProjectEpisodesResource,
    ProjectSequencesResource,
    ProjectAssetTypesResource,
    SceneTasksResource,
    SceneTaskTypesResource,
    SequenceTasksResource,
    SequenceTaskTypesResource,
    SequenceShotsResource,
    SequenceScenesResource,
    ShotTasksResource,
    ShotTaskTypesResource,
    ToChecksResource,
    TodosResource,
    DoneResource,
    FilterResource,
    FiltersResource,
    FilterGroupResource,
    FilterGroupsResource,
    DesktopLoginLogsResource,
    NotificationsResource,
    NotificationResource,
    HasTaskSubscribedResource,
    TaskSubscribeResource,
    TaskUnsubscribeResource,
    TaskTimeSpentResource,
    TimeSpentsResource,
    HasSequenceSubscribedResource,
    SequenceSubscriptionsResource,
    SequenceSubscribeResource,
    SequenceUnsubscribeResource,
)

routes = [
    ("/data/user/context", ContextResource),
    ("/data/user/assets/<asset_id>/tasks", AssetTasksResource),
    ("/data/user/shots/<shot_id>/tasks", ShotTasksResource),
    ("/data/user/scenes/<scene_id>/tasks", SceneTasksResource),
    ("/data/user/sequences/<sequence_id>/tasks", SequenceTasksResource),
    ("/data/user/assets/<asset_id>/task-types", AssetTaskTypesResource),
    ("/data/user/shots/<shot_id>/task-types", ShotTaskTypesResource),
    ("/data/user/scenes/<scene_id>/task-types", SceneTaskTypesResource),
    (
        "/data/user/sequences/<sequence_id>/task-types",
        SequenceTaskTypesResource,
    ),
    ("/data/user/projects/open", OpenProjectsResource),
    (
        "/data/user/projects/<project_id>/asset-types",
        ProjectAssetTypesResource,
    ),
    (
        "/data/user/projects/<project_id>/asset-types/<asset_type_id>/assets",
        AssetTypeAssetsResource,
    ),
    ("/data/user/projects/<project_id>/sequences", ProjectSequencesResource),
    ("/data/user/projects/<project_id>/episodes", ProjectEpisodesResource),
    ("/data/user/sequences/<sequence_id>/shots", SequenceShotsResource),
    ("/data/user/sequences/<sequence_id>/scenes", SequenceScenesResource),
    ("/data/user/tasks", TodosResource),
    ("/data/user/tasks-to-check", ToChecksResource),
    ("/data/user/done-tasks", DoneResource),
    ("/data/user/filters", FiltersResource),
    ("/data/user/filters/<filter_id>", FilterResource),
    ("/data/user/filter-groups", FilterGroupsResource),
    ("/data/user/filter-groups/<filter_group_id>", FilterGroupResource),
    ("/data/user/desktop-login-logs", DesktopLoginLogsResource),
    ("/data/user/time-spents", TimeSpentsResource),
    ("/data/user/time-spents/<date>", DateTimeSpentsResource),
    ("/data/user/tasks/<task_id>/time-spents/<date>", TaskTimeSpentResource),
    ("/data/user/day-offs/<date>", DayOffResource),
    ("/data/user/notifications", NotificationsResource),
    ("/data/user/notifications/<notification_id>", NotificationResource),
    ("/data/user/tasks/<task_id>/subscribed", HasTaskSubscribedResource),
    ("/actions/user/tasks/<task_id>/subscribe", TaskSubscribeResource),
    ("/actions/user/tasks/<task_id>/unsubscribe", TaskUnsubscribeResource),
    ("/actions/user/clear-avatar", ClearAvatarResource),
    (
        "/data/user/entities/<sequence_id>/task-types/<task_type_id>/subscribed",
        HasSequenceSubscribedResource,
    ),
    (
        "/data/user/projects/<project_id>/task-types/<task_type_id>/sequence-subscriptions",
        SequenceSubscriptionsResource,
    ),
    (
        "/actions/user/sequences/<sequence_id>/task-types/<task_type_id>/subscribe",
        SequenceSubscribeResource,
    ),
    (
        "/actions/user/sequences/<sequence_id>/task-types/<task_type_id>/unsubscribe",
        SequenceUnsubscribeResource,
    ),
]

blueprint = Blueprint("user", "user")
api = configure_api_from_blueprint(blueprint, routes)
