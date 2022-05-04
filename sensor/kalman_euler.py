from typing import Tuple
import numpy as np
from time import time
from math import sin, cos, tan
from sensor.imu import Imu

class KalmanRollPitchImu:
  phi_hat = 0.0
  theta_hat = 0.0
  imu: Imu
  
  def __init__(self, imu: Imu):
    self.imu = imu
    self.prev_time = time()
    self.C = np.array([[1, 0, 0, 0], [0, 0, 1, 0]])
    self.P = np.eye(4)
    self.Q = np.eye(4)
    self.R = np.eye(2)
    self.state_estimate = np.array([[0], [0], [0], [0]])

  def get_yaw(self):
    return self.imu.get_yaw()
    
  def calculate_offsets(self):
    for i in range(self.offset_loops):
      phi, theta = self.imu.get_accel()
      self.phi_offset += phi
      self.theta_offset += theta
    self.phi_offset = float(self.phi_offset) / float(self.offset_loops)
    self.theta_offset = float(self.theta_offset) / float(self.offset_loops)
  
  def get_raw(self):
    angles, gyro = self.imu.get_accel(), self.imu.get_gyro()
    [phi_acc, theta_acc] = angles
    return phi_acc, theta_acc

  def predict_update(self) -> Tuple[float, float]:
    dt = 0.0
    dt = time() - self.prev_time
    self.prev_time = time()

    # Get accelerometer measurements and remove offsets
    angles, gyro = self.imu.get_accel(), self.imu.get_gyro()
    [phi_acc, theta_acc] = angles
    
   # Get gyro measurements and calculate Euler angle derivatives
    [p, q, r] = gyro

    phi_dot = p + sin(self.phi_hat) * tan(self.theta_hat) * q + cos(self.phi_hat) * tan(self.theta_hat) * r
    theta_dot = cos(self.phi_hat) * q - sin(self.phi_hat) * r

    # Kalman filter
    A = np.array([[1, -dt, 0, 0], [0, 1, 0, 0], [0, 0, 1, -dt], [0, 0, 0, 1]])
    B = np.array([[dt, 0], [0, 0], [0, dt], [0, 0]])

    gyro_input = np.array([[phi_dot], [theta_dot]])
    self.state_estimate = A.dot(self.state_estimate) + B.dot(gyro_input)
    self.P = A.dot(self.P.dot(np.transpose(A))) + self.Q

    measurement = np.array([[phi_acc], [theta_acc]])
    y_tilde = measurement - self.C.dot(self.state_estimate)
    S = self.R + self.C.dot(self.P.dot(np.transpose(self.C)))
    K = self.P.dot(np.transpose(self.C).dot(np.linalg.inv(S)))
    self.state_estimate = self.state_estimate + K.dot(y_tilde)
    self.P = (np.eye(4) - K.dot(self.C)).dot(self.P)
   

    self.phi_hat = float(self.state_estimate[0])
    self.theta_hat = float(self.state_estimate[2])
    return self.phi_hat, self.theta_hat
