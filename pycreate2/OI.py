# The MIT License
#
# Copyright (c) 2017 Kevin Walchko
# I took some of these ideas from: https://bitbucket.org/lemoneer/irobot

from __future__ import print_function
from __future__ import division


# could replace with:
#   class LEDS(object): DEBRIS=0x01; SPOT=0x02; DOCK=0x04; CHECK_ROBOT=0x08
class Namespace(object):
	def __init__(self, **kwds):
		self.__dict__.update(kwds)


BAUD_RATE           = Namespace(BAUD_300=0, BAUD_600=1, BAUD_1200=2, BAUD_2400=3, BAUD_4800=4, BAUD_9600=5, BAUD_14400=6, BAUD_19200=7, BAUD_28800=8, BAUD_38400=9, BAUD_57600=10, BAUD_115200=11, DEFAULT=11)
DAYS                = Namespace(SUNDAY=0x01, MONDAY=0x02, TUESDAY=0x04, WEDNESDAY=0x08, THURSDAY=0x10, FRIDAY=0x20, SATURDAY=0x40)
DRIVE               = Namespace(STRAIGHT=0x8000, STRAIGHT_ALT=0x7FFF, TURN_CW=-1, TURN_CCW=0x0001)
MOTORS              = Namespace(SIDE_BRUSH=0x01, VACUUM=0x02, MAIN_BRUSH=0x04, SIDE_BRUSH_DIRECTION=0x08, MAIN_BRUSH_DIRECTION=0x10)
LEDS                = Namespace(DEBRIS=0x01, SPOT=0x02, DOCK=0x04, CHECK_ROBOT=0x08)
# WEEKDAY_LEDS        = Namespace(SUNDAY=0x01, MONDAY=0x02, TUESDAY=0x04, WEDNESDAY=0x08, THURSDAY=0x10, FRIDAY=0x20, SATURDAY=0x40)
WEEKDAY_LEDS        = DAYS
SCHEDULING_LEDS     = Namespace(COLON=0x01, PM=0x02, AM=0x04, CLOCK=0x08, SCHEDULE=0x10)
RAW_LED             = Namespace(A=0x01, B=0x02, C=0x04, D=0x08, E=0x10, F=0x20, G=0x40)
BUTTONS             = Namespace(CLEAN=0x01, SPOT=0x02, DOCK=0x04, MINUTE=0x08, HOUR=0x10, DAY=0x20, SCHEDULE=0x40, CLOCK=0x80)
ROBOT               = Namespace(TICK_PER_REV=508.8, WHEEL_DIAMETER=72, WHEEL_BASE=235, TICK_TO_DISTANCE=0.44456499814949904317867595046408)
MODES               = Namespace(OFF=0, PASSIVE=1, SAFE=2, FULL=3)
WHEEL_OVERCURRENT   = Namespace(SIDE_BRUSH=0x01, MAIN_BRUSH=0x02, RIGHT_WHEEL=0x04, LEFT_WHEEL=0x08)
BUMPS_WHEEL_DROPS   = Namespace(BUMP_RIGHT=0x01, BUMP_LEFT=0x02, WHEEL_DROP_RIGHT=0x04, WHEEL_DROP_LEFT=0x08)
CHARGE_SOURCE       = Namespace(INTERNAL=0x01, HOME_BASE=0x02)
LIGHT_BUMPER        = Namespace(LEFT=0x01, FRONT_LEFT=0x02, CENTER_LEFT=0x04, CENTER_RIGHT=0x08, FRONT_RIGHT=0x10, RIGHT=0x20)
STASIS              = Namespace(TOGGLING=0x01, DISABLED=0x02)
OPCODES             = Namespace(
	RESET=7,
	OI_MODE=35,
	START=128,
	# CONTROL=130,  # oi spec, p 10, this is the same as SAFE
	SAFE=131,
	FULL=132,
	POWER=133,
	# SPOT=134,
	# CLEAN=135,
	# MAX=136,
	DRIVE=137,
	MOTORS=138,
	LED=139,
	SONG=140,
	PLAY=141,
	SENSORS=142,
	SEEK_DOCK=143,
	MOTORS_PWM=144,
	DRIVE_DIRECT=145,
	DRIVE_PWM=146,
	# STREAM=148,
	QUERY_LIST=149,
	# PAUSE_RESUME_STREAM=150,
	# SCHEDULING_LED=162,
	# DIGIT_LED_RAW=163,  # doesn't work
	DIGIT_LED_ASCII=164,
	# BUTTONS=165,
	# SCHEDULE=167,
	# SET_DAY_TIME=168,
	STOP=173
)

RESPONSE_SIZES = {
	0: 26, 1: 10, 2: 6, 3: 10, 4: 14, 5: 12, 6: 52,
	# actual sensors
	7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 2, 20: 2, 21: 1,
	22: 2, 23: 2, 24: 1, 25: 2, 26: 2, 27: 2, 28: 2, 29: 2, 30: 2, 31: 2, 32: 3, 33: 3, 34: 1, 35: 1,
	36: 1, 37: 1, 38: 1, 39: 2, 40: 2, 41: 2, 42: 2, 43: 2, 44: 2, 45: 1, 46: 2, 47: 2, 48: 2, 49: 2,
	50: 2, 51: 2, 52: 1, 53: 1, 54: 2, 55: 2, 56: 2, 57: 2, 58: 1,
	# end actual sensors
	100: 80, 101: 28, 106: 12, 107: 9
}


def calc_query_data_len(pkts):
	packet_size = 0
	for p in pkts:
		packet_size += RESPONSE_SIZES[p]
	return packet_size


CHARGING_STATE = {
	0: 'not charging',
	1: 'reconditioning charging',
	2: 'full charging',
	3: 'trickle charging',
	4: 'waiting',
	5: 'charging fault condition'
}


MIDI_TABLE = {
	"rest": 0,
	"G#1": 32,
	"G#3": 56,
	"G#2": 44,
	"G#5": 80,
	"G#4": 68,
	"G#7": 104,
	"G#6": 92,
	"G#8": 116,
	"G7": 103,
	"G6": 91,
	"G5": 79,
	"G4": 67,
	"G3": 55,
	"G2": 43,
	"G1": 31,
	"G9": 127,
	"G8": 115,
	"A7": 105,
	"D#9": 123,
	"A8": 117,
	"B4": 71,
	"B5": 83,
	"B6": 95,
	"B7": 107,
	"B1": 35,
	"B2": 47,
	"B3": 59,
	"B8": 119,
	"F#2": 42,
	"F#3": 54,
	"F#4": 66,
	"F#5": 78,
	"F#6": 90,
	"F#7": 102,
	"F#8": 114,
	"F#9": 126,
	"E9": 124,
	"E8": 112,
	"E5": 76,
	"E4": 64,
	"E7": 100,
	"E6": 88,
	"E3": 52,
	"E2": 40,
	"A#3": 58,
	"A#2": 46,
	"A#1": 34,
	"pause": 0,
	"A#7": 106,
	"A#6": 94,
	"A#5": 82,
	"A#4": 70,
	"A#8": 118,
	"C9": 120,
	"C8": 108,
	"C3": 48,
	"C2": 36,
	"C7": 96,
	"C6": 84,
	"C5": 72,
	"C4": 60,
	"R": 0,
	"F2": 41,
	"F3": 53,
	"F4": 65,
	"F5": 77,
	"F6": 89,
	"F7": 101,
	"F8": 113,
	"F9": 125,
	"A1": 33,
	"A3": 57,
	"A2": 45,
	"A5": 81,
	"A4": 69,
	"D#8": 111,
	"A6": 93,
	"D#6": 87,
	"D#7": 99,
	"D#4": 63,
	"D#5": 75,
	"D#2": 39,
	"D#3": 51,
	"C#9": 121,
	"C#8": 109,
	"C#5": 73,
	"C#4": 61,
	"C#7": 97,
	"C#6": 85,
	"C#3": 49,
	"C#2": 37,
	"D8": 110,
	"D9": 122,
	"D6": 86,
	"D7": 98,
	"D4": 62,
	"D5": 74,
	"D2": 38,
	"D3": 50
}

REMOTE_OPCODES = {
	0: "none",
	129: "left",
	130: "forward",
	131: "right",
	132: "spot",
	133: "max",
	134: "small",
	135: "medium",
	136: "clean",
	137: "pause",
	138: "power",
	139: "arc-left",
	140: "arc-right",
	141: "drive-stop",
	142: "send-all",
	143: "seek-dock",
	160: "reserved",
	161: "force-field",
	162: "virtual-wall",
	164: "green-buoy",
	165: "green-buoy-and-force-field",
	168: "red-buoy",
	169: "red-buoy-and-force-field",
	172: "red-buoy-and-green-buoy",
	173: "red-buoy-and-green-buoy-and-force-field",
	240: "reserved",
	242: "force-field",
	244: "green-buoy",
	246: "green-buoy-and-force-field",
	248: "red-buoy",
	250: "red-buoy-and-force-field",
	252: "red-buoy-and-green-buoy",
	254: "red-buoy-and-green-buoy-and-force-field",
	255: "none"
}
