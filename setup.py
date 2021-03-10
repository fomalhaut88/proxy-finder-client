from setuptools import setup

with open('proxy_finder/version.py') as f:
    __version__ = f.read().split('=', 1)[1].strip()


setup(
    name='proxy_finder',
    version=__version__,
    description="API to interact with a proxy-finder instance (https://github.com/fomalhaut88/proxy-finder).",
    author='Alexander Khlebushchev',
    packages=[
        'proxy_finder',
    ],
    zip_safe=False,
    install_requires=['requests==2.25.1', 'aiohttp==3.7.4.post0'],
)
