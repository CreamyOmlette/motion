from numbers import Number
from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman 
import math
import time
import smbus

class Imu:
  id: Number
  sensorfusion: kalman.Kalman
  curr_time = time.time()

  def __init__(self, id):
    bus = smbus.SMBus(1)
    imu = MPU9250.MPU9250(bus, 0x68)
    imu.begin()
    imu.loadCalibDataFromFile(f"/home/pi/Documents/motion-sleeve/sensor/calibration/calib-{id}.json")
    self.sensorfusion = kalman.Kalman()
    self.imu = imu
    if(id == 0 or id == 4):
      imu.readSensor()
      imu.computeOrientation()
      self.sensorfusion.roll = imu.roll
      self.sensorfusion.pitch = imu.pitch
      self.sensorfusion.yaw = imu.yaw
    time.sleep(0.01)

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
  
  def get_yaw(self):
    self.imu.readSensor()
    self.imu.computeOrientation()
    new_time = time.time()
    dt = new_time - self.curr_time
    self.curr_time = new_time

    self.sensorfusion.computeAndUpdateRollPitchYaw(\
        self.imu.AccelVals[0], self.imu.AccelVals[1], self.imu.AccelVals[2],\
        self.imu.GyroVals[0], self.imu.GyroVals[1], self.imu.GyroVals[2], \
        self.imu.MagVals[0], self.imu.MagVals[1], self.imu.MagVals[2], dt)

    return self.sensorfusion.yaw