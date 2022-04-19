from typing import Sequence
import time
import RPi.GPIO as GPIO
from matplotlib.pyplot import switch_backend
from sensor.imu import Imu
from sensor.kalman_euler import KalmanRollPitchImu
import numpy as np

class Switcher:
  sensors = []
  reading_address = 0
  roll_package: list
  pitch_package: list
  yaw_package: list

  def __init__(self, dt: float):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    self.dt = dt
    self.sensors = self.init_imus()
    self.roll_package = [0. for i in range(len(self.sensors))]
    self.pitch_package = [0. for i in range(len(self.sensors))]
    self.yaw_package = [0. for i in range(len(self.sensors))]

  def init_imus(self):
    sensors = []
    for i in range(5):
      try:
        imu = Imu(i)
        sensors.append(KalmanRollPitchImu(imu))
        self.switch_address()
      except Exception:
        print(f"Exception at sensor {i}")
    return sensors

  def switch_address(self):
    if(self.reading_address == 4):
      self.reading_address = 0
    else:
      self.reading_address += 1
    self.generate_mux_signal()

  def generate_mux_signal(self):
    addr = '{0:03b}'.format(self.reading_address)
    GPIO.output(17, int(addr[0]))
    GPIO.output(27, int(addr[1]))
    GPIO.output(22, int(addr[2]))

  def get_package(self):
    for i in range(len(self.sensors)):
      try:
        roll, pitch = self.sensors[self.reading_address].predict_update()
        psi = 0.
        if(self.reading_address == 0 or self.reading_address == 4):
          self.yaw_package[self.reading_address] = self.sensors[self.reading_address].get_yaw()

        self.update_history(roll, pitch)
        self.switch_address()
        time.sleep(self.dt)
      except OSError:
        print(f"I/O arror at sensor: {self.reading_address}")
        break
    return self.roll_package, self.pitch_package, self.yaw_package

  def update_history(self, phi: float, theta: float, psi: float):
    self.roll_package[self.reading_address] = phi
    self.pitch_package[self.reading_address] = theta
    self.yaw_package[self.reading_address] = psi

  def get_relative(self):
    roll, pitch, yaw = self.get_package()
    for i in range(4):
      roll[i] = roll[i] - roll[4]
      pitch[i] = pitch[i] - pitch[4]
    yaw[0] = yaw[0] - yaw[4]

