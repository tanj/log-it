"""
    log_it.configs.testing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This is the testing configuration for log_it
    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details.

    Some portions of this file copied and adapted from FlaskBB under
    the terms of their BSD license
    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
    :source: https://github.com/flaskbb/flaskbb

"""
from log_it.configs.default import DefaultConfig


class TestingConfig(DefaultConfig):

    # Indicates that it is a testing environment
    DEBUG = False
    TESTING = True

    TESTING_USERS = [
        {
            "user": {"sEmail": "admin@example.com"},
            "roles": [
                {"sRole": "ALL"},
            ],
        },
        {
            "user": {"sEmail": "user@example.com"},
            "roles": [
                {"sRole": "SELF"},
            ],
        },
        {
            "user": {"sEmail": "user_ro@example.com"},
            "roles": [
                {"sRole": "READ"},
            ],
        },
        {
            "user": {"sEmail": "user_lo@example.com"},
            "roles": [
                {"sRole": "READ"},
                {"sRole": "INSERT"},
            ],
        },
    ]

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TEST_SQLALCHEMY_DATABASE_URI = "sqlite://"

    SERVER_NAME = "localhost:5000"

    # This will print all SQL statements
    SQLALCHEMY_ECHO = True

    # # Use the in-memory storage
    # WHOOSHEE_MEMORY_STORAGE = True

    # CELERY_ALWAYS_EAGER = True
    # CELERY_RESULT_BACKEND = "cache"
    # CELERY_CACHE_BACKEND = "memory"
    # CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

    LOG_DEFAULT_CONF = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(levelname)-7s %(name)-25s %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "NOTSET",
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
        },
        # TESTING: Log to console only
        "loggers": {
            "flask.app": {"handlers": ["console"], "level": "INFO", "propagate": False},
            "log_it": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }
