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

from __future__ import print_function
from __future__ import division
import struct
import time
from .packet import SensorPacketDecoder
from .createSerial import SerialCommandInterface
from pycreate2.OI import ascii_table
from pycreate2.OI import sensor_packet_lengths
from pycreate2.OI import opcodes


class Fatal(Exception):
	pass


class Error(Exception):
	pass


class Warning(Exception):
	pass


class Create2(object):
	"""
	The top level class for controlling a Create2.
	This is the only class that outside scripts should be interacting with.
	"""

	def __init__(self, port, baud=115200):
		"""
		Constructor, sets up class
		- creates serial port
		- creates decoder
		"""
		self.SCI = SerialCommandInterface()
		self.SCI.open(port, baud)
		self.decoder = SensorPacketDecoder()
		self.sleep_timer = 0.5

	def __del__(self):
		"""Destructor, cleans up when class goes out of scope"""
		# stop motors
		self.drive_stop()
		time.sleep(self.sleep_timer)

		self.power()
		time.sleep(0.1)
		self.stop()  # power down
		time.sleep(0.1)
		self.close()  # close serial port
		time.sleep(0.1)

	def close(self):
		"""
		Closes up serial ports and terminates connection to the Create2
		"""
		self.SCI.close()

	"""------------------- Mode Control ------------------------"""
	def start(self):
		"""
		Puts the Create 2 into Passive mode. You must always send the Start command
		before sending any other commands to the OI.
		"""
		# self.SCI.open()
		self.SCI.write(opcodes['start'])
		time.sleep(self.sleep_timer)

	def getMode(self):
		"""
		This doesn't seem to work
		"""
		self.SCI.write((opcodes.MODE))
		time.sleep(0.005)
		ans = self.SCI.read(1)
		if len(ans) == 1:
			byte = struct.unpack('B', ans)[0]
		else:
			byte = 'Error, not mode returned'
		print('Mode: {}'.format(byte))

	# def wake(self):
	# 	"""wake up robot."""
	# 	self.SCI.ser.setRTS(0)
	# 	time.sleep(0.25)
	# 	self.SCI.ser.setRTS(1)
	# 	time.sleep(1)  # Technically it should wake after 500ms.

	def reset(self):
		"""
		This command resets the robot, as if you had removed and reinserted the
		battery.

		('Firmware Version:', 'bl-start\r\nSTR730\r\nbootloader id: #x47186549 82ECCFFF\r\nbootloader info rev: #xF000\r\nbootloader rev: #x0001\r\n2007-05-14-1715-L   \r')
		"""
		msg = (opcodes['reset'],)
		self.SCI.write(msg)
		time.sleep(1)
		ret = self.SCI.read(128)
		return ret

	def stop(self):
		"""
		Puts the Create 2 into OFF mode. All streams will stop and the robot will no
		longer respond to commands. Use this command when you are finished
		working with the robot.
		"""
		self.SCI.write(opcodes['stop'])
		time.sleep(self.sleep_timer)

	def safe(self):
		"""
		Puts the Create 2 into safe mode. Blocks for a short (<.5 sec) amount
		of time so the bot has time to change modes.
		"""
		self.SCI.write(opcodes['safe'])
		time.sleep(self.sleep_timer)

	def full(self):
		"""
		Puts the Create 2 into full mode. Blocks for a short (<.5 sec) amount
		of time so the bot has time to change modes.
		"""
		self.SCI.write(opcodes['full'])
		time.sleep(self.sleep_timer)

	def seek_dock(self):
		self.SCI.write(opcodes['seek_dock'])

	def power(self):
		"""
		Puts the Create 2 into Passive mode. The OI can be in Safe, or
		Full mode to accept this command.
		"""
		msg = (opcodes['power'],)
		self.SCI.write(msg)
		time.sleep(self.sleep_timer)

	""" ------------------ Drive Commands ------------------"""

	def drive_stop(self):
		self._drive(0, 0)
		time.sleep(self.sleep_timer)  # wait just a little for the robot to stop

	def drive_turn(self, velocity, radius=1):
		self._drive(velocity, radius)

	def drive_straight(self, velocity):
		"""
		Will make the Create2 drive straight at the given velocity

		Arguments:
			velocity: Velocity of the Create2 in mm/s. Positive velocities are forward,
				negative velocities are reverse. Max speeds are still enforced by drive()

		"""
		self._drive(velocity, 32767)

	def _drive(self, velocity, radius):
		"""
		Controls the Create 2's drive wheels.

		Args:
			velocity: A number between -500 and 500. Units are mm/s.
			radius: A number between -2000 and 2000. Units are mm.
				Drive straight: 32767
				Turn in place clockwise: -1
				Turn in place counterclockwise: 1
		"""
		v = None
		r = None

		# Check to make sure we are getting sent valid velocity/radius.
		if -500 <= velocity <= 500:
			v = int(velocity) & 0xffff
			# Convert 16bit velocity to Hex
		else:
			# noError = False
			raise Exception("Invalid velocity input")

		# Special case radius
		# if radius == 32767 or radius == -1 or radius == 1:
		if radius in [-1, 1, 32767]:
			# Convert 16bit radius to Hex
			r = int(radius) & 0xffff

		# elif radius >= -2000 and radius <= 2000:
		elif -2000 <= radius <= 2000:
			# Convert 16bit radius to Hex
			r = int(radius) & 0xffff

		else:
			# noError = False
			raise Exception("Invalid radius input")

		data = struct.unpack('4B', struct.pack('>2H', v, r))
		self.SCI.write(opcodes['drive'], data)

	"""------------------------ LED ---------------------------- """

	def led(self):
		"""
		Not implementing this for now.
		"""
		# self.SCI.write(opcodes['start'],0)
		raise NotImplementedError()

	def digit_led_ascii(self, display_string):
		"""
		This command controls the four 7 segment displays using ASCII character codes.

		Arguments:
			display_string: A four character string to be displayed. This must be four
				characters. Any blank characters should be represented with a space: ' '
				Due to the limited display, there is no control over upper or lowercase
				letters. create2api will automatically convert all chars to uppercase, but
				some letters (Such as 'B' and 'D') will still display as lowercase on the
				Create 2's display. C'est la vie.
		"""
		noError = True
		display_string = display_string.upper()
		# print display_string
		if len(display_string) == 4:
			display_list = []
		else:
			# Too many or too few characters!
			noError = False
			raise Exception("Invalid ASCII input (Must be EXACTLY four characters)")
		if noError:
			# Need to map ascii to numbers from the dict.
			for i in range(0, 4):
				# Check that the character is in the list, if it is, add it.
				if display_string[i] in ascii_table:
					display_list.append(ascii_table[display_string[i]])
				else:
					# Char was not available. Just print a blank space
					# Raise an error so the software knows that the input was bad
					display_list.append(ascii_table[' '])
					# warnings.formatwarning = custom_format_warning
					# warnings.warn("Warning: Char '" + display_string[i] + "' was not found in ascii table")
					raise Exception("Warning: Char '" + display_string[i] + "' was not found in ascii table")

			# print display_list
			self.SCI.write(opcodes['digit_led_ascii'], tuple(display_list))
		else:
			raise Exception("Invalid data, failed to send")

	"""------------------------ Songs ---------------------------- """

	def createSong(self, song_num, notes):
		"""
		Creates a song

		Arguments
			song_num: 1-4
			notes: 16 notes and 16 durations each note should be held for (1 duration = 1/64 second)
		"""
		size = len(notes)
		if (2 > size > 32) or (size % 2 != 0):
			raise Exception('Songs must be between 1-16 notes and have a duration')
		if 0 > song_num > 4:
			raise Exception('Song number must be between 0 and 4')

		if not isinstance(notes, tuple):
			notes = tuple(notes)

		msg = (opcodes.SONG, song_num, size,) + notes
		self.SCI.write(msg)

	def playSong(self, song_num):
		"""
		Play a song
			Arguments
				song_num: 1-4
		"""
		if 0 > song_num > 4:
			raise Exception('Song number must be between 0 and 4')

		msg = (opcodes.PLAY, song_num,)
		self.SCI.write(msg)

	"""------------------------ Sensors ---------------------------- """

	def query_list(self, pkts, packet_size):
		"""
		This command lets you ask for a list of sensor packets. The result is returned once, as in the
		Sensors command. The robot returns the packets in the order you specify.

			Arguments
				pkts: array of packet numbers like: [34, 22, 67]
				packet_size: the number of bytes that will be returned and need to be read by the serial port
		"""
		# self.SCI.write(opcodes['start'],0)
		# raise NotImplementedError()
		if not isinstance(pkts, tuple):
			pkts = tuple(pkts,)
		cmd = (opcodes.QUERY_LIST, len(pkts)) + pkts

		# packet_size = 0
		# for p in pkts:
		# 	packet_size += sensor_packet_lengths[str(p)]

		self.SCI.write(cmd)
		time.sleep(0.015)  # wait 15 msec
		packet_byte_data = list(self.SCI.read(packet_size))
		return packet_byte_data

	def get_packet(self, packet_id):
		"""
		Requests and reads a packet from the Create 2

		Arguments:
			packet_id: The id of the packet you wish to collect.

		Returns: False if there was an error, True if the packet successfully came through.
		"""
		strid = str(packet_id)
		if strid in sensor_packet_lengths:
			packet_size = sensor_packet_lengths[strid]
			packet = (packet_id,)
		else:
			raise Exception("Invalid packet id")

		self.SCI.write(opcodes.SENSORS, packet)
		time.sleep(0.005)
		packet_byte_data = list(self.SCI.read(packet_size))

		if len(packet_byte_data) == 0:
			raise Exception('Could not communicate with Create 2')

		# Once we have the byte data, we need to decode the packet and save the new sensor state
		sensor_state = []
		sensor_state = self.decoder.decode_packet(packet_id, packet_byte_data, sensor_state)
		return sensor_state

	# def drive_pwm(self):
	# 	"""
	# 	Not implementing this for now.
	# 	"""
	# 	# self.SCI.write(opcodes['start'],0)
	# 	raise NotImplementedError()

	# def motors_pwm(self, main_pwm, side_pwm, vacuum_pwm):
	# 	"""
	# 	Serial sequence: [144] [Main Brush PWM] [Side Brush PWM] [Vacuum PWM]
	#
	# 	Arguments:
	# 		main_pwm: Duty cycle for Main Brush. Value from -127 to 127. Positive speeds spin inward.
	# 		side_pwm: Duty cycle for Side Brush. Value from -127 to 127. Positive speeds spin counterclockwise.
	# 		vacuum_pwm: Duty cycle for Vacuum. Value from 0-127. No negative speeds allowed.
	# 	"""
	# 	pwm = (main_pwm, side_pwm, vacuum_pwm)  # FIXME: these aren't on the create????
	# 	for i in pwm:
	# 		if 127 > i < -127:  # vacuum not checked right
	# 			raise Exception('motor pwm value is wrong: {}'.format(i))
	# 	self.SCI.write(opcodes['motors_pwm'], pwm)
	# def readSensors(self, packet_id):  # FIXME why is this here? move to createserial, rename write()
	# 	"""
	# 	Requests the OI to send a packet of sensor data bytes.
	#
	# 	Arguments:
	# 		packet_id: Identifies which of the 58 sensor data packets should be sent back by the OI.
	# 	"""
	# 	# Need to make sure the packet_id is a string
	# 	packet_id = str(packet_id)
	# 	# Check to make sure that the packet ID is valid.
	# 	if packet_id in sensor_packet_lengths:
	# 		# Valid packet, send request (But convert it back to an int in a list first)
	# 		packet_id = [int(packet_id)]
	# 		self.SCI.write(opcodes['sensors'], tuple(packet_id))
	# 	else:
	# 		raise Exception("Invalid packet id, failed to send")
	# def scheduling_led(self):
	# 	"""
	# 	Not implementing this for now.
	# 	"""
	# 	# self.SCI.write(opcodes['start'],0)
	# 	raise NotImplementedError()
