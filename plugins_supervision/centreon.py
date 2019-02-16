#!/usr/bin/env python3
# coding: utf-8

import sys

import requests
import yaml

# class de base des plugins de supervision
class PluginSupervisionBase(object):
  """docstring for PluginSupervisionBase."""
  def __init__(self):
    super(PluginSupervisionBase, self).__init__()
  def get_hosts(self):
    raise NotImplemented


class PluginSupervision(PluginSupervisionBase):
  """Plugin de supervision pour centreon"""
  def __init__(self):
    super(PluginSupervision, self).__init__()
    self.plugin_name = "centreon"
    self.token = None

    # Chargement des fichiers de configuration
    try:
      with open('../config.yaml', 'r') as f_config:
        self.config = yaml.load(f_config)
    except FileNotFoundError:
      sys.stderr.write("Impossible de charger le fichier config.yaml.")
      exit(10)
    try:
      with open('../secret.yaml', 'r') as f_secret:
        self.secret = yaml.load(f_secret)
    except FileNotFoundError:
      sys.stderr.write("Impossible de charger le fichier secret.yaml.")
      exit(11)

  def authenticate(self):
    """ Méthode d'authentification à l'API de Centreon."""
    try:
      r = requests.post(
        self.config[self.plugin_name]['url'],
        params={'action': 'authenticate'},
        data={'username': self.secret['centreon']['username'],
              'password': self.secret['centreon']['password']}
        )
    except Exception as e:
      sys.stderr.write("Une erreur à eu lieu durant l'authentification : {}.".format(e))
      exit(13)
    rjson = r.json()
    if 'authToken' in rjson:
      self.token = rjson['authToken']
      return rjson
    else:
      sys.stderr.write("Problème d'authentification vers centreon")
      exit(12)

  def get_hosts(self, retry=True):
    """Méthode de récupération de la liste des hôtes présent dans centreon."""
    if not self.token:
      self.authenticate()
    r = requests.get(
      self.config['centreon']['url'],
      headers={'content-type': 'application/json',
               'centreon-auth-token': self.token},
      params={'object': 'centreon_realtime_hosts',
              'action': 'list',
              'fields': 'address'}
    )
    return r.json()

