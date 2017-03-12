# -*- coding: utf-8 -*-

from setuptools import setup

from undecorated import __version__


with open('README.rst') as readme:
    long_description = readme.read()


setup(
    name='undecorated',
    version=__version__,
    author='Ionuț Arțăriși',
    author_email='ionut@artarisi.eu',
    description='Undecorate python functions, methods or classes',
    long_description=long_description,
    url='https://github.com/mapleoin/undecorated',
    py_modules=['undecorated'],
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python'
    ],
    package_data={
        'undecorated': [
        ]
    }
)
