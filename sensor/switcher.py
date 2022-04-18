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
  phi_package: list
  theta_package: list

  def __init__(self, dt: float):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    self.dt = dt
    self.sensors = self.init_imus()
    self.phi_package = [0. for i in range(len(self.sensors))]
    self.theta_package = [0. for i in range(len(self.sensors))]

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
        phi, theta = self.sensors[self.reading_address].predict_update()
        self.update_history(phi, theta)
        self.switch_address()
        time.sleep(self.dt)
      except OSError:
        print(f"I/O arror at sensor: {self.reading_address}")
        break
    return self.phi_package, self.theta_package

  def update_history(self, phi: float, theta: float):
    self.phi_package[self.reading_address] = phi
    self.theta_package[self.reading_address] = theta


