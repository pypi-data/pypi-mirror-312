import subprocess
import logging
from azure.identity import AzureCliCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.subscription.models import Subscription

class Azure:

    def __init__(self) -> None:
        self._subscriptions = None
        self._token = None
        logger = logging.getLogger("azure.identity")
        logger.propagate = False

        try:
            creds = AzureCliCredential()
            creds.get_token("https://management.azure.com/.default")
        except:
            subprocess.check_call(["az", "login"])
            creds = AzureCliCredential()
        finally:
            self._credentials = creds

    @property
    def credentials(self):
        return self._credentials
    
    @property
    def token(self):
        if not self._token:
            self._token = self.credentials.get_token("https://management.azure.com/.default").token
        return self._token
    
    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}
    
    @property
    def subscription_client(self):
        return SubscriptionClient(self.credentials)
    
    @property
    def subscriptions(self) -> list[Subscription]:
        if not self._subscriptions:
            self._subscriptions = [s for s in self.subscription_client.subscriptions.list()]
        return self._subscriptions
