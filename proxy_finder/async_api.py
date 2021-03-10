import os

import aiohttp

from .utils import prepare_list_params


# Default timeout for requests to proxy-finder instance
DEFAULT_TIMEOUT = 5.0


class AsyncAPI:
    """
    Asynchronous API object to interact with a proxy-finder instance.
    The methods implemented are the same as described for proxy-finder.
    """

    def __init__(self, root, timeout=DEFAULT_TIMEOUT):
        self._root = root
        self._timeout = timeout

    async def list(self, options={}):
        """
        List of available proxies.
        """
        params = prepare_list_params(options)
        return await self._get('list', params)

    async def geo(self, host):
        """
        Geo information of the host.
        """
        return await self._get(f'geo/{host}')

    async def check(self, host, port):
        """
        Checks host and port for HTTPS proxy.
        """
        return await self._get(f'check/{host}:{port}')

    async def version(self):
        """
        Version of proxy-finder instance.
        """
        return await self._get('version')

    async def licenses(self):
        """
        Licenses used in proxy-finder.
        """
        return await self._get('licenses')

    async def _get(self, url, params={}):
        full_url = os.path.join(self._root, url)

        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, params=params,
                                   timeout=self._timeout) as response:
                if response.headers['Content-Type'] == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
