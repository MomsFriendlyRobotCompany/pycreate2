#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import create2api
import time

"""
there are issues with creating and playing songs ... it works sometimes
"""
port = '/dev/tty.usbserial-DA01NX3Z'

baud = {
	'default': 115200,
	'alt': 19200  # shouldn't need this unless you accidentally set it to this
}

bot = create2api.Create2(port=port, baud=baud['default'])

song = [59, 64, 62, 32, 69, 96, 67, 64, 62, 32, 60, 96, 59, 64, 59, 32, 59, 32, 60, 32, 62, 32, 64, 96, 62, 96]

bot.start()
bot.safe()
bot.createSong(1, song)
time.sleep(1)
bot.playSong(1)

# don't want to end too soon, so figure out how long the song is and sleep for
# that time
dt = 0
for i in range(len(song)//2):
	dt += song[2*i+1]
dt = dt*(1/64)
print('Sleep for:', dt)
time.sleep(dt)
