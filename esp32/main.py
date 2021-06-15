import network
import usocket
from machine import Pin
from time import sleep_us
from time import ticks_ms
from utime import ticks_add
from utime import ticks_diff


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
		self.power_on()
		self.rotate_steps(mm * self.steps_per_mm)
		self.power_off()

class Single:
	def __init__(self, pin, engage_value=0, disengage_value=1):
		self.pin = Pin(pin, Pin.OUT)
		self.engage_value = engage_value
		self.disengage_value = disengage_value
		self.disengage()

	def status(self):
		return self.pin.value

	def engage(self):
		self.pin.value(self.engage_value)

	def disengage(self):
		self.pin.value(self.disengage_value)

	def activate(self, duration_ms):
		self.engage()
		sleep_ms(duration_ms)
		self.disengage()

class Endpoint:
	def __init__(self, pin):
		self.pin = Pin(pin, Pin.IN)

	def status(self):
		return self.pin.value()


stirrer_stepper = Stepper(stp_pin=19, dir_pin=21, pow_pin=18)
sampler_stepper = Stepper(stp_pin= 2, dir_pin= 4, pow_pin=15, step_sleep_us=10)
syringe_stepper = Stepper(stp_pin=32, dir_pin= 5, pow_pin=33)
perist_pump = Single(pin=26, engage_value=0, disengage_value=1)
catho_valve = Single(pin=27, engage_value=1, disengage_value=0)
anode_valve = Single(pin=14, engage_value=1, disengage_value=0)
endpoint = Endpoint(pin=25)

def zeroing_sampler():
	sampler_stepper.set_direction(1)
	sampler_stepper.power_on()
	while endpoint.status() == 1:
		sampler_stepper.rotate_steps(1)
	sampler_stepper.power_off()

def setup():
	stirrer_stepper.power_off()
	sampler_stepper.power_off()
	syringe_stepper.power_off()
	perist_pump.disengage()
	catho_valve.disengage()
	anode_valve.disengage()

def stiring(duration_ms):
	stirrer_stepper.power_on()
	stirrer_stepper.set_direction(1)
	deadline = ticks_add(ticks_ms(), duration_ms)
	while ticks_diff(deadline, ticks_ms()) > 0:
		stirrer_stepper.rotate_steps(1)
	stirrer_stepper.power_off()

def sleep_ms(ms):
	deadline = ticks_add(ticks_ms(), ms)
	while ticks_diff(deadline, ticks_ms()) > 0:
		pass

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

setup()

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
		sampler_stepper.set_direction(int(command[1]))
		sampler_stepper.rotate_mm(int(command[2]))

	elif command[0] == 'syringepump':
		syringe_stepper.set_direction(int(command[1]))
		syringe_stepper.power_on()
		syringe_stepper.rotate_steps(int(command[2]))
		syringe_stepper.power_off()

	elif command[0] == 'valvecathode':
		catho_valve.activate(int(command[1]))

	elif command[0] == 'valveanode':
		anode_valve.activate(int(command[1]))

	elif command[0] == 'peristalticpump':
		perist_pump.activate(int(command[1]))

	elif command[0] == 'autosampler_zeroing':
		zeroing_sampler()

	conn.send('HTTP/1.1 200 OK\n')
	conn.send('Content-Type: text/plain\n')
	conn.send('Connection: close\n\n')
	conn.sendall('Done')
	conn.close()
