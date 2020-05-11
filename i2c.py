from smbus import SMBus
import time

addr = 0x8 #bus address
bus = SMBus(1) #indicates /dev/ic2-1
time.sleep(1)
num = 1

print ("Enter 1 for ON or 0 for OFF")

while num == 1:

	bus.write_byte(addr, 0x1) #switch it ON
	ledstate = input(">>>>   ")

	if ledstate == "1":
		bus.write_byte(addr, 0x1) #switch it ON
		print ("send 1")
	elif ledstate == "0":
		bus.write_byte(addr, 0x0) #switch it OFF
		print ("send 0")
	else:
		numb =0