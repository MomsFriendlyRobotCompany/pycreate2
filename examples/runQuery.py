#!/usr/bin/env python

from __future__ import print_function
import pycreate2
from pycreate2.OI import calc_query_data_len
from pprint import pprint
import time


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

sensors = {}

pkts = [46, 47, 48, 49, 50, 51]
sensor_pkt_len = calc_query_data_len(pkts)

while True:
	raw = bot.query_list(pkts, sensor_pkt_len)

	if raw:
		for p in pkts:
			bot.decoder.decode_packet(p, raw, sensors)
		print('Sensors:')
		pprint(sensors)
	else:
		print('robot asleep')

	# time.sleep(0.05)
