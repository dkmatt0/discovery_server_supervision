#!/usr/bin/env python3
# coding: utf-8

import sys

from scapy.all import sr1, IP, ICMP, TCP


class ScanIP(object):
    """Permet différent type de scan ip a partir d'un ou plusieurs plage ip"""

    def __init__(self):
        self.ip = []

    def _range_ip(self, begin, end):
        """Fourniture d'une liste d'ip allant de begin (inclus) à end (inclus)."""
        # Convertion en liste
        begin = [int(x) for x in begin.split(".")]
        end = [int(x) for x in end.split(".")]

        # Mise en ordre des ip (la plus petite dans begin)
        b = ["{0:0>3}".format(x) for x in begin]
        e = ["{0:0>3}".format(x) for x in end]
        if b > e:
            begin, end = end, begin
        del b
        del e

        # Creation de la liste d'adresse
        list_address = []
        while begin <= end:
            list_address.append(".".join([str(x) for x in begin]))
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

    def add_ip(self, ip):
        if type(ip) is not tuple:
            raise TypeError
        self.ip.extend(self._range_ip(*ip))
        return len(self.ip)

    def check_ping(self, timeout=3, keep_ip=False):
        """Fonction de ping (ICMP)."""
        list_ip = []
        for ip in self.ip:
            response = sr1(IP(dst=ip) / ICMP(), timeout=timeout, verbose=False)
            if response is not None and response[1].type == 0:
                list_ip.append(ip)
        if keep_ip:
            return list_ip
        else:
            self.ip = list_ip
            len(self.ip)

    def check_icmp(self, *args, **kwargs):
        return self.check_ping(*args, **kwargs)

    def check_tcp(self, ip, timeout=3, keep_ip=False):
        """Fonction de scan tcp."""
        pass

    def get_ip(self):
        return self.ip
