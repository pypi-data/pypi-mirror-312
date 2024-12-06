from graphene_django import DjangoObjectType

from ..models import GroupType
from .base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    PermissionsTypeMixin,
)


class GroupTypeType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = GroupType
        fields = [
            "id",
            "name",
            "description",
            "owners_can_see_groups",
            "owners_can_see_members",
            "owners_can_see_members_allowed_information",
        ]


class GroupTypeBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = GroupType
        permissions = ("core.create_grouptype_rule",)
        only_fields = (
            "name",
            "description",
            "owners_can_see_groups",
            "owners_can_see_members",
            "owners_can_see_members_allowed_information",
        )


class GroupTypeBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = GroupType
        permissions = ("core.delete_grouptype_rule",)


class GroupTypeBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = GroupType
        permissions = ("core.change_grouptype_rule",)
        only_fields = (
            "id",
            "name",
            "description",
            "owners_can_see_groups",
            "owners_can_see_members",
            "owners_can_see_members_allowed_information",
        )
