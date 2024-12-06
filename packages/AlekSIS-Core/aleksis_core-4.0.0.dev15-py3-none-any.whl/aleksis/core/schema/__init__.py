from django.apps import apps
from django.contrib.messages import get_messages
from django.db.models import Q

import graphene
import graphene_django_optimizer
from guardian.shortcuts import get_objects_for_user
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
from haystack.utils.loading import UnifiedIndex

from ..models import (
    CustomMenu,
    DynamicRoute,
    Group,
    GroupType,
    Holiday,
    Notification,
    OAuthAccessToken,
    PDFFile,
    Person,
    Room,
    SchoolTerm,
    TaskUserAssignment,
)
from ..util.apps import AppConfig
from ..util.core_helpers import (
    filter_active_school_term,
    get_active_school_term,
    get_allowed_object_ids,
    get_app_module,
    get_app_packages,
    has_person,
)
from .base import FilterOrderList
from .calendar import CalendarBaseType, SetCalendarStatusMutation
from .celery_progress import CeleryProgressFetchedMutation, CeleryProgressType
from .custom_menu import CustomMenuType
from .dynamic_routes import DynamicRouteType
from .group import GroupBatchDeleteMutation
from .group import GroupType as GraphQLGroupType
from .group_type import (
    GroupTypeBatchCreateMutation,
    GroupTypeBatchDeleteMutation,
    GroupTypeBatchPatchMutation,
    GroupTypeType,
)
from .holiday import (
    HolidayBatchCreateMutation,
    HolidayBatchDeleteMutation,
    HolidayBatchPatchMutation,
    HolidayType,
)
from .installed_apps import AppType
from .message import MessageType
from .notification import MarkNotificationReadMutation, NotificationType
from .oauth import OAuthAccessTokenType, OAuthBatchRevokeTokenMutation
from .pdf import PDFFileType
from .person import PersonBatchDeleteMutation, PersonType
from .personal_event import (
    PersonalEventBatchCreateMutation,
    PersonalEventBatchDeleteMutation,
    PersonalEventBatchPatchMutation,
)
from .room import (
    RoomBatchCreateMutation,
    RoomBatchDeleteMutation,
    RoomBatchPatchMutation,
    RoomType,
)
from .school_term import (
    SchoolTermBatchCreateMutation,
    SchoolTermBatchDeleteMutation,
    SchoolTermBatchPatchMutation,
    SchoolTermType,
    SetActiveSchoolTermMutation,
)
from .search import SearchResultType
from .system_properties import SystemPropertiesType
from .two_factor import TwoFactorType
from .user import UserType


class Query(graphene.ObjectType):
    ping = graphene.String(payload=graphene.String())

    notifications = graphene.List(NotificationType)

    persons = FilterOrderList(PersonType)
    person_by_id = graphene.Field(PersonType, id=graphene.ID())
    person_by_id_or_me = graphene.Field(PersonType, id=graphene.ID())

    groups = FilterOrderList(GraphQLGroupType)
    group_by_id = graphene.Field(GraphQLGroupType, id=graphene.ID())
    groups_by_owner = FilterOrderList(GraphQLGroupType, owner=graphene.ID())

    who_am_i = graphene.Field(UserType)

    system_properties = graphene.Field(SystemPropertiesType)
    installed_apps = graphene.List(AppType)

    celery_progress_by_task_id = graphene.Field(CeleryProgressType, task_id=graphene.String())
    celery_progress_by_user = graphene.List(CeleryProgressType)

    pdf_by_id = graphene.Field(PDFFileType, id=graphene.ID())

    search_snippets = graphene.List(
        SearchResultType, query=graphene.String(), limit=graphene.Int(required=False)
    )

    messages = graphene.List(MessageType)

    custom_menu_by_name = graphene.Field(CustomMenuType, name=graphene.String())

    dynamic_routes = graphene.List(DynamicRouteType)

    two_factor = graphene.Field(TwoFactorType)

    oauth_access_tokens = graphene.List(OAuthAccessTokenType)

    rooms = FilterOrderList(RoomType)
    room_by_id = graphene.Field(RoomType, id=graphene.ID())

    active_school_term = graphene.Field(SchoolTermType)
    school_terms = FilterOrderList(SchoolTermType)

    holidays = FilterOrderList(HolidayType)
    calendar = graphene.Field(CalendarBaseType)

    group_types = FilterOrderList(GroupTypeType)

    def resolve_ping(root, info, payload) -> str:
        return payload

    def resolve_notifications(root, info, **kwargs):
        qs = Notification.objects.filter(
            Q(
                pk__in=get_objects_for_user(
                    info.context.user, "core.view_person", Person.objects.all()
                )
            )
            | Q(recipient=info.context.user.person)
        )
        return graphene_django_optimizer.query(qs, info)

    def resolve_persons(root, info, **kwargs):
        qs = get_objects_for_user(info.context.user, "core.view_person", Person.objects.all())
        if has_person(info.context.user):
            qs = qs | Person.objects.filter(id=info.context.user.person.id)

        active_school_term = get_active_school_term(info.context)
        group_q = Q(school_term=active_school_term) | Q(school_term=None)
        qs = (
            (
                qs
                | Person.objects.filter(
                    member_of__in=Group.objects.filter(group_q).filter(
                        owners=info.context.user.person,
                        group_type__owners_can_see_members=True,
                    ),
                )
            )
            .distinct()
            .annotate_permissions(info.context.user)
        )
        return graphene_django_optimizer.query(qs, info)

    def resolve_person_by_id(root, info, id):  # noqa
        person = Person.objects.get(pk=id)
        if not info.context.user.has_perm("core.view_person_rule", person):
            return None
        return person

    def resolve_person_by_id_or_me(root, info, **kwargs):  # noqa
        # Returns person associated with current user if id is None, else the person with the id
        if "id" not in kwargs or kwargs["id"] is None:
            return info.context.user.person if has_person(info.context.user) else None

        person = Person.objects.get(pk=kwargs["id"])
        if not info.context.user.has_perm("core.view_person_rule", person):
            return None
        return person

    @staticmethod
    def resolve_groups(root, info, **kwargs):
        qs = get_objects_for_user(info.context.user, "core.view_group", Group)
        qs = (
            (
                qs
                | Group.objects.filter(
                    owners=info.context.user.person,
                    group_type__owners_can_see_groups=True,
                )
            )
            .distinct()
            .annotate_permissions(info.context.user)
        )
        qs = filter_active_school_term(info.context, qs)
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_group_by_id(root, info, id):  # noqa
        group = Group.objects.filter(id=id)

        if group.exists():
            group = group.first()

            if not info.context.user.has_perm("core.view_group_rule", group):
                return None
            return group

    @staticmethod
    def resolve_groups_by_owner(root, info, owner=None):
        if owner:
            owner = Person.objects.get(pk=owner)
            if not info.context.user.has_perm("core.view_person_rule", owner):
                return []
        elif has_person(info.context.user):
            owner = info.context.user.person
        else:
            return []

        qs = filter_active_school_term(info.context, owner.owner_of.all())
        return graphene_django_optimizer.query(qs, info)

    def resolve_who_am_i(root, info, **kwargs):
        return info.context.user

    def resolve_system_properties(root, info, **kwargs):
        return True

    def resolve_installed_apps(root, info, **kwargs):
        return [app for app in apps.get_app_configs() if isinstance(app, AppConfig)]

    def resolve_celery_progress_by_task_id(root, info, task_id, **kwargs):
        task = TaskUserAssignment.objects.get(task_result__task_id=task_id)

        if not info.context.user.has_perm("core.view_progress_rule", task):
            return None
        progress = task.get_progress_with_meta()
        return progress

    def resolve_celery_progress_by_user(root, info, **kwargs):
        if info.context.user.is_anonymous:
            return None
        tasks = TaskUserAssignment.objects.filter(user=info.context.user)
        return [
            task.get_progress_with_meta()
            for task in tasks
            if task.get_progress_with_meta()["complete"] is False
        ]

    def resolve_pdf_by_id(root, info, id, **kwargs):  # noqa
        pdf_file = PDFFile.objects.get(pk=id)
        if has_person(info.context) and info.context.user.person != pdf_file.person:
            return None
        return pdf_file

    def resolve_search_snippets(root, info, query, limit=-1, **kwargs):
        indexed_models = UnifiedIndex().get_indexed_models()
        allowed_object_ids = get_allowed_object_ids(info.context.user, indexed_models)

        if allowed_object_ids:
            results = (
                SearchQuerySet().filter(id__in=allowed_object_ids).filter(text=AutoQuery(query))
            )
            if limit < 0:
                return results
            return results[:limit]
        else:
            return None

    def resolve_messages(root, info, **kwargs):
        return get_messages(info.context)

    def resolve_custom_menu_by_name(root, info, name, **kwargs):
        return CustomMenu.get_default(name)

    def resolve_dynamic_routes(root, info, **kwargs):
        dynamic_routes = []

        for dynamic_route_object in DynamicRoute.registered_objects_dict.values():
            dynamic_routes += dynamic_route_object.get_dynamic_routes()

        return dynamic_routes

    def resolve_two_factor(root, info, **kwargs):
        if info.context.user.is_anonymous:
            return None
        return info.context.user

    @staticmethod
    def resolve_oauth_access_tokens(root, info, **kwargs):
        qs = OAuthAccessToken.objects.filter(user=info.context.user)
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_room_by_id(root, info, **kwargs):
        pk = kwargs.get("id")
        room_object = Room.objects.get(pk=pk)

        if not info.context.user.has_perm("core.view_room_rule", room_object):
            return None

        return room_object

    @staticmethod
    def resolve_active_school_term(root, info, **kwargs):
        return get_active_school_term(info.context)

    @staticmethod
    def resolve_calendar(root, info, **kwargs):
        return True

    @staticmethod
    def resolve_current_school_term(root, info, **kwargs):
        if not has_person(info.context.user):
            return None

        return SchoolTerm.current

    @staticmethod
    def resolve_holidays(root, info, **kwargs):
        qs = get_objects_for_user(info.context.user, "core.view_holiday", Holiday.objects.all())
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_school_terms(root, info, **kwargs):
        if not info.context.user.has_perm("core.fetch_schoolterms_rule"):
            return []
        return graphene_django_optimizer.query(SchoolTerm.objects.all(), info)

    @staticmethod
    def resolve_group_types(root, info, **kwargs):
        if not info.context.user.has_perm("core.fetch_grouptypes_rule"):
            return []
        return graphene_django_optimizer.query(GroupType.objects.all(), info)

    @staticmethod
    def resolve_rooms(root, info, **kwargs):
        qs = get_objects_for_user(info.context.user, "core.view_room", Room.objects.all())
        return graphene_django_optimizer.query(qs, info)


class Mutation(graphene.ObjectType):
    delete_persons = PersonBatchDeleteMutation.Field()

    mark_notification_read = MarkNotificationReadMutation.Field()

    celery_progress_fetched = CeleryProgressFetchedMutation.Field()

    revoke_oauth_tokens = OAuthBatchRevokeTokenMutation.Field()

    create_rooms = RoomBatchCreateMutation.Field()
    delete_rooms = RoomBatchDeleteMutation.Field()
    update_rooms = RoomBatchPatchMutation.Field()

    create_school_terms = SchoolTermBatchCreateMutation.Field()
    delete_school_terms = SchoolTermBatchDeleteMutation.Field()
    update_school_terms = SchoolTermBatchPatchMutation.Field()
    set_active_school_term = SetActiveSchoolTermMutation.Field()

    create_holidays = HolidayBatchCreateMutation.Field()
    delete_holidays = HolidayBatchDeleteMutation.Field()
    update_holidays = HolidayBatchPatchMutation.Field()

    create_personal_events = PersonalEventBatchCreateMutation.Field()
    delete_personal_events = PersonalEventBatchDeleteMutation.Field()
    update_personal_events = PersonalEventBatchPatchMutation.Field()

    set_calendar_status = SetCalendarStatusMutation.Field()

    create_group_types = GroupTypeBatchCreateMutation.Field()
    delete_group_types = GroupTypeBatchDeleteMutation.Field()
    update_group_types = GroupTypeBatchPatchMutation.Field()

    delete_groups = GroupBatchDeleteMutation.Field()


def build_global_schema():
    """Build global GraphQL schema from all apps."""
    query_bases = [Query]
    mutation_bases = [Mutation]

    for app in get_app_packages():
        schema_mod = get_app_module(app, "schema")
        if not schema_mod:
            # The app does not define a schema
            continue

        if AppQuery := getattr(schema_mod, "Query", None):
            query_bases.append(AppQuery)
        if AppMutation := getattr(schema_mod, "Mutation", None):
            mutation_bases.append(AppMutation)

    # Define classes using all query/mutation classes as mixins
    #  cf. https://docs.graphene-python.org/projects/django/en/latest/schema/#adding-to-the-schema
    GlobalQuery = type("GlobalQuery", tuple(query_bases), {})
    GlobalMutation = type("GlobalMutation", tuple(mutation_bases), {})

    return graphene.Schema(query=GlobalQuery, mutation=GlobalMutation)


schema = build_global_schema()
