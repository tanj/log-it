# -*- coding: utf-8 -*-
"""
    log_it.extensions
    -----------------

    Flask Extensions used by Log-It

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""

from sqlalchemy import MetaData

from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_nav import Nav

from . import classful  # noqa

metadata = MetaData(
    naming_convention={
        "ix": "idx_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

debugtoolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
nav = Nav()
