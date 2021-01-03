# -*- coding: utf-8 -*-
"""
    tests.unit.utils.test_populate
    ------------------------------

    Test population utils

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
import pytest  # noqa

from log_it.utils.populate import set_fixture_defaults


def test_set_fixture_defaults():
    default = {
        "key": None,
        "common_key": "common_value",
        "rare_key": None,
    }
    fixture = [
        {"key": 1},
        {"key": 2, "common_key": "uncommon_value", "rare_key": True},
    ]
    defaults_set = set_fixture_defaults(fixture, default)

    assert "common_key" in defaults_set[0]
    assert defaults_set[0]["common_key"] == default["common_key"]

    assert "rare_key" in defaults_set[0]
    assert defaults_set[0]["rare_key"] == default["rare_key"]

    # if the fixture has the key set it doesn't get overwritten
    assert "common_key" in defaults_set[1]
    assert defaults_set[1]["common_key"] == fixture[1]["common_key"]

    assert "rare_key" in defaults_set[1]
    assert defaults_set[1]["rare_key"] == fixture[1]["rare_key"]
