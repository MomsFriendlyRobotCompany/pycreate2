#!/usr/bin/env python

from __future__ import print_function
import create2api


port = '/dev/tty.usbserial-DA01NX3Z'

baud = {
	'default': 115200,
	'alt': 19200
}

bot = create2api.Create2(port=port, baud=baud['default'])

bot.start()
ret = bot.reset()
print(ret)
