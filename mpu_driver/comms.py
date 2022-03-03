import os
import sys
import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman 

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.loadCalibDataFromFile("/home/pi/Documents/motion-sleeve/calib.json")


for i in range (30):
	imu.readSensor()
	imu.computeOrientation()

	print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
	time.sleep(0.1)