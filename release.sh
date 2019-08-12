#!/bin/bash

set -e

python setup.py sdist bdist_wheel --universal
twine upload -r pypi-abusix dist/*
rm -r dist/
