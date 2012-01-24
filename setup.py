# Copyright (c) 2011-2012 Simplistix Ltd
# See license.txt for license details.

import os
from setuptools import setup, find_packages

name = 'nose_fixes'

setup(
    name=name,
    version='1.2',
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="A plugin to make nose behave better.",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'docs','description.txt')).read(),
    url='http://packages.python.org/'+name,
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    ],    
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'nose',
        'setuptools', # so nose's EntryPointPluginManager gets used
        ],
    entry_points = {
        'nose.plugins.0.10': [
            'nose_fixes = nose_fixes.plugin:Plugin'
            ]
        },
    )
