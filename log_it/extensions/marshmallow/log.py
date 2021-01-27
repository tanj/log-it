# -*- coding: utf-8 -*-
# pylint: disable=R0903
"""
    log_it.extensions.marshmallow.log
    ---------------------------------

    Marshmallow Log Models

    :copyright: (c) 2021 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from log_it.log.model import (
    TLog,
    TField,
    TLogField,
    TMessage,
    TMessageType,
    TTag,
    TTagMessage,
    TUserPermission,
    TRolePermission,
)

from . import FixtureSchema
from .user import UserFixture, RoleFixture, ActionFixture


class LogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TLog


class FieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TField


class LogFieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TLogField


class MessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TMessage


class MessageTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TMessageType


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TTag


class TagMessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TTagMessage


class UserPermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TUserPermission


class RolePermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TRolePermission


# FixtureSchema
class LogFixture(FixtureSchema):
    """Barebones Log Fixture for stubs"""

    class Meta(FixtureSchema.Meta):
        model = TLog
        filter_attrs = ["sLog"]

    sLog = auto_field()


class FieldFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TField
        filter_attrs = ["sField"]

    sField = auto_field()


class LogFieldFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TLogField
        filter_attrs = [
            "log.ixLog",
            "field.ixField",
        ]

    log = Nested(LogFixture, many=False)
    field = Nested(FieldFixture, many=False)
    sValue = auto_field()
    iOrder = auto_field(missing=None)


class MessageTypeFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TMessageType
        filter_attrs = ["sMessageType"]


class TagFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TTag
        filter_attrs = ["sTag"]

    sTag = auto_field()


class TagMessageFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TTagMessage


class MessageFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TMessage
        # message fixtures are always inserted, never looked up
        filter_attrs = None

    log = Nested(LogFixture, many=False)
    message_type = Nested(MessageTypeFixture, many=False)
    user = Nested(UserFixture, many=False)
    utcMessage = auto_field(missing=datetime.utcnow)
    sMessage = auto_field()
    tags = Nested(TagFixture, many=True)


class UserPermissionFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TUserPermission

    log = Nested(LogFixture, many=False)
    user = Nested(UserFixture, many=False)
    action = Nested(ActionFixture, many=False)


class RolePermissionFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TRolePermission

    log = Nested(LogFixture, many=False)
    role = Nested(RoleFixture, many=False)
    action = Nested(ActionFixture, many=False)


class LogFullFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TLog
        filter_attrs = ["sLog"]

    sLog = auto_field()
    user = Nested(UserFixture, many=False)
    fields = Nested(FieldFixture, many=True)
    user_permissions = Nested(UserPermissionFixture)
    role_permissions = Nested(RolePermissionFixture)
