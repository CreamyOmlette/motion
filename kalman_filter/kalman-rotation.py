from kalman1dof import sensor_init
from kalman1dof import read_sensor
from kalman1dof import update_predict_record
from filterpy.kalman import KalmanFilter
import numpy as np
import matplotlib as plt

def get_kalman_values_rotation(dt):
  x_dim = 3
  x = np.array([[0.],  # pheta 
                [0.],  # w
                [0.]]) # bias
  F = np.array([[1., 0., -dt],
                [0., 0., -1],
                [0., 0., 0.]])
  B = np.array([[dt, 0],
                [1, 0],
                [0, 1]])
  H = np.array([[0, 1, 0],
                [1, 0, 0]])
  D = np.array([[0, 0], [0, 0]])
  P = np.empty(x_dim)
  sd_accel = 0.1
  sd_gyro = 0.1
  R = np.array([[sd_accel**2, 0],
                [0, sd_gyro**2]])
  Q = np.array([[0.04*dt*dt, 0.04*dt],
                [0.04*dt, 0.04]])
  return x ,F, B, H, P, R, Q

def kalman_rot(dt):
  f = KalmanFilter (dim_x=3, dim_z=2)
  x, F, B, H, P, R, Q = get_kalman_values_rotation(dt/1000)
  f.x = x
  f.F = F
  f.B = B
  f.H = H
  f.P = P
  f.R = R
  f.Q = Q
  return f

def main():
  dt = 1
  imu = sensor_init(1, 0x68)
  f = kalman_rot(dt)
  x_vals = [0]
  y_vals = [0]
  while len(x_vals < 5000):
    z = read_sensor(imu, dt)
    f.predict()
    f.update(z)
    y_vals.append(f.x[0])
    x_vals.append(x_vals[len(x_vals - 1)]+dt)
    plt.scatter(x_vals, y_vals)
  plt.savefig('rotation')
