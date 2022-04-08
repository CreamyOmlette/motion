import filterpy.kalman as kf
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import smbus
from filterpy.common import Q_discrete_white_noise
from imusensor.MPU9250 import MPU9250
import cmath as math

def sensor_init(address, id):
  bus = smbus.SMBus(1)
  imu = MPU9250.MPU9250(bus, address)
  imu.begin()
  imu.loadCalibDataFromFile(f"/home/pi/Documents/motion-sleeve/calibration/calib-{id}.json")
  return imu

def read_sensor(imu):
  imu.readSensor()
  imu.computeOrientation()
  ax, ay, az = imu.AccelVals
  phi = math.atan2(ay, math.sqrt(ax ** 2.0 + az ** 2.0))
  theta = math.atan2(-ax, math.sqrt(ay ** 2.0 + az ** 2.0))
  return [phi, theta], imu.GyroVals