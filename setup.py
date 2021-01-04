from setuptools import setup

from proxy_finder import __version__


setup(
    name='proxy_finder',
    version=__version__,
    description="API to interact with a proxy-finder instance (https://github.com/fomalhaut88/proxy-finder).",
    author='Alexander Khlebushchev',
    packages=[
        'proxy_finder',
    ],
    zip_safe=False,
    install_requires=['requests==2.25.1'],
)
