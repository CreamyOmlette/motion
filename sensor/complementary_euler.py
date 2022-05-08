from math import cos, sin, tan
from numbers import Number
from sqlite3 import Time
from time import time
from typing import Tuple

import numpy as np
from sensor.filter import Filter
from sensor.imu import Imu


class ComplementaryRollPitch(Filter):
  imu: Imu
  prev_time: Time
  alpha: Number
  phi_hat = 0.
  theta_hat = 0.

  def __init__(self, imu: Imu, alpha: Number = 0.98):
    self.imu = imu
    self.prev_time = time()
    self.alpha = alpha

  def get_euler(self) -> Tuple[float, float]:
    dt = 0.
    dt = time() - self.prev_time
    self.prev_time = time()
    
    phi_hat_acc, theta_hat_acc = self.imu.get_accel()
    
    p, q, r = self.imu.get_gyro()
    
    phi_dot = p + sin(self.phi_hat) * tan(self.theta_hat) * q + cos(self.phi_hat) * tan(self.theta_hat) * r
    theta_dot = cos(self.phi_hat) * q - sin(self.phi_hat) * r
    
    self.phi_hat = (1 - self.alpha) * (self.phi_hat + dt * phi_dot) + self.alpha * phi_hat_acc
    self.theta_hat = (1 - self.alpha) * (self.theta_hat + dt * theta_dot) + self.alpha * theta_hat_acc   
    
    return self.phi_hat, self.theta_hat
