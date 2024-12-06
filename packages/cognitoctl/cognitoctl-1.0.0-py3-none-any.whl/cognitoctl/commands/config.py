import click
from cognitoctl.config import Config
from cognitoctl.exceptions import ExceptionCLIValidateConfig


@click.command()
def list():
    """
    List all configuration projects.

    This command displays a list of all available configuration projects.
    """
    projects = Config.get_projects()
    click.echo("Projects:")
    for project in projects:
        click.echo(f" - {project}")


@click.command()
def current():
    """
    Show the current configuration project.

    This command displays the name of the currently active configuration project.
    """
    click.echo(f"Current project: {Config().name}")


@click.command()
@click.argument("name", type=str)
def set(name: str):
    """
    Set the current configuration project.

    This command sets the specified project as the active configuration project.
    """
    try:
        Config.set_name(name)
    except ExceptionCLIValidateConfig as e:
        click.echo(e)
    else:
        click.echo(f"Set current project to {name}")


@click.command()
@click.argument("name", type=str)
def get(name: str):
    """
    Get details of a specific configuration project.

    This command retrieves and displays the properties of a specified
    configuration project.
    """
    try:
        config = Config(name=name)
        click.echo(f"Config {name}: ")
        properties_dict = {attr: getattr(config, attr) for attr in dir(config)
                           if isinstance(getattr(type(config), attr, None), property) and attr != "name"}
        for key, value in properties_dict.items():
            click.echo(f" - {key}: {value}")
    except ExceptionCLIValidateConfig as e:
        click.echo(e)


@click.command()
@click.argument("name", type=str)
def delete(name: str):
    """
    Delete a configuration project.

    This command permanently deletes the specified configuration project.
    """
    try:
        Config.delete(name)
    except ExceptionCLIValidateConfig as e:
        click.echo(e)
    else:
        click.echo(f"Deleted config {name}")


@click.command()
@click.argument("name", type=str)
@click.option("key", "-k", type=str, required=True, help="The key of the configuration setting to edit.")
@click.option("value", "-v", type=str, required=True, help="The new value for the configuration setting.")
def edit(name: str, value: str, key: str):
    """
    Edit a configuration setting in a project.

    This command modifies a specific setting within the configuration project
    by updating the value of the specified key.
    """
    try:
        Config.edit(name=name, field=key, value=value)
    except ExceptionCLIValidateConfig as e:
        click.echo(e)
    else:
        click.echo(f"Edited config {name}")
