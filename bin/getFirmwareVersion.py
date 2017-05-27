#!/usr/bin/env python

from __future__ import print_function
import pycreate2


port = '/dev/tty.usbserial-DA01NX3Z'

baud = {
	'default': 115200,
	'alt': 19200
}

bot = pycreate2.Create2(port=port, baud=baud['default'])

bot.start()
ret = bot.reset()
print(ret)
