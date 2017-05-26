#!/usr/bin/env python

from __future__ import print_function, division


class Monitor(object):
	def __init__(self):
		pass

	def display(self, sensor):
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
	pass
