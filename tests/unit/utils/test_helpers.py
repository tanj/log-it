# -*- coding: utf-8 -*-
"""
    tests.unit.utils.test_populate
    ------------------------------

    Test population utils

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
import pytest
import os.path
import importlib

from log_it.utils.helpers import get_log_it_config, CompoundFilter


@pytest.mark.parametrize(
    "config_file, expected",
    [
        # (None, None), # not sure how to test this case TODO: should be able to mock.patch the env reads
        (
            "instance_config.py",
            lambda x: os.path.join(x.instance_path, "instance_config.py"),
        ),
        ("pyproject.toml", lambda x: os.path.abspath("pyproject.toml")),
        (
            "log_it.configs.default",
            lambda x: importlib.import_module("log_it.configs.default"),
        ),
        ("log_it.configs.does_not_exist", lambda x: None),
    ],
)
def test_get_log_it_config(application, config_file, expected):
    config = get_log_it_config(application, config_file)
    assert config == expected(application)


class TestCompoundFilter(object):
    @pytest.mark.parametrize(
        "path, key",
        [("root", "root"), ("root.next", "next"), ("root.next.third", "next.third")],
    )
    def test_key(self, path, key):
        cf = CompoundFilter(path)
        assert cf.key == key

    def test_root(self, complex_nested_data):
        cf = CompoundFilter("root")
        assert cf.get(complex_nested_data) == complex_nested_data["root"]

    def test_simple(self, complex_nested_data):
        cf = CompoundFilter("root.simple")
        assert cf.get(complex_nested_data)

    def test_nested(self, complex_nested_data):
        cf = CompoundFilter("root.nested.thing.complex.thing")
        assert cf.get(complex_nested_data) == 1
