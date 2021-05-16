import network
import usocket
import machine
import time


def toggle(pin, laps):
	lap = 0
	while lap < laps:
		pin.value(1)
		time.sleep(1)
		pin.value(0)
		time.sleep(1)
		lap += 1


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


pin13 = machine.Pin(13, machine.Pin.OUT)

wifiConnect('MOVISTAR_DF98', 'pU09K%chTQ2$mMhQ4c0U')

socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
socket.bind(('', 80))
socket.listen(5)

while True:
	conn, addr = socket.accept()
	aa = conn.recv(1024)
	bb = aa.decode('utf-8')
	cc = bb.split('\r\n')
	dd = cc[-1]
	toggle(pin13, int(dd))
	conn.send('HTTP/1.1 200 OK\n')
	conn.send('Content-Type: text/plain\n')
	conn.send('Connection: close\n\n')
	conn.sendall('Done!')
	conn.close()
