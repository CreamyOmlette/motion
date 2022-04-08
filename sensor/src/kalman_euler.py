import numpy as np
import time
from cmath import sin, cos, tan
from sensor import read_sensor

class KalmanRollPitch:
  offset_loops = 100
  state_estimate = np.array([[0], [0], [0], [0]])
  phi_hat = 0.0
  theta_hat = 0.0
  phi_offset = 0.0
  theta_offset = 0.0
  C = np.array([[1, 0, 0, 0], [0, 0, 1, 0]])
  P = np.eye(4)
  Q = np.eye(4)
  R = np.eye(2)
  is_first_run = True

  def __init__(self, imu):
    self.imu = imu
    self.prev_time = time()

  def calculate_offsets(self):
    for i in range(self.offset_loops):
      angles_acc, gyro = read_sensor(imu=self.imu, sleep_time=0.1)
      self.phi_offset += angles_acc[0]
      self.theta_offset += angles_acc[1]
    self.phi_offset = float(self.phi_offset) / float(self.offset_loops)
    self.theta_offset = float(self.theta_offset) / float(self.offset_loops)
  
  def predict_update(self):
    dt = time() - prev_time

    if(self.is_first_run):
      prev_time = time()
      dt = time() - prev_time
      self.is_first_run = False

    prev_time = time()

    # Get accelerometer measurements and remove offsets
    angles, gyro = read_sensor(imu=self.imu, sleep_time=0.1)
    
    [phi_acc, theta_acc] = angles
    
    phi_acc -= self.phi_offset
    theta_acc -= self.theta_offset
    
    # Get gyro measurements and calculate Euler angle derivatives
    [p, q, r] = gyro
    phi_dot = p + sin(self.phi_hat) * tan(self.theta_hat) * q + cos(self.phi_hat) * tan(self.theta_hat) * r
    theta_dot = cos(self.phi_hat) * q - sin(self.phi_hat) * r

    # Kalman filter
    A = np.array([[1, -dt, 0, 0], [0, 1, 0, 0], [0, 0, 1, -dt], [0, 0, 0, 1]])
    B = np.array([[dt, 0], [0, 0], [0, dt], [0, 0]])

    gyro_input = np.array([[phi_dot], [theta_dot]])
    state_estimate = A.dot(state_estimate) + B.dot(gyro_input)
    P = A.dot(P.dot(np.transpose(A))) + self.Q

    measurement = np.array([[phi_acc], [theta_acc]])
    y_tilde = measurement - self.C.dot(state_estimate)
    S = self.R + self.C.dot(P.dot(np.transpose(self.C)))
    K = P.dot(np.transpose(self.C).dot(np.linalg.inv(S)))
    state_estimate = state_estimate + K.dot(y_tilde)
    P = (np.eye(4) - K.dot(self.C)).dot(P)

    self.phi_hat = state_estimate[0][0]
    self.theta_hat = state_estimate[2][0]
