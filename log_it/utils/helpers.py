# -*- coding: utf-8 -*-
"""
    log_it.utils.helpers
    --------------------

    Helper functions

    :copyright: (c) 2021 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
import os
from werkzeug.utils import ImportStringError, import_string


def get_log_it_config(app, config_file):
    """Returns ``None`` or the config which is either the path to a config file
    or an object. They can be used by ``app.config.from_pyfile`` or
    by ``app.config.from_object``.
    :param app: The app instance.
    :param config_file: A string which is either a module that can be
                        imported, a path to a config file or an object.
                        If the provided config_file can't be found, it will
                        search for a 'flaskbb.cfg' file in the instance
                        directory and in the project's root directory.
    Adapted from FlaskBB
    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD https://github.com/flaskbb/flaskbb/blob/master/LICENSE
    :source: https://github.com/flaskbb/flaskbb/blob/master/flaskbb/utils/helpers.py

    """
    if config_file is not None:
        # config is an object
        if not isinstance(config_file, str):
            return config_file

        # config is a file
        if os.path.exists(os.path.join(app.instance_path, config_file)):
            return os.path.join(app.instance_path, config_file)

        if os.path.exists(os.path.abspath(config_file)):
            return os.path.join(os.path.abspath(config_file))

        # conifg is an importable string
        try:
            return import_string(config_file)
        except ImportStringError:
            return None
    else:  # pragma: no cover
        # this would be so much nicer and cleaner if we wouldn't
        # support the root/project dir.
        # this walks back to flaskbb/ from flaskbb/flaskbb/cli/main.py
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        project_config = os.path.join(project_dir, "log_it.cfg")

        # instance config doesn't exist
        instance_config = os.path.join(app.instance_path, "log_it.cfg")
        if os.path.exists(instance_config):
            return instance_config

        # config in root directory doesn't exist
        if os.path.exists(project_config):
            return project_config


class CompoundFilter(object):
    """Takes a string like `customer.ixCustomer` or `sJobNumber` and
    provides properties to make dictionary comprehesions easy"""

    def __init__(self, string):
        self.string = string
        self.primary = None
        self.second = None
        if "." in string:
            self.primary, self.second = string.split(".", 1)
        else:
            self.primary = string

    @property
    def key(self):
        return self.second or self.primary

    def get(self, data):
        try:
            ret = getattr(data, self.primary)
        except AttributeError:
            ret = data.get(self.primary)
        if self.second is not None and ret is not None:
            ret = CompoundFilter(self.second).get(ret)
        return ret
