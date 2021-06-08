import network
import usocket
import time
from utime import ticks_add
from utime import ticks_diff
from machine import Pin
from time import sleep_us


class Precision_Stepper:
	"""Class for stepper motor"""

	def __init__(self, step_pin, dir_pin, en_pin, step_time=1000, steps_per_rev=1600):
		"""Initialise stepper."""
		self.stp = Pin(step_pin, Pin.OUT)
		self.dir = Pin(dir_pin, Pin.OUT)
		self.en = Pin(en_pin, Pin.OUT, value=0)

		self.step_time = step_time  # us
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
			sleep_us(self.step_time)
			self.stp.value(0)
			sleep_us(self.step_time)

	def mm(self, mm, step_per_mm):
		self.steps(mm * step_per_mm)

	def set_step_time(self, us):
		"""Set time in microseconds between each step."""
		self.step_time = us

Steppers_Stirring = Precision_Stepper(step_pin=19, dir_pin=21, en_pin=18, step_time=1000)
Stepper_Autosampler = Precision_Stepper(step_pin=2, dir_pin=4, en_pin=15, step_time=1)
Stepper_Syringe_Pump = Precision_Stepper(step_pin=32, dir_pin=5, en_pin=33, step_time=1000)

Microstepping = 32
Standard_Step_Angle = 1.8
Pich_in_mm = 8
Full_rev = 360
Relation = (Full_rev / Standard_Step_Angle) / Pich_in_mm
Step_Per_mm = Relation * Microstepping

def stiring(duration_seconds):
	Steppers_Stirring.power_on()
	Steppers_Stirring.set_dir(1)
	deadline = ticks_add(time.ticks_ms(), duration_seconds * 1000)
	while ticks_diff(deadline, time.ticks_ms()) > 0:
		Steppers_Stirring.steps(1)
	Steppers_Stirring.power_off()

def autosampler(direction, travel):
	Stepper_Autosampler.set_dir(direction)
	Stepper_Autosampler.power_on()
	Stepper_Autosampler.mm(abs(travel), Step_Per_mm)
	Stepper_Autosampler.power_off()

def syringepump(direction, travel):
	Stepper_Syringe_Pump.set_dir(direction)
	Stepper_Syringe_Pump.power_on()
	Stepper_Syringe_Pump.mm(abs(travel), Step_Per_mm)
	Stepper_Syringe_Pump.power_off()

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

ifconfig = wifiConnect('Eurecat_Lab', 'Eureca2021!')

print(ifconfig)

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
	elif command[0] == 'autosampler':
		autosampler(int(command[1]), int(command[2]))
	elif command[0] == 'syringepump':
		syringepump(int(command[1]), int(command[2]))
	conn.send('HTTP/1.1 200 OK\n')
	conn.send('Content-Type: text/plain\n')
	conn.send('Connection: close\n\n')
	conn.sendall('Done')
	conn.close()
