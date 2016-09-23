#!/usr/bin/env python
'''
**********************************************************************
* Filename    : TB6612.py
* Description : A driver module for TB6612
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-23    New release
**********************************************************************
'''
import RPi.GPIO as GPIO

class Motor(object):
	''' Motor driver class
		Set direction_channel to the GPIO channel which connect to MA, 
		Set motor_B to the GPIO channel which connect to MB,
		Both GPIO channel use BCM numbering;
		Set pwm_channel to the PWM channel which connect to PWMA,
		Set pwm_B to the PWM channel which connect to PWMB;
		PWM channel using PCA9685, Set pwm_address to your address, if is not 0x40
		Set debug to True to print out debug informations.
	'''
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "TB6612.py":'

	def __init__(self, direction_channel, pwm_channel, offset=True):
		'''Init a motor on giving dir. channel and PWM channel.'''
		if self._DEBUG:
			print self._DEBUG_INFO, "Debug on"
		self.direction_channel = direction_channel
		self.pwm_channel = pwm_channel
		self.offset = offset
		self.forward_offset = self.offset

		self.backward_offset = not self.forward_offset
		self.set_debug(self._DEBUG)
		self.speed = 0
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		if self._DEBUG:
			print self._DEBUG_INFO, 'setup motor direction channel at', direction_channel
			print self._DEBUG_INFO, 'setup motor pwm channel at', pwm_channel
		GPIO.setup(self.direction_channel, GPIO.OUT)
		GPIO.setup(self.pwm_channel, GPIO.OUT)
		self.speed_control = GPIO.PWM(self.pwm_channel, 1000)
		self.speed_control.start(0)

	def set_speed(self, speed):
		''' Set Speed with giving value '''
		if speed not in range(0, 101):
			raise ValueError('speed ranges fron 0 to 100, not "{0}"'.format(speed))
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set speed to: ', speed
		self.speed = speed
		self.speed_control.ChangeDutyCycle(self.speed)

	def forward(self):
		''' Set the motor direction to forward '''
		GPIO.output(self.direction_channel, self.forward_offset)
		self.set_speed(self.speed)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor moving forward (%s)' % str(self.forward_offset)

	def backward(self):
		''' Set the motor direction to backward '''
		GPIO.output(self.direction_channel, self.backward_offset)
		self.set_speed(self.speed)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor moving backward (%s)' % str(self.backward_offset)

	def stop(self):
		''' Stop the motor by giving a 0 speed '''
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor stop'
		self.set_speed(0)

	def set_offset(self, value):
		''' Set offset for much user-friendly '''
		if value not in (True, False):
			raise ValueError('offset value must be Bool value, not"{0}"'.format(value))
		self.forward_offset = value
		self.backward_offset = not self.forward_offset
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set offset to %d' % self.offset

	def set_debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
		else:
			print self._DEBUG_INFO, "Set debug off"

if __name__ == '__main__':
	import time

	print "********************************************"
	print "*                                          *"
	print "*           SunFounder TB6612              *"
	print "*                                          *"
	print "*          Connect MA to BCM17             *"
	print "*          Connect MB to BCM18             *"
	print "*         Connect PWMA to BCM27            *"
	print "*         Connect PWMB to BCM12            *"
	print "*                                          *"
	print "********************************************"
	motorA = Motor(17, 27)
	motorB = Motor(18, 22)
	motorA.set_debug(True)
	motorB.set_debug(True)

	delay = 0.05

	motorA.forward()
	for i in range(0, 101):
		motorA.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.set_speed(i)
		time.sleep(delay)

	motorA.backward()
	for i in range(0, 101):
		motorA.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.set_speed(i)
		time.sleep(delay)

	motorB.forward()
	for i in range(0, 101):
		motorB.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.set_speed(i)
		time.sleep(delay)

	motorB.backward()
	for i in range(0, 101):
		motorB.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.set_speed(i)
		time.sleep(delay)