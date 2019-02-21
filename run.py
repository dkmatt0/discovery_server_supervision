#!/usr/bin/env python3
# coding: utf-8

import os.path

import project.plugins as pls


plugins_supervision = {
    n: m
    for (n, m) in pls.load_plugins(
        os.path("project", "plugins_supervision"), "PluginSupervision"
    )
}

from project.plugins_supervision import plugins_supervision


# test / debug
print(plugins_supervision)
