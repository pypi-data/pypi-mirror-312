import click
from cognitopy import CognitoPy
from cognitopy.exceptions import ExceptionAuthCognito
from cognitoctl.commands import init_cognitopy


@click.command()
@click.option("name", "-n", required=True, type=str, help="The name of the group.")
@click.option("description", "-d", required=True, type=str, help="The description of the group.")
@click.option("precedence", "-p", required=True, type=int, help="The precedence of the group.")
@click.option("role_arn", "-r", required=True, type=str, help="The ARN of the role associated with the group.")
@init_cognitopy
def create(cognitopy: CognitoPy, name: str, description: str, precedence: int, role_arn: str):
    """
    Create a new group in Cognito.

    The group will have a unique name, description, precedence value, and an associated role ARN.
    """
    try:
        cognitopy.admin_create_group(group_name=name, description=description, precedence=precedence, role_arn=role_arn)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("Group created successfully")


@click.command()
@click.argument("name", type=str)
@init_cognitopy
def delete(cognitopy: CognitoPy, name: str):
    """
    Delete a group from Cognito.

    The group will be permanently deleted and cannot be recovered.
    """
    try:
        cognitopy.admin_delete_group(group_name=name)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("Group deleted successfully")


@click.command()
@click.option("username", "-u", required=True, type=str, help="Username to remove from the group.")
@click.option("group", "-g", required=True, type=str, help="The name of the group.")
@init_cognitopy
def delete_user(cognitopy: CognitoPy, username: str, group: str):
    """
    Remove a user from a specific group.

    The user will no longer belong to the specified group in Cognito.
    """
    try:
        cognitopy.admin_remove_user_from_group(group_name=group, username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo(f"User {username} deleted of group {group} successfully")


@click.command()
@click.option("username", "-u", required=True, type=str, help="Username to add to the group.")
@click.option("group", "-g", required=True, type=str, help="The name of the group.")
@init_cognitopy
def add_user(cognitopy: CognitoPy, username: str, group: str):
    """
    Add a user to a specific group.

    The user will be added to the specified group in Cognito.
    """
    try:
        cognitopy.admin_add_user_to_group(username=username, group_name=group)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User added to group successfully")


@click.command()
@click.option("--username", "-u", required=False, type=str, help="Filter by username to list groups.")
@click.option("--limit", "-l", required=False, type=int, help="Limit the number of groups returned.")
@init_cognitopy
def list(cognitopy: CognitoPy, username: str, limit: int):
    """
    List all groups, optionally filtered by a user.

    This command can return all groups or filter them by a specific user and/or
    limit the number of results.
    """
    try:
        if username:
            groups = cognitopy.admin_list_groups_for_user(username=username, limit=limit)
        else:
            groups = cognitopy.list_groups(limit=limit)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for group in groups:
            for key, value in group.items():
                click.echo(f"{key}: {value}")
            click.echo("--------------------------------\n")
        click.echo(f"Total groups: {len(groups)}")


@click.command()
@click.argument("group", type=str)
@init_cognitopy
def get(cognitopy: CognitoPy, group: str):
    """
    Retrieve the details of a specific group.

    This command returns the attributes and configuration of the specified group.
    """
    try:
        user = cognitopy.get_group(group=group)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for key, value in user.items():
            click.echo(f"{key}: {value}")


@click.command()
@click.option("--group", "-g", required=True, type=str, help="The name of the group to edit.")
@click.option("--description", "-d", required=False, type=str, help="Updated description for the group.")
@click.option("--role", "-r", required=False, type=str, help="Updated role ARN for the group.")
@click.option("--precedence", "-p", required=False, type=int, help="Updated precedence for the group.")
@init_cognitopy
def edit(cognitopy: CognitoPy, group: str, description: str, role: str, precedence: int):
    """
    Edit an existing group's details.

    You can update the description, role, and precedence of the group.
    """
    try:
        cognitopy.update_group(group=group, description=description, role=role, precedence=precedence)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("Edited group successfully")
