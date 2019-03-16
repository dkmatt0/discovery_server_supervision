#!/usr/bin/env python3
# coding: utf-8

import os.path
import sys

import project.plugins as plgs
from project.scan import ScanIP
from project.common import open_yaml, compare_ip
from project.logger import logger

if __name__ == "__main__":
    logger.debug("listing des plugins")
    plugins_supervision = {
        n: m
        for (n, m) in plgs.load_plugins(
            "project/plugins_supervision", "PluginSupervision"
        )
    }

    logger.debug("chargement du plugin centreon en mémoire")
    centreon = plugins_supervision["centreon"]()

    logger.debug("création d'une instance de ScanIP")
    ip = ScanIP()

    logger.debug("chargement du fichier config.yaml")
    config = open_yaml("project/config.yaml")
    if config is not None:
        if "network" in config:
            for config_range_ip in config["network"]:
                ip.add_ip((config_range_ip["begin"], config_range_ip["end"]))
        else:
            logger.critical('Le fichier yaml n\'a pas de section "network".')
            exit(1)
    else:
        logger.critical("Fichier config.yaml non chargé!")
        exit(1)

    logger.debug("listage des hôtes de centreon")
    list_ip_supervision = centreon.get_hosts()

    logger.debug("comparaison des ip scannées et des ip de centreon")
    ip_known, ip_unknown = compare_ip(ip.get_ip(), list_ip_supervision)

    logger.debug("suppression des ip déjà connues de centreon")
    ip.rem_ip(ip_known)
    logger.debug("ping des ip inconnu de centreon")
    ip.check_ping(timeout=0.5)

    logger.debug("scan du port 22 sur les machines qui reépondent au ping")
    ip_linux = ip.check_tcp(22, update_ip=False)  # ssh
    logger.debug("scan du port 135 sur les machines qui reépondent au ping")
    ip_windows = ip.check_tcp(135, update_ip=False)  # rpc

    logger.debug("extraction des ip qui ne répondent pas au précédent scan")
    _, ip_unknown = compare_ip(ip.get_ip(), set(ip_linux + ip_windows))

    print("ip linux", ip_linux)
    print("ip windows", ip_windows)
    print("ip inconnu", ip_unknown)
