#!/usr/bin/env python

from __future__ import print_function
import pycreate2
import time


# Create a Create2 Bot
port = '/dev/tty.usbserial-DA01NX3Z'
baud = {
	'default': 115200,
	'alt': 19200  # shouldn't need this unless you accidentally set it to this
}

bot = pycreate2.Create2(port=port, baud=baud['default'])

bot.start()

bot.safe()

print('forward')
bot.drive_straight(200)
time.sleep(1)

print('back')
bot.drive_straight(-200)
time.sleep(1)

# stop
bot.drive_straight(0)

print('turn right')
bot.drive_turn(100, -1)
time.sleep(2)

print('turn left')
bot.drive_turn(-100, -1)
time.sleep(4)

print('turn right')
bot.drive_turn(100, -1)
time.sleep(2)

print('stop')
bot.drive_stop()
time.sleep(0.1)
