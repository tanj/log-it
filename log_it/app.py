# -*- coding: utf-8 -*-
"""
    log_it.app
    ----------

    The main app creation

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

    Some portions of this file copied and adapted from FlaskBB under
    the terms of their BSD license
    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
    :source: https://github.com/flaskbb/flaskbb
"""

import logging
import logging.config
import os
import time

from flask import Flask

# from flask_login import current_user
from sqlalchemy import event
from sqlalchemy.engine import Engine

from log_it.utils.helpers import get_log_it_config
from log_it.extensions import db

logger = logging.getLogger(__name__)


def create_app(config=None, instance_path=None):
    """Creates the app.
    :param instance_path: An alternative instance path for the application.
                          By default the folder ``'instance'`` next to the
                          package or module is assumed to be the instance
                          path.
                          See :ref:`Instance Folders <flask:instance-folders>`.
    :param config: The configuration file or object.
                   The environment variable is weightet as the heaviest.
                   For example, if the config is specified via an file
                   and a ENVVAR, it will load the config via the file and
                   later overwrite it from the ENVVAR.
    """

    app = Flask("log_it", instance_path=instance_path, instance_relative_config=True)

    # instance folders are not automatically created by flask
    if not os.path.exists(app.instance_path):  # pragma: no cover
        os.makedirs(app.instance_path)

    configure_app(app, config)
    configure_extensions(app)

    return app


def configure_app(app, config):
    """Configures log_it."""
    # Use the default config and override it afterwards
    app.config.from_object("log_it.configs.default.DefaultConfig")
    config = get_log_it_config(app, config)
    # Path
    if isinstance(config, str):  # pragma: no cover
        app.config.from_pyfile(config)
    # Module
    else:
        # try to update the config from the object
        app.config.from_object(config)

    # Add the location of the config to the config
    app.config["CONFIG_PATH"] = config

    # Environment
    # Get config file from envvar
    # app.config.from_envvar("APP_CONFIG_FILE")

    # Instance Config
    app.config.from_pyfile("instance_config.py")

    # Setting up logging as early as possible
    configure_logging(app)

    if not isinstance(config, str) and config is not None:
        config_name = "{}.{}".format(config.__module__, config.__name__)
    else:  # pragma: no cover
        config_name = config

    logger.info("Using config from: {}".format(config_name))

    # deprecation_level = app.config.get("DEPRECATION_LEVEL", "default")

    # never set the deprecation level during testing, pytest will handle it
    # if not app.testing:  # pragma: no branch
    #     warnings.simplefilter(deprecation_level, FlaskBBDeprecation)
    if app.testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
            "TEST_SQLALCHEMY_DATABASE_URI"
        ]

    debug_panels = app.config.setdefault(
        "DEBUG_TB_PANELS",
        [
            "flask_debugtoolbar.panels.versions.VersionDebugPanel",
            "flask_debugtoolbar.panels.timer.TimerDebugPanel",
            "flask_debugtoolbar.panels.headers.HeaderDebugPanel",
            "flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel",
            "flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel",
            "flask_debugtoolbar.panels.template.TemplateDebugPanel",
            "flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel",
            "flask_debugtoolbar.panels.logger.LoggingPanel",
            "flask_debugtoolbar.panels.route_list.RouteListDebugPanel",
            "flask_debugtoolbar.panels.profiler.ProfilerDebugPanel",
        ],
    )

    if all("WarningsPanel" not in p for p in debug_panels):
        debug_panels.append("flask_debugtoolbar_warnings.WarningsPanel")


def configure_logging(app):
    """Configures logging."""
    if app.config.get("USE_DEFAULT_LOGGING"):
        configure_default_logging(app)

    if app.config.get("LOG_CONF_FILE"):  # pragma: no cover
        logging.config.fileConfig(
            app.config["LOG_CONF_FILE"], disable_existing_loggers=False
        )

    if app.config["SQLALCHEMY_ECHO"]:  # pragma: no cover
        # Ref: http://stackoverflow.com/a/8428546
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(
            conn, cursor, statement, parameters, context, executemany
        ):
            conn.info.setdefault("query_start_time", []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(
            conn, cursor, statement, parameters, context, executemany
        ):
            total = time.time() - conn.info["query_start_time"].pop(-1)
            app.logger.debug("Total Time: %f", total)


def configure_default_logging(app):
    # Load default logging config
    logging.config.dictConfig(app.config["LOG_DEFAULT_CONF"])

    if app.config["SEND_LOGS"]:  # pragma: no cover
        configure_mail_logs(app)


def configure_mail_logs(app, formatter):  # pragma: no cover
    from logging.handlers import SMTPHandler

    formatter = logging.Formatter("%(asctime)s %(levelname)-7s %(name)-25s %(message)s")
    mail_handler = SMTPHandler(
        app.config["MAIL_SERVER"],
        app.config["MAIL_DEFAULT_SENDER"],
        app.config["ADMINS"],
        "application error, no admins specified",
        (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"]),
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(formatter)
    app.logger.addHandler(mail_handler)


def configure_extensions(app):
    """Configures the extensions."""
    # # Flask-Allows
    # allows.init_app(app)
    # allows.identity_loader(lambda: current_user)

    # # Flask-WTF CSRF
    # csrf.init_app(app)

    # Flask-SQLAlchemy
    db.init_app(app)

    # # Flask-Admin
    # admin.init_app(app)

    # # Flask-Bootstrap
    # bootstrap.init_app(app)

    # # Flask-Nav
    # nav.init_app(app)

    # # Flask-Classy
    # views.load(app)
