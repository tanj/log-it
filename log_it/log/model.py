# -*- coding: utf-8 -*-
"""
    log_it.log.model
    ----------------

    It provides the models for the log

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from datetime import datetime

from sqlalchemy_utils.models import generic_repr

from log_it.extensions import db
from log_it.utils.database import Timestamp, CRUDMixin


@generic_repr
class TLog(db.Model, CRUDMixin, Timestamp):
    __tablename__ = "tLog"

    ixLog = db.Column(db.Integer, primary_key=True)
    sLog = db.Column(db.Unicode)
    ixUser = db.Column(db.Integer, db.ForeignKey("tUser.ixUser"), nullable=False)
    user = db.relationship("TUser", uselist=False)

    fields = db.relationship("TLogField", uselist=True)

    user_permissions = db.relationship(
        "TUserPermission",
        primaryjoin="and_(TLog.ixLog == TUserPermission.ixLog, TLog.ixUser == TUserPermission.ixUser)",
    )
    role_permissions = db.relationship("TRolePermission")


# TODO: log sharing
# @generic_repr
# class TSharedLog(db.Model, CRUDMixin, Timestamp):
#     __tablename__ = "tSharedLog"

#     ixSharedLog = db.Column(db.Integer, primary_key=True)
#     ixLog = db.Column(db.Integer, db.ForeignKey("tLog.ixLog"), nullable=False)
#     permissions = db.relationship("TPermission", uselist=True)
#     # This should be it's own table
#     ixUser = db.Column(db.Integer, db.ForeignKey("tUser.ixUser"), nullable=False)
#     pemUser = db.Column(db.Integer, nullable=False)
#     ixGroup = db.Column(db.Integer, db.ForeignKey(), nullable=True)
#     pemGroup = db.Column(db.Integer, nullable=True)


@generic_repr
class TField(db.Model, CRUDMixin):
    __tablename__ = "tField"

    ixField = db.Column(db.Integer, primary_key=True)
    sField = db.Column(db.Unicode)


@generic_repr
class TLogField(db.Model, CRUDMixin):
    __tablename__ = "tLogField"

    ixLogField = db.Column(db.Integer, primary_key=True)
    ixField = db.Column(db.Integer, db.ForeignKey("tField.ixField"))
    field = db.relationship("TField", uselist=False)
    ixLog = db.Column(db.Integer, db.ForeignKey("tLog.ixLog"))
    log = db.relationship("TLog", uselist=False)
    sValue = db.Column(db.Unicode)
    iOrder = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint("ixField", "ixLog", name="uq_tlogfield_ixfield_ixlog"),
    )


@generic_repr
class TMessage(db.Model, CRUDMixin, Timestamp):
    __tablename__ = "tMessage"

    ixMessage = db.Column(db.Integer, primary_key=True)
    ixLog = db.Column(
        db.Integer, db.ForeignKey("tLog.ixLog", ondelete="CASCADE"), nullable=False
    )
    log = db.relationship("TLog", uselist=False)
    ixMessageType = db.Column(
        db.Integer, db.ForeignKey("tMessageType.ixMessageType"), nullable=False
    )
    message_type = db.relationship("TMessageType", uselist=False)

    ixUser = db.Column(
        db.Integer, db.ForeignKey("tUser.ixUser", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("TUser", uselist=False)

    # utcMessage is added for being able to change some history if a note was missed
    utcMessage = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sMessage = db.Column(db.Text)

    # TODO: need to test this relationship
    user_permissions = db.relationship(
        "TUserPermission",
        primaryjoin=(
            "and_(foreign(TMessage.ixLog) == TUserPermission.ixLog, "
            "TMessage.ixUser == TUserPermission.ixUser)"
        ),
    )


@generic_repr
class TMessageType(db.Model, CRUDMixin):
    __tablename__ = "tMessageType"

    ixMessageType = db.Column(db.Integer, primary_key=True)
    sMessageType = db.Column(db.Unicode(20), unique=True)


@generic_repr
class TTag(db.Model, CRUDMixin):
    __tablename__ = "tTag"

    ixTag = db.Column(db.Integer, primary_key=True)
    sTag = db.Column(db.Unicode(40), nullable=False)


@generic_repr
class TTagMessage(db.Model, CRUDMixin):
    __tablename__ = "tTagMessage"

    ixMessage = db.Column(
        db.Integer, db.ForeignKey("tMessage.ixMessage"), primary_key=True
    )
    ixTag = db.Column(db.Integer, db.ForeignKey("tTag.ixTag"), primary_key=True)


@generic_repr
class TUserPermission(db.Model, CRUDMixin):
    __tablename__ = "tUserPermission"

    ixUserPermission = db.Column(db.Integer, primary_key=True)
    ixLog = db.Column(db.Integer, db.ForeignKey("tLog.ixLog"), nullable=False)
    log = db.relationship("TLog", uselist=False)

    ixUser = db.Column(db.Integer, db.ForeignKey("tUser.ixUser"), nullable=False)
    user = db.relationship("TUser", uselist=False)

    ixAction = db.Column(db.Integer, db.ForeignKey("tAction.ixAction"), nullable=False)
    action = db.relationship("TAction", uselist=False)


@generic_repr
class TRolePermission(db.Model, CRUDMixin):
    __tablename__ = "tRolePermission"

    ixRolePermission = db.Column(db.Integer, primary_key=True)
    ixLog = db.Column(db.Integer, db.ForeignKey("tLog.ixLog"), nullable=False)
    log = db.relationship("TLog", uselist=False)

    ixRole = db.Column(db.Integer, db.ForeignKey("tRole.ixRole"), nullable=False)
    user = db.relationship("TRole", uselist=False)

    ixAction = db.Column(db.Integer, db.ForeignKey("tAction.ixAction"), nullable=False)
    action = db.relationship("TAction", uselist=False)


@generic_repr
class TAction(db.Model, CRUDMixin):
    __tablename__ = "tAction"

    ixAction = db.Column(db.Integer, primary_key=True)
    sAction = db.Column(db.Unicode(100), nullable=False)
    sDescription = db.Column(db.Text)


_indexes = [
    db.Index("uq_ttag_stag_lower", db.func.lower(TTag.sTag), unique=True),
]
