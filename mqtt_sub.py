import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as sub
import time
from smbus import SMBus

bus_addr = 0x04 #bus address
bus = SMBus(1) #indicates /dev/ic2-1

broker_addr   = "127.0.0.1"
topic  = "light1"
client = mqtt.Client("SERVER")
client.connect(broker_addr)
print ("I'm ready!!!")

while True:
	print (" Go >>>")
	msg = sub.simple(topic, hostname = broker_addr)

	print("%s %s" %(msg.topic, msg.payload))
	msg = msg.payload
	if msg == b'ON' or msg == 'ON':
		bus.write_byte(bus_addr, 0x0) #switch it ON
	elif msg == b'OFF' or msg == 'OFF':
		bus.write_byte(bus_addr, 0x1) #switch it OFF
	#time.sleep(1)