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
from log_it.extensions import db


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


class CRUDMixin(object):
    """
    CRUDMixin copied and adapted from FlaskBB under
    the terms of their BSD license
    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
    :source: https://github.com/flaskbb/flaskbb
    """

    @classmethod
    def create(cls, commit=True, **kwargs):
        """Create a `cls` object from kwargs

        :param cls: The class calling this method
        :param commit: whether we commit on creation or just add to session
        :returns: instance of `cls`
        :rtype: `cls`

        """
        instance = cls(**kwargs)
        return instance.save(commit)

    def save(self, commit=True):
        """Saves the object to the database."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self):
        """Delete the object from the database."""
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def pk_to_dict(self):
        """:property pk_to_dict:

        :returns: primary keys as dictionary
        :rtype: Mapping[pk_name, pk_value]

        """
        pkd = {}
        for col in self.__table__.primary_key.columns:
            pkd[col.name] = getattr(self, col.name)
        return pkd
