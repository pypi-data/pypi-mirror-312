"""Sync google calendar events with noko entries."""

import logging
from datetime import datetime

import click
from noko_client.client import NokoClient

from source.config import CONFIG, CREDENTIALS
from source.utilities import optional_string_command, validate_project_name

from .get_events import get_calendar_events
from .schemas import CalendarEvent

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def _clean_idx_input(indexes: str) -> list[int]:
    idx_list = indexes.split(",")
    return [int(idx) for idx in idx_list if idx]


def _process_entries_to_remove() -> list[int]:
    remove_entries_idx = optional_string_command(
        "Select entries to remove by providing the desired numbers separated by commas. Hit return to proceed with these entries",  # noqa: E501
    )
    return _clean_idx_input(remove_entries_idx)


def _process_entries_to_change(events: list[CalendarEvent], remove_entries_list: list[int]) -> list[int]:
    if CONFIG.default_noko_project:
        change_entries_idx = optional_string_command(
            "Select entries to change by providing the desired numbers separated by commas. Hit return to log as is",
        )
        change_entries_list = _clean_idx_input(change_entries_idx)
    else:
        change_entries_list = [idx for idx in range(1, len(events) + 1) if idx not in remove_entries_list]

    return change_entries_list


def _get_updated_event(client: NokoClient, events: list[CalendarEvent], entry: int) -> CalendarEvent:
    event = next(event for event in events if event.idx == entry)
    change = click.prompt(f"Entry: {event.idx} - {event.duration} - {event.project} - {event.summary} {event.tag}")
    changes = change.strip().split(",")
    changes = list(zip(changes[::2], changes[1::2]))
    for change in changes:
        match change[0]:
            case "p":
                projects = client.list_projects(name=change[1], enabled=True)
                project_id = validate_project_name(change[1], projects)
                if not project_id:
                    continue
                event.project = project_id
            case "m":
                event.duration = change[1]
            case "d":
                event.summary = change[1]
    return event


def _log_entry(client: NokoClient, date: str, event: CalendarEvent) -> None:
    data = {
        "date": date,
        "user_id": CONFIG.user_id,
        "minutes": event.duration,
        "description": f"{event.summary}{event.tag}",
    }
    if isinstance(event.project, str):
        data["project_name"] = event.project
    elif isinstance(event.project, int):
        data["project_id"] = event.project
    else:
        raise ValueError("Invalid project. Provide a name as a string or ID as an integer.")
    client.create_entry(**data)


@click.command()
@click.option("-d", "--date", default=datetime.today().strftime("%Y-%m-%d"), help="Date to fetch events from.")
def sync(date: str) -> None:
    """Enable the call-sync CLI command.

    Accepts a date parameter that defaults to today. Controls the flow of:

    - Fetching all valid events
    - Prompting the user for validation (remove and change)
    - Controlling the change flow
    - Creating the entries in Noko
    """
    if not CONFIG.google_cal_id or not CREDENTIALS:
        click.echo(
            "Google credentials not found or google cal ID not provided. Add a valid credentials.json file first or run setup to set the calendar ID."  # noqa: E501
        )
        return

    events = get_calendar_events(date=date)
    if not events:
        click.echo("No events found...")
        return

    click.echo("These are the entries that will be logged.")
    for idx, event in enumerate(events, 1):
        event.idx = idx
        click.echo(f"{idx}. {date} - {event.duration} minutes - {event.project} - {event.summary} {event.tag}")

    entries_to_remove = _process_entries_to_remove()
    if len(entries_to_remove) == len(events):
        click.echo("All entries have been removed.")
        return

    if entries_to_remove:
        events = [event for event in events if event.idx not in entries_to_remove]

    entries_to_change = _process_entries_to_change(events, entries_to_remove)

    client = NokoClient(CONFIG.api_key)

    if not entries_to_change:
        for event in events:
            _log_entry(client, date, event)
        click.echo(f"{len(events)} logged to Noko for date {date}.")
        return

    events_to_log = [event for event in events if event.idx not in entries_to_change]
    click.echo("Logging events without change...")
    for event in events_to_log:
        _log_entry(client, date, event)

    click.echo(
        "Only project, minutes, description, and tag can be changed. Enter p, m, d, or t followed by the change, separated by a comma. You can enter more than one pair a time."  # noqa: E501
    )
    for entry in entries_to_change:
        event = _get_updated_event(client, events, entry)
        _log_entry(client, date, event)
    click.echo(f"{len(events)} entries logged to Noko for date {date}.")


if __name__ == "__main__":
    sync()
