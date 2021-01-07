# -*- coding: utf-8 -*-
"""
    log_it.display.views
    --------------------

    Home and other misc Views

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
from flask import render_template
from flask_classful import FlaskView


class HomeView(FlaskView):
    title = "Home"

    def index(self):
        return render_template("layout.html")
