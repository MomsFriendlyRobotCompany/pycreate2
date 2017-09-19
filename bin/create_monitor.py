#!/usr/bin/env python

from __future__ import print_function, division
import argparse
import pycreate2
import time
from pycreate2.packets import Buttons, WheelOvercurrents, ChargingSources, LightBumper, Stasis, BumpsAndWheelDrop

DESCRIPTION = """
Prints the raw data from a Create 2. The default packet is 100 which get everything.
However, this can be changed and a different packet and refresh rates can be selected.

Example:
$ ./monitor.py /dev/tty.usbserial-DA01NX3Z
Create opened serial: Serial<id=0x109f3e450, open=True>(port='/dev/tty.usbserial-DA01NX3Z', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)
----------------------------------------------------------------------
                       infared char left | 0
                             temperature | 35
                      wheel overcurrents |
                                       right wheel : 0
                                        left wheel : 0
                                        main brush : 0
                                        side brush : 0
                              cliff left | 0
                       infared char omni | 0
                       cliff front right | 0
                                 voltage | 14806
                      cliff right signal | 2880
                  light bump left signal | 25
                 cliff front left signal | 2915
                      requested velocity | 0
                                 buttons |
                                              dock : 0
                                             clean : 0
                                              hour : 0
                                             clock : 0
                                          schedule : 0
                                              spot : 0
                                               day : 0
                                            minute : 0
                             cliff right | 0
                          battery charge | 596
                          charging state | 0
                side brush motor current | 1
                            song playing | 0
                        requested radius | 0
                      left motor current | 1
                             dirt detect | 0
                                 current | -250
                            light bumper |
                                             right : 0
                                      center right : 0
                                        front left : 0
                                       center left : 0
                                       front right : 0
                                              left : 0
                 requested left velocity | 0
                            virtual wall | 0
                    wheel drop and bumps |
                                        bump right : 0
                                         drop left : 0
                                        drop right : 0
                                         bump left : 0
                number of stream packets | 0
                               wall seen | 0
                             song number | 0
                                distance | 0
                                 oi mode | 2
                                  stasis | 0
                       cliff left signal | 2871
                cliff front right signal | 2880
                main brush motor current | -1
                requested right velocity | 0
                                   angle | 0
                        cliff front left | 0
          light bump center right signal | 0
           light bump front right signal | 26
                        battery capacity | 2696
                    right encoder counts | 1
           light bump center left signal | 32
              charging sources available |
                                         home base : 0
                                  internal charger : 0
                 light bump right signal | 3
            light bump front left signal | 29
                             wall signal | 0
                      infared char right | 0
                     left encoder counts | 1
                     right motor current | 1
"""


def handleArgs():
	parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
	# parser.add_argument('-m', '--max', help='max id', type=int, default=253)
	parser.add_argument('-s', '--sleep', help='time in seconds between samples, default 1.0', type=float, default=1.0)
	# parser.add_argument('-i', '--id', help='packet ID, default is 100', type=int, default=100)
	parser.add_argument('port', help='serial port name, Ex: /dev/ttyUSB0 or COM1', type=str)

	args = vars(parser.parse_args())
	return args


class Monitor(object):
	def __init__(self):
		pass

	def display_raw(self, sensor):
		sensor = sensor._asdict()
		print('-'*70)
		for k, v in sensor.items():
			# if dict is type(v):
			if type(v) in [Buttons, WheelOvercurrents, ChargingSources, LightBumper, Stasis, BumpsAndWheelDrop]:
				v = v._asdict()
				print('{:>40} |'.format(k))
				for kk, vv in v.items():
					print('{:>50} : {:<5}'.format(kk, vv))
			else:
				print('{:>40} | {:<10}'.format(k, v))

	def display_formated(self, sensor):
		raise NotImplementedError()

		print('================================================')
		print('Sensors from left to right')
		print('------------------------------------------------')
		print('  IR: {} {} {} {}'.format())
		print('  Bump: {} {} {} {} {} {}'.format())
		print('  Cliff: {} {} {} {}'.format())
		print('  Wheel drops: {} {}'.format())
		print('  Encoder: {} {}'.format())
		print('  Temperature: {} C / {} F'.format())
		print('  Wheel Overcurrents: {} {}'.format())
		print('------------------------------------------------')
		print('Electrical:')
		print('------------------------------------------------')
		print('  Battery: {:.2f}% at {} V'.format())
		print('  Current: {} A'.format())
		print('  Motor Current: {} A {} A'.format())
		print('  Charging: {}'.format())
		print('------------------------------------------------')
		print('Commands:')
		print('------------------------------------------------')
		print('  Motors: {} {} mm/sec'.format())
		print('  Turn Radius: {} mm'.format())


if __name__ == '__main__':
	# get command line args
	args = handleArgs()
	port = args['port']
	dt = args['sleep']

	# create print monitor
	mon = Monitor()

	# create robot
	bot = pycreate2.Create2(port)
	bot.start()
	bot.safe()

	# now run forever, until someone hits ctrl-C
	try:
		while True:
			try:
				sensor_state = bot.get_sensors()
				mon.display_raw(sensor_state)
				time.sleep(dt)
			except Exception as e:
				print(e)
				continue
			except:
				raise
	except KeyboardInterrupt:
		print('bye ... ')
