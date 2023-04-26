import pytest


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--runlocal",
        action="store_true",
        default=False,
        help="run tests that connect to local sensor",
    )


def pytest_configure(config) -> None:
    config.addinivalue_line("markers", "local: mark test as dependent on local sensor")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runlocal"):
        return
    skip_local = pytest.mark.skip(reason="need --runlocal option to run")
    for item in items:
        if "local" in item.keywords:
            item.add_marker(skip_local)
