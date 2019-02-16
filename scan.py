#!/usr/bin/env python3
# coding: utf-8


import sys

from scapy.all import *
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

def range_ip(begin, end):
  """Fourniture d'une liste d'ip allant de begin (inclus) à end (inclus)."""
  # Convertion en liste
  begin = [int(x) for x in begin.split('.')]
  end = [int(x) for x in end.split('.')]

  # Mise en ordre des ip (la plus petite dans begin)
  b = ['{0:0>3}'.format(x) for x in begin]
  e = ['{0:0>3}'.format(x) for x in end]
  if b>e:
    begin, end = end, begin
  del b
  del e

  # Creation de la liste d'adresse
  list_address = []
  while begin <= end:
    list_address.append('.'.join([str(x) for x in begin]))
    begin[3] += 1
    if begin[3] >= 256:
      begin[2] += 1
      begin[3] = 0
    if begin[2] >= 256:
      begin[1] += 1
      begin[2] = 0
    if begin[1] >= 256:
      begin[0] += 1
      begin[1] = 0
  return list_address

def ping(ip, timeout=3):
  """Fonction de ping (ICMP)."""
  response = sr1(IP(dst=ip) / ICMP(), timeout=timeout, verbose=False)
  if response is not None and response[1].type == 0:
    return True
  return False

def ip_exist(ip, ip_list_supervision):
  """Recherche une ip dans une liste d'ip et renvoie True si l'ip est trouvé."""
  if ip in ip_list_supervision: return True
  else: return False

