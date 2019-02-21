#!/usr/bin/env python3
# coding: utf-8

import sys

import requests
import yaml

from .base import PluginSupervisionBase


class PluginSupervision(PluginSupervisionBase):
    """Plugin de supervision pour centreon"""

    def __init__(self):
        super(PluginSupervision, self).__init__()
        self.plugin_name = "centreon"
        self.token = None

        # Chargement des fichiers de configuration
        try:
            with open("project/config.yaml", "r") as f_config:
                self.config = yaml.load(f_config)
        except FileNotFoundError:
            sys.stderr.write("Impossible de charger le fichier config.yaml.\n")
            exit(10)
        try:
            with open("project/secret.yaml", "r") as f_secret:
                self.secret = yaml.load(f_secret)
        except FileNotFoundError:
            sys.stderr.write("Impossible de charger le fichier secret.yaml.\n")
            exit(11)

        self.url = (
            "https://"
            if self.config[self.plugin_name]["https"]
            else "http://"
            + self.config[self.plugin_name]["ip"]
            + self.config[self.plugin_name]["url"]
        )

    def authenticate(self):
        """ Méthode d'authentification à l'API de Centreon."""
        try:
            r = requests.post(
                self.url,
                params={"action": "authenticate"},
                data={
                    "username": self.secret[self.plugin_name]["username"],
                    "password": self.secret[self.plugin_name]["password"],
                },
            )
        except Exception as e:
            sys.stderr.write(
                "Une erreur à eu lieu durant l'authentification : {}.".format(e)
            )
            exit(13)
        rjson = r.json()
        if "authToken" in rjson:
            self.token = rjson["authToken"]
            return rjson
        else:
            sys.stderr.write("Problème d'authentification vers centreon")
            exit(12)

    def get_hosts(self, retry=True):
        """Méthode de récupération de la liste des hôtes présent dans centreon."""
        if not self.token:
            self.authenticate()
        r = requests.get(
            self.url,
            headers={
                "content-type": "application/json",
                "centreon-auth-token": self.token,
            },
            params={
                "object": "centreon_realtime_hosts",
                "action": "list",
                "fields": "address",
            },
        )
        return [x["address"] for x in r.json()]
