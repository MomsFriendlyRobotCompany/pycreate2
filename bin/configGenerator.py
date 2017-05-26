"""
A quick script to convert various dicts describing iRobot Open Interface commands into a json config.

"""

import json

OPCODES = dict(
    start = 128,
    reset = 7,
    stop = 173,
    baud = 129,
    safe = 131,
    full = 132,
    clean = 135,
    max = 136,
    spot = 134,
    seek_dock = 143,
    power = 133,
    schedule = 167,
    set_day_time = 168,
    drive = 137,
    drive_direct = 145,
    drive_pwm = 146,
    motors = 138,
    motors_pwm = 144,
    led = 139,
    scheduling_led = 162,
    digit_led_raw = 163,
    buttons = 165,
    digit_led_ascii = 164,
    song = 140,
    play = 141,
    sensors = 142,
    query_list = 149,
    stream = 148,
    pause_resume_stream = 150
    )
    
# Because a 7 segment display is not sufficient to display alphabetic
# characters properly, all characters are an approximation, and not all
# ASCII codes are implemented.
#
# Example:
#   To write ABCD to the display, send the serial byte sequence: [164] [65] [66] [67] [68] 
#                                                           send_ascii   A    B    C    D
#

ASCII_TABLE = {' ': 32, '!': 33,
              '"': 34, '#': 35,
              '%': 37, '&': 38,
              '\'': 39, '[': 40,
              ']': 41, ',':  44,
              '-': 45, '.': 46, '/': 47,
              '0': 48, '1': 49, '2': 50,
              '3': 51, '4': 52, '5': 53,
              '6': 54, '7': 55, '8': 56,
              '9': 57, ':': 58, ';': 59,
              '<': 60, '=': 61, '>': 62,
              '?': 63, 'A': 65,
              'B': 66, 'C': 67, 'D': 68,
              'E': 69, 'F': 70, 'G': 71,
              'H': 72, 'I': 73, 'J': 74,
              'K': 75, 'L': 76, 'M': 77,
              'N': 78, 'O': 79, 'P': 80,
              'Q': 81, 'R': 82, 'S': 83,
              'T': 84, 'U': 85, 'V': 86,
              'W': 87, 'X': 88, 'Y': 89,
              'Z': 90, '\\': 92,
              '^': 94, '_': 95, '`': 96,
              '{': 123, '|': 124,
              '}': 125, '~': 126}

#SENSOR_GROUP_PACKET_LENGTHS = (26, 10, 6, 10, 14, 12, 52, 80, 28, 12, 9)
SENSOR_GROUP_PACKET_LENGTHS = {
    0: 26,
    1: 10,
    2: 6,
    3: 10,
    4: 14,
    5: 12,
    6: 52,
    7: 1,
    8: 1,
    9: 1,
    10: 1,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1,
    16: 1,
    17: 1,
    18: 1,
    19: 2,
    20: 2,
    21: 1,
    22: 2,
    23: 2,
    24: 1,
    25: 2,
    26: 2,
    27: 2,
    28: 2,
    29: 2,
    30: 2,
    31: 2,
    32: 1,
    33: 2,
    34: 1,
    35: 1,
    36: 1,
    37: 1,
    38: 1,
    39: 2,
    40: 2,
    41: 2,
    42: 2,
    43: 2,
    44: 2,
    45: 1,
    46: 2,
    47: 2,
    48: 2,
    49: 2,
    50: 2,
    51: 2,
    52: 1,
    53: 1,
    54: 2,
    55: 2,
    56: 2,
    57: 2,
    58: 1,
    100: 80,
    101: 28,
    102: 12,
    103: 9 }

SENSOR_DATA = {
    'wheel drop and bumps' : {'drop left' : False, 'drop right' : False, 'bump left' : False, 'bump right' : False},
    'wall seen' : False,
    'cliff left' : False,
    'cliff front left' : False,
    'cliff front right' : False,
    'cliff right' : False,
    'virtual wall' : False,
    'wheel overcurrents' : {'left wheel' : False, 'right wheel' : False, 'main brush' : False, 'side brush' : False},
    'dirt detect' : 0,
    'infared char omni' : 0,
    'infared char left' : 0,
    'infared char right' : 0,
    'buttons' : {'clock' : False, 'schedule' : False, 'day' : False, 'hour' : False, 'minute' : False, 'dock' : False,
        'spot' : False, 'clean' : False},
    'distance' : 0,
    'angle' : 0,
    'charging state' : 0,
    'voltage' : 0,
    'current' : 0,
    'temperature' : 0,
    'battery charge' : 0,
    'battery capacity' : 0,
    'wall signal' : 0,
    'cliff left signal' : 0,
    'cliff front left signal' : 0,
    'cliff front right signal' : 0,
    'cliff right signal' : 0,
    'charging sources available' : {'home base' : False, 'internal charger' : False},
    'oi mode' : 0,
    'song number' : 0,
    'song playing' : False,
    'number of stream packets' : 0,
    'requested velocity' : 0,
    'requested radius' : 0,
    'requested right velocity' : 0,
    'requested left velocity' : 0,
    'left encoder counts' : 0,
    'right encoder counts' : 0,
    'light bumper' : {'right' : False, 'front right' : False, 'center right' : False, 'center left' : False, 'front left' : False, 'left' : False},
    'light bump left signal' : 0,
    'light bump front left signal' : 0,
    'light bump center left signal' : 0,
    'light bump center right signal' : 0,
    'light bump front right signal' : 0,
    'light bump right signal' : 0,
    'left motor current' : 0,
    'right motor current' : 0,
    'main brush motor current' : 0,
    'side brush motor current' : 0,
    'stasis' : False
    }

CHARGING_STATES = (
    'not-charging',
    'charging-recovery',
    'charging',
    'trickle-charging',
    'waiting',
    'charging-error')

OI_MODES = (
    'off',
    'passive',
    'safe',
    'full')

# From: http://www.harmony-central.com/MIDI/Doc/table2.html
MIDI_TABLE = {'rest': 0, 'R': 0, 'pause': 0,
              'G1': 31, 'G#1': 32, 'A1': 33,
              'A#1': 34, 'B1': 35,

              'C2': 36, 'C#2': 37, 'D2': 38,
              'D#2': 39, 'E2': 40, 'F2': 41,
              'F#2': 42, 'G2': 43, 'G#2': 44,
              'A2': 45, 'A#2': 46, 'B2': 47,

              'C3': 48, 'C#3': 49, 'D3': 50,
              'D#3': 51, 'E3': 52, 'F3': 53,
              'F#3': 54, 'G3': 55, 'G#3': 56,
              'A3': 57, 'A#3': 58, 'B3': 59,

              'C4': 60, 'C#4': 61, 'D4': 62,
              'D#4': 63, 'E4': 64, 'F4': 65,
              'F#4': 66, 'G4': 67, 'G#4': 68,
              'A4': 69, 'A#4': 70, 'B4': 71,

              'C5': 72, 'C#5': 73, 'D5': 74,
              'D#5': 75, 'E5': 76, 'F5': 77,
              'F#5': 78, 'G5': 79, 'G#5': 80,
              'A5': 81, 'A#5': 82, 'B5': 83,

              'C6': 84, 'C#6': 85, 'D6': 86,
              'D#6': 87, 'E6': 88, 'F6': 89,
              'F#6': 90, 'G6': 91, 'G#6': 92,
              'A6': 93, 'A#6': 94, 'B6': 95,

              'C7': 96, 'C#7': 97, 'D7': 98,
              'D#7': 99, 'E7': 100, 'F7': 101,
              'F#7': 102, 'G7': 103, 'G#7': 104,
              'A7': 105, 'A#7': 106, 'B7': 107,

              'C8': 108, 'C#8': 109, 'D8': 110,
              'D#8': 111, 'E8': 112, 'F8': 113,
              'F#8': 114, 'G8': 115, 'G#8': 116,
              'A8': 117, 'A#8': 118, 'B8': 119,

              'C9': 120, 'C#9': 121, 'D9': 122,
              'D#9': 123, 'E9': 124, 'F9': 125,
              'F#9': 126, 'G9': 127}


REMOTE_OPCODES = {
    # Remote control.
    0: 'none',
    129: 'left',
    130: 'forward',
    131: 'right',
    132: 'spot',
    133: 'max',
    134: 'small',
    135: 'medium',
    136: 'large',
    136: 'clean',
    137: 'pause',
    138: 'power',
    139: 'arc-left',
    140: 'arc-right',
    141: 'drive-stop',
    # Scheduling remote.
    142: 'send-all',
    143: 'seek-dock',
    # Home base.
    240: 'reserved',
    242: 'force-field',
    244: 'green-buoy',
    246: 'green-buoy-and-force-field',
    248: 'red-buoy',
    250: 'red-buoy-and-force-field',
    252: 'red-buoy-and-green-buoy',
    254: 'red-buoy-and-green-buoy-and-force-field',
    255: 'none',
    # Roomba 600 drive-on charger.
    160: 'reserved',
    161: 'force-field',
    164: 'green-buoy',
    165: 'green-buoy-and-force-field',
    168: 'red-buoy',
    169: 'red-buoy-and-force-field',
    172: 'red-buoy-and-green-buoy',
    173: 'red-buoy-and-green-buoy-and-force-field',
    # Roomba 600 Virtual Wall.
    162: 'virtual-wall'
    }              

data = {'opcodes': {}, 'ascii table': {}, 'sensor group packet lengths': {}, 'sensor data': {}, 'charging states': {}, 'oi modes': {}, 'midi table': {}, 'remote opcodes': {}}

data['opcodes']  = OPCODES
data['ascii table'] = ASCII_TABLE
data['sensor group packet lengths'] = SENSOR_GROUP_PACKET_LENGTHS
data['sensor data'] = SENSOR_DATA
data['charging states'] = CHARGING_STATES
data['oi modes'] = OI_MODES
data['midi table'] = MIDI_TABLE
data['remote opcodes'] = REMOTE_OPCODES
              
with open("config.json", 'w') as outfile:
    try:
        json.dump(data, outfile, sort_keys = False, indent = 4)
        print 'saved config'
    except ValueError, e:
        print 'shits fucked up yo'