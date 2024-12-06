import logging

from .http_client import HttpClient
from .resources import Devices, Hosts, ISPMetrics, Sites

logger = logging.getLogger(__name__)

class UnifiApiClient(HttpClient):
    def __init__(self, api_token: str) -> None:
        """Creates an HttpClient

        Parameters
        ----------
        api_token: a token obtained from https://unifi.ui.com/api
                    format: '3d03892c-fe...'
        """
        unifi_root_url = 'https://api.ui.com/ea/' # TODO: Make configuration item
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_token,
        }

        super().__init__(root_url=unifi_root_url, headers=headers)

        self.devices = Devices(api_client=self)
        self.hosts = Hosts(api_client=self)
        self.isp_metrics = ISPMetrics(api_client=self)
        self.sites = Sites(api_client=self)

    def __repr__(self) -> str:
        return f"{self._root_url}"