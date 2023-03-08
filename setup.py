# -*- coding: utf-8 -*-

import setuptools

from inventree_brother_webapi.version import BROTHER_PLUGIN_VERSION

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-brotherqlwebapi-plugin",

    version=BROTHER_PLUGIN_VERSION,

    author="Jan Krajdl",

    author_email="spm@spamik.cz",

    description="Brother label printer plugin (via web API) for InvenTree",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="inventree label printer printing inventory",

    url="https://github.com/spamik/inventree-brotherqlwebapi-plugin",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
        'brother-ql-inventree',
        'requests'
    ],

    setup_requires=[
        "wheel",
        "twine",
    ],

    python_requires=">=3.9",

    entry_points={
        "inventree_plugins": [
            "BrotherWebAPILabelPlugin = inventree_brother_webapi.brother_plugin:BrotherWebAPILabelPlugin"
        ]
    },
)
