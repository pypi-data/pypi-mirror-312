import logging

logger = logging.getLogger(__name__)


class Resources:

    def __init__(self, api_client: 'UnifiApiClient', url_segment: str):  # type: ignore # noqa: F821
        self._url_segment = url_segment
        self._api_client = api_client

    def list(self):
        response = self._api_client.get_json(f"{self._url_segment}")
        return response['data']
