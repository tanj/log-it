# -*- coding: utf-8 -*-
"""
    tests.fixtures.database
    -----------------------

    DB population utils

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
import pytest

from sqlalchemy import create_engine

from sqlalchemy_utils.functions import (
    create_database,
    database_exists,
    drop_database,
)

from log_it.extensions import db
from log_it.user.model import TUser, TRole, TUserRole
from log_it.log.model import (
    TLog,
    TField,
    TLogField,
    TMessage,
    TMessageType,
    TTag,
    TTagMessage,
)
from log_it.utils.populate import (
    populate_table_from_fixture,
    populate_link_table_from_fixture,
)
from log_it.fixtures import roles


@pytest.fixture(scope="session")
def testdb_engine(session_application):
    """create and destroy database each time the test suite runs"""
    assert not database_exists(
        session_application.config["TEST_SQLALCHEMY_DATABASE_URI"]
    )
    create_database(session_application.config["TEST_SQLALCHEMY_DATABASE_URI"])
    assert database_exists(session_application.config["TEST_SQLALCHEMY_DATABASE_URI"])

    eng = create_engine(session_application.config["TEST_SQLALCHEMY_DATABASE_URI"])
    db.metadata.create_all(bind=eng, tables=db.metadata.sorted_tables)
    yield eng

    drop_database(session_application.config["TEST_SQLALCHEMY_DATABASE_URI"])
    assert not database_exists(
        session_application.config["TEST_SQLALCHEMY_DATABASE_URI"]
    )


@pytest.fixture(scope="session")
def populated_db(testdb_engine, session_application):
    populate_table_from_fixture(TRole, roles)
    return
