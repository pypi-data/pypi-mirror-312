import os
import click

@click.command('test')
@click.option(
    "--username",
    default=lambda: os.environ.get("USER", "")
)
def run(username):
    click.echo(f"Hello, {username}!")