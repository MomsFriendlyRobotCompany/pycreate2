#!/usr/bin/env python

from __future__ import division, print_function
from struct import Struct
import os
# from pprint import pprint
from collections import namedtuple

# https://stackoverflow.com/questions/2646157/what-is-the-fastest-to-access-struct-like-object-in-python


def CtoF(x):
	return x

# use: unpack_bool_byte(data)[0] -> returns tuple, but grab 0 entry
unpack_bool_byte = Struct('?').unpack         # 1 byte bool
unpack_byte = Struct('b').unpack              # 1 signed byte
unpack_unsigned_byte = Struct('B').unpack     # 1 unsigned byte
unpack_short = Struct('>h').unpack            # 2 signed bytes (short)
unpack_unsigned_short = Struct('>H').unpack   # 2 unsigned bytes (ushort)

# could replace with:
# class LEDS(object): DEBRIS=0x01; SPOT=0x02; DOCK=0x04; CHECK_ROBOT=0x08
class Namespace(object):
	def __init__(self, **kwds):
		self.__dict__.update(kwds)


# BAUD_RATE           = Namespace(BAUD_300=0, BAUD_600=1, BAUD_1200=2, BAUD_2400=3, BAUD_4800=4, BAUD_9600=5, BAUD_14400=6,
#                                BAUD_19200=7, BAUD_28800=8, BAUD_38400=9, BAUD_57600=10, BAUD_115200=11, DEFAULT=11)
# DAYS                = Namespace(SUNDAY=0x01, MONDAY=0x02, TUESDAY=0x04, WEDNESDAY=0x08, THURSDAY=0x10, FRIDAY=0x20,
#                                SATURDAY=0x40)
DRIVE               = Namespace(STRAIGHT=0x8000, STRAIGHT_ALT=0x7FFF, TURN_IN_PLACE_CW=0xFFFF, TURN_IN_PLACE_CCW=0x0001)
MOTORS              = Namespace(SIDE_BRUSH=0x01, VACUUM=0x02, MAIN_BRUSH=0x04, SIDE_BRUSH_DIRECTION=0x08,
                               MAIN_BRUSH_DIRECTION=0x10)
LEDS                = Namespace(DEBRIS=0x01, SPOT=0x02, DOCK=0x04, CHECK_ROBOT=0x08)
# WEEKDAY_LEDS        = Namespace(SUNDAY=0x01, MONDAY=0x02, TUESDAY=0x04, WEDNESDAY=0x08, THURSDAY=0x10, FRIDAY=0x20,
#                                SATURDAY=0x40)
# SCHEDULING_LEDS     = Namespace(COLON=0x01, PM=0x02, AM=0x04, CLOCK=0x08, SCHEDULE=0x10)
# RAW_LED             = Namespace(A=0x01, B=0x02, C=0x04, D=0x08, E=0x10, F=0x20, G=0x40)
BUTTONS             = Namespace(CLEAN=0x01, SPOT=0x02, DOCK=0x04, MINUTE=0x08, HOUR=0x10, DAY=0x20, SCHEDULE=0x40,
                               CLOCK=0x80)
ROBOT               = Namespace(TICK_PER_REV=508.8, WHEEL_DIAMETER=72, WHEEL_BASE=235,
                               TICK_TO_DISTANCE=0.44456499814949904317867595046408)
MODES               = Namespace(OFF=0, PASSIVE=1, SAFE=2, FULL=3)
WHEEL_OVERCURRENT   = Namespace(SIDE_BRUSH=0x01, MAIN_BRUSH=0x02, RIGHT_WHEEL=0x04, LEFT_WHEEL=0x08)
BUMPS_WHEEL_DROPS   = Namespace(BUMP_RIGHT=0x01, BUMP_LEFT=0x02, WHEEL_DROP_RIGHT=0x04, WHEEL_DROP_LEFT=0x08)
CHARGE_SOURCE       = Namespace(INTERNAL=0x01, HOME_BASE=0x02)
LIGHT_BUMPER        = Namespace(LEFT=0x01, FRONT_LEFT=0x02, CENTER_LEFT=0x04, CENTER_RIGHT=0x08, FRONT_RIGHT=0x10,
                               RIGHT=0x20)
STASIS              = Namespace(TOGGLING=0x01, DISABLED=0x02)

BumpsAndWheelDrop = namedtuple('BumpsAndWheelDrop', 'bump_left bump_right wheeldrop_left wheeldrop_right')
WheelOvercurrents = namedtuple('WheelOvercurrents', 'side_brush_overcurrent main_brush_overcurrent right_wheel_overcurrent left_wheel_overcurrent')
Buttons = namedtuple('Buttons', 'clean spot dock minute hour day schedule clock')
ChargingSources = namedtuple('ChargingSources', 'internal_charger home_base')
LightBumper = namedtuple('LightBumper', 'left front_left center_left center_right front_right right')
Stasis = namedtuple('Stasis', 'toggling disabled')

Sensors = namedtuple('Sensors', [
	'bumps_wheeldrops',
	'wall',
	'cliff_left',
	'cliff_front_left',
	'cliff_front_right',
	'cliff_right',
	'virtual_wall',
	'overcurrents',
	'dirt_detect',
	'ir_opcode',
	'buttons',
	'distance',
	'angle',
	'charger_state',
	'voltage',
	'current',
	'temperature',
	'battery_charge',
	'battery_capacity',
	'wall_signal',
	'cliff_left_signal',
	'cliff_front_left_signal',
	'cliff_front_right_signal',
	'cliff_right_signal',
	'charger_available',
	'open_interface_mode',
	'song_number',
	'song_playing',
	'oi_stream_num_packets',
	'velocity',
	'radius',
	'velocity_right',
	'velocity_left',
	'encoder_counts_left',
	'encoder_counts_right',
	'light_bumper',
	'light_bumper_left',
	'light_bumper_front_left',
	'light_bumper_center_left',
	'light_bumper_center_right',
	'light_bumper_front_right',
	'light_bumper_right',
	'ir_opcode_left',
	'ir_opcode_right',
	'left_motor_current',
	'right_motor_current',
	'main_brush_current',
	'side_brush_current',
	'statis'
])


def DecodSensorPackets(data):
	"""
	This class holds all sensors for the Create 2. It is basically like a C
	struct.
	"""

	if len(data) != 80:
		raise Exception('Sensor data not 80 bytes long, it is: {}'.format(len(data)))

	# packets 32, 33 or data bits 36, 37, 38 - unused
	# packet 16 or data bit 9 - unused
	# self.bumps_and_wheel_drops = BumpsAndWheelDrop(data[0:1])

	d = unpack_unsigned_byte(data[0:1])[0]
	bumps_wheeldrops = BumpsAndWheelDrop(
		bool(d & BUMPS_WHEEL_DROPS.BUMP_RIGHT),
		bool(d & BUMPS_WHEEL_DROPS.BUMP_LEFT),
		bool(d & BUMPS_WHEEL_DROPS.WHEEL_DROP_RIGHT),
		bool(d & BUMPS_WHEEL_DROPS.WHEEL_DROP_LEFT)
	)
	d = unpack_unsigned_byte(data[7:8])[0]
	overcurrents = WheelOvercurrents(
		bool(d & WHEEL_OVERCURRENT.SIDE_BRUSH),
		bool(d & WHEEL_OVERCURRENT.MAIN_BRUSH),
		bool(d & WHEEL_OVERCURRENT.RIGHT_WHEEL),
		bool(d & WHEEL_OVERCURRENT.LEFT_WHEEL)
	)
	# self.buttons = Buttons(data[11:12])
	d = unpack_unsigned_byte(data[11:12])[0]
	buttons = Buttons(
		bool(d & BUTTONS.CLEAN),
		bool(d & BUTTONS.SPOT),
		bool(d & BUTTONS.DOCK),
		bool(d & BUTTONS.MINUTE),
		bool(d & BUTTONS.HOUR),
		bool(d & BUTTONS.DAY),
		bool(d & BUTTONS.SCHEDULE),
		bool(d & BUTTONS.CLOCK)
	)
	# self.charging_sources = ChargingSources(data[39:40])
	d = unpack_unsigned_byte(data[39:40])[0]
	charging_sources = ChargingSources(
		bool(d & CHARGE_SOURCE.INTERNAL),
		bool(d & CHARGE_SOURCE.HOME_BASE)
	)
	# self.light_bumper = LightBumper(data[56:57])
	d = unpack_unsigned_byte(data[56:57])[0]
	light_bumper = LightBumper(
		bool(d & LIGHT_BUMPER.LEFT),
		bool(d & LIGHT_BUMPER.FRONT_LEFT),
		bool(d & LIGHT_BUMPER.CENTER_LEFT),
		bool(d & LIGHT_BUMPER.CENTER_RIGHT),
		bool(d & LIGHT_BUMPER.FRONT_RIGHT),
		bool(d & LIGHT_BUMPER.RIGHT)
	)
	# self.stasis = Stasis(data[79:80])
	d = unpack_unsigned_byte(data[79:80])[0]
	stasis = Stasis(
		bool(d & STASIS.TOGGLING),
		bool(d & STASIS.DISABLED)
	)

	sensors = Sensors(
		bumps_wheeldrops,
		unpack_bool_byte(data[1:2])[0],  # wall
		unpack_bool_byte(data[2:3])[0],  # cliff left
		unpack_bool_byte(data[3:4])[0],  # cliff front left
		unpack_bool_byte(data[4:5])[0],  # cliff front right
		unpack_bool_byte(data[5:6])[0],  # cliff right
		unpack_bool_byte(data[6:7])[0],  # virtual wall
		overcurrents,
		unpack_byte(data[8:9])[0],  # dirt detect
		# packet 16 or data bit 9 - unused
		unpack_unsigned_byte(data[10:11])[0],  # ir opcode
		buttons,
		unpack_short(data[12:14])[0],  # distance
		unpack_short(data[14:16])[0],  # angle
		unpack_unsigned_byte(data[16:17])[0],  # charge state
		unpack_unsigned_short(data[17:19])[0],  # voltage
		unpack_short(data[19:21])[0],  # current
		unpack_byte(data[21:22])[0],  # temperature C
		unpack_unsigned_short(data[22:24])[0],  # battery charge
		unpack_unsigned_short(data[24:26])[0],  # battery capacity
		unpack_unsigned_short(data[26:28])[0],  # wall
		unpack_unsigned_short(data[28:30])[0],  # cliff left
		unpack_unsigned_short(data[30:32])[0],  # cliff ront left
		unpack_unsigned_short(data[32:34])[0],  # cliff front right
		unpack_unsigned_short(data[34:36])[0],  # cliff right
		# packets 32, 33 or data bits 36, 37, 38 - unused
		charging_sources,
		unpack_unsigned_byte(data[40:41])[0],  # oi mode
		unpack_unsigned_byte(data[41:42])[0],  # song number
		unpack_bool_byte(data[42:43])[0],  # song playing
		unpack_unsigned_byte(data[43:44])[0],  # oi stream num packets
		unpack_short(data[44:46])[0],  # velocity
		unpack_short(data[46:48])[0],  # radius
		unpack_short(data[48:50])[0],  # velocity right
		unpack_short(data[50:52])[0],  # velocity left
		unpack_unsigned_short(data[52:54])[0],  # encoder left
		unpack_unsigned_short(data[54:56])[0],  # encoder right
		light_bumper,
		unpack_unsigned_short(data[57:59])[0],  # light bump left
		unpack_unsigned_short(data[59:61])[0],  # light bmp front left
		unpack_unsigned_short(data[61:63])[0],  # light bump center left
		unpack_unsigned_short(data[63:65])[0],  # light bump center right
		unpack_unsigned_short(data[65:67])[0],  # light bump front right
		unpack_unsigned_short(data[67:69])[0],  # light bump right
		unpack_unsigned_byte(data[69:70])[0],  # ir opcode left
		unpack_unsigned_byte(data[70:71])[0],  # ir opcode right
		unpack_short(data[71:73])[0],  # left motor current
		unpack_short(data[73:75])[0],  # right motor current
		unpack_short(data[75:77])[0],  # main brush current
		unpack_short(data[77:79])[0],  # side brush current
		stasis  # stasis
	)

	return sensors


if __name__ == "__main__":
	data = bytearray(os.urandom(80))
	sensors = DecodSensorPackets(data)
	print('-'*70)
	print(sensors)
