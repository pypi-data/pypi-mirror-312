import requests as rq
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Server

from pydantic import BaseModel

from tai_cli.azure import Azure

class BackupProperties(BaseModel):
    backupType: str
    source: str
    completedTime: str

class Backup(BaseModel):
    properties: BackupProperties
    id: str
    name: str
    type: str

class PSQLFlexibleServersManager:

    def __init__(self, subscription_id, az: Azure) -> None:
        self.az = az
        self.subscription_id = subscription_id
        self.client = PostgreSQLManagementClient(self.az.credentials, self.subscription_id)
        self._servers = None
    
    @property
    def psql_servers(self) -> list[Server]:
        if not self._servers:
            self._servers = [server for server in self.client.servers.list()]
        return self._servers
    
    @property
    def psql_servers_names(self):
        return [server.name for server in self.psql_servers]


class PSQLFlexibleServer:

    def __init__(self, server: Server, az: Azure) -> None:
        self.server = server
        self.az = az

    @property
    def name(self):
        return self.server.name
    
    @property
    def subscription_id(self):
        return self.server.id.split("/")[2]

    @property
    def resource_group(self):
        return self.server.id.split("/")[4]
    
    def get_backups(self) -> list[Backup]:
        url = "https://management.azure.com" \
            f"/subscriptions/{self.subscription_id}" \
            f"/resourceGroups/{self.resource_group}" \
            "/providers/Microsoft.DBforPostgreSQL" \
            f"/flexibleServers/{self.server.name}" \
            "/backups" \
            "?api-version=2023-03-01-preview"

        try:
            raw_response = rq.get(url, headers=self.az.headers)
            raw_response.raise_for_status()

            response = []

            for r in raw_response.json()['value']:
                response.append(Backup.model_validate(r))

            return response

        except Exception as e:
            print(e)


