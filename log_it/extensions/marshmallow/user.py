# -*- coding: utf-8 -*-
# pylint: disable=R0903
"""
    log_it.extensions.marshmallow.user
    ----------------------------------

    Marshmallow User Models

    :copyright: (c) 2021 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from log_it.user.model import (
    TUser,
    TRole,
    TAction,
    TUserRole,
)

from . import FixtureSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TUser


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TRole


class ActionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TAction


class UserRoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TUserRole


# FixtureSchema
class UserFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TUser
        filter_attrs = ["sEmail"]

    sEmail = auto_field()
    sName = auto_field(missing=None)
    urlProfilePic = auto_field(missing=None)
    urlDefaultLog = auto_field(missing=None)
    fs_uniquifier = auto_field(missing=None)


class RoleFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TRole
        filter_attrs = ["sRole"]

    sRole = auto_field()
    sDescription = auto_field(missing=None)


class UserWithRoles(UserFixture):
    roles = Nested(RoleFixture, many=True)


class ActionFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TAction
        filter_attrs = ["sAction"]

    sAction = auto_field()
    sDescription = auto_field(missing=None)


class UserRoleFixture(FixtureSchema):
    class Meta(FixtureSchema.Meta):
        model = TUserRole

    user = Nested(UserFixture)
    role = Nested(RoleFixture)
