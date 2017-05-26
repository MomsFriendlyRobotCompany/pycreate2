# The MIT License
#
# Copyright (c) 2007 Damon Kohler
# Copyright (c) 2015 Jonathan Le Roux (Modifications for Create 2)
# Copyright (c) 2015 Brandon Pomeroy
# Copyright (c) 2017 Kevin Walchko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Not every opcode is included here becauase they are not all useful.
# For example, no point in scheduling things, a raspberry pi is controlling
# this create 2, I can schedule things on it. There are no brushes installed
# in the create 2 model, so the cleaning modes aren't useful.

RESET = 7
OI_MODE = 35
START = 128
SAFE = 131
FULL = 132
POWER = 133
# SPOT = 134
# CLEAN = 135
# MAX = 136
DRIVE = 137
MOTORS = 138
LED = 139
SONG = 140
PLAY = 141
SENSORS = 142
SEEK_DOCK = 143
MOTORS_PWM = 144
DRIVE_DIRECT = 145
DRIVE_PWM = 146
# STREAM = 148
QUERY_LIST = 149
# PAUSE_RESUME_STREAM = 150
# SCHEDULING_LED = 162
# DIGIT_LED_RAW = 163  # doesn't work
DIGIT_LED_ASCII = 164
# BUTTONS = 165
# SCHEDULE = 167
# SET_DAY_TIME = 168
STOP = 173
