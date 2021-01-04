# proxy-finder-client

A python library that implements API to interact with a
[proxy-finder](https://github.com/fomalhaut88/proxy-finder) instance.
It also has proxy pool object to work with a list of proxies easier.

## Installation

```
pip install git+https://github.com/fomalhaut88/proxy-finder-client
```

## Basic example

Getting list of proxies through API:

```python
from proxy_finder import API

api = API("https://proxy.fomalhaut.su/api/v1")  # URL of deployed proxy-finder instance
proxy_list = api.list()

print(proxy_list)
```

## Examples

### API

API supports the methods listed for [proxy-finder](https://github.com/fomalhaut88/proxy-finder#api):

- list
- geo
- check
- version
- licenses

#### list

```python
options = {
    'country': 'US',
    'ordered': True,
    'count': 10
}
proxy_list = api.list(options)
```

Other options are the same as for **proxy-finder**.

#### geo

```python
geo = api.geo('3.80.37.204')
```

#### check

```python
check = api.check('3.80.37.204', 3128)
```

#### version

```python
version = api.version()
```

#### licenses

```python
licenses = api.licenses()
```

### Proxy

A proxy object that contains basic information about the proxy such as host,
port, country, region, city and some other. It can be created directly:

```python
from proxy_finder import Proxy

proxy = Proxy(host='3.80.37.204', port=3128)
```

or from a string:

```python
proxy = Proxy.from_str('3.80.37.204:3128')
```

For other constructor's parameters see documentation in the code.

#### Check proxy

```python
result = proxy.check(api)
```

#### Set geo

```python
proxy.set_geo(api)
```

#### Request through proxy

```python

response = proxy.request(
    url='https://github.com/',
    method='GET',
    scheme='https',
    timeout=3.0
)
```

### Pool

An object that stores a list of proxies and implements some methods to work.

```python
from proxy_finder import Pool

pool = Pool.from_api(api, options={'country': 'US'})
```

#### Get random proxy

```python
proxy = pool.get_random()
```

#### Get several random proxies

```python
proxy_list = pool.get_random_many(10)
```

#### Request multiple URLs using proxy pool

```python
args_list = [
    {'url': 'https://github.com/fomalhaut88/proxy-finder'},
    {'url': 'https://github.com/fomalhaut88/proxy-finder-client'},
    {'url': 'https://github.com/fomalhaut88/mytable'},
    {'url': 'https://github.com/fomalhaut88/mytable-rest-example'},
    {'url': 'https://github.com/fomalhaut88/bcup'},
]
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

result_list = pool.request_many(args_list, headers=headers, scheme='https', timeout=3.0)
```
