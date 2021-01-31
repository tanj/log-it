# -*- coding: utf-8 -*-
"""
    log_it.extensions.classful
    --------------------------

    Register Classful Views with init_app function

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from log_it.auth.views import LoginView
from log_it.display.views import HomeView


def init_app(app):
    """Register Classful Views"""
    HomeView.register(app, route_base="/")
    LoginView.register(app)
