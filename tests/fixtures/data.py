import pytest
import attr


@attr.s
class ComplexNestedData(object):
    thing = attr.ib(default=1)


@pytest.fixture
def complex_nested_data():
    return {
        "root": {
            "simple": True,
            "nested": ComplexNestedData({"complex": ComplexNestedData()}),
        }
    }
