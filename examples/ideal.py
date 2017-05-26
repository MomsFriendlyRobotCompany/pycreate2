#!/usr/bin/env python

from __future__ import print_function
from create2api import Create2
import time

# Create a Create2 robot
robot = Create2()

# open serial port and get ready to do things
robot.start(port='/dev/tty.usbserial-DA01NX3Z')

print('forward')
robot.drive_straight(200)
time.sleep(1)

print('back')
robot.drive_straight(-200)
time.sleep(1)

robot.stop()
robot.close()
