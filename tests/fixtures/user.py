# -*- coding: utf-8 -*-
"""
    tests.fixtures.database
    -----------------------

    DB population utils

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
import pytest

from log_it.user.model import TUser


@pytest.fixture
def user():
    """Creates a normal user"""
    user = TUser.create(
        sEmail="test_normal@example.com",
        sName="Normal Test",
        urlProfilePic="http://example.com/user/test_normal/profile_pic.png",
        urlDefaultLog="log/test_normal_at_example_com",
    )
    yield user
    user.delete()
