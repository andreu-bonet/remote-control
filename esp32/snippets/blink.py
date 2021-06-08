from machine import Pin
import time

pin13 = Pin(13, Pin.OUT)

def toggle(laps):
	lap = 0
	while lap < laps:
		pin13.value(1)
		time.sleep(1)
		pin13.value(0)
		time.sleep(1)
		lap += 1

toggle(5)
