import click

from azure.mgmt.subscription.models import Subscription
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Server

from tai_cli.azure import Azure
from tai_cli.azure.psql import PSQLFlexibleServersManager, PSQLFlexibleServer
from tai_cli.utils.loader import Loader

class RestoreWorkflow:

    def __init__(self, main_color: str='blue') -> None:
        self.az = Azure()
        self.main_color = main_color
        self._selected_subscription = None
        self._selected_server = None

    @property
    def selected_subscription(self) -> Subscription:
        return self._selected_subscription
    
    @selected_subscription.setter
    def selected_subscription(self, subscription: Subscription):
        self._selected_subscription = subscription
    
    @property
    def selected_server(self) -> Server:
        return self._selected_server
    
    @selected_server.setter
    def selected_server(self, server: Server):
        self._selected_server = server

    def run(self, stage: str):
        click.echo(click.style('Iniciando restauración', fg=self.main_color, bold=True))
        with Loader('Cargando subscripciones', '\nSubscripciones', main_color=self.main_color):
            subs: list[str] = [s.display_name for s in self.az.subscriptions]

            if stage:
                subs = [s for s in subs if stage.lower() in s.lower()]
            
        for i, s in enumerate(subs, start=1):
            click.echo(click.style(f'  [{i}]', fg=self.main_color) + s)
        
        selected_subscription: int = click.prompt(
            click.style('\nSelecciona una suscripción', fg=self.main_color),
            type=click.IntRange(min=1, max=len(subs)),
            show_choices=False,
            show_default=True
        )

        self.selected_subscription = self.az.subscriptions[selected_subscription - 1]

        psql = PSQLFlexibleServersManager(self.selected_subscription.subscription_id, self.az)

        with Loader('Cargando servidores', '\nServidores', main_color=self.main_color):
            servers = psql.psql_servers_names

        if servers:
            for i, s in enumerate(servers, start=1):
                click.echo(click.style(f'  [{i}]', fg=self.main_color) + s)
        
        else:
            click.echo(click.style(f'No se han encontrado servidores en {self.selected_subscription.display_name}', fg=self.main_color, bold=True))
            exit()
        
        selected_server = click.prompt(
            click.style('\nSelecciona un servidor', fg=self.main_color),
            default=1,
            type=click.IntRange(min=1, max=len(servers)),
            show_choices=False,
            show_default=True
        )

        self.selected_server = psql.psql_servers[selected_server - 1]

        server = PSQLFlexibleServer(self.selected_server, self.az)

        with Loader('Cargando backups', '\nBackups', main_color=self.main_color):
            backups = server.get_backups()

        for i, b in enumerate(backups, start=1):
            click.echo(click.style(f'  [{i}]', fg=self.main_color) + b.properties.completedTime)
        
        selected_backup: int = click.prompt(
            click.style('\nSelecciona un punto de restauración', fg=self.main_color),
            type=click.IntRange(min=1, max=len(backups)),
            show_choices=False,
            show_default=True
        )

        backup = backups[selected_backup - 1]

        click.echo(click.style("FALTA LÓGICA DE RECUPERACIÓN", fg='red'))

        click.echo(click.style(f"Restaurando {server.name} en {backup.properties.completedTime}...", fg="green"))