from flask import Blueprint
from lanstudio.app.utils.api import configure_api_from_blueprint

from lanstudio.app.blueprints.persons.resources import (
    DateTimeSpentsResource,
    DayOffResource,
    DayOffForMonthResource,
    DesktopLoginsResource,
    InvitePersonResource,
    NewPersonResource,
    PersonMonthQuotaShotsResource,
    PersonWeekQuotaShotsResource,
    PersonDayQuotaShotsResource,
    PersonMonthTimeSpentsResource,
    PersonMonthAllTimeSpentsResource,
    PersonWeekTimeSpentsResource,
    PersonDayTimeSpentsResource,
    PersonWeekDayOffResource,
    PersonYearDayOffResource,
    PersonMonthDayOffResource,
    PresenceLogsResource,
    TimeSpentsResource,
    TimeSpentMonthResource,
    TimeSpentMonthsResource,
    TimeSpentWeekResource,
    TimeSpentYearsResource,
    PersonYearTimeSpentsResource,
    AddToDepartmentResource,
    RemoveFromDepartmentResource,
    ChangePasswordForPersonResource,
    DisableTwoFactorAuthenticationPersonResource,
)

routes = [
    ("/data/persons/new", NewPersonResource),
    ("/data/persons/<person_id>/desktop-login-logs", DesktopLoginsResource),
    ("/data/persons/presence-logs/<month_date>", PresenceLogsResource),
    ("/data/persons/<person_id>/time-spents", TimeSpentsResource),
    ("/data/persons/<person_id>/time-spents/<date>", DateTimeSpentsResource),
    ("/data/persons/<person_id>/day-offs/<date>", DayOffResource),
    (
        "/data/persons/<person_id>/time-spents/year/<year>",
        PersonYearTimeSpentsResource,
    ),
    (
        "/data/persons/<person_id>/time-spents/month/<year>/<month>",
        PersonMonthTimeSpentsResource,
    ),
    (
        "/data/persons/<person_id>/time-spents/month/all/<year>/<month>",
        PersonMonthAllTimeSpentsResource,
    ),
    (
        "/data/persons/<person_id>/time-spents/week/<year>/<week>",
        PersonWeekTimeSpentsResource,
    ),
    (
        "/data/persons/<person_id>/time-spents/day/<year>/<month>/<day>",
        PersonDayTimeSpentsResource,
    ),
    (
        "/data/persons/<person_id>/quota-shots/month/<year>/<month>",
        PersonMonthQuotaShotsResource,
    ),
    (
        "/data/persons/<person_id>/quota-shots/week/<year>/<week>",
        PersonWeekQuotaShotsResource,
    ),
    (
        "/data/persons/<person_id>/quota-shots/day/<year>/<month>/<day>",
        PersonDayQuotaShotsResource,
    ),
    ("/data/persons/time-spents/year-table/", TimeSpentYearsResource),
    ("/data/persons/time-spents/month-table/<year>", TimeSpentMonthsResource),
    ("/data/persons/time-spents/week-table/<year>", TimeSpentWeekResource),
    (
        "/data/persons/time-spents/day-table/<year>/<month>",
        TimeSpentMonthResource,
    ),
    ("/data/persons/day-offs/<year>/<month>", DayOffForMonthResource),
    (
        "/data/persons/<person_id>/day-offs/week/<year>/<week>",
        PersonWeekDayOffResource,
    ),
    (
        "/data/persons/<person_id>/day-offs/month/<year>/<month>",
        PersonMonthDayOffResource,
    ),
    (
        "/data/persons/<person_id>/day-offs/year/<year>",
        PersonYearDayOffResource,
    ),
    ("/actions/persons/<person_id>/invite", InvitePersonResource),
    ("/actions/persons/<person_id>/departments/add", AddToDepartmentResource),
    (
        "/actions/persons/<person_id>/departments/<department_id>",
        RemoveFromDepartmentResource,
    ),
    (
        "/actions/persons/<person_id>/change-password",
        ChangePasswordForPersonResource,
    ),
    (
        "/actions/persons/<person_id>/disable-two-factor-authentication",
        DisableTwoFactorAuthenticationPersonResource,
    ),
]

blueprint = Blueprint("persons", "persons")
api = configure_api_from_blueprint(blueprint, routes)
