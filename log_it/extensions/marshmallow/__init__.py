# -*- coding: utf-8 -*-
"""
    log_it.extensions.marshmallow
    -----------------------------

    Marshmallow

    :copyright: (c) 2021 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy.orm.exc import NoResultFound

from log_it.utils.helpers import CompoundFilter


class FixtureSchema(SQLAlchemySchema):
    """Marshmallow Fixture Schema"""

    class Meta:  # pylint: disable=R0903, C0115
        load_instance = True
        filter_attrs = None  # set to list of string attributes to use as filter

    def get_instance(self, data):
        """override get_instance to query with additional fields rather than just pk.

        Revert to super if filter_attrs is None

        :param data: Serialized data to inform lookup
        :returns: instance or None
        :rtype: instance type or NoneType

        """
        if self.Meta.filter_attrs is None:
            return super().get_instance(data)
        filters = {
            prop.key: pg
            for prop in [CompoundFilter(x) for x in self.Meta.filter_attrs]
            if (pg := prop.get(data)) is not None
        }
        if len(filters) > 0:
            try:
                # make some noise if we didn't filter enough to only get one result
                return self.session.query(self.opts.model).filter_by(**filters).one()
            except NoResultFound:
                return None
        return None

    @ma.post_load
    def make_instance(self, data, **kwargs):
        """overload marshmallow_sqlalchemy make_instance to save the instance
        if it isn't in the session.

        :param data: Data to deserialize
        :returns: instance or data

        """
        # This is what load_instance_mixin does
        if not self.opts.load_instance:
            return data
        # clear out any primary or foreign keys
        keep = data.pop("KEEP_IX_KEYS", [])
        for key in list(data.keys()):
            if key not in keep and key.startswith("ix"):
                data.pop(key)

        instance = super().make_instance(data, **kwargs)
        return instance.save(commit=True)
