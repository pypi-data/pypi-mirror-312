import subprocess
import sys

import click
from tai_cli.azure import Azure
from tai_cli.utils.loader import Loader
from tai_cli.workflows.dbrestore import RestoreWorkflow

@click.group(
    help=click.style("Triple Alpha CLI", fg="cyan", bold=True),
    context_settings={"help_option_names": ['-h', '--help']}  # Cambiamos el mensaje de ayuda
)
@click.version_option(
    prog_name=click.style("Triple Alpha CLI"),
    message=f'%(prog)s {click.style(" %(version)s ", fg="blue", bold=True)}',
    help="Versión del CLI."
)
def main():
    pass

@main.command(help=click.style("Actualiza tai-cli", fg="blue"))
def upgrade():
    subprocess.check_output([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    r = subprocess.check_output([sys.executable, "-m", "pip", "install", "tai-cli", "-U"])
    click.echo(r)

@click.group(help=click.style("Gestión de Azure Cloud", fg="blue"))
def az():
    pass

@az.command(help=click.style("Subscripciones", fg="blue"))
@click.option('--stage', '-s', required=False, type=click.Choice(['pro', 'pre', 'dev'], case_sensitive=False), help=click.style("Entorno", fg="blue"))
def subscriptions(stage: str):

    main_color = 'blue'
    az = Azure()

    with Loader('Cargando subscripciones', '\nSubscripciones', main_color=main_color):
        subs: list[str] = [s.display_name for s in az.subscriptions]

        if stage:
            subs = [s for s in subs if stage.lower() in s.lower()]
        
    for i, s in enumerate(subs, start=1):
        click.echo(click.style(f'  [{i}]', fg=main_color) + s)

@click.group(help=click.style("Gestión de bases de datos", fg="blue"))
def db():
    pass

@db.command(help=click.style("Restaura un backup de una base de datos", fg="blue"))
@click.option('--stage', '-s', required=False, type=click.Choice(['pro', 'pre', 'dev'], case_sensitive=False), help=click.style("Entorno", fg="blue"))
def restore(stage: str):
    """
    Restaura un backup de una base de datos
    """
    RestoreWorkflow().run(stage)

# Registra el grupo 'db' como subcomando de 'main'
main.add_command(az)
az.add_command(db)
db.add_command(restore)