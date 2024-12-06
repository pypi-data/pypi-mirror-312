import os

import click

from source.constants import SAVE_DIRECTORY
from source.utilities import optional_string_command, write_file


@click.command()
def setup() -> None:
    click.echo(
        "To set up the Noko CLI app you'll need a valid Noko API key and user ID. To skip an optional configuration, hit return on the prompt."
    )

    config = {
        "api_key": click.prompt("Your Noko API key", type=str),
        "user_id": click.prompt("Your Noko user ID", type=str),
        "default_noko_project": optional_string_command("Your default Noko project's name. Hit return to skip it"),
        "default_noko_tag": optional_string_command("Your default Noko tag. Hit return to skip it"),
    }
    os.makedirs(SAVE_DIRECTORY, exist_ok=True)
    config_file_path = os.path.join(SAVE_DIRECTORY, "config.json")
    write_file(config_file_path, config)
