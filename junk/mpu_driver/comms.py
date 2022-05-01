import time
import smbus
import numpy as np
from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

for i in range (30):
	imu.readSensor()
	imu.computeOrientation()

	print (f"Accelerations: {imu.AccelVals}, Gyroscope: {imu.GyroVals}")
	time.sleep(0.1)