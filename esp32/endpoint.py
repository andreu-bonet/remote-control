from machine import Pin
import time
from utime import ticks_add
from utime import ticks_diff

class Endpoint:
	def __init__(self, pin):
		self.pin = Pin(pin, Pin.IN)

	def status(self):
		return self.pin.value()

endpoint = Endpoint(pin=25)

def sleep_ms(ms):
	deadline = ticks_add(time.ticks_ms(), ms)
	while ticks_diff(deadline, time.ticks_ms()) > 0:
		pass

while True:
	print(endpoint.status())
	sleep_ms(1000)
