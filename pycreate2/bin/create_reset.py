#!/usr/bin/env python3
#-*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
import pycreate2
import argparse

DESCRIPTION = """
Resets the Create 2.
"""


def handleArgs():
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('-m', '--max', help='max id', type=int, default=253)
    # parser.add_argument('-s', '--sleep', help='time in seconds between samples, default 1.0', type=float, default=1.0)
    parser.add_argument('-b', '--baud', help='baudrate, default is 115200', type=int, default=115200)
    parser.add_argument('port', help='serial port name, Ex: /dev/ttyUSB0 or COM1', type=str)

    args = vars(parser.parse_args())
    return args

def main():
    args = handleArgs()
    port = args['port']
    baud = args['baud']

    bot = pycreate2.Create2(port=port, baud=baud)

    bot.start()
    ret = bot.reset()
    print(ret)


if __name__ == "__main__":
    main()
