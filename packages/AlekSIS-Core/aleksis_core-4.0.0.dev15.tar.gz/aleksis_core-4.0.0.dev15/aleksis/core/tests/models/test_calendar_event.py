from datetime import datetime, timezone

import pytest
from aleksis.core.models import CalendarEvent
from recurrence import Recurrence, WEEKLY, Rule

from zoneinfo import ZoneInfo

pytestmark = pytest.mark.django_db


def test_calendar_event_timezone():
    datetime_start = datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc).astimezone(ZoneInfo("Europe/Berlin"))
    datetime_end = datetime(2024, 12, 31, 0, 0, tzinfo=timezone.utc).astimezone(ZoneInfo("Europe/Berlin"))

    # No timezone set
    calendar_event = CalendarEvent.objects.create(datetime_start=datetime_start, datetime_end=datetime_end)
    calendar_event.refresh_from_db()

    assert calendar_event.datetime_start == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert calendar_event.datetime_end == datetime(2024, 12, 31, 0, 0, tzinfo=timezone.utc)
    assert CalendarEvent.value_start_datetime(calendar_event) == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert CalendarEvent.value_end_datetime(calendar_event) == datetime(2024, 12, 31, 0, 0, tzinfo=timezone.utc)
    assert calendar_event.timezone is None

    # Set timezone if not allowed
    calendar_event.timezone = ZoneInfo("Europe/Berlin")
    calendar_event.save()
    calendar_event.refresh_from_db()
    assert calendar_event.timezone is None

    # Automatically set timezone
    calendar_event.datetime_start = datetime_start
    calendar_event.datetime_end = datetime_end
    calendar_event.recurrences = Recurrence(dtstart=datetime_start, rrules=[Rule(WEEKLY)])
    calendar_event.save()
    calendar_event.refresh_from_db()

    assert calendar_event.datetime_start == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert calendar_event.datetime_end == datetime(2024, 12, 31, 0, 0, tzinfo=timezone.utc)
    assert CalendarEvent.value_start_datetime(calendar_event) == datetime_start
    assert CalendarEvent.value_end_datetime(calendar_event) == datetime_end
    assert calendar_event.timezone == ZoneInfo("Europe/Berlin")

    # Manually set timezone (e. g. from frontend)
    calendar_event.timezone = ZoneInfo("Europe/Berlin")
    calendar_event.save()
    calendar_event.refresh_from_db()
    assert calendar_event.timezone == ZoneInfo("Europe/Berlin")
