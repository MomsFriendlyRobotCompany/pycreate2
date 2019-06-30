.. image:: https://raw.githubusercontent.com/walchko/pycreate2/master/pics/create.png
	:align: center

pyCreate2
================

.. image:: https://img.shields.io/pypi/l/pycreate2.svg
    :target: https://pypi.python.org/pypi/pycreate2
.. image:: https://img.shields.io/pypi/pyversions/pycreate2.svg
    :target:  https://pypi.python.org/pypi/pycreate2
.. image:: https://travis-ci.org/MomsFriendlyRobotCompany/pycreate2.svg?branch=master
    :target: https://travis-ci.org/MomsFriendlyRobotCompany/pycreate2
.. image:: https://img.shields.io/pypi/v/pycreate2.svg
    :target: https://pypi.python.org/pypi/pycreate2
.. image:: https://img.shields.io/pypi/format/pycreate2.svg
    :target:  https://pypi.python.org/pypi/pycreate2

A python library for controlling the `iRobot Create 2 <http://www.irobot.com/About-iRobot/STEM/Create-2.aspx>`_.

Install
------------

pip
~~~~~

The recommended way to install this library is::

	pip install pycreate2

Development
~~~~~~~~~~~~~

If you wish to develop and submit git-pulls, you can do::

	git clone https://github.com/walchko/pycreate2
	cd pycreate2
	pip install -e .

Unit Testing
~~~~~~~~~~~~~~~~

::

	nosetests -v -w tests test.py
	python3 -m nose -v -w tests test.py

Use
-------------

There are multiple ways to command the Create to move, here are some examples:

.. code-block:: python

	from  pycreate2 import Create2
	import time

	# Create a Create2.
	bot = Create2()

	# Start the Create 2
	bot.start()

	# Put the Create2 into 'safe' mode so we can drive it
	# This will still provide some protection
	bot.safe()

	# You are responsible for handling issues, no protection/safety in
	# this mode ... becareful
	bot.full()

	# directly set the motor speeds ... easier if using a joystick
	bot.drive_direct(100, 100)

	# turn an angle [degrees] at a speed: 45 deg, 100 mm/sec
	bot.turn_angle(45, 100)

	# drive straight for a distance: 5 meters, reverse 100 mm/sec
	bot.drive_distance(5, -100)

	# Tell the Create2 to drive straight forward at a speed of 100 mm/s
	bot.drive_straight(100)
	time.sleep(2)

	# Tell the Create2 to drive straight backward at a speed of 100 mm/s
	bot.drive_straight(-100)
	time.sleep(2)

	# Turn in place
	bot.drive_turn(100, 0)
	time.sleep(2)

	# Turn in place
	bot.drive_turn(-100, 0)
	time.sleep(4)

	# Turn in place
	bot.drive_turn(100, 0)
	time.sleep(2)

	# use the simpler drive direct
	bot.drive_direct(200,-200)  # inputs for motors are +/- 500 max
	time.sleep(2)

	# Stop the bot
	bot.drive_stop()

	# query some sensors
	sensors = bot.get_sensors()  # returns all data
	print(sensors.light_bumper_left)

	# Close the connection
	# bot.close()

More examples are found in the `examples folder <https://github.com/walchko/pycreate2/tree/master/examples>`_.

Documents
------------

Additional notes and documents are in the `docs folder <https://github.com/walchko/pycreate2/tree/master/docs/Markdown>`_.

Modes
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/walchko/pycreate2/master/pics/create_modes.png
	:align: center

The different modes (OFF, PASSIVE, SAFE, and FULL) can be switched between by calling different
commands.

- **OFF:** The robot is off and can charge, it will accept no commands
- **PASSIVE:** The robot is in standbye and can charge. It will send sensor packets, but will not move
- **SAFE:** The robot will not charge, but you full control over it with a few exceptions. If the cliff sensors or wheel drop sensors are triggered, the robot goes back to PASSIVE mode.
- **FULL:** The robot will not charge and you have full control. You are responsible to handle any response due to cliff, wheel drop or any other sensors.

Sensor Data
~~~~~~~~~~~~~

Sensor data is returned as a ``namedtuple`` from ``collections``. The information can be
accessed as either::

	sensors = bot.get_sensors()
	sensors.wall == sensors[1]  # True

=========================== =============== =================
Sensor                      Range           Index
=========================== =============== =================
bumps_wheeldrops            [0-15]           0
wall                        [0-1]            1
cliff_left                  [0-1]            2
cliff_front_left            [0-1]            3
cliff_front_right           [0-1]            4
cliff_right                 [0-1]            5
virtual_wall                [0-1]            6
overcurrents                [0-29]           7
dirt_detect                 [0-255]          8
ir_opcode                   [0-255]          9
buttons                     [0-255]          10
distance                    [-322768-32767]  11
angle                       [-322768-32767]  12
charger_state               [0-6]            13
voltage                     [0-65535]        14
current                     [-322768-32767]  15
temperature                 [-128-127]       16
battery_charge              [0-65535]        17
battery_capacity            [0-65535]        18
wall_signal                 [0-1023]         19
cliff_left_signal           [0-4095]         20
cliff_front_left_signal     [0-4095]         21
cliff_front_right_signal    [0-4095]         22
cliff_right_signal          [0-4095]         23
charger_available           [0-3]            24
open_interface_mode         [0-3]            25
song_number                 [0-4]            26
song_playing                [0-1]            27
oi_stream_num_packets       [0-108]          28
velocity                    [-500-500]       29
radius                      [-322768-32767]  30
velocity_right              [-500-500]       31
velocity_left               [-500-500]       32
encoder_counts_left         [-322768-32767]  33
encoder_counts_right        [-322768-32767]  34
light_bumper                [0-127]          35
light_bumper_left           [0-4095]         36
light_bumper_front_left     [0-4095]         37
light_bumper_center_left    [0-4095]         38
light_bumper_center_right   [0-4095]         39
light_bumper_front_right    [0-4095]         40
light_bumper_right          [0-4095]         41
ir_opcode_left              [0-255]          42
ir_opcode_right             [0-255]          43
left_motor_current          [-322768-32767]  44
right_motor_current         [-322768-32767]  45
main_brush_current          [-322768-32767]  46
side_brush_current          [-322768-32767]  47
statis                      [0-3]            48
=========================== =============== =================

Change Log
---------------

========== ======= =============================
2017-08-26 0.7.3   code clean up and doc updates
2017-08-26 0.7.2   updates and fixes
2017-05-26 0.5.0   init and published to pypi
========== ======= =============================

The MIT License
==================

**Copyright (c) 2007 Damon Kohler**

**Copyright (c) 2015 Jonathan Le Roux (Modifications for Create 2)**

**Copyright (c) 2015 Brandon Pomeroy**

**Copyright (c) 2017 Kevin Walchko**

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
