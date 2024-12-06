import click
from cognitopy import CognitoPy
from cognitopy.exceptions import ExceptionAuthCognito
from cognitoctl.commands import init_cognitopy


@click.command()
@click.option("--username", "-u", required=True, type=str, help="Username of the user to create.")
@click.option("--password", "-p", required=True, type=str, help="Password for the user.")
@init_cognitopy
def create(cognitopy: CognitoPy, username: str, password: str):
    """
    Create a new user in Cognito.
    """
    try:
        cognitopy.register(username=username, password=password)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User registered successfully")


@click.command()
@click.option("--username", "-u", required=True, type=str, help="Username of the user to confirm.")
@click.option("--code", "-c", required=False, type=str, help="Confirmation code provided to the user.")
@click.option("--force", "-f", is_flag=True, help="Force confirmation without a code.")
@init_cognitopy
def confirm(cognitopy: CognitoPy, username: str, code: str, force: bool):
    """
    Confirm a user's registration in Cognito.

    Use the confirmation code provided to the user or force the confirmation
    using administrative privileges.
    """
    try:
        if force:
            cognitopy.admin_confirm_register(username=username)
        else:
            if code:
                cognitopy.confirm_register(username=username, confirmation_code=code)
            else:
                click.echo("Confirmation code is required")
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User confirmed successfully")


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def delete(cognitopy: CognitoPy, username: str):
    """
    Delete a user from Cognito.
    """
    try:
        cognitopy.admin_delete_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User deleted successfully")


@click.command()
@click.option("--username", "-u", required=True, type=str, help="Username of the user.")
@click.option("--previous", "-r", required=True, type=str, help="Current or previous password.")
@click.option("--password", "-p", required=True, type=str, help="New password.")
@init_cognitopy
def change_password(cognitopy: CognitoPy, username: str, previous: str, password: str):
    """
    Change the password of an existing user.
    """
    try:
        tokens = cognitopy.login(username=username, password=previous)
        cognitopy.change_password(previous_password=previous, proposed_password=password,
                                  access_token=tokens["access_token"])
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User deleted successfully")


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def enable(cognitopy: CognitoPy, username: str):
    """
    Enable a disabled user in Cognito.
    """
    try:
        cognitopy.admin_enable_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User enabled successfully")


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def disable(cognitopy: CognitoPy, username: str):
    """
    Disable an active user in Cognito.
    """
    try:
        cognitopy.admin_disable_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User disabled successfully")


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def get(cognitopy: CognitoPy, username: str):
    """
    Retrieve details of a specific user.
    """
    try:
        user = cognitopy.admin_get_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for key, value in user.items():
            click.echo(f"{key}: {value}")


@click.command()
@click.option("--group", "-g", required=False, type=str, help="Filter users by group name.")
@click.option("--limit", "-l", required=False, type=int, help="Limit the number of users displayed.")
@init_cognitopy
def list(cognitopy: CognitoPy, group: str, limit: int):
    """
    List users in Cognito.

    Optionally filter users by group or limit the number of results displayed.
    """
    try:
        users = cognitopy.list_users(group=group, limit=limit)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for user in users:
            for key, value in user.items():
                click.echo(f"{key}: {value}")
            click.echo("--------------------------------\n")
        click.echo(f"Total users: {len(users)}")
