from imusensor.MPU9250 import MPU9250
import cmath as math
import smbus

class Imu:
  
  def __init__(self):
    bus = smbus.SMBus(1)
    imu = MPU9250.MPU9250(bus, 0x68)
    imu.begin()
    imu.loadCalibDataFromFile(f"/home/pi/Documents/motion-sleeve/sensor/calibration/calib-{id}.json")
    self.imu = imu

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