.. image:: https://raw.githubusercontent.com/walchko/pycreate2/master/pics/create.png
	:align: center

pyCreate2
================

A python library for controlling the iRobot Create 2

Install
------------

pip
~~~~~

The recommended way to install this library is::

	pip install pygecko

Development
~~~~~~~~~~~~~

If you wish to develop and submit git-pulls, you can do::

	git clone https://github.com/walchko/pycreate2
	cd pycreate2
	pip install -e .

Use
-------------

Create2API is meant to be interacted with through a single class: "Create2".
Interacting with your bot is a breeze::

.. code-block:: python

	import create2api
	import time

	# Create a Create2.
	bot = create2api.Create2()
	bot.wakeup()  # in case it is asleep

	# Start the Create 2
	# open serial port
	bot.start()

	# Put the Create2 into 'safe' mode so we can drive it
	# This will still provide some protection
	bot.safe()

	# Tell the Create2 to drive straight forward at a speed of 100 mm/s
	bot.drive_straight(100)
	time.sleep(2)

	# Tell the Create2 to drive straight backward at a speed of 100 mm/s
	bot.drive_straight(-100)
	time.sleep(2)

	# Turn in place
	bot.turn(100, 0)
	time.sleep(2)

	# Turn in place
	bot.turn(-100, 0)
	time.sleep(4)

	# Turn in place
	bot.turn(100, 0)
	time.sleep(2)

	# Stop the bot
	bot.stop()
	# bot.shutdown()  # powers it down saving batteries

	# Close the connection
	# bot.close()


Modes
----------

Passive Mode
~~~~~~~~~~~~~~~

Upon sending the Start command or any one of the cleaning mode commands (e.g.,
Spot, Clean, Seek Dock), the OI enters into Passive mode. When the OI is in
Passive mode, you can request and receive sensor data using any of the sensor
commands, but you cannot change the current command parameters for the actuators
(motors, speaker, lights, low side drivers, digital outputs) to something else.
To change how one of the actuators operates, you must switch from Passive mode
to Full mode or Safe mode.

While in Passive mode, you can read Roomba’s sensors, watch Roomba perform a
cleaning cycle, and charge the battery.

In Passive mode, Roomba will go into power saving mode to conserve battery
power after five minutes of inactivity. To disable sleep, pulse the BRC pin low
periodically before these five minutes expire. Each pulse resets this five
minute counter. (One example that would not cause the baud rate to inadvertently
change is to pulse the pin low for one second, every minute, but there are other
periods and duty cycles that would work, as well.)

Safe Mode
~~~~~~~~~~~~~~

When you send a Safe command to the OI, Roomba enters into Safe mode. Safe mode
gives you full control of Roomba, with the exception of the following safety-related
conditions:

- Detection of a cliff while moving forward (or moving backward with a small
turning radius, less than one robot radius).
- Detection of a wheel drop (on any wheel).
- Charger plugged in and powered.

Should one of the above safety-related conditions occur while the OI is in Safe
mode, Roomba stops all motors and reverts to the Passive mode.

If no commands are sent to the OI when in Safe mode, Roomba waits with all motors
and LEDs off and does not respond to button presses or other sensor input.

Note that charging terminates when you enter Safe Mode, and Roomba will not power
save.

Full Mode
~~~~~~~~~~~~~~~

When you send a Full command to the OI, Roomba enters into Full mode. Full mode
gives you complete control over Roomba, all of its actuators, and all of the
safety-related conditions that are restricted when the OI is in Safe mode, as
Full mode shuts off the cliff, wheel-drop and internal charger safety features.
To put the OI back into Safe mode, you must send the Safe command.

If no commands are sent to the OI when in Full mode, Roomba waits with all motors
and LEDs off and does not respond to button presses or other sensor input.

Note that charging terminates when you enter Full Mode, and Roomba will not power
save.

Sensor Data
-------------

sensor range packet 10 hz
-------------------------
ir bumper [0-127] 45
ir bumper [0-4095] 46-51
encoder [-322768-32767] 43,44

power
-----------------------------
current [-322768-32767] 23
voltage [0-65535] 22
motor current [-322768-32767] 54,55
battery charge [0-65535] 25
battery capacity [0-65535] 26 (doesn't change?)

Emergency
-------------------------------
cliff  [0-1] 9-12
cliff signal [0-4095] 28-31
overcurrents [0-29] 14
bump wheeldrops [015] 7


mode
---------------------------------
oi mode [0-3] 35

The available sensor data is:

``` python
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
    "cliff front left signal": 0,
    "charging state": 0,
    "side brush motor current": 0,
    "requested radius": 0,
    "current": 0,
    "light bumper": {
        "right": false,
        "center right": false,
        "front left": false,
        "center left": false,
        "front right": false,
        "left": false
    },
    "requested right velocity": 0,
    "angle": 0,
    "cliff front left": false,
    "temperature": 0,
    "wall seen": false,
    "battery capacity": 0,
    "cliff left signal": 0,
    "light bump center left signal": 0,
    "charging sources available": {
        "home base": false,
        "internal charger": false
    },
    "wall signal": 0,
    "infared char right": 0
}
```

Encoders
~~~~~~~~~~~~

**NOTE:** These encoders are square wave, not quadrature, so they rely on the
robot’s commanded velocity direction to know when to count up/down. So if the
robot is trying to drive forward, and you force the wheels to spin in reverse,
the encoders will count up, (and vice-versa). Additionally, the encoders will
count up when the commanded velocity is zero and the wheels spin.

To convert counts to distance, simply do a unit conversion using the equation
for circle circumference.

- N counts * (mm in 1 wheel revolution / counts in 1 wheel revolution) = mm
- N counts * (π * 72.0 / 508.8) = mm

Issues
----------

macOS
~~~~~~~~~~

Apple's [USB-A-to-C]() converter doesn't work with iRobot's USB-to-serial
converter. I used a [Monoprice USB-C Hub](https://www.amazon.com/gp/product/B019FN66IC/ref=oh_aui_detailpage_o03_s01?ie=UTF8&psc=1)
and it worked fine.


Implemented OI codes
----------------------

- Start
- Reset
- Stop
- Safe
- Full
- Seek Dock
- Power (Off)
- Drive
- Digit LED ASCII
- Sensors
- Song
- Play
- Query List

Change Log
---------------

========== ======= =============================
2017-05-26 0.0.1   init and published to pypi
========== ======= =============================

The MIT License
==================

**Copyright (c) 2007 Damon Kohler
Copyright (c) 2015 Jonathan Le Roux (Modifications for Create 2)
Copyright (c) 2015 Brandon Pomeroy
Copyright (c) 2017 Kevin Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
