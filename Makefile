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
	uv install

install_pre_commit:
	uv run pre-commit install

install: install_dependencies install_pre_commit

build:
	uv build

lint:
	uv run pre-commit run --all-files

test:
	uv run py.test tests/* -vv --cov-report html --cov=$(PROJ_SLUG) -s

docs: clean
	uv run sphinx-apidoc -o ./docs/source/modules $(PROJ_SLUG)
	uv run cd docs && uv run make html

generate_models:
	# can be deleted no usage
	rm pydantic_schemas/sensor_actions.schema.json || true
	# can be deleted due to state includes config
	rm pydantic_schemas/sensor_configs.schema.json || true
	uv run datamodel-codegen --input-file-type jsonschema --input pydantic_schemas/data_products.schema.json --output quakesaver_client/models/data_products.py
	uv run datamodel-codegen --input-file-type jsonschema --input pydantic_schemas/sensor_state.schema.json --output quakesaver_client/models/sensor_state.py
