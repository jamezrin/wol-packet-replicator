#!/usr/bin/env python

import binascii
import re
import socket
import sys
import logging
import os

BIND_ADDRESS = "0.0.0.0"
BIND_PORT = 5009

TARGET_ADDRESS = "255.255.255.255"
TARGET_PORT = 9

# https://regex101.com/r/2l8eJp/3
DGRAM_REGEX = re.compile(r'(?:^([fF]{12})(([0-9a-fA-F]{12}){16})([0-9a-fA-F]{12})?$)')


def forward_packet(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((TARGET_ADDRESS, TARGET_PORT))
    sock.send(data)
    sock.close()


def handle_packet(data):
    payload = binascii.hexlify(data)
    logger.debug("Received payload: %s" % payload)

    if DGRAM_REGEX.match(payload):
        target = DGRAM_REGEX.search(payload).group(3)
        logger.debug("Forwarding the packet for %s to ip %s port %s" % (target, TARGET_ADDRESS, TARGET_PORT))
        forward_packet(data)
    else:
        logger.debug("Received payload is not valid, ignoring...")


def start_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BIND_ADDRESS, BIND_PORT))

    while True:
        data, addr = sock.recvfrom(108)
        logger.debug("Received packet from ip %s port %s" % (addr[0], addr[1]))
        handle_packet(data)


if __name__ == '__main__':
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")
    logger = logging.getLogger()

    path = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(path, "app.log")

    fileHandler = logging.FileHandler(file)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.DEBUG)

    try:
        logger.debug("The application has now started listening for packets")
        start_listener()
    except KeyboardInterrupt:
        logger.debug("Exiting because of keyboard interrupt")
        sys.exit()
