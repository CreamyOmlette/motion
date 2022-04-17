from numbers import Number
from imusensor.MPU9250 import MPU9250
import math
import time
import smbus

class Imu:
  id: Number

  def __init__(self, id):
    bus = smbus.SMBus(1)
    imu = MPU9250.MPU9250(bus, 0x68)
    imu.begin()
    imu.loadCalibDataFromFile(f"/home/pi/Documents/motion-sleeve/sensor/calibration/calib-{id}.json")
    self.imu = imu
    time.sleep(0.1)

  def get_accel(self):
    self.imu.readSensor()
    self.imu.computeOrientation()
    ax, ay, az = self.imu.AccelVals
    phi = math.atan2(ay, math.sqrt(ax ** 2.0 + az ** 2.0))
    theta = math.atan2(-ax, math.sqrt(ay ** 2.0 + az ** 2.0))
    return phi, theta
  
  def get_gyro(self):
    self.imu.readSensor()
    self.imu.computeOrientation()
    return self.imu.GyroVals