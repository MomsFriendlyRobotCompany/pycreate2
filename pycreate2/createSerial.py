from __future__ import print_function
from __future__ import division
import serial
import struct
# import time
# from OI import sensor_packet_lengths
# from .packet import SensorPacketDecoder
# from OI import opcodes
# from pycreate2.OI import opcodes
# from pycreate2.OI import calc_query_data_len


# class CreateMessage(object):
# 	def __init__(self):
# 		pass
#
# 	def createMessage(self, opcode, data=None):
# 		msg = None
#
# 		if opcode == opcodes.PLAY:
# 			if not data:
# 				raise Exception("please specify song number to play")
# 			song_num = data[0]
# 			msg = (opcodes.PLAY, song_num,)
# 		elif opcode == opcodes.


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
		# self.decoder = SensorPacketDecoder()

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
		if self.ser.isOpen():
			# print "port was open"
			self.ser.close()
		self.ser.open()
		if self.ser.is_open:
			print("Create opened serial: {}".format(self.ser))
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
		if self.ser.isOpen():
			print('Closing port {} @ {}'.format(self.ser.port, self.ser.baudrate))
			self.ser.close()
