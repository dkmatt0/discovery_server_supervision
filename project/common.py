#!/usr/bin/env python3
# coding: utf-8

import yaml


def open_yaml(filename):
    """Lecture du fichier de config."""
    try:
        with open(filename, "r") as f:
            f_loaded = yaml.load(f)
            return f_loaded
    except:
        sys.stderr.write(f"Impossible de charger le fichier {filename}")
        return None
        exit(10)


def compare_ip(list_ip1, list_ip2):
    """
  Renvoi un tuple contenant deux elements liste :
    1 => Les ip de list_ip1 présente dans list_ip2
    2 => Les ip de list_ip1 absente de list_ip2
  """
    list_ip2 = set(list_ip2)
    ip_in, ip_out = [], []
    for ip in list_ip1:
        if ip in list_ip2:
            ip_in.append(ip)
        else:
            ip_out.append(ip)
    return (ip_in, ip_out)
