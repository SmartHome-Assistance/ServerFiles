from gpiozero import CPUTemperature
import time
while True:
    temp = CPUTemperature()
    print(temp)
    time.sleep(2)