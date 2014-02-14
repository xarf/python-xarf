import os
import sys
from setuptools import setup, find_packages

__version__ = None
here = os.path.abspath(os.path.dirname(__file__))
name = 'pyxarf'

with open('%s/version.txt' % here) as f:
    __version__ = f.readline().strip()

with open('%s/requirements.txt' % here) as f:
    requires = f.readlines()

if len(sys.argv) > 1:
    if sys.argv[1] == 'develop':
        with open('%s/requirements-develop.txt' % here) as f:
            requires += f.readlines()
    elif sys.argv[1] == 'build_sphinx':
        with open('%s/docs/conf.py' % here, 'w') as f:
            f.write('''
# -*- coding: utf-8 -*-
import os
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
master_doc = 'index'
project = '{name}'
copyright = 'abusix GmbH'
version = '{version}'
release = '{version}'
exclude_patterns = ['docs', 'scripts', 'tests', 'extras']
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = ['_themes',]
#html_logo = None
htmlhelp_basename = '{name}doc'
os.path.abspath('../{name}/')
    '''.format(name=name, version=__version__)
            )


setup(
    name=name,
    version=__version__,
    description=name,
    long_description='pyxarf - easy x-arf report generation',
    author='abusix GmbH',
    author_email='info@abusix.com',
    url='https://abusix.com/',
    keywords='xarf arf mail report',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Security',
    ],
    scripts=['scripts/xarfutil.py'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
