"""Log a Noko entry from the CLI."""

import logging
from datetime import datetime, timedelta

import click
from noko_client.client import NokoClient

from source.config import CONFIG
from source.utilities import validate_project_name

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def _process_desc_flags(call: bool, pair: bool, unbillable: bool, description: str) -> str:
    if unbillable:
        description = f"{description} #unbillable"

    if pair:
        description = f"{description} #pair"

    if call:
        description = f"{description} #calls"
    return description


def _set_date_to_yesterday(date: str) -> str:
    return (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")


@click.command()
@click.option(
    "--date",
    default=datetime.today().strftime("%Y-%m-%d"),
    help="Date of the entry in the format YYYY-MM-DD. Defaults to today.",
)
@click.option("-u", "--unbillable", is_flag=True, help="Flag to mark the entry as unbillable.")
@click.option("-p", "--pair", is_flag=True, help="Flag to mark the entry as a pair programming session.")
@click.option("-c", "--call", is_flag=True, help="Flag to mark the entry as a call.")
@click.option("-y", "--yesterday", is_flag=True, help="Flag to mark the entry as yesterday.")
@click.argument("minutes", type=int)
@click.argument("project", type=str)
@click.argument("description", type=str)
def log(
    date: str, minutes: int, project: str, description: str, unbillable: bool, pair: bool, call: bool, yesterday: bool
) -> None:
    """Enables logging an entry to Noko from the CLI.

    Controls the flow of receiving the input, checking for a valid project, confirming if multiple options and logging.
    """
    client = NokoClient(access_token=CONFIG.api_key)

    projects = client.list_projects(enabled=True, name=project)
    project_id = validate_project_name(project, projects)

    if not project_id:
        return

    description = _process_desc_flags(call, pair, unbillable, description)
    if yesterday:
        date = _set_date_to_yesterday(date)

    data = {
        "date": date,
        "minutes": minutes,
        "project_id": project_id,
        "description": description,
        "user_id": CONFIG.user_id,
    }
    response = client.create_entry(**data)
    if response:
        click.echo(f"Entry logged for {date} to project {project} for {minutes} minutes.")
    else:
        click.echo("That didn't work...")


if __name__ == "__main__":
    log()
