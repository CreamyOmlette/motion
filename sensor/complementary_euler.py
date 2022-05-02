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

  def __init__(self, imu: Imu, alpha: Number):
    self.imu = imu
    self.prev_time = time()
    self.alpha = alpha

  def get_euler(self) -> Tuple[float, float]:
    dt = 0.
    dt = time() - start_time
    start_time = time()
    
    phi_hat_acc, theta_hat_acc = self.imu.get_accel()
    
    p, q, r = self.imu.get_gyro()
    
    phi_dot = p + sin(phi_hat) * tan(theta_hat) * q + cos(phi_hat) * tan(theta_hat) * r
    theta_dot = cos(phi_hat) * q - sin(phi_hat) * r
    
    phi_hat = (1 - self.alpha) * (phi_hat + dt * phi_dot) + self.alpha * phi_hat_acc
    theta_hat = (1 - self.alpha) * (theta_hat + dt * theta_dot) + self.alpha * theta_hat_acc   
    
    return phi_hat, theta_hat
