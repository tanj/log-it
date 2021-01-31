# -*- coding: utf-8 -*-
"""
    log_it.utils.populate
    ---------------------

    DB population utils

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""


def populate_from_marshmallow_fixture(session, mm_schema, fixture, many=False):
    """Populate database from a marshmallow export

    :param session: sqlalchemy session
    :param mm_schema: Marshmallow Schema
    :param fixture: data exported by Marshmallow Schema
    :returns: mm_schema.opts.model

    """
    _mm_schema = mm_schema(session=session, many=many)
    return _mm_schema.load(fixture)
