import serial
import struct
# import time
# from OI import sensor_packet_lengths
from .packet import SensorPacketDecoder
# from OI import opcodes


class SerialCommandInterface(object):
	"""
	This class handles sending commands to the Create2.
	"""

	def __init__(self):
		self.ser = serial.Serial()
		self.decoder = SensorPacketDecoder()

	def __del__(self):
		self.close()

	def open(self, port='/dev/tty.usbserial-DA01NX3Z', baud=115200):
		self.ser.port = port
		self.ser.baudrate = baud
		self.ser.timeout = 1
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
		if not self.ser.isOpen():
			raise Exception('You must open the serial port first')

		# First thing to do is convert the opcode to a tuple.
		if not isinstance(opcode, tuple):
			opcode = (opcode,)

		msg = opcode

		# Sometimes opcodes don't need data. Since we can't add
		# a None type to a tuple, we have to make this check.
		if data:
			msg += data

		self.ser.write(struct.pack('B' * len(msg), *msg))

	# def write(self, msg):
	# 	if not isinstance(msg, tuple):
	# 		msg = tuple(msg)
	# 	self.ser.write(struct.pack('B' * len(msg), *msg))

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
