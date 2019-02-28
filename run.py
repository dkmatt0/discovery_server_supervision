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

    list_ip_supervision = centreon.get_hosts()

    ip_known, ip_unknown = compare_ip(ip.get_ip(), list_ip_supervision)

    ip.rem_ip(ip_known)
    ip.check_ping(timeout=0.5)

    ip_linux = ip.check_tcp(22, update_ip=False)  # ssh
    ip_windows = ip.check_tcp(135, update_ip=False)  # rcp

    _, ip_unknown = compare_ip(ip.get_ip(), set(ip_linux + ip_windows))

    print("ip linux", ip_linux)
    print("ip windows", ip_windows)
    print("ip inconnu", ip_unknown)
