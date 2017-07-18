#!/usr/bin/env python

from __future__ import division, print_function
from struct import Struct
import os
from pprint import pprint
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


BAUD_RATE           = Namespace(BAUD_300=0, BAUD_600=1, BAUD_1200=2, BAUD_2400=3, BAUD_4800=4, BAUD_9600=5, BAUD_14400=6,
                               BAUD_19200=7, BAUD_28800=8, BAUD_38400=9, BAUD_57600=10, BAUD_115200=11, DEFAULT=11)
DAYS                = Namespace(SUNDAY=0x01, MONDAY=0x02, TUESDAY=0x04, WEDNESDAY=0x08, THURSDAY=0x10, FRIDAY=0x20,
                               SATURDAY=0x40)
DRIVE               = Namespace(STRAIGHT=0x8000, STRAIGHT_ALT=0x7FFF, TURN_IN_PLACE_CW=0xFFFF, TURN_IN_PLACE_CCW=0x0001)
MOTORS              = Namespace(SIDE_BRUSH=0x01, VACUUM=0x02, MAIN_BRUSH=0x04, SIDE_BRUSH_DIRECTION=0x08,
                               MAIN_BRUSH_DIRECTION=0x10)
LEDS                = Namespace(DEBRIS=0x01, SPOT=0x02, DOCK=0x04, CHECK_ROBOT=0x08)
WEEKDAY_LEDS        = Namespace(SUNDAY=0x01, MONDAY=0x02, TUESDAY=0x04, WEDNESDAY=0x08, THURSDAY=0x10, FRIDAY=0x20,
                               SATURDAY=0x40)
SCHEDULING_LEDS     = Namespace(COLON=0x01, PM=0x02, AM=0x04, CLOCK=0x08, SCHEDULE=0x10)
RAW_LED             = Namespace(A=0x01, B=0x02, C=0x04, D=0x08, E=0x10, F=0x20, G=0x40)
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


# class BumpsAndWheelDrop(object):
# 	def __init__(self, data):
# 		data = unpack_unsigned_byte(data)[0]
# 		self.bump_right = bool(data & BUMPS_WHEEL_DROPS.BUMP_RIGHT)
# 		self.bump_left = bool(data & BUMPS_WHEEL_DROPS.BUMP_LEFT)
# 		self.wheel_drop_right = bool(data & BUMPS_WHEEL_DROPS.WHEEL_DROP_RIGHT)
# 		self.wheel_drop_left = bool(data & BUMPS_WHEEL_DROPS.WHEEL_DROP_LEFT)
#
# 	def __repr__(self):
# 		return str(self.__dict__)

# BAWD = namedtuple('BAWD', 'bump_right bump_left wheel_drop_right wheel_drop_left')
# class BumpsAndWheelDrop(BAWD):
BumpsAndWheelDrop = namedtuple('BumpsAndWheelDrop', 'bump_right bump_left wheel_drop_right wheel_drop_left')


class WheelOvercurrents(object):
	def __init__(self, data):
		data = unpack_unsigned_byte(data)[0]
		self.side_brush_overcurrent = bool(data & WHEEL_OVERCURRENT.SIDE_BRUSH)
		self.main_brush_overcurrent = bool(data & WHEEL_OVERCURRENT.MAIN_BRUSH)
		self.right_wheel_overcurrent = bool(data & WHEEL_OVERCURRENT.RIGHT_WHEEL)
		self.left_wheel_overcurrent = bool(data & WHEEL_OVERCURRENT.LEFT_WHEEL)

	def __repr__(self):
		return str(self.__dict__)


class Buttons(object):
	def __init__(self, data):
		data = unpack_unsigned_byte(data)[0]
		self.clean = bool(data & BUTTONS.CLEAN)
		self.spot = bool(data & BUTTONS.SPOT)
		self.dock = bool(data & BUTTONS.DOCK)
		self.minute = bool(data & BUTTONS.MINUTE)
		self.hour = bool(data & BUTTONS.HOUR)
		self.day = bool(data & BUTTONS.DAY)
		self.schedule = bool(data & BUTTONS.SCHEDULE)
		self.clock = bool(data & BUTTONS.CLOCK)

	def __repr__(self):
		return str(self.__dict__)


class ChargingSources(object):
	def __init__(self, data):
		data = unpack_unsigned_byte(data)[0]
		self.internal_charger = bool(data & CHARGE_SOURCE.INTERNAL)
		self.home_base = bool(data & CHARGE_SOURCE.HOME_BASE)

	def __repr__(self):
		return str(self.__dict__)


class LightBumper(object):
	def __init__(self, data):
		data = unpack_unsigned_byte(data)[0]
		self.left = bool(data & LIGHT_BUMPER.LEFT)
		self.front_left = bool(data & LIGHT_BUMPER.FRONT_LEFT)
		self.center_left = bool(data & LIGHT_BUMPER.CENTER_LEFT)
		self.center_right = bool(data & LIGHT_BUMPER.CENTER_RIGHT)
		self.front_right = bool(data & LIGHT_BUMPER.FRONT_RIGHT)
		self.right = bool(data & LIGHT_BUMPER.RIGHT)

	def __repr__(self):
		return str(self.__dict__)


class Stasis(object):
	def __init__(self, data):
		data = unpack_unsigned_byte(data)[0]
		self.toggling = bool(data & STASIS.TOGGLING)
		self.disabled = bool(data & STASIS.DISABLED)

	def __repr__(self):
		return str(self.__dict__)


class Sensors(object):
	"""
	This class holds all sensors for the Create 2. It is basically like a C
	struct.
	"""
	def __init__(self, data=None):
		# self.data = data
		self.bumps_and_wheel_drops = None
		self.wall_sensor = None
		self.cliff_left_sensor = None
		self.cliff_front_left_sensor = None
		self.cliff_front_right_sensor = None
		self.cliff_right_sensor = None
		self.virtual_wall_sensor = None
		self.wheel_overcurrents = None
		self.dirt_detect_sensor = None
		self.ir_char_omni_sensor = None
		self.buttons = None
		self.distance = None
		self.angle = None
		self.charging_state = None
		self.voltage = None
		self.current = None
		self.temperature = None
		self.battery_charge = None
		self.battery_capacity = None
		self.wall_signal = None
		self.cliff_left_signal = None
		self.cliff_front_left_signal = None
		self.cliff_front_right_signal = None
		self.cliff_right_signal = None
		self.charging_sources = None
		self.oi_mode = None
		self.song_number = None
		self.is_song_playing = None
		self.number_of_stream_packets = None
		self.requested_velocity = None
		self.requested_radius = None
		self.requested_right_velocity = None
		self.requested_left_velocity = None
		self.left_encoder_counts = None
		self.right_encoder_counts = None
		self.light_bumper = None
		self.light_bump_left_signal = None
		self.light_bump_front_left_signal = None
		self.light_bump_center_left_signal = None
		self.light_bump_center_right_signal = None
		self.light_bump_front_right_signal = None
		self.light_bump_right_signal = None
		self.ir_character_left = None
		self.ir_character_right = None
		self.left_motor_current = None
		self.right_motor_current = None
		self.main_brush_motor_current = None
		self.side_brush_motor_current = None
		self.stasis = None

		if data:
			self.update(data)

	def update(self, data):
		"""
		Populates the attributes
		"""
		if len(data) != 80:
			raise Exception('Sensor data not 80 bytes long, it is: {}'.format(len(data)))

		# self.bumps_and_wheel_drops = BumpsAndWheelDrop(data[0:1])

		d = unpack_unsigned_byte(data[0:1])[0]
		self.bumps_and_wheel_drops = BumpsAndWheelDrop(
				bool(d & BUMPS_WHEEL_DROPS.BUMP_RIGHT),
				bool(d & BUMPS_WHEEL_DROPS.BUMP_LEFT),
				bool(d & BUMPS_WHEEL_DROPS.WHEEL_DROP_RIGHT),
				bool(d & BUMPS_WHEEL_DROPS.WHEEL_DROP_LEFT)
		)

		self.wall_sensor = unpack_bool_byte(data[1:2])[0]
		self.cliff_left_sensor = unpack_bool_byte(data[2:3])[0]
		self.cliff_front_left_sensor = unpack_bool_byte(data[3:4])[0]
		self.cliff_front_right_sensor = unpack_bool_byte(data[4:5])[0]
		self.cliff_right_sensor = unpack_bool_byte(data[5:6])[0]
		self.virtual_wall_sensor = unpack_bool_byte(data[6:7])[0]
		self.wheel_overcurrents = WheelOvercurrents(data[7:8])
		self.dirt_detect_sensor = unpack_byte(data[8:9])[0]
		# packet 16 or data bit 9 - unused
		self.ir_char_omni_sensor = unpack_unsigned_byte(data[10:11])[0]
		self.buttons = Buttons(data[11:12])
		self.distance = unpack_short(data[12:14])[0]
		self.angle = unpack_short(data[14:16])[0]
		self.charging_state = unpack_unsigned_byte(data[16:17])[0]
		self.voltage = unpack_unsigned_short(data[17:19])[0]
		self.current = unpack_short(data[19:21])[0]
		self.temperature = unpack_byte(data[21:22])[0]
		self.battery_charge = unpack_unsigned_short(data[22:24])[0]
		self.battery_capacity = unpack_unsigned_short(data[24:26])[0]
		self.wall_signal = unpack_unsigned_short(data[26:28])[0]
		self.cliff_left_signal = unpack_unsigned_short(data[28:30])[0]
		self.cliff_front_left_signal = unpack_unsigned_short(data[30:32])[0]
		self.cliff_front_right_signal = unpack_unsigned_short(data[32:34])[0]
		self.cliff_right_signal = unpack_unsigned_short(data[34:36])[0]
		 # packets 32, 33 or data bits 36, 37, 38 - unused
		self.charging_sources = ChargingSources(data[39:40])
		self.oi_mode = unpack_unsigned_byte(data[40:41])[0]
		self.song_number = unpack_unsigned_byte(data[41:42])[0]
		self.is_song_playing = unpack_bool_byte(data[42:43])[0]
		self.number_of_stream_packets = unpack_unsigned_byte(data[43:44])[0]
		self.requested_velocity = unpack_short(data[44:46])[0]
		self.requested_radius = unpack_short(data[46:48])[0]
		self.requested_right_velocity = unpack_short(data[48:50])[0]
		self.requested_left_velocity = unpack_short(data[50:52])[0]
		self.left_encoder_counts = unpack_unsigned_short(data[52:54])[0]
		self.right_encoder_counts = unpack_unsigned_short(data[54:56])[0]
		self.light_bumper = LightBumper(data[56:57])
		self.light_bump_left_signal = unpack_unsigned_short(data[57:59])[0]
		self.light_bump_front_left_signal = unpack_unsigned_short(data[59:61])[0]
		self.light_bump_center_left_signal = unpack_unsigned_short(data[61:63])[0]
		self.light_bump_center_right_signal = unpack_unsigned_short(data[63:65])[0]
		self.light_bump_front_right_signal = unpack_unsigned_short(data[65:67])[0]
		self.light_bump_right_signal = unpack_unsigned_short(data[67:69])[0]
		self.ir_character_left = unpack_unsigned_byte(data[69:70])[0]
		self.ir_character_right = unpack_unsigned_byte(data[70:71])[0]
		self.left_motor_current = unpack_short(data[71:73])[0]
		self.right_motor_current = unpack_short(data[73:75])[0]
		self.main_brush_motor_current = unpack_short(data[75:77])[0]
		self.side_brush_motor_current = unpack_short(data[77:79])[0]
		self.stasis = Stasis(data[79:80])

	def p(self):
		# attributes = [attr for attr in dir(self) if not attr.startswith('__')]
		members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
		# print(attributes)
		print(self.__class__, '-'*25)
		for attr in members:
			if attr in ['statis', 'light_bumper', 'chargin_sources', 'buttons', 'bumps_and_wheel_drops']:
				print()
			print(attr, ':=', getattr(self, attr))


if __name__ == "__main__":
	data = bytearray(os.urandom(80))
	sensors = Sensors(data)
	# pprint(sensors.__dict__)
	print('-'*70)
	sensors.p()

	# s = dict(sensors.__dict__)
	# pprint(s)
