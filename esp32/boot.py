import network


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


wifiConnect('MOVISTAR_DF98', 'pU09K%chTQ2$mMhQ4c0U')
