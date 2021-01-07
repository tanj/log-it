# -*- coding: utf-8 -*-
"""
    log_it.display.navigation
    -------------------------

    flask_nav navigation menus

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""

from flask_nav.elements import Navbar, View

from log_it.extensions import nav


@nav.navigation()
def top_nav():
    top = Navbar(View("Log it!", "HomeView:index"), View("Login", "LoginView:index"))
    return top
