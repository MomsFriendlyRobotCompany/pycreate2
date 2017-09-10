# The MIT License
#
# Copyright (c) 2017 Kevin Walchko
#
# This is basically the interface between the Create2 and pyserial

from __future__ import print_function
from __future__ import division
import serial
import struct


class SerialCommandInterface(object):
	"""
	This class handles sending commands to the Create2. Writes will take in tuples
	and format the data to transfer to the Create.
	"""

	def __init__(self):
		"""
		Constructor.

		Creates the serial port, but doesn't open it yet. Call open(port) to open
		it.
		"""
		self.ser = serial.Serial()

	def __del__(self):
		"""
		Destructor.

		Closes the serial port
		"""
		self.close()

	def open(self, port, baud=115200, timeout=1):
		"""
		Opens a serial port to the create.

		port: the serial port to open, ie, '/dev/ttyUSB0'
		buad: default is 115200, but can be changed to a lower rate via the create api
		"""
		self.ser.port = port
		self.ser.baudrate = baud
		self.ser.timeout = timeout
		# print self.ser.name
		if self.ser.is_open:
			# print "port was open"
			self.ser.close()
		self.ser.open()
		if self.ser.is_open:
			# print("Create opened serial: {}".format(self.ser))
			print('-'*40)
			print(' Create opened serial connection')
			print('   port: {}'.format(self.ser.port))
			print('   datarate: {} bps'.format(self.ser.baudrate))
			print('-'*40)
		else:
			raise Exception('Failed to open {} at {}'.format(port, baud))

	def write(self, opcode, data=None):
		"""
		Writes a command to the create. There needs to be an opcode and optionally
		data. Not all commands have data associated with it.

		opcode: see creaet api
		data: a tuple with data associated with a given opcode (see api)
		"""
		msg = (opcode,)

		# Sometimes opcodes don't need data. Since we can't add
		# a None type to a tuple, we have to make this check.
		if data:
			msg += data

		self.ser.write(struct.pack('B' * len(msg), *msg))

	def read(self, num_bytes):
		"""
		Read a string of 'num_bytes' bytes from the robot.

		Arguments:
			num_bytes: The number of bytes we expect to read.
		"""
		if not self.ser.is_open:
			raise Exception('You must open the serial port first')

		data = self.ser.read(num_bytes)

		return data

	def close(self):
		"""
		Closes the serial connection.
		"""
		if self.ser.is_open:
			print('Closing port {} @ {}'.format(self.ser.port, self.ser.baudrate))
			self.ser.close()
