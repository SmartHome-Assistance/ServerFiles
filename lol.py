import serial
import RPi.GPIO as GPIO
import time

ser=serial.Serial("/dev/ttyUSB0",9600)
ser.boudrate=9600
s = ""

def all():
	while True:
		read_ser=ser.readline()
		print (read_ser)	

"""
def blink(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(1000)
	GPIO.output(pin, GPIO.LOW)
	time.sleep(1000)
	return
-1\r\n
"""
while True:
	s = input()
	print("Send: ")
	print(s)
	if s == '3': 
		ser.write(b'3')
	if s == '4': 
		ser.write(b'4')
	if s == '5': 
		ser.write(b'5')
	if s == '0': 
		ser.write(b'0')
	if s == 'all': 
		all()
	read_ser=ser.readline()
	print("Get: ")	
	#	read_ser = read_ser [0:-2]
	#	while (read_ser == "I am ready!"):
	#	time.sleep(1)
	print(read_ser)
	print("")