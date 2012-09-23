#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='superwrap',
    license='Apache License 2.0',
    version='0.0.2',
    description="The easy way to contribute to python packages",
    author="Steve Pulec",
    author_email="spulec@gmail.com",
    url="https://github.com/spulec/superwrap",
    requires=(
        'virtualenv',
        'virtualenvwrapper (>=2.9)',
        'requests (>=0.12.1)',
    ),
    namespace_packages=['virtualenvwrapper'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'virtualenvwrapper.pre_activate': [
            'user_scripts = virtualenvwrapper.the_scripts:pre_activate',
        ],
    }
)
