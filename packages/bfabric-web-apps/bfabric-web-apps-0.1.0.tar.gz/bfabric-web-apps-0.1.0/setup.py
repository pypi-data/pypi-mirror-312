# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bfabric_web_apps', 'bfabric_web_apps.layouts', 'bfabric_web_apps.objects']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bfabric-web-apps',
    'version': '0.1.0',
    'description': 'A package containing handy boilerplate utilities for developing bfabric web-applications',
    'long_description': None,
    'author': 'Mark Zuber, Griffin White, GWC GmbH',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
