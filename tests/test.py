# import pycreate2
from pycreate2.OI import sensor_packet_lengths
from pycreate2.OI import calc_query_data_len


# def test_dummy():
# 	assert True


def test_packet_id():
	packet_id = 100
	strid = str(packet_id)
	if strid in sensor_packet_lengths:
		packet_size = sensor_packet_lengths[strid]
		assert packet_size == 80
	else:
		assert False


def test_packet_length():
	pkts = [21, 22, 23, 24, 25]
	packet_len = calc_query_data_len(pkts)
	assert packet_len == 8
