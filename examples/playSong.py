#!/usr/bin/env python
# ----------------------------------------------------------------------------
# MIT License
# play a song

from __future__ import print_function
from __future__ import division
import pycreate2
import time


if __name__ == "__main__":
	print('there are issues with creating and playing songs ... it works sometimes')
	print('this is an iRobot/Create issue')

	port = '/dev/tty.usbserial-DA01NX3Z'

	baud = {
		'default': 115200,
		'alt': 19200  # shouldn't need this unless you accidentally set it to this
	}

	bot = pycreate2.Create2(port=port, baud=baud['default'])

	song = [59, 64, 62, 32, 69, 96, 67, 64, 62, 32, 60, 96, 59, 64, 59, 32, 59, 32, 60, 32, 62, 32, 64, 96, 62, 96]

	bot.start()
	bot.safe()
	how_long = bot.createSong(1, song)
	time.sleep(0.1)
	bot.playSong(1)

	# don't want to end too soon, so figure out how long the song is and sleep for
	# that time
	# dt = 0
	# for i in range(len(song)//2):
	# 	dt += song[2*i+1]
	# dt = dt*(1/64)
	print('Sleep for:', how_long)
	time.sleep(how_long)
