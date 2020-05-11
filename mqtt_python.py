import paho.mqtt.client as mqtt
import time

def on_message(client,userdata, message):
	print("message received    =  ", str(message.playload.decode("utf-8")))
	print("message topic       =  ", message.topic)
	print("message qos         =  ", message.qos)
	print("message retain flag =  ", message.retain)

broker_addr = "127.0.0.1"
topic = "light"

client = mqtt.Client("SERVER")
client.on_message = on_message

print("CREATE NEW INSTANCE")

client.connect(broker_addr)
client.loop_start()

print("SUBSCRIBING TO TOPIC", topic)

client.subscribe(topic)

print("PUBLISHING MESSAGE TO TOPIC", topic)

client.publish(topic,"OFF")
time.sleep(4)
client.on_message()
client.loop_stop()