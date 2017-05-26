#!/usr/bin/env python

from __future__ import print_function
import create2api
import time


port = '/dev/tty.usbserial-DA01NX3Z'

baud = {
	'default': 115200,
	'alt': 19200
}

bot = create2api.Create2(port=port, baud=baud['default'])

bot.start()
# bot.shutdown()
# time.sleep(1)
bot.stop()
time.sleep(1)

print('=====================================================')
print('\n\tCreate Shutdown')
print('\tHit power button to wake-up\n')
print('=====================================================')
