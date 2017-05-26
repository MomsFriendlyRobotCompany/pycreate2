#!/usr/bin/env python

from __future__ import print_function
import create2api
import time

"""
sensors           packet
all light bump    106

{
    "sensor data": {
        "wheel overcurrents": {
            "right wheel": false,
            "left wheel": false,
            "main brush": false,
            "side brush": false
        },
        "infared char omni": 0,
        "voltage": 0,
        "requested velocity": 0,
        "battery charge": 0,
        "light bump center right signal": 0,
        "song playing": false,
        "left motor current": 0,
        "dirt detect": 0,
        "buttons": {
            "dock": false,
            "clean": false,
            "hour": false,
            "clock": false,
            "schedule": false,
            "spot": false,
            "day": false,
            "minute": false
        },
        "requested left velocity": 0,
        "wheel drop and bumps": {
            "bump right": false,
            "drop left": false,
            "drop right": false,
            "bump left": false
        },
        "number of stream packets": 0,
        "song number": 0,
        "oi mode": 0,
        "stasis": false,
        "right encoder counts": 0,
        "cliff front right signal": 0,
        "main brush motor current": 0,
        "cliff left": false,
        "virtual wall": false,
        "light bump front right signal": 0,
        "distance": 0,
        "light bump right signal": 0,
        "light bump front left signal": 0,
        "cliff right": false,
        "left encoder counts": 0,
        "right motor current": 0,
        "infared char left": 0,
        "cliff front right": false,
        "cliff right signal": 0,
        "light bump left signal": 0,
        "cliff front right signal": 0,
        "side brush motor current": 0,
        "current": 0,
        "light bumper": {
            "left": false,
            "front left": false,
            "center left": false,
            "center right": false,
            "front right": false,
            "right": false
        },
        "requested right velocity": 0,
        "angle": 0,
        "temperature": 0,
        "battery capacity": 0,
        "cliff left signal": 0,
        "light bump center left signal": 0
    }
}
"""


# Create a Create2 Bot
port = '/dev/tty.usbserial-DA01NX3Z'
# baud = 19200
baud = 115200

bot = create2api.Create2(port=port, baud=baud)

bot.start()
# bot.reset()
# bot.wake()

bot.safe()

# bot.set_day_time('Friday', 17, 40)

# print 'Voltage: ' + str(bot.sensors['voltage'])
# print 'OI mode: ' + str(bot.sensors['oi mode'])
# print 'Battery temperature: ' + str(bot.sensors['temperature'])

print('forward')
bot.drive_straight(200)
time.sleep(1)

print('back')
bot.drive_straight(-200)
time.sleep(1)

# stop
bot.drive_straight(0)

print('turn right')
bot.drive_turn(100, -1)
time.sleep(2)

print('turn left')
bot.drive_turn(-100, -1)
time.sleep(4)

print('turn right')
bot.drive_turn(100, -1)
time.sleep(2)

# stop
bot.drive_stop()
# time.sleep(0.1)
bot.close()
