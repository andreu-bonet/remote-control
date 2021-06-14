import network
import usocket
import time
from utime import ticks_add
from utime import ticks_diff
from machine import Pin
from time import sleep_us


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

class Valve:
	def __init__(self, pin):
		self.pin = Pin(pin, Pin.OUT)
		self.disengage()

	def engage(self):
		self.pin.value(1)

	def disengage(self):
		self.pin.value(0)

	def status(self):
		return self.pin.value

class Pump:
	def __init__(self, pin):
		self.pin = Pin(pin, Pin.OUT)
		self.disengage()

	def engage(self):
		self.pin.value(0)

	def disengage(self):
		self.pin.value(1)

	def status(self):
		return self.pin.value

stirrer_stepper = Stepper(stp_pin=19, dir_pin=21, pow_pin=18)
sampler_stepper = Stepper(stp_pin= 2, dir_pin= 4, pow_pin=15, step_sleep_us=1)
syringe_stepper = Stepper(stp_pin=32, dir_pin= 5, pow_pin=33)
peristaltic_pump = Pump(pin=26)
cathode_valve = Valve(pin=27)
anode_valve = Valve(pin=14)

def sleep_ms(ms):
	deadline = ticks_add(time.ticks_ms(), ms)
	while ticks_diff(deadline, time.ticks_ms()) > 0:
		pass

def stiring(duration_ms):
	stirrer_stepper.power_on()
	stirrer_stepper.set_dir(1)
	deadline = ticks_add(time.ticks_ms(), duration_ms)
	while ticks_diff(deadline, time.ticks_ms()) > 0:
		stirrer_stepper.rotate_steps(1)
	stirrer_stepper.power_off()

def autosampler(direction, travel_mm):
	sampler_stepper.set_dir(direction)
	sampler_stepper.power_on()
	sampler_stepper.rotate_mm(travel_mm)
	sampler_stepper.power_off()

def syringepump(direction, travel_mm):
	syringe_stepper.set_dir(direction)
	syringe_stepper.power_on()
	syringe_stepper.rotate_mm(travel_mm)
	syringe_stepper.power_off()

def valvecathode(duration_ms):
	cathode_valve.engage()
	sleep_ms(duration_ms)
	cathode_valve.disengage()

def valveanode(duration_ms):
	anode_valve.engage()
	sleep_ms(duration_ms)
	anode_valve.disengage()

def peristalticpump(duration_ms):
	peristaltic_pump.engage()
	sleep_ms(duration_ms)
	peristaltic_pump.disengage()

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
	elif command[0] == 'valvecathode':
		valvecathode(int(command[1]))
	elif command[0] == 'valveanode':
		valveanode(int(command[1]))
	elif command[0] == 'peristalticpump':
		peristalticpump(int(command[1]))
	conn.send('HTTP/1.1 200 OK\n')
	conn.send('Content-Type: text/plain\n')
	conn.send('Connection: close\n\n')
	conn.sendall('Done')
	conn.close()
