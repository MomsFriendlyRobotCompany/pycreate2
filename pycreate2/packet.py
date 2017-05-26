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

import struct
# from OI import sensor_packet_lengths


class SensorPacketDecoder(object):
	"""
	A class that handles sensor packet decoding.

	This class may, in the future, become a private class. Users shouldn't be interacting with
	this class directly -- scripts should use Create2.get_packet() instead.

	"""

	def __init__(self):
		# self.lengths = sensor_packet_lengths
		pass

	# def decode_packet(self, packet_id, byte_data, sensor_data):
	def decode_packet(self, id, byte_data, sensor_data):
		"""
		Decodes an OI packet

		Arguments:
			packet_id: The id of the packet. Duh.
			byte_data: The bytes that the Create 2 sent over serial
			sensor_data: A dict containing the sensor states of the Create 2
		Returns:
			A dict containing the updated sensor states of the Create 2
		"""
		# return_dict = None
		# sensor_data = []
		if not isinstance(id, int):
			id = int(id)  # Convert the packet id from a string to an int

		# Depending on the packet id, we will need to do different decoding.
		# Packets 1-6 and 100, 101, 106, and 107 are special cases where they
		#   contain groups of packets.
		#
		# Other packets (7-58) are single packets, but some of them have two byte
		#   data, and also need special treatment.

		# Hold onto your hats. This is gonna get long fast.
		if id == 0:
			# Size 26, contains packet 7-26
			# We decode the data in reverse order to make pop() simpler
			sensor_data['battery capacity'] = self.decode_packet_26(byte_data.pop(), byte_data.pop())
			sensor_data['battery charge'] = self.decode_packet_25(byte_data.pop(), byte_data.pop())
			sensor_data['temperature'] = self.decode_packet_24(byte_data.pop())
			sensor_data['current'] = self.decode_packet_23(byte_data.pop(), byte_data.pop())
			sensor_data['voltage'] = self.decode_packet_22(byte_data.pop(), byte_data.pop())
			sensor_data['charging state'] = self.decode_packet_21(byte_data.pop())
			sensor_data['angle'] = self.decode_packet_20(byte_data.pop(), byte_data.pop())
			sensor_data['distance'] = self.decode_packet_19(byte_data.pop(), byte_data.pop())
			sensor_data['buttons'] = self.decode_packet_18(byte_data.pop())
			sensor_data['infared char omni'] = self.decode_packet_17(byte_data.pop())
			temp = self.decode_packet_16(byte_data.pop())
			sensor_data['dirt detect'] = self.decode_packet_15(byte_data.pop())
			sensor_data['wheel overcurrents'] = self.decode_packet_14(byte_data.pop())
			sensor_data['virtual wall'] = self.decode_packet_13(byte_data.pop())
			sensor_data['cliff right'] = self.decode_packet_12(byte_data.pop())
			sensor_data['cliff front right'] = self.decode_packet_11(byte_data.pop())
			sensor_data['cliff front left'] = self.decode_packet_10(byte_data.pop())
			sensor_data['cliff left'] = self.decode_packet_9(byte_data.pop())
			sensor_data['wall seen'] = self.decode_packet_8(byte_data.pop())
			sensor_data['wheel drop and bumps'] = self.decode_packet_7(byte_data.pop())

		elif id == 1:
			# Size 10, contains 7-16
			temp = self.decode_packet_16(byte_data.pop())
			sensor_data['dirt detect'] = self.decode_packet_15(byte_data.pop())
			sensor_data['wheel overcurrents'] = self.decode_packet_14(byte_data.pop())
			sensor_data['virtual wall'] = self.decode_packet_13(byte_data.pop())
			sensor_data['cliff right'] = self.decode_packet_12(byte_data.pop())
			sensor_data['cliff front right'] = self.decode_packet_11(byte_data.pop())
			sensor_data['cliff front left'] = self.decode_packet_10(byte_data.pop())
			sensor_data['cliff left'] = self.decode_packet_9(byte_data.pop())
			sensor_data['wall seen'] = self.decode_packet_8(byte_data.pop())
			sensor_data['wheel drop and bumps'] = self.decode_packet_7(byte_data.pop())

		elif id == 2:
			# size 6, contains 17-20
			sensor_data['angle'] = self.decode_packet_20(byte_data.pop(), byte_data.pop())
			sensor_data['distance'] = self.decode_packet_19(byte_data.pop(), byte_data.pop())
			sensor_data['buttons'] = self.decode_packet_18(byte_data.pop())
			sensor_data['infared char left'] = self.decode_packet_17(byte_data.pop())

		elif id == 3:
			# size 10, contains 21-26
			sensor_data['battery capacity'] = self.decode_packet_26(byte_data.pop(), byte_data.pop())
			sensor_data['battery charge'] = self.decode_packet_25(byte_data.pop(), byte_data.pop())
			sensor_data['temperature'] = self.decode_packet_24(byte_data.pop())
			sensor_data['current'] = self.decode_packet_23(byte_data.pop(), byte_data.pop())
			sensor_data['voltage'] = self.decode_packet_22(byte_data.pop(), byte_data.pop())
			sensor_data['charging state'] = self.decode_packet_21(byte_data.pop())

		elif id == 4:
			# size 14, contains 27-34
			sensor_data['charging sources available'] = self.decode_packet_34(byte_data.pop())
			temp1 = self.decode_packet_33(byte_data.pop(), byte_data.pop())
			temp = self.decode_packet_32(byte_data.pop())
			sensor_data['cliff right signal'] = self.decode_packet_31(byte_data.pop(), byte_data.pop())
			sensor_data['cliff front right signal'] = self.decode_packet_30(byte_data.pop(), byte_data.pop())
			sensor_data['cliff front left signal'] = self.decode_packet_29(byte_data.pop(), byte_data.pop())
			sensor_data['cliff left signal'] = self.decode_packet_28(byte_data.pop(), byte_data.pop())
			sensor_data['wall signal'] = self.decode_packet_27(byte_data.pop(), byte_data.pop())

		elif id == 5:
			# size 12, contains 35-42
			sensor_data['requested left velocity'] = self.decode_packet_42(byte_data.pop(), byte_data.pop())
			sensor_data['requested right velocity'] = self.decode_packet_41(byte_data.pop(), byte_data.pop())
			sensor_data['requested radius'] = self.decode_packet_40(byte_data.pop(), byte_data.pop())
			sensor_data['requested velocity'] = self.decode_packet_39(byte_data.pop(), byte_data.pop())
			sensor_data['number of stream packets'] = self.decode_packet_38(byte_data.pop())
			sensor_data['song playing'] = self.decode_packet_37(byte_data.pop())
			sensor_data['song number'] = self.decode_packet_36(byte_data.pop())
			sensor_data['oi mode'] = self.decode_packet_35(byte_data.pop())

		elif id == 6:
			# size 52, contains 7-42
			sensor_data['requested left velocity'] = self.decode_packet_42(byte_data.pop(), byte_data.pop())
			sensor_data['requested right velocity'] = self.decode_packet_41(byte_data.pop(), byte_data.pop())
			sensor_data['requested radius'] = self.decode_packet_40(byte_data.pop(), byte_data.pop())
			sensor_data['requested velocity'] = self.decode_packet_39(byte_data.pop(), byte_data.pop())
			sensor_data['number of stream packets'] = self.decode_packet_38(byte_data.pop())
			sensor_data['song playing'] = self.decode_packet_37(byte_data.pop())
			sensor_data['song number'] = self.decode_packet_36(byte_data.pop())
			sensor_data['oi mode'] = self.decode_packet_35(byte_data.pop())
			sensor_data['charging sources available'] = self.decode_packet_34(byte_data.pop())
			temp2 = self.decode_packet_33(byte_data.pop(), byte_data.pop())
			temp1 = self.decode_packet_32(byte_data.pop())
			sensor_data['cliff right signal'] = self.decode_packet_31(byte_data.pop(), byte_data.pop())
			sensor_data['cliff front right signal'] = self.decode_packet_30(byte_data.pop(), byte_data.pop())
			sensor_data['cliff front left signal'] = self.decode_packet_29(byte_data.pop(), byte_data.pop())
			sensor_data['cliff left signal'] = self.decode_packet_28(byte_data.pop(), byte_data.pop())
			sensor_data['wall signal'] = self.decode_packet_27(byte_data.pop(), byte_data.pop())
			sensor_data['battery capacity'] = self.decode_packet_26(byte_data.pop(), byte_data.pop())
			sensor_data['battery charge'] = self.decode_packet_25(byte_data.pop(), byte_data.pop())
			sensor_data['temperature'] = self.decode_packet_24(byte_data.pop())
			sensor_data['current'] = self.decode_packet_23(byte_data.pop(), byte_data.pop())
			sensor_data['voltage'] = self.decode_packet_22(byte_data.pop(), byte_data.pop())
			sensor_data['charging state'] = self.decode_packet_21(byte_data.pop())
			sensor_data['angle'] = self.decode_packet_20(byte_data.pop(), byte_data.pop())
			sensor_data['distance'] = self.decode_packet_19(byte_data.pop(), byte_data.pop())
			sensor_data['buttons'] = self.decode_packet_18(byte_data.pop())
			sensor_data['infared char omni'] = self.decode_packet_17(byte_data.pop())
			temp = self.decode_packet_16(byte_data.pop())
			sensor_data['dirt detect'] = self.decode_packet_15(byte_data.pop())
			sensor_data['wheel overcurrents'] = self.decode_packet_14(byte_data.pop())
			sensor_data['virtual wall'] = self.decode_packet_13(byte_data.pop())
			sensor_data['cliff right'] = self.decode_packet_12(byte_data.pop())
			sensor_data['cliff front right'] = self.decode_packet_11(byte_data.pop())
			sensor_data['cliff front left'] = self.decode_packet_10(byte_data.pop())
			sensor_data['cliff left'] = self.decode_packet_9(byte_data.pop())
			sensor_data['wall seen'] = self.decode_packet_8(byte_data.pop())
			sensor_data['wheel drop and bumps'] = self.decode_packet_7(byte_data.pop())

		elif id == 7:
			sensor_data['wheel drop and bumps'] = self.decode_packet_7(byte_data.pop())
		elif id == 8:
			sensor_data['wall seen'] = self.decode_packet_8(byte_data.pop())
		elif id == 9:
			sensor_data['cliff left'] = self.decode_packet_9(byte_data.pop())
		elif id == 10:
			sensor_data['cliff front left'] = self.decode_packet_10(byte_data.pop())
		elif id == 11:
			sensor_data['cliff front right'] = self.decode_packet_11(byte_data.pop())
		elif id == 12:
			sensor_data['cliff right'] = self.decode_packet_12(byte_data.pop())
		elif id == 13:
			sensor_data['virtual wall'] = self.decode_packet_13(byte_data.pop())
		elif id == 14:
			sensor_data['wheel overcurrents'] = self.decode_packet_14(byte_data.pop())
		elif id == 15:
			sensor_data['dirt detect'] = self.decode_packet_15(byte_data.pop())
		elif id == 16:
			# unused
			temp = self.decode_packet_16(byte_data.pop())
		elif id == 17:
			sensor_data['infared char omni'] = self.decode_packet_17(byte_data.pop())
		elif id == 18:
			sensor_data['buttons'] = self.decode_packet_18(byte_data.pop())
		elif id == 19:
			sensor_data['distance'] = self.decode_packet_19(byte_data.pop(), byte_data.pop())
		elif id == 20:
			sensor_data['angle'] = self.decode_packet_20(byte_data.pop(), byte_data.pop())
		elif id == 21:
			sensor_data['charging state'] = self.decode_packet_21(byte_data.pop())
		elif id == 22:

			sensor_data['voltage'] = self.decode_packet_22(byte_data.pop(), byte_data.pop())
		elif id == 23:

			sensor_data['current'] = self.decode_packet_23(byte_data.pop(), byte_data.pop())
		elif id == 24:
			sensor_data['temperature'] = self.decode_packet_24(byte_data.pop())
		elif id == 25:

			sensor_data['battery charge'] = self.decode_packet_25(byte_data.pop(), byte_data.pop())
		elif id == 26:

			sensor_data['battery capacity'] = self.decode_packet_26(byte_data.pop(), byte_data.pop())
		elif id == 27:

			sensor_data['wall signal'] = self.decode_packet_27(byte_data.pop(), byte_data.pop())
		elif id == 28:

			sensor_data['cliff left signal'] = self.decode_packet_28(byte_data.pop(), byte_data.pop())
		elif id == 29:

			sensor_data['cliff front left signal'] = self.decode_packet_29(byte_data.pop(), byte_data.pop())
		elif id == 30:

			sensor_data['cliff front right signal'] = self.decode_packet_30(byte_data.pop(), byte_data.pop())
		elif id == 31:

			sensor_data['cliff right signal'] = self.decode_packet_31(byte_data.pop(), byte_data.pop())
		elif id == 32:
			temp = self.decode_packet_32(byte_data.pop())
		elif id == 33:

			temp = self.decode_packet_33(byte_data.pop(), byte_data.pop())
		elif id == 34:
			sensor_data['charging sources available'] = self.decode_packet_34(byte_data.pop())
		elif id == 35:
			sensor_data['oi mode'] = self.decode_packet_35(byte_data.pop())
		elif id == 36:
			sensor_data['song number'] = self.decode_packet_36(byte_data.pop())
		elif id == 37:
			sensor_data['song playing'] = self.decode_packet_37(byte_data.pop())
		elif id == 38:
			sensor_data['number of stream packets'] = self.decode_packet_38(byte_data.pop())
		elif id == 39:

			sensor_data['requested velocity'] = self.decode_packet_39(byte_data.pop(), byte_data.pop())
		elif id == 40:

			sensor_data['requested radius'] = self.decode_packet_40(byte_data.pop(), byte_data.pop())
		elif id == 41:

			sensor_data['requested right velocity'] = self.decode_packet_41(byte_data.pop(), byte_data.pop())
		elif id == 42:

			sensor_data['requested left velocity'] = self.decode_packet_42(byte_data.pop(), byte_data.pop())
		elif id == 43:

			sensor_data['left encoder counts'] = self.decode_packet_43(byte_data.pop(), byte_data.pop())
		elif id == 44:

			sensor_data['right encoder counts'] = self.decode_packet_44(byte_data.pop(), byte_data.pop())
		elif id == 45:
			sensor_data['light bumper'] = self.decode_packet_45(byte_data.pop())
		elif id == 46:

			sensor_data['light bump left signal'] = self.decode_packet_46(byte_data.pop(), byte_data.pop())
		elif id == 47:

			sensor_data['light bump front left signal'] = self.decode_packet_47(byte_data.pop(), byte_data.pop())
		elif id == 48:

			sensor_data['light bump center left signal'] = self.decode_packet_48(byte_data.pop(), byte_data.pop())
		elif id == 49:

			sensor_data['light bump center right signal'] = self.decode_packet_49(byte_data.pop(), byte_data.pop())
		elif id == 50:

			sensor_data['light bump front right signal'] = self.decode_packet_50(byte_data.pop(), byte_data.pop())
		elif id == 51:

			sensor_data['light bump right signal'] = self.decode_packet_51(byte_data.pop(), byte_data.pop())
		elif id == 52:
			sensor_data['infared char left'] = self.decode_packet_52(byte_data.pop())
		elif id == 53:
			sensor_data['infared char right'] = self.decode_packet_53(byte_data.pop())
		elif id == 54:

			sensor_data['left motor current'] = self.decode_packet_54(byte_data.pop(), byte_data.pop())
		elif id == 55:

			sensor_data['right motor current'] = self.decode_packet_55(byte_data.pop(), byte_data.pop())
		elif id == 56:

			sensor_data['main brush motor current'] = self.decode_packet_56(byte_data.pop(), byte_data.pop())
		elif id == 57:

			sensor_data['side brush motor current'] = self.decode_packet_57(byte_data.pop(), byte_data.pop())
		elif id == 58:
			sensor_data['stasis'] = self.decode_packet_58(byte_data.pop())
			# Single Packets END
		elif id == 100:
			# size 80, contains 7-58 (ALL)
			sensor_data['stasis'] = self.decode_packet_58(byte_data.pop())
			sensor_data['side brush motor current'] = self.decode_packet_57(byte_data.pop(), byte_data.pop())
			sensor_data['main brush motor current'] = self.decode_packet_56(byte_data.pop(), byte_data.pop())
			sensor_data['right motor current'] = self.decode_packet_55(byte_data.pop(), byte_data.pop())
			sensor_data['left motor current'] = self.decode_packet_54(byte_data.pop(), byte_data.pop())
			sensor_data['infared char right'] = self.decode_packet_53(byte_data.pop())
			sensor_data['infared char left'] = self.decode_packet_52(byte_data.pop())
			sensor_data['light bump right signal'] = self.decode_packet_51(byte_data.pop(), byte_data.pop())
			sensor_data['light bump front right signal'] = self.decode_packet_50(byte_data.pop(), byte_data.pop())
			sensor_data['light bump center right signal'] = self.decode_packet_49(byte_data.pop(), byte_data.pop())
			sensor_data['light bump center left signal'] = self.decode_packet_48(byte_data.pop(), byte_data.pop())
			sensor_data['light bump front left signal'] = self.decode_packet_47(byte_data.pop(), byte_data.pop())
			sensor_data['light bump left signal'] = self.decode_packet_46(byte_data.pop(), byte_data.pop())
			sensor_data['light bumper'] = self.decode_packet_45(byte_data.pop())
			sensor_data['right encoder counts'] = self.decode_packet_44(byte_data.pop(), byte_data.pop())
			sensor_data['left encoder counts'] = self.decode_packet_43(byte_data.pop(), byte_data.pop())
			sensor_data['requested left velocity'] = self.decode_packet_42(byte_data.pop(), byte_data.pop())
			sensor_data['requested right velocity'] = self.decode_packet_41(byte_data.pop(), byte_data.pop())
			sensor_data['requested radius'] = self.decode_packet_40(byte_data.pop(), byte_data.pop())
			sensor_data['requested velocity'] = self.decode_packet_39(byte_data.pop(), byte_data.pop())
			sensor_data['number of stream packets'] = self.decode_packet_38(byte_data.pop())
			sensor_data['song playing'] = self.decode_packet_37(byte_data.pop())
			sensor_data['song number'] = self.decode_packet_36(byte_data.pop())
			sensor_data['oi mode'] = self.decode_packet_35(byte_data.pop())
			sensor_data['charging sources available'] = self.decode_packet_34(byte_data.pop())
			temp2 = self.decode_packet_33(byte_data.pop(), byte_data.pop())
			temp1 = self.decode_packet_32(byte_data.pop())
			sensor_data['cliff right signal'] = self.decode_packet_31(byte_data.pop(), byte_data.pop())
			sensor_data['cliff front right signal'] = self.decode_packet_30(byte_data.pop(), byte_data.pop())
			sensor_data['cliff front left signal'] = self.decode_packet_29(byte_data.pop(), byte_data.pop())
			sensor_data['cliff left signal'] = self.decode_packet_28(byte_data.pop(), byte_data.pop())
			sensor_data['wall signal'] = self.decode_packet_27(byte_data.pop(), byte_data.pop())
			sensor_data['battery capacity'] = self.decode_packet_26(byte_data.pop(), byte_data.pop())
			sensor_data['battery charge'] = self.decode_packet_25(byte_data.pop(), byte_data.pop())
			sensor_data['temperature'] = self.decode_packet_24(byte_data.pop())
			sensor_data['current'] = self.decode_packet_23(byte_data.pop(), byte_data.pop())
			sensor_data['voltage'] = self.decode_packet_22(byte_data.pop(), byte_data.pop())
			sensor_data['charging state'] = self.decode_packet_21(byte_data.pop())
			sensor_data['angle'] = self.decode_packet_20(byte_data.pop(), byte_data.pop())
			sensor_data['distance'] = self.decode_packet_19(byte_data.pop(), byte_data.pop())
			sensor_data['buttons'] = self.decode_packet_18(byte_data.pop())
			sensor_data['infared char omni'] = self.decode_packet_17(byte_data.pop())
			temp = self.decode_packet_16(byte_data.pop())
			sensor_data['dirt detect'] = self.decode_packet_15(byte_data.pop())
			sensor_data['wheel overcurrents'] = self.decode_packet_14(byte_data.pop())
			sensor_data['virtual wall'] = self.decode_packet_13(byte_data.pop())
			sensor_data['cliff right'] = self.decode_packet_12(byte_data.pop())
			sensor_data['cliff front right'] = self.decode_packet_11(byte_data.pop())
			sensor_data['cliff front left'] = self.decode_packet_10(byte_data.pop())
			sensor_data['cliff left'] = self.decode_packet_9(byte_data.pop())
			sensor_data['wall seen'] = self.decode_packet_8(byte_data.pop())
			sensor_data['wheel drop and bumps'] = self.decode_packet_7(byte_data.pop())

		elif id == 101:
			# size 28, contains 43-58
			sensor_data['stasis'] = self.decode_packet_58(byte_data.pop())
			sensor_data['side brush motor current'] = self.decode_packet_57(byte_data.pop(), byte_data.pop())
			sensor_data['main brush motor current'] = self.decode_packet_56(byte_data.pop(), byte_data.pop())
			sensor_data['right motor current'] = self.decode_packet_55(byte_data.pop(), byte_data.pop())
			sensor_data['left motor current'] = self.decode_packet_54(byte_data.pop(), byte_data.pop())
			sensor_data['infared char right'] = self.decode_packet_53(byte_data.pop())
			sensor_data['infared char left'] = self.decode_packet_52(byte_data.pop())
			sensor_data['light bump right signal'] = self.decode_packet_51(byte_data.pop(), byte_data.pop())
			sensor_data['light bump front right signal'] = self.decode_packet_50(byte_data.pop(), byte_data.pop())
			sensor_data['light bump center right signal'] = self.decode_packet_49(byte_data.pop(), byte_data.pop())
			sensor_data['light bump center left signal'] = self.decode_packet_48(byte_data.pop(), byte_data.pop())
			sensor_data['light bump front left signal'] = self.decode_packet_47(byte_data.pop(), byte_data.pop())
			sensor_data['light bump left signal'] = self.decode_packet_46(byte_data.pop(), byte_data.pop())
			sensor_data['light bumper'] = self.decode_packet_45(byte_data.pop())
			sensor_data['right encoder counts'] = self.decode_packet_44(byte_data.pop(), byte_data.pop())
			sensor_data['left encoder counts'] = self.decode_packet_43(byte_data.pop(), byte_data.pop())

		elif id == 106:
			# size 12, contains 46-51
			sensor_data['light bump right signal'] = self.decode_packet_51(byte_data.pop(), byte_data.pop())
			sensor_data['light bump front right signal'] = self.decode_packet_50(byte_data.pop(), byte_data.pop())
			sensor_data['light bump center right signal'] = self.decode_packet_49(byte_data.pop(), byte_data.pop())
			sensor_data['light bump center left signal'] = self.decode_packet_48(byte_data.pop(), byte_data.pop())
			sensor_data['light bump front left signal'] = self.decode_packet_47(byte_data.pop(), byte_data.pop())
			sensor_data['light bump left signal'] = self.decode_packet_46(byte_data.pop(), byte_data.pop())

		elif id == 107:
			# size 9, contains 54-58
			sensor_data['stasis'] = self.decode_packet_58(byte_data.pop())
			sensor_data['side brush motor current'] = self.decode_packet_57(byte_data.pop(), byte_data.pop())
			sensor_data['main brush motor current'] = self.decode_packet_56(byte_data.pop(), byte_data.pop())
			sensor_data['right motor current'] = self.decode_packet_55(byte_data.pop(), byte_data.pop())
			sensor_data['left motor current'] = self.decode_packet_54(byte_data.pop(), byte_data.pop())

		else:
			# warnings.formatwarning = custom_format_warning
			# warnings.warn("Warning: Packet '" + id + "' is not a valid packet!")
			Exception("Warning: Packet '" + id + "' is not a valid packet!")

		return sensor_data

	def decode_packet_7(self, data):
		""" Decode Packet 7 (wheel drop and bumps) and return its value

			Arguments:
				data: The bytes to decode

			Returns: A dict of 'wheel drop and bumps'
		"""
		byte = struct.unpack('B', data)[0]
		return_dict = {
			'drop left': bool(byte & 0x08),
			'drop right': bool(byte & 0x04),
			'bump left': bool(byte & 0x02),
			'bump right': bool(byte & 0x01)}
		return return_dict

	def decode_packet_8(self, data):
		""" Decode Packet 8 (wall seen) and return its value

			Arguments:
				data: The bytes to decode

			Returns: True or False
		"""
		return self.decode_bool(data)

	def decode_packet_9(self, data):
		""" Decode Packet 9 (cliff left) and return its value

			Arguments:
				data: The bytes to decode

			Returns: True or False
		"""
		return self.decode_bool(data)

	def decode_packet_10(self, data):
		""" Decode Packet 10 (cliff front left) and return its value

			Arguments:
				data: The bytes to decode

			Returns: True or False
		"""
		return self.decode_bool(data)

	def decode_packet_11(self, data):
		""" Decode Packet 11 (cliff front right) and return its value

			Arguments:
				data: The bytes to decode

			Returns: True or False
		"""
		return self.decode_bool(data)

	def decode_packet_12(self, data):
		""" Decode Packet 12 (cliff right) and return its value

			Arguments:
				data: The bytes to decode

			Returns: True or False
		"""
		return self.decode_bool(data)

	def decode_packet_13(self, data):
		""" Decode Packet 13 (virtual wall) and return its value

			Arguments:
				data: The bytes to decode

			Returns: True or False
		"""
		return self.decode_bool(data)

	def decode_packet_14(self, data):
		""" Decode Packet 14 (wheel overcurrents) and return its value

			Arguments:
				data: The bytes to decode

			Returns: A dict of 'wheel overcurrents'
		"""
		byte = struct.unpack('B', data)[0]
		return_dict = {
			'left wheel': bool(byte & 0x10),
			'right wheel': bool(byte & 0x08),
			'main brush': bool(byte & 0x04),
			'side brush': bool(byte & 0x01)}
		return return_dict

	def decode_packet_15(self, data):
		""" Decode Packet 15 (dirt detect) and return its value

			Arguments:
				data: The bytes to decode

			Returns: unsigned Byte (0-255)
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_16(self, data):
		""" Decode Packet 16 (unused byte) and return its value

			Arguments:
				data: The bytes to decode

			Returns: None
		"""
		return None

	def decode_packet_17(self, data):
		""" Decode Packet 17 (infared char omni) and return its value

			Arguments:
				data: The bytes to decode

			Returns: unsigned Byte (0-255)
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_18(self, data):
		""" Decode Packet 18 (buttons) and return its value

			Arguments:
				data: The bytes to decode

			Returns: a dict of 'buttons'
		"""
		byte = struct.unpack('B', data)[0]
		return_dict = {
			'clock': bool(byte & 0x80),
			'schedule': bool(byte & 0x40),
			'day': bool(byte & 0x20),
			'hour': bool(byte & 0x10),
			'minute': bool(byte & 0x08),
			'dock': bool(byte & 0x04),
			'spot': bool(byte & 0x02),
			'clean': bool(byte & 0x01)}

		return return_dict

	def decode_packet_19(self, low, high):
		""" Decode Packet 19 (distance) and return its value

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: signed 16bit short
		"""
		return self.decode_short(low, high)

	def decode_packet_20(self, low, high):
		""" Decode Packet 20 (angle) and return its value

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: signed 16 bit short. Represents difference between distance two wheels travelled
		"""
		return self.decode_short(low, high)

	def decode_packet_21(self, data):
		""" Decode Packet 21 (charging state) and return its value

			Arguments:
				data: The bytes to decode

			Returns: A value from 0-5, that describes the charging state
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_22(self, low, high):
		"""
		Decode Packet 22 (voltage) and return its value
		Range: 0 - 65535 mV

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short, battery voltage in mV
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_23(self, low, high):
		"""
		Decode Packet 23 (current) and return its value
		Range: -32768 - 32767 mA

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: signed 16bit short. Positive currents is charging, negative is discharging
		"""
		return self.decode_short(low, high)

	def decode_packet_24(self, data):
		""" Decode Packet 24 (temperature) and return its value
		Range: -128 - 127

			Arguments:
				data: The bytes to decode

			Returns: A signed byte, Create 2's battery temperature in Celsius
		"""
		return self.decode_byte(data)

	def decode_packet_25(self, low, high):
		""" Decode Packet 25 (battery charge) and return its value
		Range: 0 - 65535 mAh

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Current charge of battery in milliAmp-hours
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_26(self, low, high):
		""" Decode Packet 26 (battery capacity) and return its value
		Range: 0 - 65535 mAh

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Estimated charge capacity of battery in milliAmp-hours
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_27(self, low, high):
		""" Decode Packet 27 (wall signal) and return its value
		NOTE: This packet is deprecated and only kept for backwards compatibility.
		It is recommended you use the Light Bump Right Signal (ID: 51) packet
		instead, which has a higher resolution.

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of wall signal from 0-1023
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_28(self, low, high):
		""" Decode Packet 28 (cliff left signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of cliff left signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_29(self, low, high):
		""" Decode Packet 29 (cliff front left signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of cliff front left signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_30(self, low, high):
		""" Decode Packet 30 (cliff front right signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of cliff front right signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_31(self, low, high):
		""" Decode Packet 31 (cliff right signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of cliff right signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_32(self, data):
		""" Decode Packet 32 (Unused) and return its value

			Arguments:
				data: The bytes to decode

			Returns: None
		"""
		return None

	def decode_packet_33(self, low, high):
		""" Decode Packet 33 (Unused) and return its value

			Arguments:
				low: The bytes to ignore
				high: The bytes to ignore

			Returns: None
		"""
		return None

	def decode_packet_34(self, data):
		""" Decode Packet 34 (charging sources available) and return its value

			Arguments:
				data: The bytes to decode

			Returns: A dict of 'charging sources available'
		"""
		byte = struct.unpack('B', data)[0]
		return_dict = {
			'home base': bool(byte & 0x02),
			'internal charger': bool(byte & 0x01)}

		return return_dict

	def decode_packet_35(self, data):
		""" Decode Packet 35 (OI Mode) and return its value

			Arguments:
				data: The bytes to decode

			Returns: A unsigned byte, the current OI mode id from 0-3
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_36(self, data):
		""" Decode Packet 36 (Song number) and return its value

			Arguments:
				data: The bytes to decode

			Returns: An unsigned byte, the current song id playing (0-15)
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_37(self, data):
		""" Decode Packet 35 (Song playing) and return its value

			Arguments:
				data: The bytes to decode

			Returns: True or False, stating whether the song is playing
		"""
		return self.decode_bool(data)

	def decode_packet_38(self, data):
		""" Decode Packet 38 (Number of stream packets) and return its value

			Arguments:
				data: The bytes to decode

			Returns: An unsigned byte, the number of data stream packets
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_39(self, low, high):
		""" Decode Packet 39 (requested velocity) and return its value

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Velocity most recently requested by Drive()
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_40(self, low, high):
		""" Decode Packet 40 (requested radius) and return its value

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Radius most recently requested by Drive()
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_41(self, low, high):
		""" Decode Packet 41 (Requested right velocity) and return its value

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Right wheel velocity recently requested by DriveDirect()
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_42(self, low, high):
		""" Decode Packet 42 (Requested left velocity) and return its value

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Left wheel velocity recently requested by DriveDirect()
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_43(self, low, high):
		""" Decode Packet 41 (Left Encoder Counts) and return its value
		Range: -32768 - 32767 counts

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Cumulative number of raw left encoder counts. Rolls over
						to 0 after it passes 65535
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_44(self, low, high):
		""" Decode Packet 44 (Right Encoder Counts) and return its value
		Range: -32768 - 32767 counts

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Cumulative number of raw right encoder counts. Rolls over
						to 0 after it passes 65535
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_45(self, data):
		""" Decode Packet 45 (infared char left) and return its value
		Range: 0-127

			Arguments:
				data: The bytes to decode

			Returns: A dict of 'light bumper'
		"""
		byte = struct.unpack('B', data)[0]
		return_dict = {
			'right': bool(byte & 0x20),
			'front right': bool(byte & 0x10),
			'center right': bool(byte & 0x08),
			'center left': bool(byte & 0x04),
			'front left': bool(byte & 0x02),
			'left': bool(byte & 0x01)}
		return return_dict

	def decode_packet_46(self, low, high):
		""" Decode Packet 46 (Light Bump Left Signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of light bump left signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_47(self, low, high):
		""" Decode Packet 47 (Light Bump Front Left Signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of light bump front left signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_48(self, low, high):
		""" Decode Packet 48 (Light Bump Center Left Signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of light bump center left signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_49(self, low, high):
		""" Decode Packet 49 (Light Bump Center Right Signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of light bump center right signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_50(self, low, high):
		""" Decode Packet 50 (Light Bump Front Right Signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of light bump front right signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_51(self, low, high):
		""" Decode Packet 51 (Light Bump Right Signal) and return its value
		Range: 0-4095

			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: unsigned 16bit short. Strength of light bump right signal from 0-4095
		"""
		return self.decode_unsigned_short(low, high)

	def decode_packet_52(self, data):
		""" Decode Packet 52 (infared char left) and return its value

			Arguments:
				data: The bytes to decode

			Returns: unsigned Byte (0-255)
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_53(self, data):
		""" Decode Packet 53 (infared char right) and return its value

			Arguments:
				data: The bytes to decode

			Returns: unsigned Byte (0-255)
		"""
		return self.decode_unsigned_byte(data)

	def decode_packet_54(self, low, high):
		""" Decode Packet 54 (Left Motor Current) and return its value
		Range: -32768 - 32767 mA


			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: signed 16bit short. Strength of left motor current from -32768 - 32767 mA
		"""
		return self.decode_short(low, high)

	def decode_packet_55(self, low, high):
		""" Decode Packet 55 (Right Motor Current) and return its value
		Range: -32768 - 32767 mA


			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: signed 16bit short. Strength of right motor current from -32768 - 32767 mA
		"""
		return self.decode_short(low, high)

	def decode_packet_56(self, low, high):
		""" Decode Packet 54 (Main Brush Motor Current) and return its value
		Range: -32768 - 32767 mA


			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: signed 16bit short. Strength of main brush motor current from -32768 - 32767 mA
		"""
		return self.decode_short(low, high)

	def decode_packet_57(self, low, high):
		""" Decode Packet 57 (Side Brush Motor Current) and return its value
		Range: -32768 - 32767 mA


			Arguments:
				low: Low byte of the 2's complement. Low is specified first to make pop() easier
				high: High byte of the 2's complement

			Returns: signed 16bit short. Strength of side brush motor current from -32768 - 32767 mA
		"""
		return self.decode_short(low, high)

	def decode_packet_58(self, data):
		""" Decode Packet 58 (Stasis) and return its value
		The stasis caster sensor returns 1 when the robot is making forward
		progress and 0 when it is not. It always returns 0 when the robot is
		turning, driving backward, or not driving. If the stasis wheel is too
		dirty to be read, a value of 2 is returned. If this happens, remove the
		stasis wheel and clean it with a damp cloth, then dry it thoroughly
		before reinstalling the wheel.

		Range: 0 - 3

			Arguments:
				data: The bytes to decode

			Returns: True if robot is making forward progress, else False
		"""
		return self.decode_bool(data)

	def decode_bool(self, byte):
		""" Decode a byte and return the value

			Arguments:
				byte: The byte to be decoded
			Returns: True or False
		"""
		return bool(struct.unpack('B', byte)[0])

	def decode_unsigned_short(self, low, high):
		""" Decode an 16 bit unsigned short from two bytes.

			Arguments:
				low: The low byte of the 2's complement. This is specified first
					to make it easier when popping bytes off a list.
				high: The high byte o the 2's complement.
			Returns: 16bit unsigned short
		"""
		return struct.unpack('>H', high + low)[0]

	def decode_short(self, low, high):
		""" Decode an 16 bit short from two bytes.

			Arguments:
				low: The low byte of the 2's complement. This is specified first
					to make it easier when popping bytes off a list.
				high: The high byte of the 2's complement.
			Returns: 16bit short
		"""
		return struct.unpack('>h', high + low)[0]

	def decode_byte(self, byte):
		""" Decode a signed byte into a signed char

			Arguments:
				byte: The byte to be decoded
			Returns: A signed int
		"""
		return struct.unpack('b', byte)[0]

	def decode_unsigned_byte(self, byte):
		""" Decode an unsigned byte into an unsigned char

			Arguments:
				byte: The byte to be decoded
			Returns: An unsigned int
		"""
		return struct.unpack('B', byte)[0]
