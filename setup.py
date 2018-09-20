"""pypi package setup."""
from __future__ import print_function
import codecs
from os import path
from setuptools import setup, find_packages
try:
    import ROOT  # pylint: disable=W0611
except ImportError:
    print("ROOT is required by this library.")

HERE = path.abspath(path.dirname(__file__))

with codecs.open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='lhereader',
    version='1.0',
    description='',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='',
    url='',
    author='',
    author_email='',
    classifiers=[
    ],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    zip_safe=False,
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    project_urls={
    }, )
