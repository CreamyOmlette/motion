from kalman1dof import sensor_init
from kalman1dof import read_sensor
from filterpy.kalman import KalmanFilter
import numpy as np
import matplotlib as plt
from filterpy.common import Q_discrete_white_noise

def get_kalman_values_3dof(dt):
  x_dim = 9
  dt = dt/1000
  x = np.array([[0.], # x_postion
                [0.], # x_velocity
                [0.], # x_acceleration
                [0.], # y_postion
                [0.], # y_velocity
                [0.], # y_acceleration
                [0.], # z_postion
                [0.], # z_velocity
                [0.], # z_acceleration
                ])
  F = np.array([[1., dt, dt**2/2, 0., 0., 0.,      0., 0.       ,0.],
                [0., 1., dt,      0., 0., 0.,      0., 0.       ,0.],
                [0., 0., 1.,      0., 0., 0.,      0., 0.       ,0.],
                [0., 0., 0.,      1., dt, dt**2/2, 0., 0.       ,0.],
                [0., 0., 0.,      0., 1., dt,      0., 0.       ,0.],
                [0., 0., 0.,      0., 0., 1.,      0., 0.       ,0.],
                [0., 0., 0.,      0., 0. ,0.,      1., dt, dt**2/2,],
                [0., 0., 0.,      0., 0. ,0.,      0., 1., dt,     ],
                [0., 0., 0.,      0., 0. ,0.,      0., 0., 1.,     ],])

  H = np.array([[0., 0., 1.],
                [0., 0., 1.],
                [0., 0., 1.]])
  P = np.eye(x_dim)
  R = 0.0784
  Q = Q_discrete_white_noise(dim=x_dim, dt=dt, var=0.1)
  return x ,F, H, P, R, Q

def kalman_3dof(dt):
  f = KalmanFilter (dim_x=9, dim_z=3)
  x, F, B, H, P, R, Q = get_kalman_values_3dof(dt/1000)
  f.x = x
  f.F = F
  f.B = B
  f.H = H
  f.P = P
  f.R = R
  f.Q = Q
  return f

def main():
  dt = 0.001
  x, F, H, P, R, Q = get_kalman_values_3dof(dt)
  imu = sensor_init(0x68)
  x_vals = [0]
  y_vals = [0]
  sum = 0.
  for i in range(5000):
    x_vals, y_vals, x, P = kalman_3dof(dt,imu, x, F, H, P, R, Q, x_vals, y_vals)
  plt.scatter(x_vals[0][1], y_vals)
  plt.savefig('xyz distance')

main()