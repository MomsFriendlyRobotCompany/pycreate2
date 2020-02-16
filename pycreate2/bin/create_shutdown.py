#!/usr/bin/env python

from __future__ import print_function
import pycreate2
import argparse
import time


DESCRIPTION = """
Shuts down the Create 2.
"""


def handleArgs():
	parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
	# parser.add_argument('-m', '--max', help='max id', type=int, default=253)
	# parser.add_argument('-s', '--sleep', help='time in seconds between samples, default 1.0', type=float, default=1.0)
	parser.add_argument('-b', '--baud', help='baudrate, default is 115200', type=int, default=115200)
	parser.add_argument('port', help='serial port name, Ex: /dev/ttyUSB0 or COM1', type=str)

	args = vars(parser.parse_args())
	return args


if __name__ == "__main__":

	args = handleArgs()
	port = args['port']
	baud = args['baud']

	bot = pycreate2.Create2(port=port, baud=baud)

	bot.start()
	time.sleep(0.25)
	bot.power()  # this seems to shut it down more than stop ... confused
	# bot.shutdown()
	time.sleep(0.25)
	bot.stop()
	time.sleep(1)

	print('=====================================================')
	print('\n\tCreate Shutdown')
	print('\tHit power button to wake-up\n')
	print('=====================================================')
