import os

import requests


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
        params = self._prepare_list_params(options)
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

    def _prepare_list_params(self, options):
        params = {}
        self._dict_pass_value(options, params, 'country')
        self._dict_pass_value(options, params, 'region')
        self._dict_pass_value(options, params, 'city')
        self._dict_pass_value(options, params, 'count', str)
        self._dict_pass_value(options, params, 'score', str)
        self._dict_pass_value(options, params, 'ordered',
                              lambda x: '1' if x else '')
        self._dict_pass_value(options, params, 'format')
        return params

    @classmethod
    def _dict_pass_value(cls, src_dict, dst_dict, key, modifier=None):
        if modifier is None:
            modifier = lambda x: x
        if key in src_dict:
            dst_dict[key] = modifier(src_dict[key])
