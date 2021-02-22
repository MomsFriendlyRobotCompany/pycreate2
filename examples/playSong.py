#!/usr/bin/env python3
#-*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
# play a song

import pycreate2
import time


if __name__ == "__main__":
    port = '/dev/tty.usbserial-DA01NX3Z'
    # port = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DA01NX3Z-if00-port0"

    bot = pycreate2.Create2(port=port)
    bot.start()
    bot.full()

    # random MIDI songs I found on the internet
    # they cannot be more than 16 midi notes or really 32 bytes arranged
    # as [(note, duration), ...]
    song = [59, 64, 62, 32, 69, 96, 67, 64, 62, 32, 60, 96, 59, 64, 59, 32, 59, 32, 60, 32, 62, 32, 64, 96, 62, 96]
    song = [76, 16, 76, 16, 76, 32, 76, 16, 76, 16, 76, 32, 76, 16, 79, 16, 72, 16, 74, 16, 76, 32, 77, 16, 77, 16, 77, 16, 77, 32, 77, 16]
    song = [76, 12, 76, 12, 20, 12, 76, 12, 20, 12, 72, 12, 76, 12, 20, 12, 79, 12, 20, 36, 67, 12, 20, 36]
    song = [72, 12, 20, 24, 67, 12, 20, 24, 64, 24, 69, 16, 71, 16, 69, 16, 68, 24, 70, 24, 68, 24, 67, 12, 65, 12, 67, 48]

    print(">> song len: ", len(song)//2)

    # song number can be 0-3
    song_num = 3
    bot.createSong(song_num, song)
    time.sleep(0.1)
    how_long = bot.playSong(song_num)

    # The song will run in the back ground, don't interrupt it
    # how_long is the time in secods for it to finish
    print('Sleep for:', how_long)
    time.sleep(how_long)
