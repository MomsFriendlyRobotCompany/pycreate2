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

    # port = '/dev/tty.usbserial-DA01NX3Z'
    port = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DA01NX3Z-if00-port0"

    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    bot = pycreate2.Create2(port=port, baud=baud['default'])
    bot.start()
    bot.full()

    song_num = 3

    # if True:
    #     for sn in range(4):
    #         song = [70,0]
    #         bot.createSong(sn,song)
    #         bot.playSong(sn)
    #     time.sleep(0.25)

    # song = [59, 64, 62, 32, 69, 96, 67, 64, 62, 32, 60, 96, 59, 64, 59, 32, 59, 32, 60, 32, 62, 32, 64, 96, 62, 96]
    song = [76, 16, 76, 16, 76, 32, 76, 16, 76, 16, 76, 32, 76, 16, 79, 16, 72, 16, 74, 16, 76, 32, 77, 16, 77, 16, 77, 16, 77, 32, 77, 16]
    song = [76, 12, 76, 12, 20, 12, 76, 12, 20, 12, 72, 12, 76, 12, 20, 12, 79, 12, 20, 36, 67, 12, 20, 36]
    song = [72, 12, 20, 24, 67, 12, 20, 24, 64, 24, 69, 16, 71, 16, 69, 16, 68, 24, 70, 24, 68, 24, 67, 12, 65, 12, 67, 48]

    print(">> song len: ", len(song))

    bot.createSong(song_num, song)
    time.sleep(0.1)
    how_long = bot.playSong(song_num)

    # don't want to end too soon, so figure out how long the song is and sleep for
    # that time
    # dt = 0
    # for i in range(len(song)//2):
    #     dt += song[2*i+1]
    # dt = dt*(1/64)
    print('Sleep for:', how_long)
    time.sleep(how_long)
