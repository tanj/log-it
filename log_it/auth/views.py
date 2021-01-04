# -*- coding: utf-8 -*-
"""
    log_it.auth.views
    -----------------

    Auth Views

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from flask_classful import FlaskView

_auth_prefix = "/auth/"


class LoginView(FlaskView):
    route_prefix = _auth_prefix
    title = "Login"

    def index(self):
        pass
