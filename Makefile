# Simple Makefile for building the RPM / testing
# Author: Michael DeGuzis

USERHOME = $(shell echo ${HOME})

all: usage

usage:
	@echo -e "\nPython API util for Icinga2: "
	@echo "Usage: "
	@echo "make <OPTIONS>"
	@echo "    dev: build virtual environment for dev work (pipenv)"
	@echo "    rpm: Build RPM for project"
	@echo "    install: Install RPM for project"
	@echo "    uninstall: Uninstall RPM for project and remove virtual env"

# Note: setup.py needs fixed for this, name is "NAME" in setup file.
install:
	@echo "Installing RPM package"
	sudo rpm -i dist/python-icinga2api-*.noarch.rpm

install-venv:
	pip install --user --upgrade setuptools
	pip install --user pipenv
	pipenv install --dev
	pipenv run pip install -e .

rpm:
	@echo "Bulding RPM"
	@python setup.py bdist_rpm
	@echo -e "\nRPM build complete. RPM: "
	@find $(CURDIR) -name "*.rpm"
	@find build/ -name "*.spec" -exec cp -v {} $(CURDIR) \;
	
uninstall:
	@echo "Cleaning any applicable pipenv installations from this path"
	@-$(USERHOME)/.local/bin/pipenv --rm
	@echo "Uninstalling RPM package"
	@if rpm -q icinga2api; then \
		sudo rpm -e icinga2api; \
	fi

