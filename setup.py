import sys

from os import path
from setuptools import setup, find_packages

__version__ = None
here = path.abspath(path.dirname(__file__))
name = 'pyxarf'

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(path.join(here, 'version.txt')) as f:
    __version__ = f.readline().strip()

with open(path.join(here, 'requirements.txt')) as f:
    requires = f.readlines()

setup(
    author='abusix',
    author_email='info@abusix.com',
    description='pyxarf - easy x-arf report generation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=name,
    packages=find_packages(),
    install_requires=requires,
    python_requires='>=2.7',
    url='http://xarf.org/',
    project_urls={
        'Source': 'https://github.com/xarf/python-xarf',
        'Company': 'https://www.abusix.com/'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Security',
        'License :: OSI Approved :: Apache Software License'

    ],
    keywords = ['keyword', 'search', 'purepython', 'aho-corasick', 'ahocorasick', 'abusix'],
    license='Apache Software License',
    version=__version__,
    scripts=['scripts/xarfutil.py'],
)
