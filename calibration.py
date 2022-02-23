import os
import sys
import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.caliberateAccelerometer()
accelscale = imu.Accels
accelBias = imu.AccelBias
gyroBias = imu.GyroBias
imu.saveCalibDataToFile("/home/pi/Documents/motion-sleeve/calib.json")
print ("calib data saved")

imu.loadCalibDataFromFile("/home/pi/Documents/motion-sleeve/calib.json")

if np.array_equal(accelscale, imu.Accels) & np.array_equal(accelBias, imu.AccelBias) & \
	np.array_equal(gyroBias, imu.GyroBias):
	print ("calib loaded properly")