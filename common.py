#!/usr/bin/env python3
# coding: utf-8

import yaml


def open_yaml(filename):
  """Lecture du fichier de config."""
  try:
    with open(filename, 'r') as f:
      f_loaded = yaml.load(f)
      return f_loaded
  except:
    sys.stderr.write("Impossible de charger le fichier {}".format(filename))
    return None
    exit(10)
