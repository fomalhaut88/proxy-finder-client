import requests
import aiohttp


class Proxy:
    """
    Proxy object.
    """

    def __init__(self, host, port, country=None, region=None, city=None,
                 score=None, created_at=None, last_check_at=None):
        self.host = host
        self.port = port
        self.country = country
        self.region = region
        self.city = city
        self.score = score
        self.created_at = created_at
        self.last_check_at = last_check_at

    def __repr__(self):
        return f"{self.host}:{self.port}"

    @classmethod
    def from_str(cls, s):
        """
        Creates a proxy object from a string of kind <host>:<port>
        (example: "3.80.37.204:3128")
        """
        host, port = s.split(':', 1)
        return cls(host=host, port=int(port))

    def request(self, url, method='GET', scheme='https', params={}, data={},
                headers={}, timeout=None):
        """
        Requests the URL through the proxy with the given parameters.
        """
        proxies = {scheme: f"http://{self.host}:{self.port}"}
        func = getattr(requests, method.lower())
        return func(url, proxies=proxies, params=params, data=data,
                    headers=headers, timeout=timeout)

    async def request_async(self, url, method='GET', scheme='https', params={},
                            data={}, headers={}, timeout=None):
        """
        Asynchronous requests the URL through the proxy with the given
        parameters. The method builds and returns Response object from
        'requests' in order to finalize the asynchronous session correctly.
        """
        proxy = f"http://{self.host}:{self.port}"
        async with aiohttp.ClientSession() as session:
            func = getattr(session, method.lower())
            async with func(url, proxy=proxy, params=params, data=data,
                                 headers=headers, timeout=timeout) as response:
                response_from_requests = requests.models.Response()
                response_from_requests.url = response.url
                response_from_requests.cookies = response.cookies
                response_from_requests.history = response.history
                response_from_requests.reason = response.reason
                response_from_requests.headers = response.headers
                response_from_requests.status_code = response.status
                response_from_requests._content = await response.content.read()
                return response_from_requests


    def check(self, api):
        """
        Checks proxy by API object.
        """
        return api.check(self.host, self.port)['result']

    async def check_async(self, api):
        """
        Asynchronous checks proxy by API object.
        """
        return (await api.check(self.host, self.port))['result']

    def set_geo(self, api):
        """
        Sets geo information using API object.
        """
        geo = api.geo(self.host)['geo']
        self.country = geo['country']
        self.region = geo['region']
        self.city = geo['city']

    async def set_geo_async(self, api):
        """
        Asynchronous sets geo information using API object.
        """
        geo = (await api.geo(self.host))['geo']
        self.country = geo['country']
        self.region = geo['region']
        self.city = geo['city']
