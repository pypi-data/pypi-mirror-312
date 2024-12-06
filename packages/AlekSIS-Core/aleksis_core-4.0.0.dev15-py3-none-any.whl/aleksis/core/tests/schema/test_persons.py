import pytest

from aleksis.core.models import Group, GroupType, Person
from django.contrib.auth.models import Permission


pytestmark = pytest.mark.django_db


def test_persons_query(client_query):
    p = Person.objects.first()
    correct_group_type = GroupType.objects.create(name="correct")
    wrong_group_type = GroupType.objects.create(name="wrong")

    group_not_owner = Group.objects.create(name="not_owner")
    group_correct_group_type_owner = Group.objects.create(name="correct_group_type_owner", group_type=correct_group_type)

    group2_correct_group_type_owner = Group.objects.create(name="correct_group_type_owner", group_type=correct_group_type)
    group_wrong_group_type_owner = Group.objects.create(name="wrong_group_type_owner", group_type=wrong_group_type)
    group_no_group_type_owner = Group.objects.create(name="no_group_type_owner")

    for g in (group_correct_group_type_owner, group2_correct_group_type_owner, group_wrong_group_type_owner, group_no_group_type_owner):
        g.owners.add(p)

    correct_member = Person.objects.create(first_name="correct_member", last_name="correct_member")
    correct_member_2 = Person.objects.create(first_name="correct_member_2", last_name="correct_member_2")
    wrong_member = Person.objects.create(first_name="wrong_member", last_name="wrong_member")

    for g in (group_correct_group_type_owner, group2_correct_group_type_owner):
        g.members.add(correct_member, correct_member_2)

    for g in (group_not_owner, group_wrong_group_type_owner, group_no_group_type_owner):
        g.members.add(wrong_member)



    response, content = client_query(
        "{persons{id}}"
    )
    assert len(content["data"]["persons"]) == 1
    assert content["data"]["persons"][0]["id"] == str(p.id)

    for g in Person.objects.exclude(pk=p.id):
        response, content = client_query(
            "query personById($id: ID) {object: personById(id: $id) { id } }",
            variables={"id": g.id},
        )
        assert content["data"]["object"] == None

    global_permission = Permission.objects.get(codename="view_person", content_type__app_label="core")
    p.user.user_permissions.add(global_permission)

    response, content = client_query(
        "{persons{id}}"
    )
    assert set(int(g["id"]) for g in content["data"]["persons"]) == set(Person.objects.values_list("id", flat=True))

    p.user.user_permissions.remove(global_permission)

    correct_group_type.owners_can_see_members = True
    correct_group_type.save()

    response, content = client_query(
        "{persons{id}}"
    )
    assert set(int(g["id"]) for g in content["data"]["persons"]) == {p.id, correct_member.id, correct_member_2.id}

    for g in (correct_member, correct_member_2):
        response, content = client_query(
            "query personById($id: ID) {object: personById(id: $id) { id } }",
            variables={"id": g.id},
        )
        assert content["data"]["object"]["id"] == str(g.id)

    response, content = client_query(
        "query personById($id: ID) {object: personById(id: $id) { id } }",
        variables={"id": wrong_member.id},
    )
    assert content["data"]["object"] == None
