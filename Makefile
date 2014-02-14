AUTHOR:=$(shell python setup.py --author)
AUTHOR_EMAIL:=$(shell python setup.py --author-email)
VERSION:=$(shell python setup.py --version)
NAME:=$(shell python setup.py --name)
MAINTAINER:="${AUTHOR} <${AUTHOR_EMAIL}>"

all: clean package

clean:
	rm -f *.deb
	rm -fr build
	rm -fr *.egg-info
	rm -fr dist
	find . -name '*.pyc' -delete
	rm -fr dist_eggs
	rm -fr docs/html
	rm -fr docs/doctrees

package: clean
	python setup.py bdist_egg --exclude-source-files

release: clean
	python setup.py bdist_egg --exclude-source-files sdist upload -r ${AIX_RELEASES_URL}

register:
	python setup.py register -r ${AIX_RELEASES_URL}

docs:
	python setup.py build_sphinx

docs-release: docs
	scp -r docs/html/* ${AIX_DOCS_PATH}/${NAME}/${VERSION}/

.PHONY: clean package release register docs