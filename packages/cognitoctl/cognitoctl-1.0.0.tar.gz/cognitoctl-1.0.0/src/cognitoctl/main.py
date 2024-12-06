# flake8: noqa
import click
from cognitoctl.commands import init
from cognitoctl.commands import user as user_commands
from cognitoctl.commands import group as group_commands
from cognitoctl.commands import config as config_commands


@click.group()
def cli():
    pass


@cli.group()
def user():
    """
    Manage Cognito users.

    Provides a set of actions to create, confirm, delete, enable, disable,
    retrieve, and manage user passwords in AWS Cognito. You can also list
    users with optional filters.
    """
    pass


@cli.group()
def group():
    """
    Manage Cognito groups.

    This set of commands allows you to create, edit, delete, and manage users
    in Cognito groups. You can list groups and manage their properties like
    description, precedence, and role ARN.
    """
    pass


@cli.group()
def config():
    """
    Manage configuration projects.

    This group of commands allows you to list, set, get, edit, and delete
    configuration projects. You can also view and modify specific settings
    within a project.
    """
    pass


cli.add_command(init)
commands_by_group = {
    user: user_commands,
    group: group_commands,
    config: config_commands
}

for group, commands in commands_by_group.items():
    for name, cmd in commands.__dict__.items():
        if isinstance(cmd, click.Command):
            group.add_command(cmd)
