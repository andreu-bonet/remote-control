import network
import usocket
import machine
import time

from utime import ticks_add
from utime import ticks_diff

import classes

stirring_steppers = classes.PrecisionStepper(step_pin=19, dir_pin=21, en_pin=18, step_time=1000)

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
	conn.send('HTTP/1.1 200 OK\n')
	conn.send('Content-Type: text/plain\n')
	conn.send('Connection: close\n\n')
	conn.sendall('Done')
	conn.close()
