# -*- coding: utf-8 -*-
"""
    log_it.user.model
    -----------------

    It provides the models for the user

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""

from sqlalchemy_utils.models import generic_repr
from sqlalchemy_utils.types import EmailType, URLType

from flask_security import UserMixin, RoleMixin

from log_it.extensions import db
from log_it.utils.database import Timestamp, CRUDMixin


@generic_repr
class TUser(db.Model, CRUDMixin, UserMixin, Timestamp):
    __tablename__ = "tUser"

    ixUser = db.Column(db.Integer, primary_key=True)
    sEmail = db.Column(EmailType, unique=True, nullable=False)
    sName = db.Column(db.Unicode(255))
    urlProfilePic = db.Column(URLType)
    urlDefaultLog = db.Column(URLType)
    fs_uniquifier = db.Column(db.Text)

    roles = db.relationship("TRole", secondary="tUserRole")
    user_permissions = db.relationship("TUserPermission")
    role_permissions = db.relationship(
        "TRolePermission",
        secondary="tUserRole",
        primaryjoin=("TUser.ixUser == TUserRole.ixUser"),
        secondaryjoin=("TUserRole.ixRole == TRolePermission.ixRole"),
    )


@generic_repr
class TRole(db.Model, CRUDMixin, RoleMixin):
    __tablename__ = "tRole"

    ixRole = db.Column(db.Integer, primary_key=True)
    sRole = db.Column(db.Unicode(80), unique=True)
    sDescription = db.Column(db.Text)

    users = db.relationship("TUser", secondary="tUserRole")


@generic_repr
class TUserRole(db.Model, CRUDMixin):
    __tablename__ = "tUserRole"

    ixUser = db.Column(db.Integer, db.ForeignKey("tUser.ixUser"), primary_key=True)
    user = db.relationship("TUser")

    ixRole = db.Column(db.Integer, db.ForeignKey("tRole.ixRole"), primary_key=True)
    role = db.relationship("TRole")


@generic_repr
class TAction(db.Model, CRUDMixin):
    __tablename__ = "tAction"

    ixAction = db.Column(db.Integer, primary_key=True)
    sAction = db.Column(db.Unicode(100), nullable=False)
    sDescription = db.Column(db.Text)
