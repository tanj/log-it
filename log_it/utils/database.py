# -*- coding: utf-8 -*-
"""
    log_it.utils.database
    ---------------------

    Database helpers

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from datetime import datetime

import sqlachemy as sa
from sqlalchemy.ext.declarative import declared_attr


def last_position(cls):
    # get highest column order of all Column objects of this class.
    return max(
        [
            value._creation_order
            for key, value in vars(cls).items()
            if isinstance(value, sa.Column)
        ]
    )


class Timestamp(object):
    """Adds `utcCreated` and `utcUpdated` columns to derived declarative models.

    The `utcCreated` is handled through a default and the `utcUpdated`
    column is handled through a `before_update` event that propagates
    for all derived declarative models.
    """

    @declared_attr
    def utcCreated(cls):
        col = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
        col._creation_order = last_position(cls) + 0.5
        return col

    @declared_attr
    def utcUpdated(cls):
        col = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
        col._creation_order = last_position(cls) + 0.5
        return col


@sa.event.listens_for(Timestamp, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    """Listen for `before_update` event and set `utcUpdated`"""
    target.utcUpdated = datetime.utcnow()
