![image](https://raw.githubusercontent.com/walchko/pycreate2/master/pics/create.png)

# pyCreate2

[![Actions Status](https://github.com/MomsFriendlyRobotCompany/pycreate2/workflows/CheckPackage/badge.svg)](https://github.com/MomsFriendlyRobotCompany/pycreate2/actions)
![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/pycreate2)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycreate2)
![PyPI](https://img.shields.io/pypi/v/pycreate2)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pycreate2?color=aqua)

A python library for controlling the [iRobot
Create 2](http://www.irobot.com/About-iRobot/STEM/Create-2.aspx). This was used
in ECE 387 Introduction to Robotics class I taught at the US Air Force Academy.

- [video](https://vimeo.com/266619301): robot could only follow the black tap road and couldn't run into anything. If anything got in the way, it had to naviage around it to its final destination
- [video](https://vimeo.com/266619767): robot pet, follow the pink ball
- [video](https://vimeo.com/266619636): robot pet, follow the pink ball

## Install

### pip

The recommended way to install this library is:

```bash
pip install pycreate2
```

### Development

If you wish to develop and submit git-pulls, you can do:

```bash
git clone https://github.com/walchko/pycreate2
cd pycreate2
poetry install
poetry run pytest -v
```

## Use

There are multiple ways to command the Create to move, here are some
examples:

```python
from  pycreate2 import Create2
import time

# Create a Create2.
port = "/dev/serial"  # where is your serial port?
bot = Create2(port)

# Start the Create 2
bot.start()

# Put the Create2 into 'safe' mode so we can drive it
# This will still provide some protection
bot.safe()

# You are responsible for handling issues, no protection/safety in
# this mode ... becareful
bot.full()

# directly set the motor speeds ... move forward
bot.drive_direct(100, 100)
time.sleep(2)

# turn in place
bot.drive_direct(200,-200)  # inputs for motors are +/- 500 max
time.sleep(2)

# Stop the bot
bot.drive_stop()

# query some sensors
sensors = bot.get_sensors()  # returns all data
print(sensors.light_bumper_left)

# Close the connection
# bot.close()
```

More examples are found in the [examples
folder](https://github.com/walchko/pycreate2/tree/master/examples).

## Documents

Additional notes and documents are in the [docs
folder](https://github.com/walchko/pycreate2/tree/master/docs/Markdown).

### Modes

![image](https://raw.githubusercontent.com/walchko/pycreate2/master/pics/create_modes.png)

The different modes (OFF, PASSIVE, SAFE, and FULL) can be switched
between by calling different commands.

  - **OFF:** The robot is off and can charge, it will accept no commands
  - **PASSIVE:** The robot is in standbye and can charge. It will send
    sensor packets, but will not move
  - **SAFE:** The robot will not charge, but you full control over it
    with a few exceptions. If the cliff sensors or wheel drop sensors
    are triggered, the robot goes back to PASSIVE mode.
  - **FULL:** The robot will not charge and you have full control. You
    are responsible to handle any response due to cliff, wheel drop or
    any other sensors.

### Sensor Data

Sensor data is returned as a `namedtuple` from `collections`. The
information can be accessed as either:

```python
sensors = bot.get_sensors()
sensors.wall == sensors[1]  # True
```

| Sensor                       | Range             | Index |
|------------------------------|-------------------|-------|
| bumps\_wheeldrops            | \[0-15\]          |   0   |
| wall                         | \[0-1\]           |   1   |
| cliff\_left                  | \[0-1\]           |   2   |
| cliff\_front\_left           | \[0-1\]           |   3   |
| cliff\_front\_right          | \[0-1\]           |   4   |
| cliff\_right                 | \[0-1\]           |   5   |
| virtual\_wall                | \[0-1\]           |   6   |
| overcurrents                 | \[0-29\]          |   7   |
| dirt\_detect                 | \[0-255\]         |   8   |
| ir\_opcode                   | \[0-255\]         |   9   |
| buttons                      | \[0-255\]         |   10  |
| distance                     | \[-322768-32767\] |   11  |
| angle                        | \[-322768-32767\] |   12  |
| charger\_state               | \[0-6\]           |   13  |
| voltage                      | \[0-65535\]       |   14  |
| current                      | \[-322768-32767\] |   15  |
| temperature                  | \[-128-127\]      |   16  |
| battery\_charge              | \[0-65535\]       |   17  |
| battery\_capacity            | \[0-65535\]       |   18  |
| wall\_signal                 | \[0-1023\]        |   19  |
| cliff\_left\_signal          | \[0-4095\]        |   20  |
| cliff\_front\_left\_signal   | \[0-4095\]        |   21  |
| cliff\_front\_right\_signal  | \[0-4095\]        |   22  |
| cliff\_right\_signal         | \[0-4095\]        |   23  |
| charger\_available           | \[0-3\]           |   24  |
| open\_interface\_mode        | \[0-3\]           |   25  |
| song\_number                 | \[0-4\]           |   26  |
| song\_playing                | \[0-1\]           |   27  |
| oi\_stream\_num\_packets     | \[0-108\]         |   28  |
| velocity                     | \[-500-500\]      |   29  |
| radius                       | \[-322768-32767\] |   30  |
| velocity\_right              | \[-500-500\]      |   31  |
| velocity\_left               | \[-500-500\]      |   32  |
| encoder\_counts\_left        | \[-322768-32767\] |   33  |
| encoder\_counts\_right       | \[-322768-32767\] |   34  |
| light\_bumper                | \[0-127\]         |   35  |
| light\_bumper\_left          | \[0-4095\]        |   36  |
| light\_bumper\_front\_left   | \[0-4095\]        |   37  |
| light\_bumper\_center\_left  | \[0-4095\]        |   38  |
| light\_bumper\_center\_right | \[0-4095\]        |   39  |
| light\_bumper\_front\_right  | \[0-4095\]        |   40  |
| light\_bumper\_right         | \[0-4095\]        |   41  |
| ir\_opcode\_left             | \[0-255\]         |   42  |
| ir\_opcode\_right            | \[0-255\]         |   43  |
| left\_motor\_current         | \[-322768-32767\] |   44  |
| right\_motor\_current        | \[-322768-32767\] |   45  |
| main\_brush\_current         | \[-322768-32767\] |   46  |
| side\_brush\_current         | \[-322768-32767\] |   47  |
| statis                       | \[0-3\]           |   48  |


## Change Log

|            |       |                               |
| ---------- | ----- | ----------------------------- |
| 2021-02-22 | 0.8.1 | Cleaned up code               |
| 2020-02-16 | 0.8.0 | Simplified interface and bug fixes |
| 2020-02-16 | 0.7.7 | Fixed typo with poetry        |
| 2020-02-16 | 0.7.6 | Fixed typo erro in `bin`      |
| 2020-02-16 | 0.7.5 | Switched to toml and poetry   |
| 2019-06-30 | 0.7.4 | Midi sounds working           |
| 2017-08-26 | 0.7.3 | code clean up and doc updates |
| 2017-08-26 | 0.7.2 | updates and fixes             |
| 2017-05-26 | 0.5.0 | init and published to pypi    |

# The MIT License

**Copyright (c) 2007 Damon Kohler**

**Copyright (c) 2015 Jonathan Le Roux (Modifications for Create 2)**

**Copyright (c) 2015 Brandon Pomeroy**

**Copyright (c) 2017 Kevin Walchko**

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
