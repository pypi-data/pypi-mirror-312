from .resources import Resources

class Hosts(Resources):

    def __init__(self, api_client: 'UnifiApiClient'):  # type: ignore # noqa: F821
        super().__init__(api_client=api_client, url_segment='hosts')