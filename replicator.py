#!/usr/bin/env python

import sys
import socket, binascii
import logging.config, yaml
from textwrap import wrap
from wakeonlan import wol

BIND_ADDRESS = "0.0.0.0"
BIND_PORT = 5009


def read_payload(payload):
    try:
        frame = payload[:12]

        if frame.lower() == 'f' * 12:
            repetitions = payload[12:]
            list = wrap(repetitions, 12)

            if len(list) == 16:
                return list[0]

    except Exception:
        pass

    raise ValueError("Received payload is not valid")


def main():
    logconfig = yaml.load(open('logging.yml'))
    logging.config.dictConfig(logconfig)
    logger = logging.getLogger('replicator')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BIND_ADDRESS, BIND_PORT))

    while True:
        try:
            data, addr = sock.recvfrom(102)
            logger.debug("Received packet from %s:%s" % (addr[0], addr[1]))

            payload = binascii.hexlify(data)
            logger.debug("Received payload: %s" % payload)

            try:
                target = read_payload(payload)
                logger.debug("Waking up: %s" % target)
                wol.send_magic_packet(target)

            except ValueError as error:
                logger.debug(error)

        except KeyboardInterrupt:
            logger.debug("Exiting because of keyboard interrupt")
            sys.exit()


if __name__ == '__main__':
    main()
