#!/usr/bin/env python
# ----------------------------------------------------------------------------
# MIT License
# shows how to get sensor data from the create 2

from __future__ import print_function
from pycreate2 import Create2
import time


if __name__ == "__main__":
    port = '/dev/tty.usbserial-DA01NX3Z'
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    bot = Create2(port=port, baud=baud['default'])

    bot.start()

    bot.safe()

    print('Starting ...')

    while True:
        # Packet 100 contains all sensor data.
        sensor_state = bot.get_sensors()

        print('==============Updated Sensors==============')
        print(sensor_state)
        time.sleep(2)
