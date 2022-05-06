import os
import sys
import time
import smbus
import numpy as np
import RPi.GPIO as GPIO

from imusensor.MPU9250 import MPU9250
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.output(17, 1)
GPIO.output(27, 0)
GPIO.output(22, 0)
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
imu.caliberateAccelerometer()
accelscale = imu.Accels
accelBias = imu.AccelBias
gyroBias = imu.GyroBias
imu.saveCalibDataToFile("/home/pi/Documents/motion-sleeve/sensor/calibration/calib-3.json")
print ("calib data saved")

imu.loadCalibDataFromFile("/home/pi/Documents/motion-sleeve/sensor/calibration/calib-3.json")

if np.array_equal(accelscale, imu.Accels) & np.array_equal(accelBias, imu.AccelBias) & \
	np.array_equal(gyroBias, imu.GyroBias):
	print ("calib loaded properly")