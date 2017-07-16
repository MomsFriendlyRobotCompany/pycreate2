##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from setuptools import setup
from pycreate2.version import __version__ as VERSION
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution


PACKAGE_NAME = 'pycreate2'
BuildCommand.pkg = PACKAGE_NAME
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION


setup(
	author='Kevin Walchko',
	author_email='walchko@users.noreply.github.com',
	name=PACKAGE_NAME,
	version=VERSION,
	description='A library to control iRobot Create 2 with python',
	long_description=open('README.rst').read(),
	url='http://github.com/walchko/{}'.format(PACKAGE_NAME),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.6',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Libraries :: Application Frameworks'
	],
	license='MIT',
	keywords=['irobot', 'create 2', 'api', 'framework', 'library', 'robotics', 'robot', 'smart'],
	packages=[PACKAGE_NAME],
	install_requires=open('requirements.txt').readlines(),
	cmdclass={
		'publish': PublishCommand,
		'make': BuildCommand
	},
	scripts=[
		'bin/create_reset.py',
		'bin/create_shutdown.py',
		'bin/create_monitor.py'
	]
)
