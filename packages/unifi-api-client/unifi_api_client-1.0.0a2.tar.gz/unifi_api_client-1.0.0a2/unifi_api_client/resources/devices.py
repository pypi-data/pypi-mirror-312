from .resources import Resources

class Devices(Resources):

    def __init__(self, api_client: 'UnifiApiClient'):  # type: ignore # noqa: F821
        super().__init__(api_client=api_client, url_segment='devices')

    def get_all(self):
        device_list = self.list()
        return device_list['devices']