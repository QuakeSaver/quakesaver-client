.DEFAULT_GOAL := build
.PHONY: clean \
		install \
		docs lint test build

# general variables
PROJ_SLUG = quakesaver_client

clean:
	rm -rf .pytest_cache
	rm -rf build
	rm -rf docs/_build
	rm -rf docs/modules
	rm -rf dist
	rm -rf quakesaver_client.egg-info
	rm -rf htmlcov
	rm -rf .coverage


install:
	poetry install

build:
	poetry build

lint:
	poetry run pre-commit run --all-files

test:
	poetry run py.test -vv --cov-report html --cov=$(PROJ_SLUG)
	${BROWSER} htmlcov/index.html

docs: clean
	poetry run sphinx-apidoc -o ./docs/modules $(PROJ_SLUG)
	cd docs && poetry run make html
	$(info You can find the docs in './docs/_build/html/index.html')
