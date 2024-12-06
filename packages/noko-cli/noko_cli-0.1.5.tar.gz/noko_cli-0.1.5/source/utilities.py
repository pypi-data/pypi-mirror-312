"""Collection of utilities for the Noko CLI."""

import json
import os

import click


def read_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)


def write_file(file_path: str, data: dict) -> None:
    with open(file_path, "w") as file:
        json.dump(data, file)


def optional_string_command(text: str) -> str:
    return click.prompt(text, type=str, default="", show_default=False)


def validate_project_name(project: str, projects: list[dict]) -> int | None:
    """Validate that a project exists in Noko and which project to log to if multiple are found.

    Args:
        project (str): The name of the project to validate.
        projects (list[dict]): The list of projects retrieve from Noko to validate against.

    Returns:
        int | None: The ID of the project to log the entry to or None if no project found.
    """
    if not projects:
        click.echo(f"Project {project} not found.")
        return None

    if len(projects) > 1:
        click.echo(f"Multiple projects found with name {project}:\n")
        for idx, proj in enumerate(projects, 1):
            click.echo(f"{idx}. {proj['name']}")

        project_idx = click.prompt("Enter the number of the project you want to log time to", type=int)
        if 1 <= project_idx <= len(projects):
            project_id = projects[project_idx - 1]["id"]
        else:
            click.echo("Invalid project number. I'm out.")
            return None
    else:
        project_id = projects[0]["id"]
    return project_id
