import network
import usocket
import machine
import time

from utime import ticks_add
from utime import ticks_diff


class PrecisionStepper:
	"""Class for stepper motor"""

	def __init__(self, step_pin, dir_pin, en_pin, step_time=1000, steps_per_rev=1600):
		"""Initialise stepper."""
		self.stp = machine.Pin(step_pin, Pin.OUT)
		self.dir = machine.Pin(dir_pin, Pin.OUT)
		self.en = machine.Pin(en_pin, Pin.OUT, value=0)

		self.step_time = step_time
		self.steps_per_rev = steps_per_rev

	def power_on(self):
		"""Power on stepper."""
		self.en.value(0)

	def power_off(self):
		"""Power off stepper."""
		self.en.value(1)

	def set_dir(self, _dir):
		self.dir.value(_dir)

	def steps(self, step_count):
		"""Rotate stepper for given steps."""
		for i in range(abs(step_count)):
			self.stp.value(1)
			thime.sleep_us(self.step_time)
			self.stp.value(0)
			thime.sleep_us(self.step_time)

	def mm(self, mm, step_per_mm):
		self.steps(mm * step_per_mm)

	def set_step_time(self, us):
		"""Set time in microseconds between each step."""
		self.step_time = us

stirring_steppers = PrecisionStepper(step_pin=19, dir_pin=21, en_pin=18, step_time=1000)

def stiring(duration_seconds):
	stirring_steppers.power_on()
	stirring_steppers.set_dir(1)
	deadline = ticks_add(time.ticks_ms(), duration_seconds * 1000)
	while ticks_diff(deadline, time.ticks_ms()) > 0:
		stirring_steppers.steps(1)
	stirring_steppers.power_off()

def wifiConnect(ssid, password):
	station = network.WLAN(network.STA_IF)
	
	if station.isconnected():
		return station.ifconfig()

	if not station.active():
		station.active(True)
	
	station.connect(ssid, password)

	while not station.isconnected():
		pass

	return station.ifconfig()

wifiConnect('Eurecat_Lab', 'Eureca2021!')

socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
socket.bind(('', 3000))
socket.listen(5)

while True:
	conn, addr = socket.accept()
	payload = conn.recv(1024).decode('utf-8')
	command = payload.split('\r\n')[-1].split(' ')
	print(command)
	if command[0] == 'stiring':
		stiring(int(command[1]))
	conn.send('HTTP/1.1 200 OK\n')
	conn.send('Content-Type: text/plain\n')
	conn.send('Connection: close\n\n')
	conn.sendall('Done')
	conn.close()
