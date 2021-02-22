#!/usr/bin/env python3
#-*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

import pycreate2
import time


def prettyPrint(sensors):
    print('-'*70)
    print('{:>40} | {:<5}'.format('Sensor', 'Value'))
    print('-'*70)
    for k, v in sensors._asdict().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    # Create a Create2 Bot
    port = '/dev/tty.usbserial-DA01NX3Z'
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    # setup create 2
    bot = pycreate2.Create2(port)
    bot.start()
    bot.safe()

    bot.digit_led_ascii('hi')  # set a nice message
    bot.led(1)  # turn on debris light

    sensors = {}

    try:
        while True:
            sensors = bot.get_sensors()
            if sensors:
                prettyPrint(sensors)
            else:
                print('robot asleep')

            time.sleep(1)

    except KeyboardInterrupt:
        print('shutting down ... bye')
