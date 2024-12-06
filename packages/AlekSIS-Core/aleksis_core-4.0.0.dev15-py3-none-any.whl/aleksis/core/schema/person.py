from typing import Union

from django.utils import timezone

import graphene
import graphene_django_optimizer
from graphene_django import DjangoObjectType

from ..filters import PersonFilter
from ..models import DummyPerson, Person
from ..util.core_helpers import get_site_preferences, has_person
from .base import (
    BaseBatchDeleteMutation,
    DjangoFilterMixin,
    FieldFileType,
    PermissionsTypeMixin,
)
from .notification import NotificationType


class PersonPreferencesType(graphene.ObjectType):
    theme_design_mode = graphene.String()
    days_of_week = graphene.List(graphene.Int)

    def resolve_theme_design_mode(parent, info, **kwargs):
        return parent["theme__design"]

    @staticmethod
    def resolve_days_of_week(root, info, **kwargs):
        first_day = root["calendar__first_day_of_the_week"]

        if first_day == "default":
            first_day = get_site_preferences()["calendar__first_day_of_the_week"]

        first_day = int(first_day)

        days = list(map(str, range(7)))
        sorted_days = days[first_day:] + days[:first_day]

        return list(map(int, sorted_days))


class PersonType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Person
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "additional_name",
            "short_name",
            "street",
            "housenumber",
            "postal_code",
            "place",
            "phone_number",
            "mobile_number",
            "email",
            "date_of_birth",
            "place_of_birth",
            "sex",
            "photo",
            "avatar",
            "guardians",
            "primary_group",
            "description",
            "children",
            "owner_of",
            "member_of",
        ]
        filterset_class = PersonFilter

    full_name = graphene.String()
    username = graphene.String()
    userid = graphene.ID()
    photo = graphene.Field(FieldFileType, required=False)
    avatar = graphene.Field(FieldFileType, required=False)
    avatar_url = graphene.String()
    avatar_content_url = graphene.String()
    secondary_image_url = graphene.String(required=False)

    street = graphene.String(required=False)
    housenumber = graphene.String(required=False)
    postal_code = graphene.String(required=False)
    place = graphene.String(required=False)

    phone_number = graphene.String(required=False)
    mobile_number = graphene.String(required=False)
    email = graphene.String(required=False)

    date_of_birth = graphene.String(required=False)
    place_of_birth = graphene.String(required=False)

    notifications = graphene.List(NotificationType)
    unread_notifications_count = graphene.Int(required=False)

    is_dummy = graphene.Boolean()
    preferences = graphene.Field(PersonPreferencesType)

    can_change_person_preferences = graphene.Boolean()
    can_impersonate_person = graphene.Boolean()
    can_invite_person = graphene.Boolean()

    def resolve_street(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_address_rule", root):
            return root.street
        return None

    def resolve_housenumber(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_address_rule", root):
            return root.housenumber
        return None

    def resolve_postal_code(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_address_rule", root):
            return root.postal_code
        return None

    def resolve_place(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_address_rule", root):
            return root.place
        return None

    def resolve_phone_number(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_contact_details_rule", root):
            return root.phone_number
        return None

    def resolve_mobile_number(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_contact_details_rule", root):
            return root.mobile_number
        return None

    def resolve_email(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_contact_details_rule", root):
            return root.email
        return None

    def resolve_date_of_birth(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_personal_details_rule", root):
            return root.date_of_birth
        return None

    def resolve_place_of_birth(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_personal_details_rule", root):
            return root.place_of_birth
        return None

    def resolve_children(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_personal_details_rule", root):
            return root.children.all()
        return []

    def resolve_guardians(root, info, **kwargs):  # noqa
        if info.context.user.has_perm("core.view_personal_details_rule", root):
            return root.guardians.all()
        return []

    def resolve_member_of(root, info, **kwargs):  # noqa
        if getattr(root, "can_view_person_groups", False) or info.context.user.has_perm(
            "core.view_person_groups_rule", root
        ):
            return root.member_of.all()
        return []

    def resolve_owner_of(root, info, **kwargs):  # noqa
        if getattr(root, "can_view_person_groups", False) or info.context.user.has_perm(
            "core.view_person_groups_rule", root
        ):
            return root.owner_of.all()
        return []

    @graphene_django_optimizer.resolver_hints(
        model_field="user",
    )
    def resolve_username(root, info, **kwargs):  # noqa
        return root.user.username if root.user else None

    @graphene_django_optimizer.resolver_hints(
        model_field="user",
    )
    def resolve_userid(root, info, **kwargs):  # noqa
        return root.user.id if root.user else None

    def resolve_unread_notifications_count(root, info, **kwargs):  # noqa
        if root.pk and has_person(info.context) and root == info.context.user.person:
            return root.unread_notifications_count
        elif root.pk:
            return 0
        return None

    def resolve_photo(root, info, **kwargs):
        if info.context.user.has_perm("core.view_photo_rule", root):
            return root.photo
        return None

    def resolve_avatar(root, info, **kwargs):
        if info.context.user.has_perm("core.view_avatar_rule", root):
            return root.avatar
        return None

    def resolve_avatar_url(root, info, **kwargs):
        if info.context.user.has_perm("core.view_avatar_rule", root) and root.avatar:
            return root.avatar.url
        return root.identicon_url

    def resolve_avatar_content_url(root, info, **kwargs):  # noqa
        # Returns the url for the main image for a person, either the avatar, photo or identicon,
        # based on permissions and preferences
        if get_site_preferences()["account__person_prefer_photo"]:
            if info.context.user.has_perm("core.view_photo_rule", root) and root.photo:
                return root.photo.url
            elif info.context.user.has_perm("core.view_avatar_rule", root) and root.avatar:
                return root.avatar.url

        else:
            if info.context.user.has_perm("core.view_avatar_rule", root) and root.avatar:
                return root.avatar.url
            elif info.context.user.has_perm("core.view_photo_rule", root) and root.photo:
                return root.photo.url

        return root.identicon_url

    def resolve_secondary_image_url(root, info, **kwargs):  # noqa
        # returns either the photo url or the avatar url,
        # depending on the one returned by avatar_content_url

        if get_site_preferences()["account__person_prefer_photo"]:
            if info.context.user.has_perm("core.view_avatar_rule", root) and root.avatar:
                return root.avatar.url
        elif info.context.user.has_perm("core.view_photo_rule", root) and root.photo:
            return root.photo.url
        return None

    def resolve_is_dummy(root: Union[Person, DummyPerson], info, **kwargs):
        return root.is_dummy if hasattr(root, "is_dummy") else False

    def resolve_notifications(root: Person, info, **kwargs):
        if root.pk and has_person(info.context) and root == info.context.user.person:
            return root.notifications.filter(send_at__lte=timezone.now()).order_by(
                "read", "-created"
            )
        return []

    def resolve_can_change_person_preferences(root, info, **kwargs):  # noqa
        return info.context.user.has_perm("core.change_person_preferences_rule", root)

    def resolve_can_impersonate_person(root, info, **kwargs):  # noqa
        return root.user and info.context.user.has_perm("core.impersonate_rule", root)

    def resolve_can_invite_person(root, info, **kwargs):  # noqa
        return (not root.user) and info.context.user.has_perm("core.invite_rule", root)

    @staticmethod
    def resolve_can_edit(root, info, **kwargs):
        if hasattr(root, "can_edit"):
            return root.can_edit
        return info.context.user.has_perm("core.edit_person_rule", root)

    @staticmethod
    def resolve_can_delete(root, info, **kwargs):
        if hasattr(root, "can_delete"):
            return root.can_delete
        return info.context.user.has_perm("core.delete_person_rule", root)


class PersonBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = Person
        permissions = ("core.delete_person_rule",)
