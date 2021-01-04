import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--keepdb",
        action="store_true",
        # default=False,
        help="don't drop database on completion",
    )


@pytest.fixture(scope="session")
def keepdb(request):
    return request.config.getoption("--keepdb")
