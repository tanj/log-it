# -*- coding: utf-8 -*-
"""
    tests.fixtures.database
    -----------------------

    DB population utils

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
import pytest
from sqlalchemy.orm.exc import NoResultFound
import attr

from log_it.user.model import TUser
from log_it.fixtures import roles


@pytest.fixture
def fx_user():
    return dict(
        sEmail="test_normal@example.com",
        sName="Normal Test",
        urlProfilePic="http://example.com/user/test_normal/profile_pic.png",
        urlDefaultLog="log/test_normal_at_example_com",
    )


@pytest.fixture
def user(fx_user):
    """Creates or fetches test_normal user"""
    try:
        user = TUser.query.filter(TUser.sEmail == fx_user["sEmail"]).one()
    except NoResultFound:
        user = TUser.create(**fx_user)
    return user


@pytest.fixture
def fx_default_roles():
    return roles.fixture


@attr.s
class LinkTableFixture(object):
    fixture = attr.ib()
    default = attr.ib()
    lookup_one = attr.ib()
    lookup_two = attr.ib()


@pytest.fixture
def fx_user_role(user, fx_default_roles):
    (role,) = [x["sRole"] for x in fx_default_roles if x["sRole"] == "User"]
    ur = LinkTableFixture(
        fixture=[
            dict(sEmail=user.sEmail, sRole=role),
        ],
        default={},
        lookup_one="sEmail",
        lookup_two="sRole",
    )
    return ur
