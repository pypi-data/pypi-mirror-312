from .resources import Resources

class ISPMetrics(Resources):
    def __init__(self, api_client: 'UnifiApiClient'):  # type: ignore # noqa: F821
        # if (interval != '5m' and interval !='1h'):
        #     raise ValueError('Invalid metrics interval. Must be one of: "5m" or "1h". Defaults to "5m".')
        super().__init__(api_client=api_client, url_segment='isp-metrics/5m')