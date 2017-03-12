#!/usr/bin/env python

import binascii
import logging.config
import os
import re
import socket
import sys
import yaml

BIND_ADDRESS = "0.0.0.0"
BIND_PORT = 5009

TARGET_ADDRESS = "255.255.255.255"
TARGET_PORT = 9

# https://regex101.com/r/2l8eJp/2
DGRAM_REGEX = re.compile(r'(?:^([fF]){12}([0-9a-fA-F]{12}){16}([0-9a-fA-F]{12})?$)')


def forward_packet(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((TARGET_ADDRESS, TARGET_PORT))
    sock.send(data)
    sock.close()


def main():
    with open(os.path.join(os.path.dirname(__file__), 'logging.yml')) as file:
        logging.config.dictConfig(yaml.load(file))

    logger = logging.getLogger('replicator')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BIND_ADDRESS, BIND_PORT))

    while True:
        try:
            data, addr = sock.recvfrom(108)
            logger.debug("Received packet from ip %s port %s" % (addr[0], addr[1]))

            payload = binascii.hexlify(data)
            logger.debug("Received payload: %s" % payload)

            if DGRAM_REGEX.match(payload):
                target = DGRAM_REGEX.search(payload).group(2)
                logger.debug("Forwarding the packet for %s to ip %s port %s" % (target, TARGET_ADDRESS, TARGET_PORT))
                forward_packet(data)
            else:
                logger.debug("Received payload is not valid, ignoring...")

        except KeyboardInterrupt:
            logger.debug("Exiting because of keyboard interrupt")
            sys.exit()


if __name__ == '__main__':
    main()
