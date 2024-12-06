"""Google Calendar event retrieval and validation."""

import logging
from dataclasses import fields

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from source.config import CONFIG, CREDENTIALS

from .schemas import CalendarEvent

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def _get_events_from_calendar(start_date: str, end_date: str) -> list[dict]:
    creds = Credentials.from_authorized_user_info(CREDENTIALS, scopes=CONFIG.scopes)
    service = build("calendar", "v3", credentials=creds)
    calendar_events = (
        service.events().list(calendarId=CONFIG.google_cal_id, timeMin=start_date, timeMax=end_date).execute()
    )
    return calendar_events.get("items", [])


def _remove_invalid_events(events: list[dict]) -> list[dict]:
    keys_to_keep = [field.name for field in fields(CalendarEvent)]
    valid_events = []
    for event in events:
        if event.get("eventType", "") in CONFIG.keep_event_types:
            valid_events.append(
                {k: v if k not in ["start", "end"] else v["dateTime"] for k, v in event.items() if k in keys_to_keep}
            )
    return [event for event in valid_events if event["status"] == "confirmed"]


def _eliminate_repeated_events(objects: list[CalendarEvent]) -> list[CalendarEvent]:
    seen = set()
    unique_objects = []

    for obj in objects:
        prop_value = getattr(obj, "summary")
        if prop_value not in seen:
            unique_objects.append(obj)
            seen.add(prop_value)

    return unique_objects


def get_calendar_events(date: str) -> list[CalendarEvent]:
    """Retrieve, clean and validate google calendar events for a specific date.

    Args:
        date (str): The date to retrieve events for as an ISO 8601 string (YYYY-MM-DD).

    Returns:
        list[CalendarEvent]: A list of formatted Google Calendar events for a given date.
    """
    start_date = f"{date}T00:00:00-03:00"
    end_date = f"{date}T23:59:59-03:00"

    events = _get_events_from_calendar(start_date, end_date)
    events = _remove_invalid_events(events)
    calendar_events = [CalendarEvent(**event) for event in events]

    return _eliminate_repeated_events(calendar_events)
