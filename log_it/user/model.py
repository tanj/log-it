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

from flask_login import UserMixin

from log_it.extensions import db
from log_it.utils.database import Timestamp


@generic_repr
class TUser(db.Model, UserMixin, Timestamp):
    __tablename__ = "tUser"

    ixUser = db.Column(db.Integer, primary_key=True)
    sEmail = db.Column(EmailType, unique=True, nullable=False)
    sName = db.Column(db.Unicode(255))
    urlProfilePic = db.Column(URLType)
    urlDefaultLog = db.Column(URLType)
