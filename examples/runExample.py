#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# MIT License
# moves the roomba through a simple sequence

# from __future__ import print_function
import pycreate2
import time


if __name__ == "__main__":
    # Create a Create2 Bot
    port = '/dev/tty.usbserial-DA01NX3Z'  # this is the serial port on my iMac
    # port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    bot = pycreate2.Create2(port=port, baud=baud['default'])

    # define a movement path
    path = [
        ['forward', 200, 1, 'for'],
        ['back', -200, 2, 'back'],
        ['stop', 0, 0.1, 'stop'],
        ['turn right', 100, 2, 'rite'],
        ['turn left', -100, 4, 'left'],
        ['turn right', 100, 2, 'rite'],
        ['stop', 0, 0.1, 'stop']
    ]

    bot.start()
    bot.safe()

    # path to move
    for mov in path:
        name, vel, dt, string = mov
        print(name)
        bot.digit_led_ascii(string)
        if name in ['forward', 'back', 'stop']:
            bot.drive_straight(vel)
            time.sleep(dt)
        elif name in ['turn right', 'turn left']:
            bot.drive_turn(vel, -1)
        else:
            raise Exception('invalid movement command')

    print('shutting down ... bye')
    bot.drive_stop()
    time.sleep(0.1)
