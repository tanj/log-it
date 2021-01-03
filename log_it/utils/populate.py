# -*- coding: utf-8 -*-
"""
    log_it.utils.populate
    ---------------------

    DB population utils

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from collections.abc import Mapping
from boltons.iterutils import remap, default_enter


def set_fixture_defaults(fixture, default={}):
    def set_defaults_enter(path, key, value):
        new_parent, new_items = default_enter(path, key, value)
        if isinstance(new_parent, Mapping):
            _new_parent = {}
            _new_parent.update(default)
            try:
                _new_parent.update(new_parent)
                new_parent = _new_parent
            except Exception:
                pass
        return new_parent, new_items

    return remap(fixture, enter=set_defaults_enter)


def populate_table_from_fixture(table, fixture):
    """Populate DB `table` from `fixture` data

    :param table: SQLAlchemy Table class with `CRUDMixin`
    :param fixture: A list of mappings
    :returns: list of created table objects
    :rtype: List[table]

    """
    _fixtures = []
    for elm in fixture.fixture:
        _fixtures.append(table.create(**elm, commit=False))
    if len(_fixtures) > 0:
        _fixtures[0].save()
    return _fixtures


def populate_link_table_from_fixture(link_table, table_one, table_two, fixture):
    """Populate a linking table from a fixture.

    Performs a query using the key named in lookup_<one|two> to find a
    single result.

    TODO: Add Possible multiple key lookup

    :param link_table: SQLAlchemy Table class with `CRUDMixin` uses
    primary_keys from `table_one` and `table_two` to create a linking
    table.

    :param table_one: SQLAlchemy Table class with `CRUDMixin`
    :param table_two: SQLAlchemy Table class with `CRUDMixin`
    :param fixture: object or module with attributes fixture, default,
    lookup_one, and lookup_two

    :returns: list of created table objects
    :rtype: List[link_table]

    """
    _fixture = set_fixture_defaults(fixture.fixture, fixture.default)
    links = []
    for obj in _fixture:
        one = table_one.query.filter(
            getattr(table_one, _t1 := fixture.lookup_one) == obj[_t1]
        ).one()

        two = table_two.query.filter(
            getattr(table_two, _t2 := fixture.lookup_two) == obj[_t2]
        ).one()

        links.append(link_table.create(**one.pk_to_dict, **two.pk_to_dict))

    return links
