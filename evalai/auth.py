import click

from click import echo


@click.command()
def auth():
    """Example script."""
    echo('Hello auth!')
