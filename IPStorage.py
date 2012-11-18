#!/usr/bin/env python
# -*- coding: utf8 -*-
import socket
import struct
from trie import PrefixTrie

__author__ = 'uli'

class DB(object):

    def __init__(self):
        self._db = PrefixTrie()

    def __getstate__(self):
        return self._db

    def insert(self, ip, message=None):
        ipv4 = DB.IPv4(ip)
        self._db[bin(ipv4.network)[2:ipv4.netmask + 1]] = (ipv4, message)

    def __getitem__(self, ip):
        ipv4 = DB.IPv4(ip)
        return self._db.longest_prefix(bin(ipv4.network)[2:ipv4.netmask + 1])[1]

    def __delitem__(self, ip):
        ipv4 = DB.IPv4(ip)
        del self._db[bin(ipv4.network)[2:ipv4.netmask + 1]]

    def get(self, ip):
        return self.__getitem__(ip)

    class IPv4(object):
        def __init__(self, ip):
            self.ip, self.netmask  = self.normalize(ip)

            if self.netmask:
                self.wildcard = (1 << (32 - self.netmask)) - 1
            else:
                self.netmask = 32
                self.wildcard = 0x00000000

        def __getstate__(self):
            return (self.ip, self.netmask, self.wildcard)

        def __setstate__(self, state):
            self.ip, self.netmask, self.wildcard = state

        @property
        def network(self):
            return (self.ip - (self.ip & self.wildcard))

        def generate(self):
            network = self.network
            current_ip = network
            while (current_ip - (current_ip & self.wildcard)) == network:
                yield self.to_str(current_ip)
                current_ip += 1

        @classmethod
        def to_str(cls, ip):
            return "{0}.{1}.{2}.{3}".format((ip & 0XFF000000) >> 24, (ip & 0X00FF0000) >> 16, (ip & 0x0000FF00) >> 8, ip & 0x000000FF)

        @classmethod
        def normalize(cls, ip):
            netmask =  None

            if not ip:
                raise ValueError

            if '/' in ip:
                ip, netmask = ip.split("/", 1)

            octets = ip.split('.')

            if len(octets) >  4:
                raise ValueError("Too many octets for IPv4 address")

            if not netmask:
                netmask = len(octets) * 8

            try:
                netmask =  int(netmask)
            except ValueError:
                raise ValueError("netmask has invalid format: %s" % netmask)

            if not 0 <= netmask <=  32:
                raise ValueError("Netmask not between 0 and 32")

            ipnum = 0
            for index, octet in enumerate(octets):
                octet =  int(octet)
                if not 0 <=  octet <= 255:
                    raise ValueError("Value for octet too big: %d" % octet)


                ipnum += int(octet) * (256 ** (3-index))

            return (ipnum,  netmask)
