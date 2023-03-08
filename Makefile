.DEFAULT_GOAL := build
.PHONY: clean \
		install install_dependencies install_pre_commit \
		docs lint test build \
		generate_models

# general variables
PROJ_SLUG = quakesaver_client

clean:
	rm -rf .pytest_cache
	rm -rf build
	rm -rf docs/build
	rm -rf docs/source/modules
	rm -rf dist
	rm -rf quakesaver_client.egg-info
	rm -rf htmlcov
	rm -rf .coverage

install_dependencies:
	poetry install

install_pre_commit:
	poetry run pre-commit install

install: install_dependencies install_pre_commit

build:
	poetry build

lint:
	poetry run pre-commit run --all-files

test:
	poetry run py.test tests/* -vv --cov-report html --cov=$(PROJ_SLUG)

docs: clean
	poetry run sphinx-apidoc -o ./docs/source/modules $(PROJ_SLUG)
	poetry dynamic-versioning && cd docs && poetry run make html

generate_models:
	# can be deleted no usage
	rm pydantic_schemas/sensor_actions.schema.json || true
	# can be deleted due to state includes config
	rm pydantic_schemas/sensor_configs.schema.json || true
	poetry run datamodel-codegen --input-file-type jsonschema --input pydantic_schemas/data_products.schema.json --output quakesaver_client/models/data_products.py
	poetry run datamodel-codegen --input-file-type jsonschema --input pydantic_schemas/sensor_state.schema.json --output quakesaver_client/models/sensor_state.py
