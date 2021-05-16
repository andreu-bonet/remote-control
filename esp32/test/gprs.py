import socket
import machine
import time
import sys
import gsm


MODEM_POWER_PIN = 23
MODEM_RST = 5
MODEM_PWRKEY_PIN = 4
MODEM_TX = 27
MODEM_RX = 26
LED_PIN = 13

GSM_APN = "telefonica.es"
GSM_USER = "telefonica"
GSM_PASS = "telefonica"
simPin = "4140"

GSM_POWER = machine.Pin(MODEM_POWER_PIN, machine.Pin.OUT)
GSM_POWER.value(1)

LED = machine.Pin(LED_PIN, machine.Pin.OUT)
LED.value(1)

MODEM_RST = machine.Pin(MODEM_RST, machine.Pin.OUT)
MODEM_RST.value(1)

GSM_PWR = machine.Pin(MODEM_PWRKEY_PIN, machine.Pin.OUT)
GSM_PWR.value(1)
time.sleep_ms(200)
GSM_PWR.value(0)
time.sleep_ms(1000)
GSM_PWR.value(1)

gsm.start(tx=MODEM_TX, rx=MODEM_RX, apn=GSM_APN,
          user=GSM_USER, password=GSM_PASS)

sys.stdout.write('Waiting for AT command response...')
for retry in range(20):
    if gsm.atcmd('AT'):
        break
    else:
        sys.stdout.write('.')
        time.sleep_ms(5000)
else:
    raise Exception("Modem not responding!")
print()

print("Connecting to GSM...")
gsm.connect()

while gsm.status()[0] != 1:
    pass

print('IP:', gsm.ifconfig()[0])
print("Connected !")
