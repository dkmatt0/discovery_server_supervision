#!/usr/bin/env python3
# coding: utf-8


class PluginSupervisionBase(object):
    """Classe de base des plugins de supervision."""

    def __init__(self):
        self.version = None

    def get_version(self):
        return self.version

    def get_hosts(self):
        raise NotImplemented

    def set_host(self):
        raise NotImplemented
