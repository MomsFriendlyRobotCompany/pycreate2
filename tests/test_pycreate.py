from pycreate2.OI import RESPONSE_SIZES
from pycreate2.OI import calc_query_data_len
from pycreate2.packets import SensorPacketDecoder
import pycreate2
import os
import time



def testConstructor():
    bot = pycreate2.Create2(port="COM43", baud=115200)
    bot.start()
    bot.safe()
    # bot.clean()
    bot.enableVacuum()
    time.sleep(3)
    bot.disableVaacum()

    # bot.reset()
    # time.sleep(10)
    # bot.drive_direct(-50, -50)
    # time.sleep(1)
    # bot.stop()
    # bot.enableVacuum()
    # time.sleep(3)
    # bot.disableVaacum()
    assert True

# def test_packet_id():
#     packet_id = 100
#     if packet_id in RESPONSE_SIZES:
#         packet_size = RESPONSE_SIZES[packet_id]
#         assert packet_size == 80
#     else:
#         assert False


# def test_packet_length():
#     pkts = [21, 22, 23, 24, 25]
#     packet_len = calc_query_data_len(pkts)
#     assert packet_len == 8
#     pkts = [100]
#     packet_len = calc_query_data_len(pkts)
#     assert packet_len == 80


# def test_process_packet():
#     try:
#         # i need to get a known packet and check values
#         data = bytearray(os.urandom(80))
#         sensors = SensorPacketDecoder(data)
#         assert isinstance(sensors, tuple)
#     except:
#         assert False
