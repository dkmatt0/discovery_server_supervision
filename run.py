#!/usr/bin/env python3
# coding: utf-8

import os.path
import sys

import project.plugins as plgs
from project.scan import ScanIP
from project.common import open_yaml, compare_ip

plugins_supervision = {
    n: m
    for (n, m) in plgs.load_plugins("project/plugins_supervision", "PluginSupervision")
}

centreon = plugins_supervision["centreon"]()

# test / debug

if __name__ == "__main__":
    ip = ScanIP()

    config = open_yaml("project/config.yaml")
    if config is not None:
        if "network" in config:
            for config_range_ip in config["network"]:
                ip.add_ip((config_range_ip["begin"], config_range_ip["end"]))
        else:
            sys.stderr.write('Le fichier yaml n\'a pas de section "network".')
            exit(1)
    else:
        sys.stderr.write("Fichier config.yaml non chargé!")
        exit(1)

    # ip.check_ping()

    list_ip_supervision = centreon.get_hosts()

    known_ip, unknown_ip = compare_ip(ip.get_ip(), list_ip_supervision)

    print(known_ip, unknown_ip)
