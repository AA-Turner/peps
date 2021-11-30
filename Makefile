# Builds PEP files to HTML using sphinx
# Also contains testing targets

PYTHON=python3
VENV_DIR=venv
SPHINX_JOBS=8
SPHINX_BUILD=$(PYTHON) build.py -j $(SPHINX_JOBS)

all: sphinx-local

clean:
	-rm pep-0000.rst
	-rm -rf build

update:
	git pull https://github.com/python/peps.git

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	./$(VENV_DIR)/bin/python -m pip install -r requirements.txt

lint:
	pre-commit --version > /dev/null || python3 -m pip install pre-commit
	pre-commit run --all-files

rss:
	$(PYTHON) pep_rss_gen.py

pages: rss
	$(SPHINX_BUILD) --index-file

# for building Sphinx without a web-server
sphinx-local:
	$(SPHINX_BUILD) --build-files

fail-warning:
	$(SPHINX_BUILD) --fail-on-warning

check-links:
	$(SPHINX_BUILD) --check-links
