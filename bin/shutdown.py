#!/usr/bin/env python

from __future__ import print_function
import pycreate2
import time


port = '/dev/tty.usbserial-DA01NX3Z'

baud = {
	'default': 115200,
	'alt': 19200
}

bot = pycreate2.Create2(port=port, baud=baud['default'])

bot.start()
# bot.shutdown()
# time.sleep(1)
bot.stop()
time.sleep(1)

print('=====================================================')
print('\n\tCreate Shutdown')
print('\tHit power button to wake-up\n')
print('=====================================================')
