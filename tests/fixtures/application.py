import pytest

from log_it import create_app
from log_it.configs.testing import TestingConfig


@pytest.fixture(autouse=True)
def application():
    """application with context"""
    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope="class")
def class_application():
    """application with context"""
    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope="session")
def session_application():
    """application with context"""
    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture()
def request_context(application):
    with application.test_request_context():
        yield


@pytest.fixture()
def post_request_context(application):
    with application.test_request_context(method="POST"):
        yield
