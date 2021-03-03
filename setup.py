#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages


setup(
    name='ejtraderDB',
    version=__import__('ejtraderDB').__version__,
    description=(
        'A thread-safe DictSqlite.'
    ),
    long_description=open('README.rst').read(),
    author=__import__('ejtraderDB').__author__,
    author_email='emerson@ejtrader.com',
    maintainer=__import__('ejtraderDB').__author__,
    maintainer_email='support@ejtrader.com',
    license=__import__('ejtraderDB').__license__,
    packages=find_packages(),
    platforms=["all"],
    url='http://github.com/traderpedroso/ejtraderDB',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
)
