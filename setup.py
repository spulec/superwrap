#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='superwrap',
    version='git',
    description='',
    requires=('virtualenv', 'virtualenvwrapper (>=2.9)'),
    namespace_packages=['virtualenvwrapper'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'virtualenvwrapper.pre_activate': [
            'user_scripts = virtualenvwrapper.the_scripts:pre_activate',
        ],
    }
)
