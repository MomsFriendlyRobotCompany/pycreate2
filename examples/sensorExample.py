#!/usr/bin/env python

from __future__ import print_function
import create2api
# import json   # We'll use this to format the output
import time
from pprint import pprint


port = '/dev/tty.usbserial-DA01NX3Z'
# baud = 19200
baud = 115200

bot = create2api.Create2(port=port, baud=baud)

# bot.start()

# bot.reset()

# bot.start()

# exit()

# bot.getMode()

# bot.reset()
# time.sleep(1)

bot.start()  # ??

bot.getMode()

bot.safe()   # set to drive

bot.getMode()

exit(0)

print('Starting ...')

while True:
	# Packet 100 contains all sensor data.
	bot.get_packet(100)

	print('==============Updated Sensors==============')
	# print json.dumps(bot.sensor_state, indent=4, sort_keys=False)
	pprint(bot.sensor_state)
	time.sleep(2)
