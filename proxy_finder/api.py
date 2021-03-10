import os

import requests

from .utils import prepare_list_params


# Default timeout for requests to proxy-finder instance
DEFAULT_TIMEOUT = 5.0


class API:
    """
    API object to interact with a proxy-finder instance. The methods
    implemented are the same as described for proxy-finder.
    """

    def __init__(self, root, timeout=DEFAULT_TIMEOUT):
        self._root = root
        self._timeout = timeout

    def list(self, options={}):
        """
        List of available proxies.
        """
        params = prepare_list_params(options)
        return self._get('list', params)

    def geo(self, host):
        """
        Geo information of the host.
        """
        return self._get(f'geo/{host}')

    def check(self, host, port):
        """
        Checks host and port for HTTPS proxy.
        """
        return self._get(f'check/{host}:{port}')

    def version(self):
        """
        Version of proxy-finder instance.
        """
        return self._get('version')

    def licenses(self):
        """
        Licenses used in proxy-finder.
        """
        return self._get('licenses')

    def _get(self, url, params={}):
        full_url = os.path.join(self._root, url)
        with requests.get(full_url, params=params,
                          timeout=self._timeout) as response:
            if response.headers['Content-Type'] == 'application/json':
                return response.json()
            else:
                return response.text
