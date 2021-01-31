# -*- coding: utf-8 -*-
"""
    log_it.fixtures.permissions
    ---------------------------

    default permissions

    :copyright: (c) 2020 by John te Bokkel
    :license: BSD, see LICENSE for more details

"""
actions = [
    {"sAction": "ALL", "sDescription": "All actions on all objects"},
    {"sAction": "SELF", "sDescription": "All actions on objects owned by user"},
    {"sAction": "READ"},
    {"sAction": "INSERT"},
    {"sAction": "DELETE"},
    {"sAction": "UPDATE"},
]
roles = [
    {"sRole": "Admin", "sDescription": "Site Administrator"},
    # {"sRole": "Domain Admin", "sDescription": "Domain Administrator"},
    # {"sRole": "Domain User", "sDescription": "Domain User"},
    {"sRole": "User", "sDescription": "Normal User"},
]

role_permissions = [
    {"sRole": "Admin", "sAction": "ALL"},
    {"sRole": "User", "sAction": "SELF"},
]
