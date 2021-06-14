from machine import Pin
import time
from utime import ticks_add
from utime import ticks_diff

class Endpoint:
	def __init__(self, pin):
		self.pin = Pin(pin, Pin.IN)

	def status(self):
		return self.pin.value()

class Stepper:
	def __init__(self, stp_pin, dir_pin, pow_pin, step_sleep_us=1000, full_rev=360, step_angle=1.8, pitch_mm=8, microstepping=32):
		self.stp = Pin(stp_pin, Pin.OUT)
		self.dir = Pin(dir_pin, Pin.OUT)
		self.pow = Pin(pow_pin, Pin.OUT, value=0)
		self.step_sleep_us = step_sleep_us
		self.steps_per_mm = ((full_rev / step_angle) / pitch_mm) * microstepping

	def power_on(self):
		self.pow.value(0)

	def power_off(self):
		self.pow.value(1)

	def set_direction(self, direction):
		self.dir.value(direction)

	def rotate_steps(self, steps):
		for i in range(abs(steps)):
			self.stp.value(1)
			sleep_us(self.step_sleep_us)
			self.stp.value(0)
			sleep_us(self.step_sleep_us)

	def rotate_mm(self, mm):
		self.rotate_steps(mm * self.steps_per_mm)

endpoint = Endpoint(pin=25)
sampler_stepper = Stepper(stp_pin= 2, dir_pin= 4, pow_pin=15, step_sleep_us=100)

sampler_stepper.set_dir(0)
sampler_stepper.power_on()

while endpoint.status() == 1:
	sampler_stepper.rotate_steps(1)

sampler_stepper.power_off()
